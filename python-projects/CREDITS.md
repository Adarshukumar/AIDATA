# CREDITS.md — who wrote what

This folder mixes my own work with two open-source collections. This file is the record of
which is which.

## My own work

| Path | What it is | Author |
|---|---|---|
| `python-learning/` | 54 files: roadmap, 50 numbered lessons, cheatsheet, 40 practice challenges | **Adarsh** ([@Adarshukumar](https://github.com/Adarshukumar)) |
| `README.md`, `CREDITS.md` | This documentation | **Adarsh** |

## Third-party collections (not my work)

| Folder | Upstream repository | License | Main authors |
|---|---|---|---|
| `collections/python-mini-project/` | [ndleah/python-mini-project](https://github.com/ndleah/python-mini-project) | **MIT** — Copyright (c) 2021 Leah Nguyen | [@ndleah](https://github.com/ndleah) and **100+ contributors** |
| `collections/all-in-one-python-projects/` | [king04aman/All-In-One-Python-Projects](https://github.com/king04aman/All-In-One-Python-Projects) | **MIT** — Copyright (c) 2023 Aman Kumar | [@king04aman](https://github.com/king04aman) and contributors |

Both folders keep their upstream `LICENSE` file and carry a `SOURCE.md`. The MIT license
requires the copyright notice and permission notice to stay with the code — that is why the
license files are kept verbatim and why this file exists.

### Modifications made to the copies

Only housekeeping, no content changes:

- removed: `.git/`, `.github/`, the `IMG/` badge folder, `__pycache__/`, `*.pyc`,
  `.DS_Store`, `.ipynb_checkpoints/`
- removed: individual assets larger than **2 MB** (videos, PDFs, large datasets and images)
  to keep this copy light — the originals are in the upstream repositories

No file was renamed, reworded, or re-attributed.

## Third-party projects deliberately **not** included

| Project | Stars | Reason |
|---|---:|---|
| [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python) | 225,250 | MIT, but extremely popular — use the original |
| [vinta/awesome-python](https://github.com/vinta/awesome-python) | 327,411 | CC BY — extremely popular |
| [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | 553,229 | **no license** → redistribution not permitted |
| [practical-tutorials/project-based-learning](https://github.com/practical-tutorials/project-based-learning) | 286,700 | MIT, but extremely popular |
| [MunGell/awesome-for-beginners](https://github.com/MunGell/awesome-for-beginners) | 90,251 | **no license** |
| [asabeneh/30-Days-Of-Python](https://github.com/asabeneh/30-Days-Of-Python) | 76,222 | **no license** |
| [jakevdp/PythonDataScienceHandbook](https://github.com/jakevdp/PythonDataScienceHandbook) | 50,140 | MIT, but extremely popular |
| [gto76/python-cheatsheet](https://github.com/gto76/python-cheatsheet) | 38,695 | **no license** |
| [satwikkansal/wtfpython](https://github.com/satwikkansal/wtfpython) | 37,123 | WTFPL, but extremely popular |
| [donnemartin/interactive-coding-challenges](https://github.com/donnemartin/interactive-coding-challenges) | 31,912 | custom license, extremely popular |

Rule used: **no license → cannot redistribute**; **≥ 30,000 stars → link instead of copy**
(a verbatim copy of a world-famous repo adds nothing over the link).

## License of this folder

No file here is relicensed. `python-learning/` is my own work; each collection folder stays
under its upstream license (MIT), shown above. If you reuse something, follow the license of
the folder you take it from.
