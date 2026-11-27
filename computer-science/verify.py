"""Exact census of curvature profiles of unlabeled trees, using the standard library."""

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from math import isqrt


def edges(tree):
    return [(u, v) for u, neighbors in enumerate(tree) for v in neighbors if u < v]


def rooted_code(tree, u, parent):
    children = sorted(rooted_code(tree, v, u) for v in tree[u] if v != parent)
    return "(" + "".join(children) + ")"


def canonical_code(tree):
    degree = [len(adj) for adj in tree]
    layer = [v for v, d in enumerate(degree) if d <= 1]
    remaining = len(tree)
    while remaining > 2:
        remaining -= len(layer)
        following = []
        for u in layer:
            for v in tree[u]:
                degree[v] -= 1
                if degree[v] == 1:
                    following.append(v)
        layer = following
    return min(rooted_code(tree, u, -1) for u in layer)


def next_size(trees):
    shapes = {}
    for tree in trees:
        n = len(tree)
        for root in range(n):
            larger = tree[:root] + (tree[root] + (n,),) + tree[root + 1:] + ((root,),)
            shapes.setdefault(canonical_code(larger), larger)
    return list(shapes.values())


def parent_order(tree, root):
    parent = {root: -1}
    order = [root]
    for u in order:
        for v in tree[u]:
            if v != parent[u]:
                parent[v] = u
                order.append(v)
    return parent, order


def diameter(tree):
    def farthest(root):
        parent, order = parent_order(tree, root)
        distance = {root: 0}
        for node in order[1:]:
            distance[node] = distance[parent[node]] + 1
        return order[-1], distance[order[-1]]
    end, _ = farthest(0)
    return farthest(end)[1]


def endpoint_profile(tree):
    return Counter(tuple(sorted((len(tree[u]), len(tree[v])))) for u, v in edges(tree))


def four_arm_tree(length, separate):
    """Two branching vertices joined by length - 1 edges, with two long arms."""
    graph = [[] for _ in range(length)]
    for i in range(1, length):
        graph[i - 1].append(i)
        graph[i].append(i - 1)
    arms = ((length, 1), (length, 1)) if separate else ((length, length), (1, 1))
    for center, lengths in zip((0, length - 1), arms):
        for arm_length in lengths:
            end = center
            for _ in range(arm_length):
                new = len(graph)
                graph.append([end])
                graph[end].append(new)
                end = new
    return tuple(tuple(neighbors) for neighbors in graph)


@lru_cache(maxsize=None)
def edge_curvature(a, b):
    return 4 - a - b, -2 * max(0, 1 - Fraction(1, a) - Fraction(1, b))


def transport_curvature(tree, u, v):
    """Exact unit-cost W1 on a tree from subtree mass imbalances."""
    a, b = len(tree[u]), len(tree[v])
    mass = [0] * len(tree)
    for i in tree[u]:
        mass[i] += b
    for i in tree[v]:
        mass[i] -= a
    parent, order = parent_order(tree, u)
    cost = 0
    for w in reversed(order[1:]):
        cost += abs(mass[w])
        mass[parent[w]] += mass[w]
    assert mass[u] == 0
    return 1 - Fraction(cost, a * b)


def decode(profile):
    """Reconstruct endpoint pairs using only the joint histogram."""
    n = 1 + sum(profile.values())
    known = Counter()
    ambiguous = profile.get((0, 0), 0)
    reciprocal_total = Fraction(0)
    for (forman, ollivier), count in profile.items():
        if (forman, ollivier) == (0, 0):
            continue
        degree_sum = 4 - forman
        if ollivier < 0:
            product = Fraction(degree_sum) / (1 + ollivier / 2)
            assert product.denominator == 1
            square = degree_sum**2 - 4 * int(product)
            root = isqrt(square)
            assert root**2 == square
            a, b = (degree_sum - root) // 2, (degree_sum + root) // 2
        else:
            a, b = 1, degree_sum - 1
        known[a, b] += count
        reciprocal_total += count * (Fraction(1, a) + Fraction(1, b))
    leaves_at_three = 3 * (n - reciprocal_total - ambiguous)
    assert leaves_at_three.denominator == 1 and 0 <= leaves_at_three <= ambiguous
    known[1, 3] += int(leaves_at_three)
    known[2, 2] += ambiguous - int(leaves_at_three)
    return +known


def main():
    # Unrooted tree counts, also tabulated in OEIS A000055.
    counts = (1, 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, 551, 1301)
    trees = [((),)]
    first = None
    print("n  trees  profiles  profiles_with_multiple_diameters  largest_diameter_gap")
    for n in range(2, len(counts) + 1):
        trees = next_size(trees)
        assert len(trees) == counts[n - 1]
        groups = defaultdict(dict)
        for tree in trees:
            raw = endpoint_profile(tree)
            curvature = Counter()
            for u, v in edges(tree):
                f, k = edge_curvature(len(tree[u]), len(tree[v]))
                assert transport_curvature(tree, u, v) == k
                curvature[f, k] += 1
            assert decode(curvature) == raw
            groups[tuple(sorted(raw.items()))].setdefault(diameter(tree), tree)
        mixed = [d for d in groups.values() if len(d) > 1]
        largest_gap = max(max(d) - min(d) for d in groups.values())
        print(n, len(trees), len(groups), len(mixed), largest_gap)
        if mixed and first is None:
            first = (n, mixed[0])
    n, pair = first
    print("First different diameters in a common profile, n =", n)
    for d in sorted(pair):
        print("diameter", d, "edges", edges(pair[d]))
    print("Common edge-degree histogram", sorted(endpoint_profile(next(iter(pair.values()))).items()))
    assert n == 8 and sorted(pair) == [4, 5]
    for length in range(2, 33):
        adjacent_arms = four_arm_tree(length, separate=False)
        split_arms = four_arm_tree(length, separate=True)
        assert len(adjacent_arms) == len(split_arms) == 3 * length + 2
        assert endpoint_profile(adjacent_arms) == endpoint_profile(split_arms)
        assert diameter(adjacent_arms) == 2 * length
        assert diameter(split_arms) == 3 * length - 1
    print("Four-arm construction checked for lengths 2 through 32.")


if __name__ == "__main__":
    main()
