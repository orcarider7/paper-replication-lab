"""Recalculate the two comparisons in a published ESOL cross-validation table."""

import argparse
import csv
from hashlib import sha256
from io import BytesIO, StringIO
from itertools import permutations
from math import hypot, isclose, sqrt
from pathlib import Path
from statistics import mean, stdev
from urllib.request import urlopen
from zipfile import ZipFile


COMMIT = "be0dacb6dc045b452a81f077a93db77108dcf2d0"
URL = f"https://codeload.github.com/a346616355/ESOL/zip/{COMMIT}"
COMMIT_ARCHIVE_SHA = "3581159e4efece0f741cf7e9cab84e8af4e36ed25c6d8ba09259dedf1be80517"
RELEASE_ZIP_SHA = "8b219f43f636c5a35e82bfe1fb27f7f0cc39fafbb9d6c7ce6f5c87a9921707b9"
TABLE_HASHES = {
    "cv_fold_metrics.csv": "4c1d9f3c4fc5d6b7c85064b72aa9f94d026fb727e32d1f90944e31aef51a108f",
    "statistical_tests.csv": "799926ffceb35bd21f89afe10608f79e539c73e261814779bd0a01bde89091c1",
}
FOLDS = range(5)
SPLITS = ("random_cv", "scaffold_cv")
SVR = "SVR_Descriptors"


def load_tables(local_zip):
    if local_zip is None:
        with urlopen(URL, timeout=60) as response:
            data = response.read()
    else:
        data = local_zip.read_bytes()
    if sha256(data).hexdigest() == COMMIT_ARCHIVE_SHA:
        with ZipFile(BytesIO(data)) as outer:
            data = outer.read(f"ESOL-{COMMIT}/ESOL-main.zip")
    if sha256(data).hexdigest() != RELEASE_ZIP_SHA:
        raise ValueError("Unexpected release archive SHA-256")
    tables = {}
    with ZipFile(BytesIO(data)) as archive:
        for name, expected in TABLE_HASHES.items():
            contents = archive.read(f"ESOL-main/results/tables/{name}")
            if sha256(contents).hexdigest() != expected:
                raise ValueError(f"Unexpected SHA-256 for {name}")
            tables[name] = list(csv.DictReader(StringIO(contents.decode("utf-8-sig"))))
    return tables


def paired_test(random, scaffold):
    """Two-sided paired Student t-test for five observations (four df)."""
    differences = [y - x for x, y in zip(random, scaffold)]
    assert len(random) == len(scaffold) == 5
    delta = mean(differences)
    t = abs(delta) * sqrt(5) / stdev(differences)
    x = t / hypot(t, 2)
    return delta, (1 - x) ** 2 * (2 + x) / 2


def audit(tables):
    by_split = {split: {} for split in SPLITS}
    for row in tables["cv_fold_metrics.csv"]:
        model = by_split[row["split"]].setdefault(row["model"], {})
        fold = int(row["fold"])
        assert fold not in model
        model[fold] = float(row["RMSE"])
    fixed, oracle = {}, {}
    for split, models in by_split.items():
        assert len(models) == 5 and all(set(folds) == set(FOLDS) for folds in models.values())
        winner = min(models, key=lambda model: mean(models[model].values()))
        assert winner == SVR
        fixed[split] = [models[winner][i] for i in FOLDS]
        winners = [min(models, key=lambda model: models[model][i]) for i in FOLDS]
        expected = [SVR] * 5
        if split == "scaffold_cv":
            expected[0] = "XGBoost_Descriptors"
        assert winners == expected
        oracle[split] = [models[winners[i]][i] for i in FOLDS]

    published, = tables["statistical_tests.csv"]
    assert published["comparison"] == "best_random_cv_vs_best_scaffold_cv_RMSE"
    fixed_delta, fixed_p = paired_test(fixed["random_cv"], fixed["scaffold_cv"])
    oracle_delta, oracle_p = paired_test(oracle["random_cv"], oracle["scaffold_cv"])
    assert isclose(fixed_delta, float(published["delta_RMSE"]), abs_tol=1e-12)
    assert isclose(oracle_p, float(published["paired_ttest_p"]), abs_tol=1e-12)
    assert isclose(oracle_delta, 0.14547938175, abs_tol=1e-10)
    assert isclose(fixed_p, 0.0152124486, abs_tol=1e-9)
    for name, vectors, delta, p in [
        ("fixed SVR", fixed, fixed_delta, fixed_p),
        ("within-fold minimum", oracle, oracle_delta, oracle_p),
    ]:
        ps = [paired_test(vectors["random_cv"], order)[1]
              for order in permutations(vectors["scaffold_cv"])]
        below = sum(value < 0.05 for value in ps)
        assert below == (120 if name == "fixed SVR" else 89)
        if name == "within-fold minimum":
            assert isclose(min(ps), 0.02573242, abs_tol=1e-8)
            assert isclose(max(ps), 0.06178059, abs_tol=1e-8)
        print(f"{name}: delta={delta:.10f}, original pairing p={p:.10f}")
        print(f"  p range {min(ps):.10f} to {max(ps):.10f}; {below}/120 below .05")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip_file", nargs="?", type=Path,
                        help="optional local snapshot; otherwise download the pinned commit")
    audit(load_tables(parser.parse_args().zip_file))
