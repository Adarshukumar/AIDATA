#!/usr/bin/env python3
"""Static scanner for Agent Skill folders (SKILL.md + bundled files).

Flags patterns that research has linked to skill-based attacks:
prompt injection, hidden instructions, exfiltration, remote execution,
approval bypass, destructive commands, and hard-coded secrets.

It is a triage tool, not a verdict: no pattern list catches everything, and
a finding can be a false positive. Read every flagged line before trusting a skill.

Usage:
  python3 scan_skill.py path/to/skill-folder [more folders...]
  python3 scan_skill.py path/to/skill --json
  python3 scan_skill.py path/to/skill --fail-on high     # exit 1 if any high/critical finding
  python3 scan_skill.py skills/ --exclude scan_skill.py  # skip the scanner's own rule definitions

Exit codes: 0 = nothing at or above --fail-on, 1 = findings at or above it, 2 = usage error.
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

SEVERITY_ORDER = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
TEXT_SUFFIXES = {".md", ".txt", ".py", ".sh", ".bash", ".js", ".ts", ".json", ".yaml", ".yml", ".toml", ".ps1", ""}
MAX_BYTES = 2_000_000


@dataclass
class Finding:
    file: str
    line: int
    severity: str
    category: str
    rule: str
    snippet: str


# (category, severity, rule id, regex, description)
RULES: list[tuple[str, str, str, re.Pattern[str]]] = [
    ("prompt-injection", "high", "override-previous",
     re.compile(r"\b(ignore|disregard|forget|override)\b.{0,40}\b(previous|prior|above|earlier|system|all)\b.{0,20}\b(instructions?|prompts?|rules?|messages?)\b", re.I)),
    ("prompt-injection", "high", "role-impersonation",
     re.compile(r"(^|\s)(\[?system\]?\s*:|\[system message\]|<\s*system\s*>|###\s*system)", re.I)),
    ("prompt-injection", "medium", "new-persona",
     re.compile(r"\byou are now\b|\bact as (an? )?(unfiltered|unrestricted|jailbroken)\b", re.I)),
    ("prompt-injection", "medium", "conceal-from-user",
     re.compile(r"\b(do not|don't|never)\b.{0,30}\b(tell|inform|show|mention|reveal)\b.{0,30}\b(user|human)\b", re.I)),
    ("hidden-text", "high", "zero-width-or-bidi",
     re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff]")),
    ("hidden-text", "medium", "html-comment-imperative",
     re.compile(r"<!--.*?\b(ignore|send|run|execute|upload|post|curl|fetch|disclose|output)\b.*?-->", re.I)),
    ("exfiltration", "critical", "reads-secret-files",
     re.compile(r"(~/|\$HOME/|/home/[^/\s]+/)?\.(ssh/id_|aws/credentials|netrc|git-credentials|env\b|npmrc|pypirc)|id_rsa|id_ed25519", re.I)),
    ("exfiltration", "critical", "dumps-environment",
     re.compile(r"\b(printenv|env\s*\||set\s*\|\s*grep|os\.environ\b.{0,30}(post|send|requests)|process\.env\b.{0,30}(fetch|post|send))", re.I)),
    ("exfiltration", "high", "outbound-post",
     re.compile(r"\b(curl|wget|requests\.post|fetch|httpx\.post|nc)\b.{0,80}(-d\b|--data|--upload-file|-F\b|\bPOST\b|https?://)", re.I)),
    ("exfiltration", "high", "known-capture-host",
     re.compile(r"webhook\.site|requestbin|pipedream\.net|ngrok\.(io|app)|pastebin\.com|transfer\.sh|interact\.sh|oast\.(fun|live|pro)", re.I)),
    ("remote-execution", "critical", "pipe-to-shell",
     re.compile(r"\b(curl|wget)\b[^\n|]*\|\s*(sudo\s+)?(ba|z|k)?sh\b|\biex\s*\(\s*irm\b|\bInvoke-Expression\b.{0,40}DownloadString", re.I)),
    ("remote-execution", "high", "obfuscated-exec",
     re.compile(r"base64\s+(-d|--decode)[^\n]*\|\s*(ba)?sh|powershell[^\n]{0,30}-(enc|encodedcommand)\b|\beval\s*\(\s*(base64|atob|bytes\.fromhex|__import__)", re.I)),
    ("remote-execution", "medium", "dynamic-code",
     re.compile(r"\b(eval|exec)\s*\(|subprocess\.(Popen|run|call)\(.*shell\s*=\s*True", re.I)),
    ("approval-bypass", "high", "no-confirmation",
     re.compile(r"(don'?t|do not|never)\s+ask\s+(me\s+|the user\s+)?(again|for (confirmation|permission|approval))|without (asking|confirmation|approval)|skip (the )?(confirmation|approval)|auto-?approve|--yes\b|--no-confirm", re.I)),
    ("destructive", "critical", "wipe-or-format",
     re.compile(r"rm\s+-[a-z]*r[a-z]*f?\s+(/|~|\$HOME|\*)(\s|$)|\bmkfs\b|\bdd\s+if=.*of=/dev/|:\(\)\s*\{\s*:\|:&\s*\};:", re.I)),
    ("destructive", "medium", "privilege-or-perm",
     re.compile(r"\bsudo\b|chmod\s+(-R\s+)?(777|a\+rwx)|\bchown\s+-R\b", re.I)),
    ("supply-chain", "medium", "install-from-url",
     re.compile(r"(pip|pip3|uv)\s+install\s+(https?://|git\+)|npm\s+install\s+(https?://|git\+|github:)|npx\s+(-y\s+)?[\w@/.-]+@latest", re.I)),
    ("supply-chain", "low", "unpinned-download",
     re.compile(r"\b(curl|wget)\s+-[a-zA-Z]*[sSL]\w*\s+https?://", re.I)),
    ("secrets", "critical", "private-key-block",
     re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("secrets", "high", "provider-token",
     re.compile(r"\b(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{60,}|sk-[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,})\b")),
    ("secrets", "medium", "hardcoded-credential",
     re.compile(r"(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]", re.I)),
]

B64_RUN = re.compile(r"[A-Za-z0-9+/]{120,}={0,2}")


def redact(text: str) -> str:
    """Hide secret values in snippets so the report itself does not leak them."""
    text = re.sub(r"(AKIA|ghp_|github_pat_|sk-|xox[baprs]-)[A-Za-z0-9_\-]+", r"\1<redacted>", text)
    text = re.sub(r"((?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"])[^'\"\s]{8,}", r"\1<redacted>", text, flags=re.I)
    return text.strip()[:160]


def decode_check(line: str) -> str | None:
    """Flag long base64 runs that decode to instruction-like text."""
    for m in B64_RUN.finditer(line):
        raw = m.group(0)
        try:
            decoded = base64.b64decode(raw + "=" * (-len(raw) % 4), validate=False).decode("utf-8", "ignore")
        except (ValueError, UnicodeDecodeError):
            continue
        if re.search(r"ignore|system|instruction|send|curl|password|token|exec", decoded, re.I):
            return decoded[:80]
    return None


def scan_file(path: Path, root: Path) -> list[Finding]:
    rel = str(path.relative_to(root.parent)) if root.parent != root else str(path)
    try:
        data = path.read_bytes()[:MAX_BYTES]
    except OSError:
        return []
    if b"\x00" in data[:2048]:
        return [Finding(rel, 0, "medium", "binary", "binary-file", "binary file in skill folder; inspect manually")]
    text = data.decode("utf-8", "replace")
    findings: list[Finding] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for category, severity, rule, pattern in RULES:
            if pattern.search(line):
                findings.append(Finding(rel, lineno, severity, category, rule, redact(line)))
        decoded = decode_check(line)
        if decoded:
            findings.append(Finding(rel, lineno, "high", "prompt-injection", "base64-instruction",
                                    f"decodes to: {decoded!r}"))
    return findings


def scan_folder(folder: Path, exclude: list[str]) -> list[Finding]:
    if not folder.is_dir():
        raise SystemExit(f"error: not a folder: {folder}")
    findings: list[Finding] = []
    files = sorted(
        p for p in folder.rglob("*")
        if p.is_file() and ".git" not in p.parts
        and not any(p.match(pat) or p.name == pat for pat in exclude)
    )
    if not any(p.name.lower() == "skill.md" for p in files):
        findings.append(Finding(str(folder), 0, "info", "structure", "no-skill-md",
                                "no SKILL.md found; this may not be an Agent Skill folder"))
    for p in files:
        if p.suffix.lower() in TEXT_SUFFIXES or p.name.lower() == "skill.md":
            findings.extend(scan_file(p, folder))
        else:
            findings.append(Finding(str(p), 0, "low", "structure", "non-text-file",
                                    f"unusual file type {p.suffix or '(none)'}; check what it does"))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folders", nargs="+", type=Path)
    ap.add_argument("--json", action="store_true", help="print findings as JSON")
    ap.add_argument("--exclude", action="append", default=[],
                    help="file name or glob to skip (repeatable), e.g. --exclude scan_skill.py")
    ap.add_argument("--fail-on", default="high", choices=list(SEVERITY_ORDER),
                    help="exit 1 if a finding at or above this severity exists (default: high)")
    args = ap.parse_args()

    all_findings: list[Finding] = []
    for folder in args.folders:
        all_findings.extend(scan_folder(folder.resolve(), args.exclude))

    threshold = SEVERITY_ORDER[args.fail_on]
    failing = [f for f in all_findings if SEVERITY_ORDER[f.severity] >= threshold]

    if args.json:
        print(json.dumps([asdict(f) for f in all_findings], indent=2, ensure_ascii=False))
    else:
        if not all_findings:
            print("no findings")
        for f in sorted(all_findings, key=lambda x: (-SEVERITY_ORDER[x.severity], x.file, x.line)):
            loc = f"{f.file}:{f.line}" if f.line else f.file
            print(f"[{f.severity.upper():8}] {f.category}/{f.rule}  {loc}\n            {f.snippet}")
        counts: dict[str, int] = {}
        for f in all_findings:
            counts[f.severity] = counts.get(f.severity, 0) + 1
        print(f"\nsummary: {len(all_findings)} finding(s) {dict(sorted(counts.items()))}; "
              f"{len(failing)} at or above '{args.fail_on}'")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
