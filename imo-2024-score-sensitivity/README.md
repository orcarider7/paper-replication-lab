# How much does the 2024 IMO score comparison depend on one problem?

Hubert and colleagues report that AlphaProof solved problems 1, 2 and 6 of the 2024 International Mathematical Olympiad (IMO), and AlphaGeometry 2 solved problem 4. The combined system received seven points on each of those four and zero on the other two. This note reconstructs its silver-medal-equivalent score, then removes each problem in turn from both the system and all 609 contestants. The paper was published in *Nature* in 2025. SCImago lists the journal in Q1 for Multidisciplinary in 2025. [Paper](https://doi.org/10.1038/s41586-025-09833-y) · [Authors' account of grading and timing](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/) · [Journal quartile](https://www.scimagojr.com/journalsearch.php?q=21206&tip=sid)

## Reproduction

The combined system scored **28 out of 42**. The official silver threshold was 22, and gold began at 29. Exactly 58 contestants scored above 28, 17 scored 28 and 534 scored below it. Inserting the system into this fixed score distribution would place it joint 59th. An October 2026 study by IQ Metrics also reports this baseline rank. The authors of the Nature paper describe human formalization and up to three days of machine computation. Contestants sat two sessions of 4.5 hours. The comparison concerns the points awarded to the solutions. [Official score table](https://www.imo-official.org/results/individual/year/2024/) · [Official medal thresholds](https://www.imo-official.org/editions/2024/) · [Prior score comparison](https://zenodo.org/records/23760888)

## Removing one problem at a time

For each omission, add the remaining five scores for the system and for every contestant. The rank is one plus the number of humans strictly above the system. Tied humans share that rank. The 609 people remain the comparison field throughout. “All six” uses a maximum of 42 points. Every other row uses 35.

| Omitted problem | System points | Humans above | Tied | Below | Hypothetical rank |
| --- | ---: | ---: | ---: | ---: | ---: |
| All six scored | 28 | 58 | 17 | 534 | 59 |
| P1 | 21 | 58 | 18 | 533 | 59 |
| P2 | 21 | 82 | 46 | 481 | 83 |
| P3 | 28 | 38 | 29 | 542 | 39 |
| P4 | 21 | 61 | 17 | 531 | 62 |
| P5 | 28 | 8 | 8 | 593 | 9 |
| P6 | 21 | 163 | 47 | 399 | 164 |

The extremes show how the particular choice of questions affects the comparison. P5 was a combinatorics problem on which the system scored zero. Removing it lets the system retain all 28 points and leaves eight contestants ahead. P6 was an algebra problem on which it earned full marks. Removing that problem puts 163 ahead. The other four omissions produce intermediate ranks. These are six deterministic changes to one exam. Contestants and systems could allocate their time differently on a five-problem exam, and no five-problem medals were awarded. This calculation evaluates the published outputs. Training, proof search and grading were outside its scope. Priority for this sensitivity check has not been established.

## Reproduce the table

Run `python verify.py` from this directory with Python 3.9 or later. The standard-library script reads the official table and reconstructs every contestant's published total and competition rank. It uses only numeric results and prints aggregate counts. To use a previously saved copy of the source page, run `python verify.py path/to/official-2024-results.html`. [Script](verify.py) · [Official table](https://www.imo-official.org/results/individual/year/2024/)

The November 26, 2026 retrieval produced an anonymous 609-by-6 matrix with SHA-256 `260ae36b5b53cd3db57669f8230a0f718e3954dd4d3f2f6d4f5b41d64e3cf151`. To obtain the same digest, retain duplicate score vectors, sort the six-integer tuples lexicographically, write one comma-separated tuple per line with a final LF, and encode in ASCII. This identifies the mathematical input independently of page layout or contestant ordering.

As a separate check, filtering the archived TidyTuesday CSV to `year == 2024` and selecting `p1` through `p6` reproduced the same 609 rows and digest. This archive is a second copy of the IMO observations. [Commit-pinned CSV](https://github.com/rfordatascience/tidytuesday/blob/6a9aaa7402f456f6c49070b393036678e2f59f72/data/2024/2024-09-24/individual_results_df.csv)

OpenAI Codex assisted with the analysis, code and text. The primary sources above credit the system developers and the IMO results team.
