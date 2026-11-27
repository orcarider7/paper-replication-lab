# Exact stabilization probabilities on finite bracelet sandpiles

Fey, Levine and Wilson studied a cycle with each edge doubled, which they called the *bracelet*. Their bracelet calculation gives the infinite-bracelet threshold density (about 2.496608) and stationary density (2.5). Their proof groups grains into mobile pairs and a fixed remainder at each vertex. Here we use that reduction to answer a finite-size question. If exactly eight grains are independently dropped at uniformly chosen vertices of a four-site bracelet with no sink, what is the probability of stabilization? The exact answer is **1879/2048**. [Original paper, Section III](https://doi.org/10.1103/PhysRevE.82.031121) · [Author's open manuscript](https://arxiv.org/abs/1001.3401)

## Finite experiment

Start from an empty cycle of $n\ge3$ vertices numbered $0,\ldots,n-1$. With $b$ parallel edges between each neighboring pair, a vertex with at least $2b$ grains can send $b$ to each neighbor. All grains stay on the cycle. Every one of the $n^t$ sequences of $t$ deposited grains has equal probability. This is also independent, identically distributed Poisson initial occupancy conditioned on its total $t$. The bracelet in the paper has $b=2$.

| Vertices | Grains | Stabilizing deposit sequences | Probability of stabilization | Probability given exactly $n$ mobile pairs |
| ---: | ---: | ---: | ---: | ---: |
| 3 | 6 | 639 of 729 | 71/81 | 31/61 |
| 4 | 8 | 60,128 of 65,536 | 1879/2048 | 7/20 |
| 5 | 10 | 9,294,325 of 9,765,625 | 371773/390625 | 31501/125761 |

Eight grains distributed as $(6,0,2,0)$ stabilize, whereas $(8,0,0,0)$ repeats a configuration. In both cases there are four mobile pairs. Their locations decide whether the pairs can reach one per vertex. At this critical pair count, treating the four residue classes as equally likely would predict a conditional success probability of $1/4$. The exact conditional probability under independent grain placement is $7/20$.

## A finite criterion for any edge multiplicity

For initial heights $h_i$, let $p_i=\lfloor h_i/b\rfloor$, $K=\sum_i p_i$, and $M=\sum_i i p_i\pmod n$. Topplings preserve each remainder $h_i\bmod b$. The blocks of $b$ grains obey the ordinary cycle rule of firing at two blocks and sending one block to each neighbor. The following cases exhaust the possible totals.

* If $K<n$, every configuration stabilizes.
* If $K=n$, the configuration stabilizes exactly when $M\equiv n(n-1)/2\pmod n$.
* If $K>n$, every configuration is unstable forever.

To prove this, a stable vector $v$ of block counts must have entries 0 or 1. Fix its total $K$. We show that the configuration stabilizes if and only if at least one stable vector of total $K$ has the same moment as $p$. For the algebraic step, write $d=p-v$ and $(\Delta u)_i=2u_i-u_{i-1}-u_{i+1}$. For $\sum_i d_i=0$, the equation $d=\Delta u$ has an integer solution precisely when $\sum_i i d_i$ is divisible by $n$. Indeed, writing $g_i=u_i-u_{i-1}$ gives $g_{i+1}=g_i-d_i$. Summing the integrated differences gives $\sum_jg_j=n g_0+\sum_i i d_i$, which must vanish for $u$ to be periodic. Conversely, divisibility gives an integer $g_0$, then periodic integer differences summing to zero, then a periodic integer $u$.

For the dynamical step, add a constant to $u$ to make all its entries nonnegative. In any legal firing sequence a vertex cannot fire more often than its entry in $u$. At the first attempted excess firing it has already fired $u_i$ times, while its neighbors have fired at most their entries. Its current height in blocks is at most $(p-\Delta u)_i=v_i\le1$. Thus a legal sequence terminates whenever such a stable representative exists. Conversely, a sequence ending in a stable vector supplies the required $u$ by counting firings.

When $0<K<n$, the sums of the indices of $K$ distinct vertices run through all integers in an interval of width $K(n-K)\ge n-1$. One sees this by starting from the subset $0,\ldots,K-1$ and moving its rightmost index to $n-1$ one unit at a time, then its next-rightmost index to $n-2$, and so on. Every residue occurs. When $K=0$ the configuration is already stable. When $K=n$ the unique stable vector consists of all ones, giving the stated residue. For $K>n$ even the total stable capacity is exceeded.

## Counting independent placements

The script processes one vertex at a time. Its table counts labelled deposit sequences by grains placed, block total, and moment modulo $n$. Giving a new vertex height $h$ inserts $h$ identical vertex labels into a sequence of $s$ previous placements in $\binom{s+h}{h}$ ways. At the end the criterion above gives the successful count. The independent check enumerates every occupancy vector, directly fires all eligible vertices until the configuration is stable or repeats, and weights it by $t!/\prod_i h_i!$. Simultaneously eligible vertices can legally fire one after another in any order within a round.

For $b=2$ the code compares these two counts at **every** total from $0$ through $3n$ for $n=3,4,5$. Beyond $3n$ a stable state is impossible. If $T$ is the first addition that fails to stabilize, then $\Pr(T>t)$ is the stabilization probability after $t$ grains. Stabilizability is monotone under removing grains since a firing bound $u$ valid for the larger input still bounds every legal firing count for the smaller one. Hence $\mathbb E[T]=\sum_{t=0}^{3n}\Pr(T>t)$. The expected last-stable densities $\mathbb E[T-1]/n$ are 2.27338312, 2.26607895, and 2.28342680 for the three sizes. They decrease once before increasing. These small sizes do not estimate the infinite-volume critical density reliably.

## Run and provenance

Run `python check.py` from this directory with Python 3.8 or later. The script uses only the standard library and reads no external data. It also checks the criterion with edge multiplicities one and three on a triangle. [Verification code](check.py)

The pair decomposition is due to Fey, Levine and Wilson. General algorithms for firing finite graphs already exist, including the SageMath sandpile implementation. This note supplies a self-contained derivation and exact finite numerical checks for uniform independent deposits. A targeted search did not establish priority for the finite fractions or the small-size comparison. OpenAI Codex drafted the note and implemented both computations. [SageMath sandpile source](https://github.com/sagemath/sage/blob/develop/src/sage/sandpiles/sandpile.py) · [Björner and Lovász, chip-firing on directed graphs](https://doi.org/10.1023/A:1022467132614)
