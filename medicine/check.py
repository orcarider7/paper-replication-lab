"""Recompute model rankings from the authors' published MedHELM score table."""

import argparse
import csv
import hashlib
import io
from collections import Counter
from decimal import Decimal
from pathlib import Path
from urllib.request import urlopen


SOURCE = "https://raw.githubusercontent.com/som-shahlab/medhelm/main/data/leaderboard.csv"
DIGEST = "75d510d317df8a79e5694c6278331dcf4156cac453738847d41c625791fcd7c0"
PAIR = ("DeepSeek R1", "o3-mini (2025-01-31)")


def rank_points(scores, columns, tie_points):
    """Two points per opponent beaten; integer tie_points specifies the convention."""
    points = {}
    for name, row in scores.items():
        points[name] = {
            col: sum(2 * (row[col] > other[col]) + tie_points * (row[col] == other[col])
                     for opponent, other in scores.items() if opponent != name)
            for col in columns
        }
    return points


def analyze(data):
    if hashlib.sha256(data).hexdigest() != DIGEST:
        raise ValueError("The CSV differs from the publication snapshot used in this note.")
    reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig")))
    records = list(reader)
    columns = [c for c in reader.fieldnames if c not in {"Model", "Mean win rate"}]
    scores = {r["Model"]: {c: Decimal(r[c]) for c in columns} for r in records}
    assert len(records) == len(scores) == 9 and len(columns) == 37
    left, right = PAIR
    groups = {
        "All": columns,
        "Jury Score": [c for c in columns if c.endswith(" - Jury Score")],
        "Other metrics": [c for c in columns if not c.endswith(" - Jury Score")],
    }
    for group, cols in groups.items():
        differences = [scores[left][c] - scores[right][c] for c in cols]
        counts = (sum(d > 0 for d in differences), differences.count(0),
                  sum(d < 0 for d in differences))
        print(f"{group}: {left} wins/ties/losses against {right} = {counts}")

    for tie_points in (0, 1, 2):
        points = rank_points(scores, columns, tie_points)
        totals = {name: sum(p.values()) for name, p in points.items()}
        leaders = Counter()
        for omitted in columns:
            reduced = {name: totals[name] - p[omitted] for name, p in points.items()}
            leaders[tuple(sorted(m for m, v in reduced.items() if v == max(reduced.values())))] += 1
        print(f"Win credit for ties = {tie_points}/2; leave-one-out leaders:")
        for names, times in sorted(leaders.items()):
            print(f"  {times:2}   {' and '.join(names)}")
        if tie_points == 1:
            denominator = 2 * (len(scores) - 1) * len(columns)
            for name in PAIR:
                print(f"  full table: {name}: {totals[name]}/{denominator}")
            assert (totals[left], totals[right]) == (392, 391)
            assert leaders == Counter({(left,): 17, (right,): 20})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="?", type=Path, help="local copy of leaderboard.csv")
    args = parser.parse_args()
    if args.csv:
        raw = args.csv.read_bytes()
    else:
        with urlopen(SOURCE, timeout=30) as response:
            raw = response.read()
    analyze(raw)
