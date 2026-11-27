"""Finite conservative sandpiles on a cycle with parallel edges, Python 3."""

from collections import defaultdict
from fractions import Fraction
from math import comb, factorial, prod


def invariant_stable(heights, multiplicity):
    n = len(heights)
    pairs = [height // multiplicity for height in heights]
    total = sum(pairs)
    if total != n:
        return total < n
    moment = sum(i * count for i, count in enumerate(pairs))
    return (moment - n * (n - 1) // 2) % n == 0


def stabilizes_by_firing(heights, multiplicity):
    """Fire each eligible site once per round and detect repeated configurations."""
    state = tuple(heights)
    n = len(state)
    seen = set()
    while state not in seen:
        firing = [height >= 2 * multiplicity for height in state]
        if not any(firing):
            return True
        seen.add(state)
        state = tuple(
            state[i] + multiplicity * (
                firing[(i - 1) % n] + firing[(i + 1) % n] - 2 * firing[i]
            )
            for i in range(n)
        )
    return False


def occupancies(total, sites):
    if sites == 1:
        yield (total,)
        return
    for height in range(total + 1):
        for suffix in occupancies(total - height, sites - 1):
            yield (height,) + suffix


def check_directly(n, multiplicity, grains):
    stable = boundary = stable_at_boundary = sequences = 0
    factorials = [factorial(j) for j in range(grains + 1)]
    for heights in occupancies(grains, n):
        by_firing = stabilizes_by_firing(heights, multiplicity)
        assert by_firing == invariant_stable(heights, multiplicity), heights
        weight = factorials[grains] // prod(factorials[h] for h in heights)
        sequences += weight
        if by_firing:
            stable += weight
        if sum(h // multiplicity for h in heights) == n:
            boundary += weight
            if by_firing:
                stable_at_boundary += weight
    assert sequences == n**grains
    return stable, stable_at_boundary, boundary


def survival_curve(n, multiplicity):
    """Count uniform labelled placements by total grains, mobile blocks and moment."""
    largest_stable = n * (2 * multiplicity - 1)
    counts = {(0, 0, 0): 1}
    for vertex in range(n):
        updated = defaultdict(int)
        for (placed, blocks, moment), ways in counts.items():
            for h in range(largest_stable - placed + 1):
                add = h // multiplicity
                # K > n can never return to a stable class on adding more sites.
                if blocks + add > n:
                    break
                key = (placed + h, blocks + add, (moment + vertex * add) % n)
                updated[key] += comb(placed + h, h) * ways
        counts = updated
    target = n * (n - 1) // 2 % n
    successful = [0] * (largest_stable + 1)
    for (placed, blocks, moment), ways in counts.items():
        if blocks < n or moment == target:
            successful[placed] += ways
    return [Fraction(ways, n**t) for t, ways in enumerate(successful)]


def main():
    expected = {3: Fraction(71, 81), 4: Fraction(1879, 2048),
                5: Fraction(371773, 390625)}
    for n, probability in expected.items():
        b = 2
        curve = survival_curve(n, b)
        # The dynamics check uses every occupancy, even those pruned by the DP.
        for t in range(len(curve)):
            stable, on_boundary, boundary = check_directly(n, b, t)
            assert curve[t] == Fraction(stable, n**t)
            if t == 2 * n:
                assert curve[t] == probability
                print(f"n={n}, grains={t}: {stable}/{n**t} = {probability}; "
                      f"conditional on K=n: {Fraction(on_boundary, boundary)}")
        assert all(a >= bval for a, bval in zip(curve, curve[1:]))
        first_failure = sum(curve)
        print(f"  Expected grains at first failure: {first_failure}. "
              f"Expected last-stable density: {float((first_failure - 1) / n):.8f}")
    for b in (1, 3):
        n = 3
        curve = survival_curve(n, b)
        for t in range(len(curve)):
            count, _, _ = check_directly(n, b, t)
            assert curve[t] == Fraction(count, n**t)
    assert not stabilizes_by_firing((8, 0, 0, 0), 2)
    assert stabilizes_by_firing((6, 0, 2, 0), 2)


if __name__ == "__main__":
    main()
