# Paper Replication Lab

Five small studies using published formulas, released scores and field observations. Each directory contains a cited research note and a Python verification script. The scripts require only the standard library. The two 2026 papers are listed first.

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
```

The data-based scripts accept a local file as an optional argument and check its checksum. Tree enumeration and sandpile stabilization run offline. Each note links its sources and explains how far the calculation supports the conclusion.

## Review and authorship

OpenAI Codex produced these AI-assisted notes and checks. The original researchers are credited in each study. Astra, Sol and Terra reviewed the claims and checked numerical outputs. Gemini reviewed the supplied reasoning and challenged the interpretations. Its medicine and penguin feedback was methodological. The numerical verification for those studies used the public input files. Terra identified a Windows line-ending mismatch in the penguin data, and the script now handles that conversion while checking the canonical hash.

For chemistry, all four reviews examined the distinction between the two model-selection rules. The 120 ways of matching fold labels quantify sensitivity to numbering. They do not supply a null distribution for a significance test. The paper’s separate bootstrap interval was outside the audit. For medicine, the 37 omissions describe a fixed set of tasks. No patient-level outcome was evaluated.

The mathematical extensions are working results. Independent literature priority and formal peer review remain open.
