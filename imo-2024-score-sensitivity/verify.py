"""Reconstruct the 2024 IMO score comparison from the official results table."""

import argparse
import hashlib
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen


SOURCE = "https://www.imo-official.org/results/individual/year/2024/"
SCORE_SHA256 = "260ae36b5b53cd3db57669f8230a0f718e3954dd4d3f2f6d4f5b41d64e3cf151"
SYSTEM = (7, 7, 0, 7, 0, 7)
PROBLEMS = tuple(f"p{i}" for i in range(1, 7))
NUMERIC = {"rank", "total", *PROBLEMS}


class ResultsTable(HTMLParser):
    """Keep only the public numeric columns of the individual results table."""

    def __init__(self):
        super().__init__()
        self.columns = []
        self.score_rows = []
        self.row = {}
        self.column = None
        self.index = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.columns = []
        elif tag == "tr":
            self.index = 0
            self.row = {}
        elif tag == "th":
            self.columns.append(dict(attrs).get("data-sort"))
        elif tag == "td" and self.index < len(self.columns):
            self.column = self.columns[self.index]
            self.index += 1
            self.parts = []

    def handle_data(self, data):
        if self.column in NUMERIC:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == "td":
            if self.column in NUMERIC:
                self.row[self.column] = int("".join(self.parts).strip())
            self.column = None
        elif tag == "tr" and self.row:
            if self.row.keys() != NUMERIC:
                raise ValueError("Incomplete score row")
            scores = tuple(self.row[p] for p in PROBLEMS)
            if not all(0 <= value <= 7 for value in scores):
                raise ValueError("Problem score outside 0–7")
            if sum(scores) != self.row["total"]:
                raise ValueError("Published total differs from the six scores")
            self.score_rows.append((scores, self.row["rank"]))


def counts(rows, omitted=None):
    keep = [i for i in range(6) if i != omitted]
    system = sum(SYSTEM[i] for i in keep)
    totals = [sum(scores[i] for i in keep) for scores in rows]
    above = sum(total > system for total in totals)
    tied = totals.count(system)
    return system, above, tied, len(totals) - above - tied


def main():
    arguments = argparse.ArgumentParser(description=__doc__)
    arguments.add_argument("html", type=Path, nargs="?", help="saved official results HTML")
    options = arguments.parse_args()
    if options.html:
        html = options.html.read_bytes()
    else:
        request = Request(SOURCE, headers={"User-Agent": "IMO-score-replication/1.0"})
        with urlopen(request, timeout=30) as response:
            html = response.read()

    table = ResultsTable()
    table.feed(html.decode("utf-8-sig"))
    table.close()
    rows = [scores for scores, _ in table.score_rows]
    if len(rows) != 609:
        raise ValueError(f"Expected 609 contestants, found {len(rows)}")
    totals = Counter(sum(scores) for scores in rows)
    for scores, rank in table.score_rows:
        if rank != 1 + sum(n for total, n in totals.items() if total > sum(scores)):
            raise ValueError("Reconstructed competition rank differs from the official rank")
    canonical = "".join(",".join(map(str, row)) + "\n" for row in sorted(rows))
    digest = hashlib.sha256(canonical.encode("ascii")).hexdigest()
    if digest != SCORE_SHA256:
        raise ValueError(f"Official score matrix differs from the 2024 snapshot: {digest}")
    print("SHA-256 of canonical anonymous score matrix:", digest)
    print("Gold (29+) and silver (22-28) counts:",
          sum(n for score, n in totals.items() if score >= 29),
          sum(n for score, n in totals.items() if 22 <= score <= 28))
    print("Omitted  System  Humans-above  Humans-tied  Humans-below")
    for omitted in (None, *range(6)):
        label = "None" if omitted is None else f"P{omitted + 1}"
        print(label, *counts(rows, omitted))


if __name__ == "__main__":
    main()
