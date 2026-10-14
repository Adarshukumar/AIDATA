#!/usr/bin/env python3
"""Generate the study-skills library in <repo>/skills/ (Agent Skills standard).

  python3 arena-session-3b2d329a/artifacts/build_study_skills.py

Output:
  skills/study-<level>-<subject>/SKILL.md   one coach skill per (level, subject)
  skills/study-method-<method>/SKILL.md     reusable study-technique skills
  skills/README.md                          index of everything generated here

Re-running overwrites only the files this script owns (the paths above).
Content is original work by the repository owner (not third-party material).
"""
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "skills"

LEVELS = {
    "primary": {
        "label": "primary school (ages 6-11)",
        "session": "15-20 minutes",
        "focus": [
            "Keep sessions short and playful; stop before attention drops.",
            "Use concrete objects, pictures and stories before symbols or abstract words.",
            "Praise the strategy the child used, not only the right answer.",
            "Start every session by revisiting something from the last session.",
        ],
    },
    "secondary": {
        "label": "secondary school (ages 11-18)",
        "session": "30-45 minutes",
        "focus": [
            "Organise study around the official syllabus. Use your school board or exam syllabus (for example CBSE, ICSE, a state board, or JEE/NEET for entrance exams).",
            "Practise under timed conditions with past papers, and mark them with the official scheme.",
            "Use retrieval practice and spaced review in the weeks before a test.",
            "Break each unit into weekly targets with a visible checklist.",
        ],
    },
    "undergraduate": {
        "label": "undergraduate university",
        "session": "45-60 minutes",
        "focus": [
            "Read the lecture notes, then the textbook section, then do the problem set or reading questions.",
            "Build one concept map per module and link it to earlier modules, because exams are cumulative.",
            "Start assignments early and use office hours for specific gaps, not general confusion.",
            "Check the module outline for what is assessed and in what weighting.",
        ],
    },
    "postgraduate": {
        "label": "postgraduate (master's / PhD)",
        "session": "60-90 minutes",
        "focus": [
            "Read primary literature critically: question, method, main claim, and stated limitations.",
            "Keep a research log and a running notes file that tracks how the argument is changing.",
            "Plan against milestones (proposal, data collection, drafts, defence) and meet your supervisor on a fixed rhythm.",
            "Write in small, reviewable pieces, and separate your results from your interpretation.",
        ],
    },
    "self-learning": {
        "label": "self-directed adult learning",
        "session": "45-60 minutes",
        "focus": [
            "Define a concrete outcome and a deadline before starting (for example: 'solve a past paper in 60 minutes by June').",
            "Plan 3-5 sessions a week in a fixed calendar slot.",
            "Finish with a small project that proves understanding, not only a course completion.",
            "Share progress with one other person for accountability.",
        ],
    },
}

