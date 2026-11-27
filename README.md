# Paper Replication Lab

Maintained by **Yingbo Sun (orcarider7)**. The first nine studies each have a public repository with sources and verification code. Further studies are listed below with their own research notes. [Citation information](CITATION.cff)

## Study catalogue

- [Restricted Arndt compositions and a tiling proof](https://github.com/orcarider7/arndt-compositions-tiling-proof) — Reconstructs the missing weight-10 entry in Table 1 and gives a direct tiling proof for the identity in Open Problem 3. [Nadji et al. (2025)](https://cs.uwaterloo.ca/journals/JIS/VOL28/Ramirez/ramirez19.html) · [Q3, Discrete Mathematics and Combinatorics](https://www.scimagojr.com/journalsearch.php?q=23914&tip=sid) · [Original lab directory](arndt-padovan/)
- [Adélie penguin mass differences within nest pairs](https://github.com/orcarider7/adelie-penguin-nest-pairs) — Males were heavier in 62 of 65 eligible pairs. One pair tied, and the median male-minus-female difference was 650 g. [Field study](https://doi.org/10.1371/journal.pone.0090081) · [Data archive](https://doi.org/10.6073/pasta/98b16d7d563f265cb52372c8ca99e60f) · [Original lab directory](biology/)
- [ESOL scaffold split audit](https://github.com/orcarider7/esol-scaffold-split-audit) — The reported mean error gap and paired p-value can be reconstructed from model selections that differ on one fold. Both selections give higher mean error on the scaffold split. [Zheng, Ju and Hong (2026)](https://doi.org/10.1080/00319104.2026.2727897) · [Original lab directory](chemistry/)
- [Tree edge curvature and diameter](https://github.com/orcarider7/tree-curvature-and-diameter) — The paired curvature histogram recovers the endpoint-degree counts. Eight-vertex trees with the same histogram have diameters four and five, and a general construction gives arbitrarily large gaps. [Forman curvature](https://arxiv.org/abs/1603.00386) · [Jost and Liu’s tree formula](https://arxiv.org/pdf/1103.4037#page=9) · [M-polynomial](https://arxiv.org/abs/1407.1592) · [Original lab directory](computer-science/)
- [2024 IMO score sensitivity for AlphaProof and AlphaGeometry 2](https://github.com/orcarider7/imo-2024-score-sensitivity) — The systems’ combined score of 28 points would tie for 59th against 609 contestants. Dropping one problem at a time gives hypothetical ranks from 9th to 164th. [Hubert et al. (2025)](https://doi.org/10.1038/s41586-025-09833-y) · [Q1, Multidisciplinary](https://www.scimagojr.com/journalsearch.php?q=21206&tip=sid) · [Original lab directory](imo-2024-score-sensitivity/)
- [MedHELM ranking sensitivity](https://github.com/orcarider7/medhelm-ranking-sensitivity) — With half credit for ties, DeepSeek R1 leads in 17 of 37 single-task omissions and o3-mini leads in the other 20. [MedHELM paper](https://doi.org/10.1038/s41591-025-04151-2) · [Original lab directory](medicine/)
- [Stabilization on finite bracelet sandpiles](https://github.com/orcarider7/finite-bracelet-sandpiles) — Two exact methods give a stabilization probability of 1879/2048 for eight grains deposited independently and uniformly on a four-site bracelet. [Fey, Levine and Wilson](https://doi.org/10.1103/PhysRevE.82.031121) · [Original lab directory](physics/)
- [Finite-bandwidth reconstruction of a quantum well](https://github.com/orcarider7/quantum-well-bandwidth) — A symmetric wave-number cutoff at ten times the inverse well width recovers 93.65% of the bound-state density at every position. A separate calculation tests a 1% change in well depth. [Erman and Turgut (2024)](https://doi.org/10.1119/5.0228452) · [Q2, Physics and Astronomy (miscellaneous)](https://www.scimagojr.com/journalsearch.php?q=26997&tip=sid) · [Original lab directory](quantum-scattering/)
- [τ²-Bench telecom workflow audit](https://github.com/orcarider7/tau2-telecom-workflow-audit) — All 12 telecom scores in Figure 4 reproduce. With the oracle action plan, the workflow manual changed GPT‑4.1 success by −16.23 percentage points in dual control and +2.63 in solo control. For o4-mini, the changes were −8.33 and −8.55 points. [Barres et al., ICML 2026](https://proceedings.mlr.press/v306/barres26a.html) · [Original lab directory](tau2-telecom/)

Quartiles refer to SCImago’s ranking for the publication year and the named subject category.

## Further studies

- [When does retrieval weight change the MMTEB leader?](mmteb-retrieval-weight/) — Reproduces all 12 published category means. The two leading models tie when retrieval has about 67% of the weight and the other seven categories share the rest equally. [ICLR 2025, Table 2](https://proceedings.iclr.cc/paper_files/paper/2025/file/fc0e3f908a2116ba529ad0a1530a3675-Paper-Conference.pdf#page=8)
- [How rare are single-handed L-tetromino tilings?](l-tetromino-chirality/) — Reproduces the nine counts in Table 3 of Lucy Martinez’s 2026 preprint. When both mirror shapes are allowed, at most $109^{-n}$ of the tilings of a fixed $5 \times 8n$ board use just one handedness. At $n=1$, exactly 4 of 436 tilings do. [Original preprint, Proposition 3](https://arxiv.org/html/2607.29369v2#S2.SS2)

## Related project and guestbook

- [Alternating Riesz chains](https://github.com/orcarider7/alternating-riesz-chains) includes analytic proofs and a 78-site rational collapse certificate.
- [友善 · 公开 · 自愿 / Friendly, public, optional reader guestbook](ai-guestbook/README.md) welcomes human readers and AI agents. What brought you here, and where did you need help reading or checking a paper? [Research questions and methods](ai-guestbook/study-design.md)
- [Does a keyword change which research note ranks first?](ai-guestbook/keyword-pilot/) reports a paired retrieval test on the nine original notes, with frozen queries, scores and code.
- [Four invited AI interviews](ai-guestbook/invited-responses.md) records responses collected by invitation.

## Running the checks

From the repository root with Python 3.9 or later:

```sh
python arndt-padovan/verify.py --fetch-table
python biology/check_penguins.py
python chemistry/check.py
python computer-science/verify.py
python imo-2024-score-sensitivity/verify.py
python medicine/check.py
python physics/check.py
python quantum-scattering/verify.py
python tau2-telecom/verify.py
python l-tetromino-chirality/verify.py
python mmteb-retrieval-weight/verify.py
```

The data-based scripts accept a local file as an optional argument and verify its checksum. Tree enumeration and sandpile stabilization run offline.
