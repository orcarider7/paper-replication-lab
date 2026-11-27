"""Reproduce same-nest Adélie body-mass comparisons using Python 3.9+."""

import argparse
import csv
import hashlib
import io
import re
from collections import defaultdict
from pathlib import Path
from statistics import mean, median
from urllib.request import urlopen


SOURCE = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins_raw.csv"
SHA256 = "144f623143c9360fd77322a4f86acb06dc198814dbd2669724c63e6457b907bd"
SPECIES = "Adelie Penguin (Pygoscelis adeliae)"


def analyze(data):
    # The upstream CSV uses LF. A Windows Git checkout can translate it to CRLF.
    data = data.replace(b"\r\n", b"\n")
    if hashlib.sha256(data).hexdigest() != SHA256:
        raise ValueError("The CSV differs from the analyzed release. See the README.")
    nests = defaultdict(dict)
    for row in csv.DictReader(io.StringIO(data.decode("utf-8-sig"))):
        if row["Species"] != SPECIES:
            continue
        match = re.fullmatch(r"(N\d+)A([12])", row["Individual ID"])
        if match is None:
            raise ValueError(f"Unexpected individual ID: {row['Individual ID']}")
        nest_id, adult = match.groups()
        nest = nests[row["studyName"], row["Island"], nest_id]
        if adult in nest:
            raise ValueError("Duplicate adult record within season, island, and nest")
        nest[adult] = row

    strata = defaultdict(list)
    complete_count = 0
    all_diffs = []
    for (season, island, _), adults in sorted(nests.items()):
        assert adults.keys() == {"1", "2"}
        a, b = adults.values()
        assert a["Date Egg"] == b["Date Egg"]
        assert a["Clutch Completion"] == b["Clutch Completion"]
        completed = a["Clutch Completion"] == "Yes"
        complete_count += completed
        if {a["Sex"], b["Sex"]} != {"FEMALE", "MALE"}:
            continue
        if "NA" in (a["Body Mass (g)"], b["Body Mass (g)"]):
            continue
        weights = {r["Sex"]: int(r["Body Mass (g)"]) for r in (a, b)}
        difference = weights["MALE"] - weights["FEMALE"]
        all_diffs.append(difference)
        if completed:
            strata[season, island].append(difference)

    primary = [d for stratum in strata.values() for d in stratum]
    assert (len(nests), complete_count, len(primary), len(all_diffs)) == (76, 69, 65, 72)
    print(f"{len(nests)} nest-seasons; {complete_count} recorded completed clutches")
    for label, ds in [("Completed clutches", primary), ("All eligible pairs", all_diffs)]:
        print(f"{label}: n={len(ds)}, heavier={sum(d > 0 for d in ds)},"
              f" tied={ds.count(0)}, lighter={sum(d < 0 for d in ds)},"
              f" mean={mean(ds):.3f} g, median={median(ds):.1f} g")
    print(f"Completed-clutch pairs with recorded difference > 100 g: "
          f"{sum(d > 100 for d in primary)}")
    print("Season Island     Pairs Mean difference (g)")
    for (season, island), ds in sorted(strata.items()):
        print(f"{season} {island:<10} {len(ds):>3} {mean(ds):>9.3f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="?", type=Path, help="local copy of penguins_raw.csv")
    args = parser.parse_args()
    if args.csv:
        raw = args.csv.read_bytes()
    else:
        with urlopen(SOURCE, timeout=30) as response:
            raw = response.read()
    analyze(raw)