# topics are ordered foundational -> advanced; each level starts at the front and goes as far as it needs
SUBJECTS = {
    "mathematics": {
        "title": "Mathematics",
        "topics": [
            "Number sense, place value and the four operations",
            "Fractions, decimals and percentages",
            "Ratio, proportion and rates",
            "Algebra: expressions, equations and inequalities",
            "Geometry, measurement and trigonometry",
            "Functions, graphs and sequences",
            "Statistics and probability",
            "Calculus: limits, derivatives and integrals",
            "Linear algebra and mathematical proof",
        ],
        "pitfalls": [
            "Memorising procedures without knowing why they work",
            "Skipping the check step (substitute the answer back in)",
            "Losing marks to sign errors and missing units",
        ],
        "practice": [
            "Study a worked example, then solve the same type of problem with the example covered",
            "Keep an error log: write each wrong step and the rule it broke",
            "Mix problem types in one session so the learner has to pick the method",
        ],
        "check": "Can you solve a new problem of this type without the example in front of you?",
    },
    "physics": {
        "title": "Physics",
        "topics": [
            "Units, measurement and dimensional analysis",
            "Kinematics and Newton's laws",
            "Work, energy and power",
            "Waves, sound and light",
            "Electricity and magnetism",
            "Thermodynamics and kinetic theory",
            "Modern physics: atoms, nuclei and relativity",
            "Quantum mechanics and statistical physics",
        ],
        "pitfalls": [
            "Plugging numbers into formulas without drawing a sketch or free-body diagram",
            "Mixing up scalar and vector quantities",
            "Leaving units until the final answer",
        ],
        "practice": [
            "Draw a diagram before every problem, even when it is not asked for",
            "Derive one formula a week from first principles",
            "Explain each law in one sentence, in your own words",
        ],
        "check": "Can you predict how the result changes when one variable changes, before calculating?",
    },
    "chemistry": {
        "title": "Chemistry",
        "topics": [
            "Atomic structure and the periodic table",
            "Chemical bonding and molecular shape",
            "Stoichiometry and the mole concept",
            "States of matter and gas laws",
            "Chemical equilibrium and reaction rates",
            "Acids, bases and buffers",
            "Redox and electrochemistry",
            "Organic chemistry: functional groups and mechanisms",
            "Spectroscopy and analytical techniques",
        ],
        "pitfalls": [
            "Balancing equations by guessing",
            "Confusing moles, mass and number of particles",
            "Memorising reactions without the trend or mechanism behind them",
        ],
        "practice": [
            "Redraw the periodic table from memory, then check the trends",
            "Draw electron-pushing arrows by hand for each mechanism",
            "Do one stoichiometry problem a day until the unit conversions become automatic",
        ],
        "check": "Can you explain why a reaction goes the way it does, not only what the product is?",
    },
    "biology": {
        "title": "Biology",
        "topics": [
            "Cell structure and organelles",
            "Biochemistry: enzymes, carbohydrates, proteins and lipids",
            "Genetics and inheritance",
            "Molecular biology: DNA, RNA and protein synthesis",
            "Physiology of the body systems",
            "Ecology, evolution and biodiversity",
            "Microbiology and immunology",
            "Plant biology and photosynthesis",
        ],
        "pitfalls": [
            "Memorising long lists of terms without linking them to a process",
            "Mixing up similar terms (mitosis vs meiosis, DNA vs RNA)",
            "Ignoring the diagrams the exam will ask you to label or draw",
        ],
        "practice": [
            "Draw each process as a flowchart from memory",
            "Write flashcards with 'why' questions, not only definitions",
            "Explain a process aloud, as if teaching a younger student",
        ],
        "check": "Can you draw the process and explain what happens at each step?",
    },
    "english-literature": {
        "title": "English Language and Literature",
        "topics": [
            "Grammar, punctuation and sentence structure",
            "Vocabulary in context and word formation",
            "Reading comprehension and inference",
            "Writing paragraphs, essays and argument structure",
            "Literary analysis: theme, character, form and style",
            "Rhetoric and persuasive writing",
            "Research writing and referencing",
            "Literary theory and criticism",
        ],
        "pitfalls": [
            "Summarising the text instead of analysing it",
            "Writing a thesis that states a fact instead of an arguable claim",
            "Quoting without explaining what the quotation shows",
        ],
        "practice": [
            "Read one passage a day and write a one-paragraph analysis",
            "Rewrite one paragraph in three different styles and compare the effect",
            "Keep a vocabulary notebook with an example sentence for each word",
        ],
        "check": "Does each paragraph make one clear point that supports the thesis?",
    },
    "history": {
        "title": "History",
        "topics": [
            "Chronology and timelines",
            "Causes, consequences and change over time",
            "Primary and secondary sources",
            "Historiography and competing interpretations",
            "Economic and social history",
            "Political and constitutional history",
            "Connecting regional and world history",
            "Historical argument and essay writing",
        ],
        "pitfalls": [
            "Memorising dates without the causes that link them",
            "Treating a single source as the whole truth",
            "Writing narrative when the question asks for an argument",
        ],
        "practice": [
            "Build a timeline and add cause arrows between events",
            "Compare two sources that disagree and write down why",
            "Answer 'to what extent' questions in three paragraphs: for, against, judgement",
        ],
        "check": "Can you name three causes and rank them by importance, with reasons?",
    },
    "geography": {
        "title": "Geography",
        "topics": [
            "Maps, scale and basic GIS",
            "Physical geography: landforms, climate and water",
            "Human geography: population, settlement and migration",
            "Economic geography and development",
            "Environment, hazards and sustainability",
            "Urban geography",
            "Regional case studies",
            "Quantitative methods and fieldwork",
        ],
        "pitfalls": [
            "Learning case studies without their key facts (places, dates, numbers)",
            "Describing a pattern without explaining the process behind it",
            "Ignoring the map or diagram that comes with the question",
        ],
        "practice": [
            "Sketch each process as a labelled diagram",
            "Make a case-study card: place, cause, effect, response",
            "Read one news story a week and link it to a geographic concept",
        ],
        "check": "Can you explain a pattern on a map using two processes?",
    },
    "economics": {
        "title": "Economics",
        "topics": [
            "Scarcity, opportunity cost and choice",
            "Supply, demand and market equilibrium",
            "Elasticity",
            "Market structures and competition",
            "Macroeconomics: GDP, inflation and unemployment",
            "Monetary and fiscal policy",
            "International trade and exchange rates",
            "Econometrics and data analysis",
        ],
        "pitfalls": [
            "Using jargon without applying it to the scenario",
            "Drawing diagrams without labelling the axes and the shift",
            "Confusing a movement along a curve with a shift of the curve",
        ],
        "practice": [
            "Draw each diagram from memory and label every part",
            "Apply one concept to a current news item each week",
            "Solve one numerical problem (elasticity or multiplier) a day",
        ],
        "check": "Can you say what shifts the curve, and what only moves along it?",
    },
    "computer-science": {
        "title": "Computer Science and Programming",
        "topics": [
            "Programming fundamentals: variables, control flow and functions",
            "Data structures: arrays, lists, stacks, queues, trees and graphs",
            "Algorithms: searching, sorting and complexity",
            "Databases and SQL",
            "Operating systems and networks",
            "Software design and testing",
            "Discrete mathematics and logic",
            "Machine learning and advanced systems",
        ],
        "pitfalls": [
            "Copying code without tracing it by hand",
            "Ignoring edge cases and error handling",
            "Memorising syntax instead of the underlying model",
        ],
        "practice": [
            "Trace code line by line on paper before running it",
            "Solve one problem a day, then compare your solution with a clean one",
            "Build a small project that uses each new concept",
        ],
        "check": "Can you implement it from a blank file without looking at your notes?",
    },
    "statistics": {
        "title": "Statistics and Data Analysis",
        "topics": [
            "Descriptive statistics and data visualisation",
            "Probability distributions",
            "Sampling and sampling distributions",
            "Hypothesis testing and p-values",
            "Confidence intervals",
            "Regression and correlation",
            "Experimental design",
            "Bayesian inference and modelling",
        ],
        "pitfalls": [
            "Reading a p-value as the probability that the hypothesis is true",
            "Confusing correlation with causation",
            "Running a test without checking its assumptions",
        ],
        "practice": [
            "Analyse a real dataset and write a one-paragraph conclusion",
            "Simulate a concept (such as sampling) in code to see it happen",
            "For each test, write: question, assumption, statistic, decision",
        ],
        "check": "Can you say what the result means, and what it does not mean?",
    },
    "accounting-finance": {
        "title": "Accounting and Finance",
        "topics": [
            "Double-entry bookkeeping and the accounting cycle",
            "Financial statements: balance sheet, income statement and cash flow",
            "Cost and management accounting",
            "Ratio analysis",
            "Time value of money and investment appraisal",
            "Corporate finance and capital structure",
            "Auditing and internal control",
            "Taxation basics",
        ],
        "pitfalls": [
            "Debiting and crediting by memory instead of by the logic of the account",
            "Reading ratios as numbers without context",
            "Mixing up cash timing and accrual timing",
        ],
        "practice": [
            "Post each transaction to T-accounts before writing the journal entry",
            "Read a real annual report and find the key lines in each statement",
            "Redo a past exam question from a blank page",
        ],
        "check": "Can you explain what changed in the balance sheet after one transaction?",
    },
    "foreign-languages": {
        "title": "Foreign Language Learning",
        "topics": [
            "Pronunciation and listening",
            "High-frequency vocabulary",
            "Basic grammar: word order, verbs and tenses",
            "Reading short texts",
            "Speaking and conversation",
            "Writing short texts and messages",
            "Idioms, register and culture",
            "Advanced grammar and nuance",
        ],
        "pitfalls": [
            "Learning word lists without any context",
            "Putting off speaking until the learner feels ready",
            "Translating word for word",
        ],
        "practice": [
            "Review 20 new words a day with spaced repetition, always inside a sentence",
            "Shadow a native speaker's audio for 10 minutes (repeat each sentence aloud)",
            "Write a short diary entry each day and get it corrected",
        ],
        "check": "Can you hold a two-minute conversation on a familiar topic without preparing?",
    },
    "psychology": {
        "title": "Psychology",
        "topics": [
            "Research methods and basic statistics",
            "Biological bases of behaviour",
            "Learning and memory",
            "Cognition, perception and language",
            "Development across the lifespan",
            "Social psychology",
            "Personality and individual differences",
            "Abnormal psychology and clinical practice",
            "Ethics and research design",
        ],
        "pitfalls": [
            "Memorising theorists without the study that supports them",
            "Confusing correlation with causation",
            "Using everyday meanings of terms (such as 'stress' or 'learning') instead of the technical definition",
        ],
        "practice": [
            "Summarise one study as: question, method, result, limitation",
            "Apply a theory to an everyday example you have seen this week",
            "Make a comparison table for two related theories",
        ],
        "check": "Can you describe a classic study and say what it does and does not show?",
    },
    "law": {
        "title": "Law",
        "topics": [
            "Legal reasoning and sources of law",
            "Contract law: formation, terms and remedies",
            "Tort law: negligence and liability",
            "Criminal law: actus reus, mens rea and defences",
            "Constitutional and administrative law",
            "Property and land law",
            "Evidence and procedure",
            "Legal writing and case analysis",
        ],
        "pitfalls": [
            "Memorising case names without the principle each one establishes",
            "Writing a conclusion without applying the rule to the facts",
            "Ignoring jurisdiction: the rules differ between countries and between states",
        ],
        "practice": [
            "Brief one case a day: facts, issue, rule, reasoning, holding",
            "Write one IRAC answer (Issue, Rule, Application, Conclusion) a week and get it marked",
            "Make a one-page outline for each topic",
        ],
        "check": "Can you apply the rule to a new set of facts and reach a reasoned conclusion?",
    },
    "arts-design": {
        "title": "Visual Arts and Design",
        "topics": [
            "Visual elements and principles: line, shape, colour and composition",
            "Colour theory and palettes",
            "Drawing and observation",
            "Art history and movements",
            "Design process: research, ideation and prototyping",
            "Typography and layout",
            "Media and techniques: painting, digital and photography",
            "Critique, concept development and portfolio",
        ],
        "pitfalls": [
            "Copying an image without understanding the principle behind it",
            "Skipping research and jumping straight to the final piece",
            "Taking critique personally instead of using it as information",
        ],
        "practice": [
            "Do a 15-minute observational sketch every day",
            "Study one artwork a week: context, technique and intent",
            "Keep a sketchbook with notes on what you tried and why",
        ],
        "check": "Can you explain why a design choice works, not only that it looks good?",
    },
    "music-theory": {
        "title": "Music Theory",
        "topics": [
            "Rhythm, metre and note values",
            "Pitch, scales and key signatures",
            "Intervals and chords",
            "Harmony and voice leading",
            "Musical form and structure",
            "Ear training and dictation",
            "Sight-reading",
            "Counterpoint and advanced harmony",
        ],
        "pitfalls": [
            "Learning scales on paper without hearing them",
            "Memorising chord names without knowing their function",
            "Practising only what already feels comfortable",
        ],
        "practice": [
            "Sing intervals and scales for 10 minutes a day (ear training)",
            "Analyse one piece a week: key, form and cadences",
            "Write a short melody or harmonisation every week",
        ],
        "check": "Can you name an interval or chord by ear without looking?",
    },
}

