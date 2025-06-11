# A Conditional Proof of a Uniqueness Hypothesis for `A^x + B^y = C^z`

[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.XXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXX)

<!-- замените XXXXX на реальный номер после первого релиза -->

> **Status:** version 1.0 (16 Jun 2025); results hold *conditionally on the abc‑conjecture*.

This repository hosts the complete reproducible package for the paper
**“A Conditional Proof of a Uniqueness Hypothesis for $A^x + B^y = C^z$ under the abc‑Conjecture.”**
The manuscript proves that, assuming the *abc*-conjecture, equation
$A^x+B^y=C^z$ with $x,y,z>1$ has **at most one** solution in natural exponents.

---

## Directory layout

```text
.
├── main.tex                  ← LaTeX source of the paper
├── docs/UniquenessProof.pdf  ← compiled PDF (same as on arXiv)
├── kraiz_checker.py          ← finite‑search verification script
├── kraiz_log_20250605_142830.txt
├── .gitignore
└── README.md
```

---

## Build instructions

> **Prerequisites:** TeX Live 2023 + `latexmk`
> **Compile:**
>
> ```bash
> latexmk -pdf -interaction=nonstopmode main.tex
> ```
>
> The PDF is already provided in `docs/`, so compiling is optional.

---

## Reproducing the numerical check

```bash
python3 kraiz_checker.py                   # default ranges (≈10 s)
python3 kraiz_checker.py --help            # all options
```

`kraiz_log_*.txt` stores the run summary (number of triples scanned, runtime, near‑misses).

---

## How to cite

If you use this work, please cite **both** the article *and* this code/data archive:

```bibtex
@misc{Sosnovsky2025-Uniqueness,
  author       = {Oleksandr Sosnovsky},
  title        = {A Conditional Proof of a Uniqueness Hypothesis
                  for A^x + B^y = C^z under the abc-Conjecture},
  note         = {Zenodo: 10.5281/zenodo.XXXXX, v1.0},
  year         = 2025
}

@article{Sosnovsky2025-arXiv,
  author  = {Oleksandr Sosnovsky},
  title   = {A Conditional Proof of a Uniqueness Hypothesis
             for A^x + B^y = C^z under the abc-Conjecture},
  eprint  = {arXiv:2506.XXXXX},
  archivePrefix = {arXiv},
  primaryClass  = {math.NT},
  year    = 2025
}
```

*(replace `XXXXX` with the actual Zenodo/arXiv identifiers once assigned).*

---

## License

| Part              | License                              |
| ----------------- | ------------------------------------ |
| **Code** (`*.py`) | MIT License                          |
| **Manuscript**    | CC BY 4.0 © 2025 Oleksandr Sosnovsky |

---

## Contact

Questions, comments, or improvements are welcome — please open an issue or email me at [sosnovsky.math@proton.me](mailto:sosnovsky.math@proton.me).
