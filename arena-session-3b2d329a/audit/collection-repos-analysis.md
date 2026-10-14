# Analysis — two community Python-collection repos

*Session `3b2d329a`, 2026-10-14. Requested by the user: "see all the projects in detailed
manner". Method: GitHub API trees + blob-hash overlap checks (no eyeballing).*

Both repos were audited the same way as `Adarshukumar/Python`: metadata
(`GET /repos/{o}/{r}`), recursive tree, blob hashes, and the actual LICENSE/README text.

---

## 1. `ndleah/python-mini-project`

| Field | Value |
|---|---|
| Description | "🙌 Welcome open-source Python mini-project contributions!" |
| Created / last push | 2021-07-16 / 2024-08-16 |
| Stars / forks | **4,426** stars |
| License | **MIT** (Copyright (c) 2021 Leah Nguyen) |
| Size | 126 MB · language Python |
| Contributors | **100+** (first page alone) |
| Files | 587 blobs · **157 `.py`** · 122 `.md` (each project has a README from the repo's template) |
| Project folders | **131** |

**Structure:** one folder per project, each with a `README.md` generated from the repo's
own template (`🛠️ Description`, `⚙️ Languages or Frameworks Used`, `🌟 How to run`, …).
That README template is why the repo feels uniform — it is the contribution guide, not a
single author's style.

**Notable contents:** the collection spans small scripts (`Caesar_Cipher`,
`Currency_Converter`, `Number`, `Simple_dice`) to real mini-apps (`Chess_Game` 18 files,
`Othello-Reversi-Game` 16 files, `Firebase_Authentication_Using_Flask`, `Crud_in_flask`,
`digit-recognizer` with notebooks, `Finding_Lanes` computer vision, `Object_Detection`,
`Motion_Detection`, `Speech_To_Text`, `Text_Predication`, `RSS_Manager`, `website-builder`).

**Quality caveats found:**
- **14 committed `__pycache__` entries** and **4 `.DS_Store` files** — build junk that was
  never cleaned; a sign this is a merge-target for drive-by contributions.
- 7 notebooks and a 44-file `IMG/` folder of badges; a `Web/` folder.
- Because 100+ contributors wrote into it, the quality varies project to project; some are
  classroom-level scripts, a few are substantial apps.

**Overlap with what you already have:** Python-World/python-mini-projects shares only
**7 of 580** unique blobs (1%) — this is genuinely different content, not a re-upload.

### All 131 project folders (file counts)

| Address Validator | 2 |
| Animalese_translator | 28 |
| Automated_Mailing | 3 |
| Binary_Search_Tree | 2 |
| Binary_tree | 8 |
| CODE_OF_CONDUCT.md | 1 |
| Caesar_Cipher | 2 |
| Cat_command | 3 |
| Caterpillar_Game | 2 |
| Chess_Game | 18 |
| Chinese_FlashCard | 7 |
| Clip_Organizer | 4 |
| Color_Game | 3 |
| Connect-Four | 2 |
| Converter | 5 |
| Converting_Roman_to_Integer | 2 |
| Convoys_GameofLife | 4 |
| Crud_in_flask | 10 |
| Currency_Converter | 2 |
| Demerge_pdfs | 9 |
| Dice_Rolling_Stimulator | 2 |
| Dictionary | 4 |
| Diff_Utility | 3 |
| Download Audio | 2 |
| Egg_Catcher | 2 |
| Email Slicer | 2 |
| Encode_Morse.py | 4 |
| Execute Shell Command | 4 |
| Exercise-Timer | 6 |
| Expense_Tracker | 2 |
| ExtractPhoneNumberEmail | 3 |
| Face_Recognition | 2 |
| Fancy_Text_Generator | 3 |
| Finance_Tracker | 2 |
| Finding_Lanes | 6 |
| Firebase_Authentication_Using_Flask | 11 |
| GK_Maestro | 8 |
| Geo_Plot_Using_Folium | 6 |
| Google_Translate | 2 |
| HangMan | 3 |
| Hangman_Game | 2 |
| Hashed_and_Salted_Pass | 2 |
| IMG | 44 |
| IP_Locator | 4 |
| Image_compressor | 3 |
| Investment Calculator | 4 |
| LICENSE | 1 |
| Lazy_Pong | 4 |
| Madlibs | 2 |
| Mail_Checker | 3 |
| Matchmaker | 2 |
| Math_Game | 2 |
| Minesweeper_game | 4 |
| Morse_code_beep | 2 |
| Motion_Detection | 3 |
| Music-Player | 9 |
| NASA_Image_Extraction | 39 |
| Number Guessing | 2 |
| Number Guessing Upper Boundary | 3 |
| Object_Detection | 4 |
| Othello-Reversi-Game | 16 |
| Password Generator | 2 |
| Password_Generator_2 | 3 |
| Password_Manager | 2 |
| Plotter | 6 |
| Port Scanner | 2 |
| PostgreSQL_Dumper | 3 |
| Prefix_Trie | 3 |
| QR Code Generator | 3 |
| README.md | 1 |
| README_TEMPLATE.md | 1 |
| RSS_Manager | 18 |
| Regression using ANN | 2 |
| Rock_Paper_Scissors_Spock | 2 |
| Screenpet | 2 |
| Shape_Recognition | 4 |
| Simple_Http_Server | 2 |
| Simple_Image_resize | 5 |
| Simple_dice | 3 |
| Slideshare to PDF | 5 |
| Smart_Calculator | 3 |
| Snake_game | 3 |
| Socket_example | 3 |
| Speaking_Dictionary | 3 |
| Speaking_Wikipedia | 2 |
| Speech_To_Text | 3 |
| Spinning Donut | 4 |
| Sqlite-crud | 3 |
| Stack_structure | 2 |
| Star_Pyramid | 2 |
| Sudoku_solver | 2 |
| TEXTVENTURE | 3 |
| TestTypingSpeed | 2 |
| TextEncryptor | 2 |
| TextToSpeech | 2 |
| Text_Predication | 5 |
| Tic_Tac_Toe | 2 |
| Todo_App | 4 |
| Tower-of_Hanoi | 2 |
| Triangle Calculator | 2 |
| Url_Shortener | 4 |
| Web Scraping IPhone from Flipkart | 4 |
| Web scraping for book names | 2 |
| Weights_on_different_planets | 3 |
| Whatsapp_Bot | 2 |
| Windows_Shutdown | 2 |
| Word_Jumble | 2 |
| Wordle_Aid | 4 |
| Youtube_video_download | 2 |
| Zombie_Game | 4 |
| assests | 2 |
| csv_to_json | 2 |
| desktopassistant | 2 |
| digit-recognizer | 14 |
| earth.py | 1 |
| highest_score.txt | 1 |
| image_comparator | 2 |
| images_to_pdf_converter | 2 |
| img_to_ascii | 3 |
| infix_postfix_calculator | 3 |
| linked_lists | 11 |
| lorem_in_python | 3 |
| minionGame | 2 |
| mnist_digit_recognizer | 3 |
| qr_with_logo | 4 |
| requirements.txt | 1 |
| simple-chatbot | 2 |
| spam_bot | 6 |
| string_manipulator | 3 |
| web scraping- Find python jobs from a website | 2 |
| website-builder | 9 |
| xls_to_xlsx | 3 |

---

## 2. `king04aman/All-In-One-Python-Projects`

| Field | Value |
|---|---|
| Description | "A huge collection of awesome beginner-friendly Python projects starting from very basics to advance…" |
| Created / last push | 2023-01-26 / 2025-09-04 |
| Stars / forks | **410** stars |
| License | **MIT** (Copyright (c) 2023 by Aman Kumar) |
| Size | ~3 MB · language Python |
| Contributors | 24+ |
| Files | 237 blobs · **75 `.py`** · 40 `.md` |
| Project folders | **65** |

**Structure:** same idea, smaller scale — one folder per project, each with a README and a
small script. Projects are beginner-tier: `Age Calculator`, `Alarm Bot`, `Ascii Art
Generator`, `CountDown Timer`, `Digital Clock`, `Password`, `Pomodoro`, `Snake-Game`,
`Tic-Tac-Toc`, `QR`, `Weather`, plus a few with dependencies (`Audio Book Generator`,
`Facebook Video Downloader`, `Helmet Detection`, `Headlight Detection`, `Handwritten-Assignments`,
`Plagiarism-Checker`, `Extractive Text Summarization`, `Gesture-Based-Game-Controller`).

**Quality caveats found:**
- **3 committed `__pycache__` entries**, a stray `Example README.md`, and folder names that
  were truncated at spaces in the tree (`To`, `Simple`, `Text`, `Random`, `Video`,
  `Custom`, `Image`, `Gauss`, `Geographic`, `Expense`, `Currency`…) — the *real* names have
  spaces (e.g. `To-Do List`, `Custom GPT`); the truncation here is an artifact of my
  `split("/")` grouping, not of the repo.
- Several projects need API keys / external services (Custom GPT, Facebook Video
  Downloader, Weather) — they won't run as-is.
- **Overlap with Python-World/python-mini-projects: 1 of 198 unique blobs (0%).**
- Overlap with `ndleah/python-mini-project`: negligible — the two collections are distinct.

### All 65 project folders (file counts)

| Age Calculator | 2 |
| Alarm Bot | 3 |
| Ascii Art Generator | 3 |
| Audio Book Generator | 3 |
| CODE_OF_CONDUCT.md | 1 |
| CONTRIBUTING.md | 1 |
| CountDown Timer | 3 |
| Currency Converter | 3 |
| Custom GPT | 4 |
| Customizable_Workout_Playlist_Generator | 4 |
| Digital Clock | 3 |
| Example README.md | 1 |
| Expense Splitter | 3 |
| Extractive Text Summarization | 3 |
| Facebook Video Downloader | 3 |
| Gauss Elimination with Partial Pivoting | 5 |
| Geographic Distance | 5 |
| Gesture-Based-Game-Controller | 4 |
| Handwritten-Assignments | 3 |
| Headlight Detection | 3 |
| Helmet Detection | 3 |
| Image Compression | 3 |
| ImageSize Reducer | 3 |
| Img-Steganograpy | 3 |
| LICENSE | 1 |
| Learn-FastAPI | 3 |
| Mental Health chatbot | 3 |
| Merge PDFs | 3 |
| MobileNumber Tracker | 3 |
| Mood Based Music Recommender | 4 |
| Movie Scraper | 3 |
| My-Personal-Journal | 12 |
| Notepad | 3 |
| OCR Image-to-Text Conversion | 3 |
| PROJECTS.md | 1 |
| Password Generator | 3 |
| Plagiarism-Checker | 5 |
| Pomodoro Timer | 3 |
| QR Code Generator | 6 |
| README.md | 1 |
| Random Movie Selector | 3 |
| Random Quotes Generator | 3 |
| Real-Time Cryptocurrency Price Tracker | 4 |
| Recipe Finder with Meal Planner | 3 |
| Resume Builder | 3 |
| Simple Assistant | 6 |
| Snake-Game | 10 |
| Speech To Text | 3 |
| Spell Checker | 3 |
| Telegram Bot | 3 |
| Text Summarizer | 5 |
| Text To Speech | 4 |
| Text to Morse Code | 2 |
| Text_Adventure_Game | 2 |
| Tic-Tac-Toc using AI (min-max) | 3 |
| To Do List | 9 |
| Translator | 3 |
| URL Sortener | 3 |
| Validate-Email | 2 |
| Video Processor | 3 |
| Video To Audio | 3 |
| Weather Alert | 5 |
| Word_frequency_counter | 4 |
| Youtube Video Downloader | 4 |
| personal-finance-tracker | 6 |

---

## 3. What the two repos have in common

1. **Both are MIT** — so vendoring their content *is* legal **if** the MIT license text and
   the copyright notice travel with the copy (MIT's only real condition).
2. **Neither is a single-author project.** `ndleah` has 100+ contributors, `king04aman`
   24+. Each project folder is somebody's submission. The repo owner's name is on the
   collection (README, LICENSE), but the copyright in individual projects belongs to the
   people who wrote them.
3. **Both are aggregators, not tutorials.** Their value is the *breadth* — 131 + 65 small
   runnable examples across games, CLI tools, Flask apps, CV, NLP.
4. **Neither is a copy of Python-World/python-mini-projects** (1% and 0% overlap), so
   adding them would actually add new material — unlike the 26 near-identical folders in
   `Adarshukumar/Python`.

## 4. Practical notes if you use them

- Both are safe to **fork** (GitHub keeps attribution automatically) or to **vendor with a
  `CREDITS.md`** pointing at the upstream repo + its LICENSE.
- Strip `__pycache__/`, `.DS_Store`, `IMG/` badges if you vendor — they are junk.
- Best use as a *learning index*: pick 10 projects, read them, rewrite them yourself in
  your own style with your own tests. That is work that is genuinely yours and it teaches
  more than copying 196 folders ever will.