METHODS = {
    "active-recall": {
        "title": "Active Recall",
        "description": "Study technique that makes the learner retrieve answers from memory instead of rereading notes. Use when a learner is rereading, highlighting, or asking how to remember more for a test.",
        "steps": [
            "Close the notes. Write or say everything you remember about the topic in two minutes.",
            "Open the notes and mark what you missed, in a different colour or with a symbol.",
            "Turn the missed items into questions (front of a card, or a question line in your notes).",
            "Repeat the questions the next day, then in a few days. Stop when you can answer them all cold.",
        ],
        "example": "After a biology lesson on the cell cycle, write the phases from memory, then check against the textbook and make one question per missed phase.",
        "mistakes": [
            "Rereading the same page several times and calling it revision",
            "Making questions that can be answered yes or no",
            "Checking the answer before you have tried to recall it",
        ],
    },
    "spaced-repetition": {
        "title": "Spaced Repetition",
        "description": "Scheduling method that reviews material just before it would be forgotten, so it is remembered for longer. Use when a learner has a long list of facts (vocabulary, definitions, dates) or an exam weeks away.",
        "steps": [
            "Put each item on a card with a question on the front and the answer on the back.",
            "Review new cards the next day. If correct, review again after about 3 days, then about a week, then about 2-3 weeks.",
            "If a card is wrong, bring it back the next day.",
            "Limit daily reviews to a number you can finish (for example 30-50 cards).",
        ],
        "example": "A language learner adds 20 new words a day as cards with a full example sentence on the back. Reviews are done each morning in the order the app schedules them.",
        "mistakes": [
            "Adding too many new cards per day, so reviews pile up",
            "Writing cards that contain several facts at once",
            "Stopping the schedule during a busy week and never restarting it",
        ],
    },
    "feynman-technique": {
        "title": "Feynman Technique",
        "description": "Learning method that tests understanding by explaining a concept in plain language and finding the gaps. Use when a learner can repeat definitions but cannot explain or apply them.",
        "steps": [
            "Write the concept's name at the top of a blank page.",
            "Explain it in simple words, as if to a 12-year-old. Do not use jargon you have not defined.",
            "Note every point where you hesitate, skip, or fall back on a technical term.",
            "Go back to the source for those points only, then explain again from memory.",
        ],
        "example": "Explaining osmosis to a friend: 'water moves across a membrane from where there is more water to where there is less'. The hesitation is 'why', so reread that part and try again.",
        "mistakes": [
            "Explaining with words you have only memorised",
            "Skipping the explanation for topics that already feel familiar",
            "Stopping at the first clean explanation without applying the idea to a new example",
        ],
    },
    "pomodoro-focus": {
        "title": "Pomodoro and Focus Blocks",
        "description": "Time-management method that splits study into fixed focus blocks with short breaks. Use when a learner struggles to start, keeps checking the phone, or loses track of time.",
        "steps": [
            "Choose one task and write it at the top of the page.",
            "Set a timer for 25 minutes (or 15 for primary school learners, 45-50 for self-learners who prefer longer blocks).",
            "Work on the task only. Put the phone in another room.",
            "Take a 5-minute break. After four blocks, take a longer break of 15-30 minutes.",
        ],
        "example": "A secondary school learner does four 25-minute blocks on quadratic equations, with a checklist of the questions they want to finish in each block.",
        "mistakes": [
            "Using the timer but choosing a vague task like 'study maths'",
            "Taking the break on the phone, so the break becomes the new distraction",
            "Changing the block length on every attempt before measuring what works",
        ],
    },
    "cornell-notes": {
        "title": "Cornell Notes",
        "description": "Note-taking layout with three parts: notes, cues and summary. Use when a learner's notes are a long unstructured copy of the lecture or textbook.",
        "steps": [
            "Divide the page: a narrow left column (cues), a wide right column (notes), and a bottom strip (summary).",
            "During the lesson, write the main notes in the right column. Use short phrases, not full sentences.",
            "After the lesson, write questions and keywords in the left column.",
            "Cover the right column and use the cues to recall the notes. Then write a 2-3 line summary at the bottom.",
        ],
        "example": "A history lecture on the French Revolution: the cue column reads 'causes?', 'Estates-General', 'who benefited?'. The summary gives the chain of causes in three lines.",
        "mistakes": [
            "Copying everything word for word",
            "Leaving the cue column empty, so the page cannot be used for recall",
            "Skipping the summary, which is where the understanding is checked",
        ],
    },
    "interleaved-practice": {
        "title": "Interleaved Practice",
        "description": "Practice method that mixes different problem types in one session so the learner has to choose the right approach. Use when a learner can solve each type in isolation but cannot tell which method a new problem needs.",
        "steps": [
            "Collect problems from at least three topics you have covered.",
            "Shuffle them. Do not label the topic.",
            "For each problem, first write which method you think applies and why.",
            "Solve it, then check the method choice as well as the answer.",
        ],
        "example": "A maths session with a mixed set: one percentage problem, one linear equation, one geometry problem. The learner writes the method for each before solving.",
        "mistakes": [
            "Practising one topic for an hour, then moving on, so the mix never happens",
            "Checking only whether the answer is right, not whether the method fits",
            "Using interleaving for topics the learner has never been taught",
        ],
    },
    "past-paper-practice": {
        "title": "Past-Paper Practice",
        "description": "Exam preparation method: solving real past papers under timed conditions and marking them against the official scheme. Use when a learner is preparing for a board, entrance, or university exam.",
        "steps": [
            "Get the official past papers and mark schemes for the exam (from the examining body or the school).",
            "Sit one paper under timed conditions with no notes. Keep to the time for each section.",
            "Mark it with the official scheme. Use a different colour for marks lost.",
            "For each mark lost, write the cause (knowledge, method, reading the question, time) and the fix.",
        ],
        "example": "A learner does a two-hour physics paper in 2 hours 10 minutes, marks it, and finds 12 marks lost on units and 8 on timing. The plan for next week addresses both.",
        "mistakes": [
            "Looking up answers during the attempt",
            "Marking vaguely ('mostly right') instead of against the scheme",
            "Doing only the paper you like, instead of the whole range of question types",
        ],
    },
    "exam-day-strategy": {
        "title": "Exam-Day Strategy",
        "description": "Plan for the day of an exam: time allocation, question order and handling of blanks. Use when a learner is anxious about exam conditions or runs out of time in exams.",
        "steps": [
            "Before the exam, read the paper rules and write the time per section in pencil in the margin.",
            "Answer the questions you can do well first, to bank marks and calm down.",
            "If a question is stuck after the allotted time, mark it and move on. Return to it at the end.",
            "In the last 10 minutes, check the answers you were unsure about, and check that every question has an answer.",
        ],
        "example": "A 3-hour paper with 6 questions: 30 minutes each, plus 15 minutes at the end. The learner leaves a hard 4-mark part for the end and comes back to it with fresh thinking.",
        "mistakes": [
            "Spending the whole time on the first question because it feels fair",
            "Leaving a blank when some partial method would earn marks",
            "Doing no practice under exam conditions, so the real timing is a surprise",
        ],
    },
}

