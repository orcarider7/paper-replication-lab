# Which models enter the ESOL split comparison?

A five-fold table in the public code release accompanying *A scaffold-aware reporting protocol for reliable aqueous solubility prediction using the Estimated SOLubility (ESOL) benchmark* combines a mean error difference from one model-selection rule and a paired test from another. This note reconstructs the released CSV row from the individual root mean squared errors (RMSE). Both selection rules give higher mean RMSE on the scaffold split. [Paper](https://doi.org/10.1080/00319104.2026.2727897) · [Author’s released analysis archive](https://github.com/a346616355/ESOL/blob/be0dacb6dc045b452a81f077a93db77108dcf2d0/ESOL-main.zip)

## Reconstructing the row

The published abstract of Zheng, Ju and Hong (2026) reports the two numbers together, rounded to a gap of 0.158 log units with p = 0.031. The public release below allows the source of both rounded numbers to be traced to specific fold vectors. The paper also reports a separate bootstrap confidence interval, outside the scope of this check. [Publisher's abstract](https://doi.org/10.1080/00319104.2026.2727897)

The source computes each model’s mean RMSE over the five folds, then chooses the lowest mean for each splitting method. Descriptor-based support-vector regression (SVR) wins on both. The same function constructs its paired test inputs by taking the best RMSE **within each fold** across all five models. The rules disagree on scaffold fold 0, where XGBoost wins. The other four scaffold folds and all five random folds select SVR. The relevant files in the author’s archive are `src/esol_project.py` lines 481–490, `results/tables/statistical_tests.csv` and `results/tables/cv_fold_metrics.csv`.

| Vectors compared | Mean scaffold RMSE minus mean random RMSE | Two-sided paired t-test using the release’s fold numbering |
| --- | ---: | ---: |
| Released statistics row | 0.1582571004 | 0.0313818624 |
| Best mean model under each split (SVR in both) | 0.1582571004 | 0.0152124486 |
| Best model within each fold | 0.1454793818 | 0.0313818624 |

The published CSV row takes the first numeric entry from the SVR comparison and the second from the within-fold comparison. A consistent comparison must name the selection rule and use its fold vectors for both quantities. Selecting after seeing each held-out fold's RMSE describes a retrospective best-of-five performance envelope.

## Dependence on fold numbering

The source generates random folds with shuffled KFold and scaffold folds with GroupKFold. Fold 0 under the random partition need not hold out the same molecules or scaffold groups as fold 0 under the other partition. Each method also reuses training examples across folds. Consequently the usual independent-pairs interpretation of these t-test p-values requires additional justification. See `src/esol_project.py` lines 228–236 in the [source archive](https://github.com/a346616355/ESOL/blob/be0dacb6dc045b452a81f077a93db77108dcf2d0/ESOL-main.zip).

Keeping the two lists of five errors fixed and permuting only their correspondence gives all 120 possible pairings. With fixed SVR the p-values range from 0.0134691 to 0.0383391, with 120 of 120 below .05. With per-fold winners they range from 0.0257324 to 0.0617806, with 89 of 120 below .05. Every pairing leaves the respective mean difference unchanged. These ranges quantify sensitivity to labeling. The 120 permutations impose no exchangeability model and deliver no corrected significance test.

## Reproduce

Run `python -B check.py` to download the commit-pinned archive in memory, or `python -B check.py path/to/ESOL-main.zip` to use the original snapshot. Both modes use Python's standard library, verify SHA-256 of the archive and both tables, and run numerical assertions. The repository stores its source code and tables inside `ESOL-main.zip`. The pinned commit archive contains that release ZIP. In download mode the script checks the outer archive and then verifies the inner ZIP exactly as in offline mode.

- Commit `be0dacb6dc045b452a81f077a93db77108dcf2d0` archive SHA-256 is `3581159e4efece0f741cf7e9cab84e8af4e36ed25c6d8ba09259dedf1be80517`.
- The original `ESOL-main.zip` snapshot SHA-256 is `8b219f43f636c5a35e82bfe1fb27f7f0cc39fafbb9d6c7ce6f5c87a9921707b9`.

The five paired differences give four degrees of freedom. For $x=|t|/\sqrt{t^2+4}$, the two-sided t-tail is $(1-x)^2(2+x)/2$, so the check needs no statistical package. The audit covers the released table and code at the specified commit. It uses reported fold scores, and it leaves independent evaluation of predictive performance and the choice of a sampling design open. OpenAI Codex assisted with the analysis, code and text. This is an independent reproducibility note awaiting external review. [Verification script](check.py)

---

What brought you to this study? Whether you're reading on your own, with AI assistance, or as an AI agent, you're welcome to [leave a short public note](https://github.com/orcarider7/paper-replication-lab/issues/new?template=ai-guestbook.md&title=ESOL%20split%20comparison%20%E2%80%94%20reader%20note).
