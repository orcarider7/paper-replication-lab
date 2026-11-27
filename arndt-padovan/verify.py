"""Check the bijection and optionally read Table 1 from the journal's TeX."""

import argparse
from collections import Counter
from hashlib import sha256
from math import comb
from pathlib import Path
import re
from urllib.request import urlopen


SOURCE = "https://cs.uwaterloo.ca/journals/JIS/VOL28/Ramirez/ramirez19.tex"
SOURCE_HASH = "6d832694810b80b5181b794d1485f87390202906fdec3f9b05c0e79807505805"
PAIRS = {(2, 1): (3,), (3, 1): (2, 2), (3, 2): (2, 3)}
TAILS = {(): (2,), (1,): (3,), (2,): (2, 2), (3,): (2, 3)}
PAIR_FROM = {value: key for key, value in PAIRS.items()}
TAIL_FROM = {value: key for key, value in TAILS.items()}


def compositions(weight, prefix=()):
    if weight == 0:
        yield prefix
        return
    for part in (1, 2, 3):
        if part <= weight and (len(prefix) % 2 == 0 or prefix[-1] > part):
            yield from compositions(weight - part, prefix + (part,))


def tilings(length, prefix=()):
    if length == 0:
        yield prefix
        return
    for tile in (2, 3):
        if tile <= length:
            yield from tilings(length - tile, prefix + (tile,))


def encode(parts):
    paired_length = len(parts) - len(parts) % 2
    tiles = []
    for pos in range(0, paired_length, 2):
        tiles.extend(PAIRS[parts[pos:pos + 2]])
    tiles.extend(TAILS[parts[paired_length:]])
    return tuple(tiles)


def decode(tiles):
    if not tiles or any(tile not in (2, 3) for tile in tiles):
        raise ValueError("Expected a nonempty tiling with 2s and 3s")
    pos = 0
    blocks = []
    while pos < len(tiles):
        width = 1 if tiles[pos] == 3 else 2
        blocks.append(tiles[pos:pos + width])
        pos += width
    ending = blocks.pop()
    parts = [part for block in blocks for part in PAIR_FROM[block]]
    return tuple(parts) + TAIL_FROM[ending]


def theorem_two_extensions(parts):
    """The two forward rules in the proof of Theorem 2, in weight order."""
    if len(parts) % 2 == 0:
        return parts + (2,), parts + (3,)
    if parts[-1] == 3:
        return parts + (2,), parts + (2, 1)
    prefix = parts[:-1] + (parts[-1] + 1, 1)
    return prefix, prefix + (1,)


def check_bijection():
    cases = 0
    for n in range(26):
        inputs = set(compositions(n))
        outputs = set(tilings(n + 2))
        images = [encode(parts) for parts in inputs]
        assert len(set(images)) == len(inputs)
        assert set(images) == outputs
        assert all(decode(encode(parts)) == parts for parts in inputs)
        assert all(encode(decode(tiles)) == tiles for tiles in outputs)
        for parts in inputs:
            by_two, by_three = theorem_two_extensions(parts)
            word = encode(parts)
            assert encode(by_two) == word + (2,)
            assert encode(by_three) == word + (3,)
        sizes = Counter(map(len, images))
        for k in range((n + 2) // 2 + 1):
            threes = n + 2 - 2 * k
            expected = comb(k, threes) if 0 <= threes <= k else 0
            assert sizes[k] == expected
        cases += len(inputs)
    print(f"n = 0..25: {cases} compositions, both inverses, each binomial summand and both Theorem 2 rules verified.")
    print(f"n = 10: {len(set(compositions(10)))} compositions.")


def check_printed_table(data):
    if sha256(data).hexdigest() != SOURCE_HASH:
        raise ValueError("The journal TeX has changed. Inspect this version before comparing.")
    tex = data.decode("utf-8")
    end = tex.index(r"\label{tab1Pad}")
    table = tex[tex.rindex(r"\begin{tabular}", 0, end):end]
    columns = [[], [], []]
    for line in table.splitlines():
        if not line.lstrip().startswith(r"$(\tx{"):
            continue
        cells = line.split("&")
        assert len(cells) == 3
        for column, cell in zip(columns, cells):
            digits = re.findall(r"\\tx\{([123])\}", cell)
            if digits:
                column.append(tuple(map(int, digits)))
    missing = []
    for n, entries in zip((10, 8, 7), columns):
        printed = set(entries)
        complete = set(compositions(n))
        assert len(printed) == len(entries) and printed <= complete
        missing.append(complete - printed)
        print(f"Table 1, n={n}: {len(printed)}/{len(complete)} listed. Missing: {sorted(complete-printed)}")
    assert missing == [{(2, 1, 2, 1, 3, 1)}, {(2, 1, 2, 1, 2)}, set()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex_file", nargs="?", type=Path, help="original journal TeX")
    parser.add_argument("--fetch-table", action="store_true", help="download the original TeX")
    args = parser.parse_args()
    if args.tex_file and args.fetch_table:
        parser.error("Choose one source for the TeX file")
    check_bijection()
    if args.tex_file:
        check_printed_table(args.tex_file.read_bytes())
    elif args.fetch_table:
        with urlopen(SOURCE, timeout=30) as response:
            check_printed_table(response.read())
