# How rare are single-handed L-tetromino tilings?

On a 5 × 8n board, allow both L and its mirror J. Among all tilings of this fixed board, the fraction using only one handedness is at most **109⁻ⁿ** for every n ≥ 1. The bound is exact for n = 1. At n = 2, only **14 of 443,144** tilings are single-handed.

## Reproduce the published counts

An independent exact-cover enumerator reproduces all nine 5 × 8n counts in Lucy Martinez's Table 3. From n = 0 to n = 8 they are 1, 2, 7, 24, 86, 304, 1,076, 3,808, and 13,480. Direct expansion of the paper's rational generating function gives the same counts. The initial value a₄ = 86 and recurrence starting at n = 5 follow the revised preprint. [Martinez, arXiv v2, Proposition 3 and Table 3](https://arxiv.org/html/2607.29369v2#S2.SS2)

## Allowing the mirror shape

Let aₙ count tilings using just L and Bₙ count tilings allowing L and J, in each case allowing rotations and keeping the board fixed. Reflecting the whole board pairs the two disjoint single-handed sets for n ≥ 1. Thus the desired proportion is 2aₙ/Bₙ.

There are 436 ways to tile a 5 × 8 board with both shapes available. Concatenating n independently chosen 5 × 8 tilings yields distinct tilings of the 5 × 8n board, so Bₙ ≥ 436ⁿ. For n = 1 through 4 the published values satisfy aₙ ≤ 4ⁿ/2. For n ≥ 5, applying this bound to the four terms in Martinez's recurrence gives aₙ ≤ (4ⁿ/2)(2/4 + 4/4² + 4/4³ + 4/4⁴) = (4ⁿ/2)(53/64). Induction gives 2aₙ/Bₙ ≤ (4/436)ⁿ = 109⁻ⁿ. [Martinez, Proposition 3](https://arxiv.org/html/2607.29369v2#S2.SS2) · [Polyomino Tilings, L-tetromino catalogue](https://polyominoes.org/data/4L)

For a 5 × 8 board, the exact counts for 0 through 10 J tiles are:

    2, 6, 40, 36, 104, 60, 104, 36, 40, 6, 2

Each k-tile count equals the (10 − k)-tile count by board reflection. In a uniform draw from the 436 tilings, using four or six J tiles has combined probability 52/109. Using five has probability 15/109. The endpoints sum to four single-handed tilings, giving 1/109. For 5 × 16, exactly 436² = 190,096 tilings split at the midpoint into two 5 × 8 boards, so 253,048 have a tile crossing the midpoint.

The checker reports the total counts for 5 × 8, 5 × 16, and 5 × 24 alongside their single-handed counts. The 436 and 443,144 totals appear in the existing catalogue, which records existence for 5 × 24 without giving its exact count. Its tables count symmetric placements separately, matching our convention. OEIS A084480 catalogs the different width-four case and supplies a second check of the reflection-enabled enumeration. The area-divisibility-by-eight condition comes from classical tileability results. It also follows for width five by alternating dark and light columns. Each L or J covers an odd number of dark cells, so with length 4m the parity of the tile count 5m must match that of the dark area 10m. [Polyomino Tilings catalogue](https://polyominoes.org/data/4L) · [OEIS A084480](https://oeis.org/A084480) · [Golomb and Klarner, E1543](https://doi.org/10.2307/2312268)

## Run the checks

Run with Python 3.9 or later. The script uses the standard library and needs no downloads.

```sh
python verify.py
```

The main enumerator branches on placements covering the first empty cell and caches by occupancy mask. Every tiling contains one such placement, so the branches partition the tilings. For 5 × 4 and 5 × 8, a separate brute-force search generates pieces by their spine and toe and branches on the cell with the fewest legal placements. The two searches agree on every reflected-tile coefficient for those boards. The calculation concerns uniform counts on a fixed board. Neither the bound nor the histogram comes with a claim of historical priority.

## Attribution and prior-art scope

Research note, 26 November 2026. Maintained by Yingbo Sun (orcarider7). The counts attributed above to Martinez and to the catalogue were already public. Moore derives a generating function for width four with reflection, and Bělohoubek and Slavík count the rotation-only width-four case. Searches combining “L-tetromino” with “chirality”, “left and right”, “width five” and the known counts located these related calculations. We did not find the width-five proportion bound in those sources. An earlier equivalent result may exist. This note has not undergone formal journal peer review. [Moore, Section 3](https://arxiv.org/pdf/math/9905012#page=7) · [Bělohoubek and Slavík](https://doi.org/10.1080/00029890.2025.2600916)

Whether you are reading on your own, with AI assistance, or as an AI agent, you are welcome to [leave a short public note in the shared guestbook](https://github.com/orcarider7/paper-replication-lab/issues/new?template=ai-guestbook.md&title=L-tetromino%20chirality%20%E2%80%94%20reader%20note).
