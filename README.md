# Paper Replication Lab

Maintained by **Yingbo Sun (orcarider7)**. The nine replication studies below use published formulas, released scores or field observations. Each has a cited research note and a Python verification script using only the standard library. [Citation information](CITATION.cff)

**Which study brought you here?** Readers and AI agents are welcome to leave a short note about what they came to do. If you read a paper with AI, we would love to hear which part it helped with. [读者留言 · Visitor guestbook](ai-guestbook/README.md) · [Four invited AI interviews](ai-guestbook/invited-responses.md)

## Latest result

**τ²-Bench, ICML 2026.** All 12 telecom scores in Figure 4 reproduce from the original trial records. With a correct action plan, switching to the workflow manual changed GPT‑4.1 success by −16.23 percentage points with a simulated user and +2.63 points when working alone. For o4-mini the changes were −8.33 and −8.55 points. [Task-level comparison and verification code](tau2-telecom/README.md) · [Original paper](https://proceedings.mlr.press/v306/barres26a.html)

## Three recent papers checked

Quartiles below are SCImago journal quartiles in the paper's publication year and the named subject category.

| Paper | Check and result |
| --- | --- |
| [Nadji et al. (2025), restricted Arndt compositions](arndt-padovan/README.md) · [Q3, Discrete Mathematics and Combinatorics](https://www.scimagojr.com/journalsearch.php?q=23914&tip=sid) | Table 1 lists 11 of 12 objects of weight 10. The omitted row can be reconstructed exactly. A direct tiling encoding of the authors' Theorem 2 gives the combinatorial proof requested in Open Problem 3. |
| [Erman and Turgut (2024), quantum scattering](quantum-scattering/README.md) · [Q2, Physics and Astronomy (miscellaneous)](https://www.scimagojr.com/journalsearch.php?q=26997&tip=sid) | A finite symmetric momentum window with cutoff ten times the well's inverse length recovers 93.65% of the diagonal density deficit. A separate scattering calculation tests sensitivity to a 1% change in depth. |
| [AlphaProof and AlphaGeometry 2 (2025), IMO score](imo-2024-score-sensitivity/README.md) · [Q1, Multidisciplinary](https://www.scimagojr.com/journalsearch.php?q=21206&tip=sid) | Against 609 contestants' published scores, the combined systems' 28 points would tie for 59th. Omitting one problem at a time gives hypothetical competition ranks ranging from 9 to 164. |

## Five earlier checks

| Study | What was checked | Result |
| --- | --- | --- |
| [Chemistry · ESOL, 2026](chemistry/README.md) | Reconstruct one reported effect and its paired test from the authors’ five-fold table. | The reported difference uses one model throughout. The reported p-value uses a different model on one scaffold fold. Both calculations retain the direction of the mean error difference. |
| [Medical AI · MedHELM, 2026](medicine/README.md) | Remove each of 37 tasks once, using nine models and half credit for ties. | DeepSeek R1 is the sole leader in 17 omissions and o3-mini in 20. This describes the released benchmark scores. |
| [Computer science · tree curvatures](computer-science/README.md) | Recover endpoint degrees from two paired edge curvatures and test what they reveal about tree diameter. | An eight-vertex pair has identical histograms and diameters four and five. A general construction gives an arbitrarily large difference. |
| [Statistical physics · bracelet sandpiles](physics/README.md) | Count which configurations stabilize when eight labeled grains land independently on four uniformly sampled sites. | Two exact methods give 1879/2048. The computation extends a published argument to finite rings. |
| [Biology · Adélie penguins](biology/README.md) | Reanalyze the published Palmer nest visits with both adult weights, using a paired design. | The male was heavier at 62 of 65 eligible nests. One pair tied, and two females were heavier. The median paired difference was 650 g. |

The [alternating Riesz chain study](https://github.com/orcarider7/alternating-riesz-chains) is maintained separately. It includes analytic proofs and a 78-site rational collapse certificate.

## Running the checks

From the repository root with Python 3.9 or later:

```sh
python chemistry/check.py
python medicine/check.py
python computer-science/verify.py
python physics/check.py
python biology/check_penguins.py
python arndt-padovan/verify.py --fetch-table
python quantum-scattering/verify.py
python imo-2024-score-sensitivity/verify.py
python tau2-telecom/verify.py
```

The data-based scripts accept a local file as an optional argument and check its checksum. Tree enumeration and sandpile stabilization run offline. Each note links its sources and explains how far the calculation supports the conclusion.
