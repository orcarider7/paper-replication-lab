# How much of a bound state can a finite momentum window recover?

Fatih Erman and O. Teoman Turgut reconstructed the bound-state projector of a one-dimensional reflectionless quantum well from its continuum states. We check the diagonal of their identity and compute the fraction recovered when the continuum integral stops at a finite wave number. At a cutoff ten times the inverse width, the reconstruction recovers 93.65% of the bound-state density at every position. A separate scattering calculation tests the effect of changing the well depth. [2024 paper, *American Journal of Physics* 92, 950–956](https://doi.org/10.1119/5.0228452) · [Versioned author manuscript, Eqs. (4.2), (4.9) and (6.1)](https://arxiv.org/html/2411.14941v1)

SCImago lists the journal in Q2 for **Physics and Astronomy (miscellaneous), 2024**, the year the paper appeared. The same category was Q3 in 2025. [SCImago journal profile and quartile history](https://www.scimagojr.com/journalsearch.php?q=26997&tip=sid)

## Continuum bandwidth

Let $\kappa>0$ be the well's inverse width and $K$ the largest measured or computed wave number. The normalized continuum state in Eq. (4.2) has density

$$
|\psi_k(x)|^2=\frac{k^2+\kappa^2\tanh^2(\kappa x)}{2\pi(k^2+\kappa^2)}.
$$

Subtract that density from the corresponding free-particle density $1/(2\pi)$ **before** integrating. This avoids evaluating a delta function on its diagonal. The resulting integrand is proportional to $1/(k^2+\kappa^2)$. For a symmetric window, the truncated deficit is

$$
D_K(x)=\int_{-K}^K\left[\frac{1}{2\pi}-|\psi_k(x)|^2\right]dk
=\frac{\kappa\,\mathrm{sech}^2(\kappa x)}{2}\,
  \frac{2}{\pi}\arctan(K/\kappa).
$$

As $K$ increases, the first factor gives precisely the diagonal bound-state projector reported in Eq. (6.1). The second factor quantifies the effect of the cutoff independently of position. For example, recovering a fraction $f$ requires $K/\kappa\ge\tan(\pi f/2)$.

| Target fraction | Minimum $K/\kappa$ |
| --- | ---: |
| 50% | 1 |
| 95% | 12.70620474 |
| 99% | 63.65674116 |

Thresholds with decimals are rounded. The script integrates the squared modulus of the complex continuum wave by composite Simpson quadrature and compares it with the closed form at four bandwidths and three positions. This checks the diagonal deficit. Off-diagonal projected kernels and errors from experimental noise require separate analysis.

## Well-depth sensitivity

Use the dimensionless coordinate $u=\kappa x$, wave number $s=k/\kappa$, and well strength $g$. The stationary equation is

$$
-\psi''(u)-g\,\mathrm{sech}^2(u)\,\psi(u)=s^2\psi(u).
$$

The 2024 paper's one-bound-state example has $g=2$ and zero reflection probability for every $s>0$. To check sensitivity, keep the width fixed and perturb the well depth by one percent. Write $g=\nu(\nu+1)$ with $\nu>0$. The known exact reflection probability is $R=\sin^2(\pi\nu)/(\sinh^2(\pi s)+\sin^2(\pi\nu))$. Equation (9) of the cited work uses $\lambda=\nu+1$, which leaves this expression unchanged. [Primary scattering formula, Eqs. (7)–(9)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5937562/)

| $s$ | $g=1.98$ | $g=2$ | $g=2.02$ |
| ---: | ---: | ---: | ---: |
| 0.02 | 0.100270026 | 0 | 0.099471053 |
| 0.10 | 0.004301079 | 0 | 0.004263183 |
| 1.00 | 0.000003303 | 0 | 0.000003274 |

Entries are reflection probabilities. At fixed noninteger $\nu$, $R$ tends to one as $s$ tends to zero. At the tuned depth, $R$ stays zero for every positive $s$. The table illustrates how the order of these limits matters for low-energy transmission. It assumes monochromatic scattering and an unchanged well shape.

## Reproduce

Run `python quantum-scattering/verify.py` from the repository root with Python 3.9 or later. The standard-library script runs offline. It solves the differential equation independently of the scattering formula by propagating a unit right-going wave back from the right endpoint and decomposing it into incident and reflected waves at the left endpoint. Two runs use intervals $[-16,16]$ and $[-20,20]$ with step magnitudes 0.01 and 0.005. Both check reflection against the exact formula and verify flux conservation. [Verification script](verify.py)

This AI-assisted note reproduces a specific identity from the paper and applies known formulas to stated bandwidths and depths. Its figures are theoretical calculations. The results support the paper's single-well example.

---

What brought you to this study? Whether you're reading on your own, with AI assistance, or as an AI agent, you're welcome to [leave a short public note](https://github.com/orcarider7/paper-replication-lab/issues/new?template=ai-guestbook.md&title=Finite-window%20quantum%20scattering%20%E2%80%94%20reader%20note).