GENERATED_NOTE = (
    "<!-- Generated by arena-session-3b2d329a/artifacts/build_study_skills.py. "
    "Edit the generator, not this file. -->"
)


def frontmatter(name: str, description: str) -> str:
    return f"---\nname: {name}\ndescription: {description}\n---\n"


def coach_skill(level_key: str, subj_key: str) -> tuple[str, str]:
    level = LEVELS[level_key]
    subj = SUBJECTS[subj_key]
    name = f"study-{level_key}-{subj_key}"
    description = (
        f"Study coach for {subj['title']} at the {level['label']} level. Use when the learner asks for "
        f"a study plan, an explanation, practice questions, a self-check, or a revision strategy for "
        f"{subj['title'].lower()}. Covers the core topics, common pitfalls, and a repeatable session routine "
        f"of {level['session']}."
    )
    topics = "\n".join(f"{i}. {t}" for i, t in enumerate(subj["topics"], 1))
    focus = "\n".join(f"- {f}" for f in level["focus"])
    pitfalls = "\n".join(f"- {p}" for p in subj["pitfalls"])
    practice = "\n".join(f"- {p}" for p in subj["practice"])
    body = f"""{GENERATED_NOTE}

# {subj['title']} study coach — {level['label']}

## When to use

Use this skill when the learner is studying {subj['title'].lower()} at the {level['label']} level, or asks for
help planning, explaining, practising or revising it. Do not use it for other subjects.

## Level focus

{focus}

## Session routine ({level['session']})

1. **Recall (5 min):** ask the learner to recall the last session's key points from memory before you say anything.
2. **Explain (about 1/3 of the session):** teach one topic from the list below, with one worked example. Ask first what the learner already knows.
3. **Practise (about 1/3):** the learner solves 3-5 items. Check each step, not only the final answer.
4. **Review (last 10%):** the learner writes each error and the rule it broke into an error log, then picks the next topic.

## Core topics (foundational to advanced)

Start at the first topic that the learner does not yet know well. Move on only when the learner passes the check below.

{topics}

## Common pitfalls to watch for

{pitfalls}

## Practice activities

{practice}

## Check understanding

Ask: **{subj['check']}**

Then ask the learner one question from a topic they have not seen yet in this session, so you can see what transfers.

## Coach rules

- Find out what the learner already knows before explaining.
- Ask the learner to explain back in their own words before moving on.
- Never invent references, page numbers, or exam questions. Say when the learner should check the official syllabus, the textbook, or the examining body.
- If the learner is stuck for more than two attempts, change the explanation (a different example or a diagram), not only the wording.
"""
    return name, frontmatter(name, description) + "\n" + body


