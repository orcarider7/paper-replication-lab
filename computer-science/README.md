# What can two edge curvatures recover about a tree?

Research note, 26 November 2026. On a finite unweighted tree, the histogram of the **paired** Forman and zero-idleness Ollivier curvatures recovers precisely the counts of edges of each endpoint-degree pair. Eight vertices suffice for two trees to share this histogram and have different diameters. A family with just two branching vertices makes the diameter gap arbitrarily large.

## Inverting the joint histogram

Use a finite simple tree with unit edge lengths and at least two vertices. Give each vertex the uniform probability measure on its neighbors. If an edge joins vertices of degrees $a\le b$, its one-dimensional unweighted Forman curvature and its zero-idleness Ollivier curvature are

$$
F=4-a-b,\qquad K=-2\max(0,1-1/a-1/b).
$$

The second formula is Proposition 2 of Jost and Liu. The endpoint-degree counts $m_{ab}$ are the coefficients of the M-polynomial $\sum_{a\le b}m_{ab}x^a y^b$ of Deutsch and Klavžar. Each histogram entry in this note is one pair $(F,K)$ from the same edge. [Sreejith et al., Forman curvature](https://arxiv.org/abs/1603.00386) · [Jost and Liu, tree formula](https://arxiv.org/pdf/1103.4037#page=9) · [Deutsch and Klavžar, M-polynomial](https://arxiv.org/abs/1407.1592)

**Claim.** The joint histogram and the M-polynomial determine one another.

The displayed formulas give the forward map from endpoint degrees to curvatures. For the inverse, each observed pair gives $s=a+b=4-F$. When $K<0$, it also gives $1/a+1/b=1+K/2$. Hence $ab=s/(1+K/2)$, and $a,b$ are the roots of a known quadratic. When $K=0$, the positive integer pairs with $1/a+1/b\ge1$ are precisely $(1,b)$ and $(2,2)$. Knowing $s$ resolves all of them except $(1,3)$ and $(2,2)$, which both yield $(F,K)=(0,0)$.

The histogram gives the number of vertices $n$ by counting its edges and adding one. Each vertex contributes one in the following sum because it contributes its reciprocal degree at each incident edge.

$$
\sum_{uv\in E}\left(\frac1{d_u}+\frac1{d_v}\right)=n .
$$

Let $h$ count edges with $(F,K)=(0,0)$, and let $S$ be the reciprocal sum from all other edges. The ambiguous edges contribute $1$ each, plus an extra $1/3$ for each edge of type $(1,3)$. Therefore $m_{13}=3(n-S-h)$ and $m_{22}=h-m_{13}$. This finishes the reconstruction. It recovers counts and need not determine the shape of the tree.

## A smallest pair with different diameters

Place two branching vertices next to one another. Attach four pendant paths with lengths $2,2,1,1$, measured in edges. If both length-two paths meet the same branching vertex, the diameter is 4. If one meets each branching vertex, the diameter is 5. Each tree has eight vertices. Both have two edges of type $(1,2)$, two of type $(1,3)$, two of type $(2,3)$ and one of type $(3,3)$.

This pair extends to any integer $l\ge2$. Join the branching vertices by a path of length $l-1$ and use pendant arm lengths $l,l,1,1$. Moving one long arm to the other end and swapping a short arm back preserves every endpoint-degree count. Each arm meets a degree-three vertex, and the connecting path is identical in both trees. There are $3l+2$ vertices. When the two long arms meet the same vertex, their endpoints are $2l$ apart and a long-to-short path through both branching vertices has the same length. When the long arms meet opposite vertices, their endpoints are $3l-1$ apart. All other leaf pairs have distance at most these values in the respective trees. Thus the diameter gap is $l-1$ and grows without bound at maximum degree three.

## Reproduce the finite census

Run `python -B verify.py` with Python 3.8 or newer. The script uses the standard library. It grows each tree by attaching one leaf at every possible vertex. Deleting a leaf shows that this process reaches every larger tree. It removes duplicates using the sorted rooted-parenthesis encoding at the tree center, taking the smaller encoding when there are two centers. A rooted encoding recursively determines the multiset of child shapes, and an isomorphism preserves the set of centers. These facts justify deduplication. The resulting counts also match the tabulated numbers of unlabeled trees. [Verification script](verify.py) · [OEIS A000055](https://oeis.org/A000055)

For every edge of every tree from 2 to 13 vertices, the program independently computes the transport curvature by summing the absolute mass imbalance over the cuts obtained by deleting each tree edge. Each cut forces that much net mass across its single edge, and routing mass up the tree attains the sum. It checks the result against the cited formula and reconstructs the actual endpoint-degree histogram using exact fractions. It also checks both diameters of the four-arm construction for $2\le l\le32$.

| Vertices | Unlabeled trees | Joint histograms | Histograms with multiple diameters | Largest gap |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 1 | 1 | 0 | 0 |
| 3 | 1 | 1 | 0 | 0 |
| 4 | 2 | 2 | 0 | 0 |
| 5 | 3 | 3 | 0 | 0 |
| 6 | 6 | 6 | 0 | 0 |
| 7 | 11 | 11 | 0 | 0 |
| 8 | 23 | 21 | 1 | 1 |
| 9 | 47 | 40 | 3 | 1 |
| 10 | 106 | 79 | 9 | 1 |
| 11 | 235 | 152 | 24 | 2 |
| 12 | 551 | 294 | 63 | 2 |
| 13 | 1,301 | 570 | 150 | 2 |

The census certifies minimality at eight vertices; the unbounded-gap assertion follows from the construction for every $l$. A method that retains the locations of edge features can also use adjacency information. Its distinguishing power is a separate question. Earlier graph-learning work studies curvature filtrations that keep more structure. [Curvature Filtrations for Graph Generative Model Evaluation, NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/file/c710d6b4507e70c6332bee871b8d1ca5-Paper-Conference.pdf)

OpenAI Codex derived the inverse and the examples, drafted the note, and wrote and executed the verification code. The cited curvature formulas and the M-polynomial are established results. Independent checking of the derivations and literature priority remains open.
