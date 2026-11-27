# Paper Replication Lab

Maintained by **Yingbo Sun (orcarider7)**. Eight studies use published formulas, released scores or field observations. Each directory contains a cited research note and a Python verification script using only the standard library. [Citation information](CITATION.cff)

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
```

The data-based scripts accept a local file as an optional argument and check its checksum. Tree enumeration and sandpile stabilization run offline. Each note links its sources and explains how far the calculation supports the conclusion.

## Review and authorship

OpenAI Codex produced these AI-assisted notes and checks. The original researchers are credited in each study. Astra, Sol and Terra reviewed the claims and checked numerical outputs. Gemini reviewed the supplied reasoning and challenged the interpretations. Its medicine and penguin feedback was methodological. The numerical verification for those studies used the public input files. Terra identified a Windows line-ending mismatch in the penguin data, and the script now handles that conversion while checking the canonical hash.

For chemistry, all four reviews examined the distinction between the two model-selection rules. The 120 ways of matching fold labels quantify sensitivity to numbering. They do not supply a null distribution for a significance test. The paper’s separate bootstrap interval was outside the audit. For medicine, the 37 omissions describe a fixed set of tasks. No patient-level outcome was evaluated.

The mathematical extensions are working results. Independent literature priority and formal peer review remain open.

For the three recent checks, Astra, Sol, Terra and Gemini examined the arguments. Astra and Sol independently recovered the IMO ranks from the official results. Terra verified the journal's TeX table and ran the quantum script. Gemini reviewed the supplied formulas and counts without accessing the source data or executing code. Sol identified the Arndt tile code as the published recursive map in closed form. The Arndt note shows the equivalence explicitly. These are AI technical checks. The research notes have not received journal peer review.