def method_skill(key: str) -> tuple[str, str]:
    m = METHODS[key]
    name = f"study-method-{key}"
    steps = "\n".join(f"{i}. {s}" for i, s in enumerate(m["steps"], 1))
    mistakes = "\n".join(f"- {x}" for x in m["mistakes"])
    body = f"""{GENERATED_NOTE}

# {m['title']}

## When to use

{m['description']}

## Steps

{steps}

## Example

{m['example']}

## Common mistakes

{mistakes}

## Coach rules

- Explain the method briefly, then have the learner try it on their own material straight away.
- Check at the end of the session: did the learner actually do the method, or only talk about it?
"""
    return name, frontmatter(name, m["description"]) + "\n" + body


def index_readme(entries: list[tuple[str, str]]) -> str:
    lines = [
        "# skills/",
        "",
        "Agent Skills (open standard: one folder per skill, each with a `SKILL.md`). Works with Claude Code,",
        "GitHub Copilot, Cursor and other agents that read the Agent Skills format.",
        "",
        "Generated by `arena-session-3b2d329a/artifacts/build_study_skills.py`, except `agent-skill-security-audit/`,",
        "which is hand-written. Regenerate the study skills with:",
        "",
        "```bash",
        "python3 arena-session-3b2d329a/artifacts/build_study_skills.py",
        "```",
        "",
        "## Study method skills",
        "",
        "| Skill | Use it for |",
        "|---|---|",
    ]
    for name, desc in entries:
        if name.startswith("study-method-"):
            lines.append(f"| `{name}` | {desc.split('.')[0]}. |")
    lines += ["", "## Subject coaches by level", ""]
    for level_key, level in LEVELS.items():
        lines.append(f"### {level['label'].capitalize()}")
        lines.append("")
        lines.append("| Subject | Skill |")
        lines.append("|---|---|")
        for subj_key, subj in SUBJECTS.items():
            lines.append(f"| {subj['title']} | `study-{level_key}-{subj_key}` |")
        lines.append("")
    lines += [
        "## Security",
        "",
        "| Skill | Use it for |",
        "|---|---|",
        "| `agent-skill-security-audit` | Scan a skill folder for prompt-injection, exfiltration and supply-chain risks before installing it. |",
        "",
        "See `../security/redteam-eval/` for the canary-based guardrail test set.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    entries: list[tuple[str, str]] = []
    written = 0
    for key in METHODS:
        name, text = method_skill(key)
        d = OUT / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(text, encoding="utf-8")
        entries.append((name, METHODS[key]["description"]))
        written += 1
    for level_key in LEVELS:
        for subj_key in SUBJECTS:
            name, text = coach_skill(level_key, subj_key)
            d = OUT / name
            d.mkdir(parents=True, exist_ok=True)
            (d / "SKILL.md").write_text(text, encoding="utf-8")
            entries.append((name, ""))
            written += 1
    (OUT / "README.md").write_text(index_readme(entries), encoding="utf-8")
    print(f"wrote {written} skills to {OUT.relative_to(REPO)}/ (+ README.md)")


if __name__ == "__main__":
    main()
