"""Reproduce Martinez's 5 x 8n counts and audit reflected-tile frequencies."""

from collections import Counter
from fractions import Fraction
from functools import cache


# Martinez v2, section 2.2 and Table 3.
BASE = ((0, 0), (0, 1), (0, 2), (1, 0))
TABLE_3 = (1, 2, 7, 24, 86, 304, 1076, 3808, 13480)


def orientations(shape):
    """Rotate a shape and normalize each rotation to its bounding box."""
    result = set()
    for _ in range(4):
        left = min(x for x, _ in shape)
        top = min(y for _, y in shape)
        result.add(tuple(sorted((x - left, y - top) for x, y in shape)))
        shape = tuple((-y, x) for x, y in shape)
    return result


def tilings_by_mirrors(width, length, allow_mirrors=False):
    """Count fixed-board tilings by the number of reflected tiles."""
    original = orientations(BASE)
    mirrored = orientations(tuple((-x, y) for x, y in BASE))
    assert len(original) == len(mirrored) == 4
    assert not original & mirrored
    shapes = [(shape, 0) for shape in sorted(original)]
    if allow_mirrors:
        shapes.extend((shape, 1) for shape in sorted(mirrored))

    # Group candidate placements by their first cell in column-major order.
    placements = [[] for _ in range(width * length)]
    for shape, mirror_count in shapes:
        max_x = max(x for x, _ in shape)
        max_y = max(y for _, y in shape)
        for left in range(length - max_x):
            for top in range(width - max_y):
                cells = tuple((left + x) * width + top + y for x, y in shape)
                mask = sum(1 << cell for cell in cells)
                placements[min(cells)].append((mask, mirror_count))

    full = (1 << (width * length)) - 1

    @cache
    def count(filled):
        if filled == full:
            return {0: 1}
        empty = full ^ filled
        anchor = (empty & -empty).bit_length() - 1
        counts = Counter()
        for mask, mirror_count in placements[anchor]:
            if mask & filled == 0:
                for remaining_mirrors, ways in count(filled | mask).items():
                    counts[remaining_mirrors + mirror_count] += ways
        return counts

    result = count(0)
    count.cache_clear()
    return result


def brute_force_histogram(width, length):
    """Cross-check using geometric placements and a least-options cell search."""
    board = {(x, y) for x in range(length) for y in range(width)}
    covering = {cell: [] for cell in board}
    for x, y in board:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            for flipped in (0, 1):
                sign = 1 - 2 * flipped
                # The base tile's spine goes down and its toe goes right.
                piece = {
                    (x, y),
                    (x + dx, y + dy),
                    (x + 2 * dx, y + 2 * dy),
                    (x + sign * dy, y - sign * dx),
                }
                if piece <= board:
                    for cell in piece:
                        covering[cell].append((piece, flipped))

    result = Counter()

    def visit(remaining, mirrors):
        if not remaining:
            result[mirrors] += 1
            return
        best = None
        for cell in sorted(remaining):
            options = [(piece, flipped) for piece, flipped in covering[cell]
                       if piece <= remaining]
            if not options:
                return
            if best is None or len(options) < len(best):
                best = options
        for piece, flipped in best:
            visit(remaining - piece, mirrors + flipped)

    visit(board, 0)
    return result


def published_series(number_of_terms):
    """Extract coefficients of Proposition 3's rational generating function."""
    numerator = (1, 0, -1, -2, -2)
    result = []
    for n in range(number_of_terms):
        coefficient = numerator[n] if n < len(numerator) else 0
        coefficient += sum(
            multiplier * result[n - lag]
            for lag, multiplier in enumerate((2, 4, 4, 4), start=1)
            if n >= lag
        )
        result.append(coefficient)
    return tuple(result)


def main():
    assert published_series(len(TABLE_3)) == TABLE_3
    for n, expected in enumerate(TABLE_3):
        actual = tilings_by_mirrors(5, 8 * n).get(0, 0)
        assert actual == expected, (n, expected, actual)

    # Independent published benchmarks for rotations plus reflections.
    for n, expected in enumerate((1, 2, 10, 42, 182)):  # OEIS A084480
        actual = sum(tilings_by_mirrors(4, 2 * n, allow_mirrors=True).values())
        assert actual == expected, (n, expected, actual)

    print(f"Martinez v2, Table 3, n=0..8: {TABLE_3}")
    print("Length    Fixed L    L or mirror    Exactly 1 mirror    Exactly 2 mirrors")
    histograms = {}
    for length in (4, 8, 12, 16, 20, 24):
        restricted = tilings_by_mirrors(5, length).get(0, 0)
        histogram = tilings_by_mirrors(5, length, allow_mirrors=True)
        histograms[length] = histogram
        tiles = 5 * length // 4
        assert histogram.get(0, 0) == restricted
        assert all(histogram.get(tiles - k, 0) == count
                   for k, count in histogram.items())
        print(f"{length:6} {restricted:10,} {sum(histogram.values()):14,} "
              f"{histogram.get(1, 0):19,} {histogram.get(2, 0):20,}")

    # Polyomino Tilings catalogue, data/4L, width-five entries.
    assert tuple(sum(histograms[length].values()) for length in (8, 16)) == (436, 443144)
    histogram = histograms[8]
    assert histogram == brute_force_histogram(5, 8)
    assert histograms[4] == brute_force_histogram(5, 4)
    total = sum(histogram.values())
    print("5 x 8 mirror-count distribution:", [histogram.get(k, 0) for k in range(11)])
    print("Uniform 5 x 8, exactly five mirrors:", Fraction(histogram[5], total))
    print("Uniform 5 x 8, four or six mirrors:", Fraction(histogram[4] + histogram[6], total))

    # The first four positive-index terms seed the induction in the README.
    assert all(2 * TABLE_3[n] <= 4 ** n for n in range(1, 5))
    assert sum(Fraction(weight, 4 ** lag)
               for lag, weight in enumerate((2, 4, 4, 4), start=1)) == Fraction(53, 64)
    assert total == 4 * 109
    for n in (1, 2, 3):
        unrestricted = sum(histograms[8 * n].values())
        assert unrestricted >= total ** n
        pure_share = Fraction(2 * TABLE_3[n], unrestricted)
        assert pure_share <= Fraction(1, 109 ** n)
        print(f"5 x {8*n}, uniform single-handed share: {pure_share} "
              f"(bound 1/{109 ** n})")

    midpoint_free = sum(histograms[16].values()) - total ** 2
    print("5 x 16 tilings crossing the midpoint:", midpoint_free)


if __name__ == "__main__":
    main()
