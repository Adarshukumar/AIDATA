#!/usr/bin/env python3
"""Build the project-description indexes for python-projects/collections/*.

Reads each project folder, extracts a short description from its own README (when the
README has a Description section, as the ndleah template does), otherwise derives a
description from the folder name, and classifies the project into a category.

Writes:
  python-projects/PROJECTS.md              all projects, grouped by category
  python-projects/collections/README.md    modern index for the two collections
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "python-projects"
COLLECTIONS = ROOT / "collections"

COLLECTION_META = {
    "python-mini-project": {
        "title": "Python Mini Projects",
        "upstream": "https://github.com/ndleah/python-mini-project",
        "emoji": "🧩",
        "license": "MIT",
        "authors": "@ndleah + 100 contributors",
    },
    "all-in-one-python-projects": {
        "title": "All-In-One Python Projects",
        "upstream": "https://github.com/king04aman/All-In-One-Python-Projects",
        "emoji": "📦",
        "license": "MIT",
        "authors": "@king04aman + contributors",
    },
}

SKIP_DIRS = {".github", "IMG", "assets", "images", ".git", "__pycache__", "SOURCES"}

CATEGORIES = [
    ("🎮 Games", ["game", "chess", "snake", "pong", "mine", "zombie", "tetris", "othello",
                  "reversi", "caterpillar", "dice", "hangman", "wordle", "connect", "lazy",
                  "color game", "guessing", "tic tac", "text adventure", "sudoku"]),
    ("🖥️ Desktop & GUI", ["tkinter", "gui", "clock", "timer", "notepad", "calculator",
                          "player", "music", "flash card", "flashcard", "paint", "screen",
                          "keyboard", "mouse", "typing", "voice assistant", "alarm"]),
    ("🌐 Web & APIs", ["flask", "django", "streamlit", "fastapi", "web", "html", "crud",
                       "authentication", "firebase", "api", "url shortener", "blog",
                       "website", "dashboard", "rest", "weather", "currency", "translator",
                       "telegram", "youtube", "movie", "recipe", "journal", "expense",
                       "finance", "tracker", "quiz app", "login"]),
    ("🤖 ML, AI & Vision", ["machine learning", "neural", "cnn", "mnist", "digit",
                            "recogni", "detection", "nlp", "summariz", "plagiarism",
                            "gesture", "handwriting", "helmet", "headlight", "lane",
                            "predict", "model", "opencv", "image process", "sentiment",
                            "langchain", "openai", "chatbot", "ocr", "face", "recommend",
                            "classification", "deep learning", "dataset", "train"]),
    ("📊 Data, CSV & Visualisation", ["csv", "pandas", "json", "plot", "folium", "geo",
                                      "excel", "xls", "visual", "statistic", "chart",
                                      "graph", "jupyter", "analysis", "scrap", "spider",
                                      "extract", "data"]),
    ("🔐 Security & Encoding", ["cipher", "encrypt", "decrypt", "stegano", "password",
                                "hash", "morse", "caesar", "security", "token", "otp",
                                "validator", "validator"]),
    ("⚙️ Automation & Files", ["bot", "automat", "download", "mail", "rss", "pdf",
                               "convert", "resize", "compress", "rename", "organiz",
                               "dump", "backup", "merge", "split", "file", "folder",
                               "clip", "zip", "crawl", "scrap", "monitor", "schedul"]),
    ("🧮 Algorithms & CLI Tools", ["algorithm", "sort", "search", "tree", "linked list",
                                   "trie", "stack", "queue", "calculator", "converter",
                                   "string", "regex", "ascii", "morse", "infix", "prefix",
                                   "number", "math", "generator", "utility", "tool", "cli",
                                   "command", "terminal", "dictionary", "counter"]),
]


def clean(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)        # html comments
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)          # images
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)      # links
    text = re.sub(r"[`*_>#]", "", text)                       # md marks
    text = re.sub(r"<[^>]+>", "", text)                       # html
    text = re.sub(r"[🛠️⚙🌟📺🧩📦📝🔗✨🚀📁🎯💡]+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def read_text(path: Path) -> str:
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except Exception:
            continue
    return ""


def describe(folder: Path) -> tuple[str, str]:
    """Return (description, tech) for a project folder."""
    desc, tech = "", ""
    candidates = sorted(folder.glob("README*")) + sorted(folder.glob("readme*"))
    if candidates:
        raw = read_text(candidates[0])
        # "Description" section (ndleah template)
        m = re.search(r"#+\s*[^\n]*Description[^\n]*\n+(.+?)(?=\n#|\Z)", raw,
                      re.I | re.S)
        if m:
            desc = clean(m.group(1).split("\n\n")[0])
        if not desc:
            # first paragraph after the title
            body = re.sub(r"^#.*\n", "", raw)
            for para in re.split(r"\n\s*\n", body):
                p = clean(para)
                if len(p) > 40 and not p.lower().startswith(
                        ("how to run", "requirements", "installation", "setup", "usage")):
                    desc = p
                    break
        # tech / modules
        m2 = re.search(r"#+\s*[^\n]*(Languages or Frameworks|Modules|Requirements|"
                       r"Technolog)[^\n]*\n+(.+?)(?=\n#|\Z)", raw, re.I | re.S)
        if m2:
            tech = clean(m2.group(2).split("\n\n")[0])[:90]
    desc = desc[:180].rstrip(" ,;.")
    name = folder.name.replace("_", " ").replace("-", " ").strip()
    bad = (not desc or len(desc) < 30 or "<" in desc or "src=" in desc
           or desc.lower() in name.lower() or desc.lower().startswith(("screenshot", "demo", "output")))
    if bad:
        desc = ""
    return desc, tech


PROJECT_NOTES = {
    "Minesweeper_game": "Classic Minesweeper with a graphical interface.",
    "Simple_dice": "Rolls a die and shows the result.",
    "Zombie_Game": "Small zombie-themed survival game.",
    "Crud_in_flask": "Flask app doing create / read / update / delete operations.",
    "Currency Converter": "Converts amounts between currencies using live rates.",
    "MobileNumber Tracker": "Looks up operator and region for a mobile number.",
    "Movie Scraper": "Scrapes movie details from a website.",
    "Random Movie Selector": "Picks a random movie from a list.",
    "Real-Time Cryptocurrency Price Tracker": "Shows live cryptocurrency prices in a GUI.",
    "Recipe Finder with Meal Planner": "Finds recipes and plans meals for the week.",
    "Telegram Bot": "A Telegram bot with simple commands.",
    "Translator": "Command-line translation between languages.",
    "web scraping- Find python jobs from a website": "Scrapes Python job listings from a job board.",
    "Youtube Video Downloader": "Downloads YouTube videos by URL.",
    "Ascii Art Generator": "Turns text or images into ASCII art.",
    "Audio Book Generator": "Reads a text/PDF file aloud as an audiobook.",
    "Binary_tree": "Binary tree with insert and traversal operations.",
    "infix_postfix_calculator": "Converts infix expressions to postfix and evaluates them.",
    "QR Code Generator": "Generates QR codes from text or links.",
    "Random Quotes Generator": "Prints a random quote.",
    "Stack_structure": "Stack data structure implementation.",
    "URL Sortener": "Shortens long URLs (folder name typo is upstream's).",
    "Image Compression": "Compresses images to reduce file size.",
    "Merge PDFs": "Merges several PDF files into one.",
    "Validate-Email": "Checks whether an email address is valid.",
    "Facebook Video Downloader": "Downloads Facebook videos by URL.",
    "Headlight Detection": "Detects vehicle headlights in images/video (OpenCV).",
    "Helmet Detection": "Flags riders without helmets in images/video (OpenCV).",
    "Plagiarism-Checker": "Compares two texts and reports similarity.",
    "assests": "Supporting assets (images/data) used by other projects — not a project itself.",
    "Google_Translate": "Translates text through Google Translate.",
    "Handwritten-Assignments": "Converts handwritten notes into digital text.",
    "ImageSize Reducer": "Resizes images down to a smaller dimension.",
    "Port Scanner": "Scans a host for open TCP ports.",
    "Simple Assistant": "Voice assistant that answers a few simple commands.",
    "Socket_example": "Demonstrates TCP sockets with a small client/server.",
    "Speech To Text": "Transcribes speech into text.",
    "Speech_To_Text": "Transcribes microphone speech into text.",
    "Spell Checker": "Suggests corrections for misspelled words.",
    "Url_Shortener": "REST API that shortens URLs.",
    "Video To Audio": "Extracts the audio track from a video file.",
    "Age Calculator": "Calculates age from a birth date (Tkinter GUI).",
    "Alarm Bot": "Plays an alarm at a time you set.",
    "CountDown Timer": "Countdown timer app.",
    "Digital Clock": "Shows a ticking digital clock.",
    "Exercise-Timer": "Interval timer for workouts.",
    "Notepad": "Simple text editor.",
    "TestTypingSpeed": "Measures your typing speed.",
    "Triangle Calculator": "Solves triangle sides and angles.",
    "Encode_Morse.py": "Encodes text into Morse code.",
    "Hashed_and_Salted_Pass": "Stores passwords hashed and salted.",
    "Img-Steganograpy": "Hides a secret message inside an image.",
    "Password Generator": "Generates random strong passwords.",
    "Text to Morse Code": "Converts text to Morse code.",
}

FALLBACK = {
    "🎮 Games": "A small Python game — see the folder README.",
    "🖥️ Desktop & GUI": "A small Tkinter/Pygame desktop tool — see the folder README.",
    "🌐 Web & APIs": "A small web/API project — see the folder README.",
    "🤖 ML, AI & Vision": "A small ML/vision project — see the folder README.",
    "📊 Data, CSV & Visualisation": "A small data/visualisation script — see the folder README.",
    "🔐 Security & Encoding": "A small security/encoding utility — see the folder README.",
    "⚙️ Automation & Files": "A small file/automation script — see the folder README.",
    "🧮 Algorithms & CLI Tools": "A small CLI/algorithms tool — see the folder README.",
    "🧰 Other Utilities": "A small utility script — see the folder README.",
}


def categorize(name: str, desc: str) -> str:
    hay = f"{name} {desc}".lower()
    best, score = "🧰 Other Utilities", 0
    for cat, keys in CATEGORIES:
        s = sum(hay.count(k) for k in keys)
        if s > score:
            best, score = cat, s
    return best


def main() -> int:
    everything: dict[str, list[dict]] = defaultdict(list)
    per_collection: dict[str, list[dict]] = {}

    for cdir in sorted(COLLECTIONS.iterdir()):
        if not cdir.is_dir():
            continue
        projects = []
        for p in sorted(cdir.iterdir()):
            if not p.is_dir() or p.name.startswith(".") or p.name in SKIP_DIRS:
                continue
            desc, tech = describe(p)
            py = len(list(p.rglob("*.py")))
            final_desc = (desc or PROJECT_NOTES.get(p.name) or "")
            entry = {
                "name": p.name,
                "desc": (desc or PROJECT_NOTES.get(p.name)
                         or FALLBACK.get(categorize(p.name, desc),
                                         "A small Python project — see the folder README.")),
                "tech": tech,
                "files": sum(1 for _ in p.rglob("*") if _.is_file()),
                "py": py,
                "category": categorize(p.name, final_desc or desc),
                "collection": cdir.name,
            }
            projects.append(entry)
            everything[entry["category"]].append(entry)
        per_collection[cdir.name] = projects

    total = sum(len(v) for v in per_collection.values())

    # ---------- PROJECTS.md ----------
    out = ["# Projects Index\n",
           f"All **{total} projects** in [`collections/`](./collections), grouped by what "
           "they do. Each entry links to the project's own folder, where the author's "
           "README and code live.\n",
           "> The code in these folders is **not mine** — credit, licenses and sources are "
           "in [CREDITS.md](./CREDITS.md).\n",
           "## 🎓 My own work",
           "",
           "| Folder | What it is |",
           "|---|---|",
           "| [`python-learning/`](./python-learning) | My own lessons: roadmap, 50 numbered "
           "lesson files (basics → sqlite3), a cheatsheet and 40 practice challenges |",
           ""]
    for cat in sorted(everything, key=lambda c: (-len(everything[c]), c)):
        items = sorted(everything[cat], key=lambda e: e["name"].lower())
        out.append(f"\n## {cat} · {len(items)}\n")
        out.append("| Project | What it does | Source |")
        out.append("|---|---|---|")
        for e in items:
            link = f"[`{e['name']}`](./collections/{e['collection']}/{e['name']})"
            src = "mini-projects" if e["collection"] == "python-mini-project" else "all-in-one"
            out.append(f"| {link} | {e['desc']} | {src} |")
    (ROOT / "PROJECTS.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    # ---------- collections/README.md ----------
    c = ["<div align=\"center\">\n",
         "# 📚 Collections\n",
         "Two community collections of small Python projects, kept complete and credited.\n",
         "</div>\n"]
    for slug, meta in COLLECTION_META.items():
        projects = per_collection.get(slug, [])
        cats: dict[str, int] = defaultdict(int)
        for p in projects:
            cats[p["category"]] += 1
        c.append(f"\n## {meta['emoji']} {meta['title']}\n")
        c.append(f"**{len(projects)} projects** · {meta['license']} · "
                 f"by {meta['authors']} · [upstream]({meta['upstream']})\n")
        c.append("\n| Category | Projects |")
        c.append("|---|---:|")
        for cat, n in sorted(cats.items(), key=lambda kv: -kv[1]):
            c.append(f"| {cat} | {n} |")
        c.append(f"\n→ Full list: [`/PROJECTS.md`](../PROJECTS.md) · "
                 f"credit: [`/CREDITS.md`](../CREDITS.md) · "
                 f"folder: [`{slug}/`](./{slug})\n")
    (COLLECTIONS / "README.md").write_text("\n".join(c) + "\n", encoding="utf-8")

    print(f"projects: {total}")
    for slug, projects in per_collection.items():
        print(f"  {slug}: {len(projects)}")
    print("categories:", {k: len(v) for k, v in sorted(everything.items())})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
