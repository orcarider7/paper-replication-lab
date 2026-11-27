# Can one benchmark change the leader in the MedHELM paper?

MedHELM appeared in *Nature Medicine* on 20 January 2026. Its Table 1 reports a mean win rate of 0.66 for each of the two leading models, DeepSeek R1 and o3-mini. The authors' paper-specific score file gives 0.662 and 0.660. Recomputing pairwise wins from all 37 benchmark columns and leaving out one benchmark at a time, **DeepSeek R1 leads in 17 of 37 omissions and o3-mini leads in the other 20** under half credit for ties. Both models refer to the versions in the paper. [Original study, Table 1](https://doi.org/10.1038/s41591-025-04151-2) · [Authors' analysis code and data](https://github.com/som-shahlab/medhelm) · [Score file](https://github.com/som-shahlab/medhelm/blob/main/data/leaderboard.csv)

## Calculation

On each benchmark, compare each of the nine models to its eight opponents using the publicly displayed decimal scores. Award one point per higher score and half a point per tie. Average over all opponents and all benchmarks. This gives each benchmark the same weight regardless of its number of examples and avoids averaging raw metrics with different scales. On all 37 benchmarks the two leaders receive 392/592 and 391/592, respectively, in half-point units. Omitting MedCalc-Bench gives 376/576 and 377/576, flipping the order. Omitting CLEAR gives 378/576 and 375/576, retaining it.

To distinguish actual wins from the ranking credits, compare just the two models on each benchmark:

| Benchmark group | DeepSeek R1 higher | Tied at reported precision | o3-mini higher |
| --- | ---: | ---: | ---: |
| All 37 | 20 | 2 | 15 |
| 13 columns labeled “Jury Score” | 10 | 0 | 3 |
| 24 other columns | 10 | 2 | 12 |

The jury-scored benchmarks and the other benchmarks cover different tasks. These counts cannot isolate a causal effect of using a jury.

## Effect of displayed ties

Ties in the released table may result from decimal rounding. The script reruns every omission under three explicit conventions. More than one model can share first place.

| Win credit for ties | DeepSeek R1 alone | o3-mini alone | Both share first |
| --- | ---: | ---: | ---: |
| Zero | 15 | 20 | 2 |
| Half | 17 | 20 | 0 |
| Full | 17 | 12 | 8 |

These are exact counts on a fixed table. Their scope excludes patient outcomes, performance on future tasks, uncertainty within each benchmark, and the probability that either model is better. The published aggregates come from the authors. Reconstructing a ranking from the displayed decimal entries can change close comparisons. The live MedHELM leaderboard also has other versions.

The original article already identifies both models as leading performers. Sensitivity of rankings to aggregation choices is an established concern in biomedical benchmarking. The contribution here is a reproducible, paper-specific set of omission counts and a check of how ties influence them. Priority for this precise computation has not been established. [Earlier empirical work on biomedical ranking sensitivity](https://pubmed.ncbi.nlm.nih.gov/30523263/)

## Reproducibility

Run `python check.py` with Python 3.9 or later. It retrieves the authors' aggregate table and checks SHA-256 `75d510d317df8a79e5694c6278331dcf4156cac453738847d41c625791fcd7c0`. To work offline, run `python check.py path/to/leaderboard.csv`. The code uses the standard library and exact decimal comparisons. It needs no individual patient data or model calls.

OpenAI Codex drafted the note and wrote and ran the reanalysis. The benchmark, model scores and underlying evaluations are the original team's work.
