# A direct tiling proof for Open Problem 3 on restricted Arndt compositions

Nadji, Ahmia, Checa and Ramírez ask for a combinatorial proof of a binomial sum on page 6 of their 2025 *Journal of Integer Sequences* paper. They give the formula and the recursive map in Theorem 2. We exhibit that map as a direct tile encoding, count the required summands, and identify an omitted row in their worked example. [Original question and table](https://cs.uwaterloo.ca/journals/JIS/VOL28/Ramirez/ramirez19.pdf#page=6) · [Journal's LaTeX source](https://cs.uwaterloo.ca/journals/JIS/VOL28/Ramirez/ramirez19.tex)

## The correspondence

Let $A(n)$ be the set of ordered compositions of $n$ with parts in $\{1,2,3\}$ in which each odd-indexed part exceeds its successor, if present. Include the empty composition at $n=0$. Every composition splits uniquely into descending pairs and one optional final part. Encode the pairs in order. Then append exactly one ending according to the table. Digits in the output stand for individual tiles of length 2 or 3.

| Pair | Tiles | Final part | Ending tiles |
| --- | --- | --- | --- |
| $(2,1)$ | 3 | absent | 2 |
| $(3,1)$ | 22 | 1 | 3 |
| $(3,2)$ | 23 | 2 | 22 |
| | | 3 | 23 |

Each pair keeps its total weight. The ending adds two units to the weight of the optional part, so the tiles cover a strip of length $n+2$. For example, $(3,1,2,1,3)$ maps to $22\mid3\mid23$, a tiling of length 12. The empty composition maps to the one-tile word 2.

**Inverse.** Read the tiling from the left. A 3 completes a block immediately. A 2 consumes the next tile, if present, completing a block 22 or 23. If a single 2 remains at the very end, discard it and decode every complete block as a pair. Otherwise reserve the final complete block as the ending for part 1, 2 or 3 and decode all preceding blocks as pairs. Every tiling of length at least two has either that single residual tile or a final complete block. The three pair codes are prefix-free. The end rule therefore recovers exactly the original pairs and optional part, including all one-block cases.

A tiling with $k$ tiles must contain $n+2-2k$ threes. Choosing their positions proves the formula in Open Problem 3 for every $n\geq0$:

$$
|A(n)|=\sum_{k=0}^{\lfloor(n+2)/2\rfloor}\binom{k}{n+2-2k}.
$$

A binomial coefficient is zero when its lower index lies outside $[0,k]$. The map also identifies the summands with disjoint classes of compositions according to their encoded tile count.

## One omitted row in Table 1

The first column of Table 1 contains 11 distinct compositions of 10. Direct enumeration gives 12, in agreement with the paper's Table 3. The missing member of $A(8)$ is $(2,1,2,1,2)$. In the weight-increase-by-two branch of the authors' Theorem 2, its final 2 becomes the pair $(3,1)$, giving the missing member $(2,1,2,1,3,1)$ of $A(10)$. The five entries in the $A(7)$ column are complete. Inserting this row reconciles the example with the theorem.

## Relation to the authors' map

Let $W$ be the tile word of a composition. In the order of final parts absent, 1, 2, 3, the four possible endings are 2, 3, 22, 23. Under the paper's weight-increase-by-two rule these endings become 22, 32, 222, 232. Under the weight-increase-by-three rule they become 23, 33, 223, 233. Earlier pair blocks stay fixed. Thus the two operations in Theorem 2 act exactly as appending a single tile 2 or 3 to $W$. The one-tile words correspond to the empty composition and the singleton (1). This proves that iterating the published recurrence gives this very same bijection. The direct code spells out the binomial refinement that the authors requested. The paper has priority for the recursive construction.

## Reproduction and priority

Run `python arndt-padovan/verify.py` from the repository root. The program generates the two sets independently, checks both directions and the binomial counts through $n=25$, and reproduces the 12 objects of weight 10. To check the actual printed columns against the originals, download the journal's linked LaTeX file and pass its path as the sole argument, or use `--fetch-table`. The source check verifies the SHA-256 digest before extracting the three columns.

The counting identity and the recurrence belong to the cited paper. An earlier proof for unrestricted Arndt compositions also uses tilings. Public searches on the paper title, “Open Problem 3”, “Arndt compositions”, “Padovan”, “tilings” and “binomial” established neither priority for writing out this direct encoding nor priority for noticing the Table 1 omission. The 2025 journal quartile was Q3 in Discrete Mathematics and Combinatorics. [Hopkins and Tangboonduangjit (2022)](https://www.fq.math.ca/Papers1/60-5/hopkins.pdf) · [Nadji et al. (2025)](https://cs.uwaterloo.ca/journals/JIS/VOL28/Ramirez/ramirez19.html) · [Related 2026 work](https://doi.org/10.1016/j.tcs.2026.116156) · [SCImago journal record](https://www.scimagojr.com/journalsearch.php?q=23914&tip=sid)

Maintained by Yingbo Sun (orcarider7). OpenAI Codex devised and drafted the block code, source audit and verification program. This is a public research note awaiting independent human review.

---

What brought you to this study? Whether you're reading on your own, with AI assistance, or as an AI agent, you're welcome to [leave a short public note](https://github.com/orcarider7/paper-replication-lab/issues/new?template=ai-guestbook.md&title=Restricted%20Arndt%20compositions%20%E2%80%94%20reader%20note).
