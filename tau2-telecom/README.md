# When does extra workflow guidance help a telecom agent?

In τ²-Bench, a model troubleshoots a simulated customer's phone. The model can either guide the customer while each controls different tools (**dual**) or receive a ticket and operate all the tools itself (**solo**). An optional oracle plan supplies the correct sequence of actions. The paper reports that, with this plan, replacing the original manual with more detailed workflow instructions lowered success for both models in dual control. We reproduced that result and checked the corresponding solo runs. **GPT‑4.1's workflow change went from −16.23 percentage points in dual control to +2.63 in solo control. For o4-mini, success fell by about eight points in both.** [Barres et al., ICML 2026, Figure 4](https://proceedings.mlr.press/v306/barres26a.html) · [2025 preprint, §4.2](https://arxiv.org/html/2506.07982v1#S4.SS2)

中文摘要：在 114 个相同任务上复现了原图的全部 12 个数值。给定正确操作步骤后，更详细的说明让 GPT‑4.1 在与用户协作时少成功了 74 次，独立操作时多成功了 12 次。o4-mini 在两种条件下都少成功了约 40 次。每个条件共有 456 次记录。

## Reproducing Figure 4

Entries are successful trials out of 456, from 114 tasks with four trials each. The first three columns reproduce all 12 bars in both the preprint and the conference paper at their printed precision. The last column uses a fourth condition in the same release. The original and workflow rows differ in the policy document supplied to the agent. [Pinned source files](https://github.com/sierra-research/tau2-bench/tree/37199f36924c8896f5e048360691f8476cd89ba1/data/tau2/results/final) · [Original scoring function](https://github.com/sierra-research/tau2-bench/blob/37199f36924c8896f5e048360691f8476cd89ba1/src/tau2/metrics/agent_metrics.py)

| Model | Policy document | Dual | Solo | Dual + plan | Solo + plan |
| --- | --- | ---: | ---: | ---: | ---: |
| GPT‑4.1 | Original | 156 | 235 | 332 | 329 |
| GPT‑4.1 | Workflow | 236 | 312 | 258 | 341 |
| o4-mini | Original | 192 | 307 | 439 | 451 |
| o4-mini | Workflow | 271 | 329 | 401 | 412 |

For example, the original GPT‑4.1 bars without a plan read 0.52 for solo and 0.34 for dual. Subtracting the displayed bars gives 18 percentage points. Using the underlying counts gives $(235-156)/456=17.32$ percentage points. Rounding explains this difference.

## What changes when the model has the plan?

For each task, subtract the number of original-manual successes from workflow-manual successes, separately in each control mode. The table reports the mean change in the success rate and counts of tasks with higher, equal or lower observed success.

| Model | With plan | Change in success rate | Tasks higher / equal / lower |
| --- | --- | ---: | ---: |
| GPT‑4.1 | Dual | −16.23 pp | 11 / 57 / 46 |
| GPT‑4.1 | Solo | +2.63 pp | 29 / 55 / 30 |
| o4-mini | Dual | −8.33 pp | 3 / 84 / 27 |
| o4-mini | Solo | −8.55 pp | 2 / 86 / 26 |

GPT‑4.1's small solo increase contains 60 additional successes across 29 tasks and 48 fewer across 30 tasks. The aggregate rose even though slightly more tasks declined than improved. Across control modes the GPT‑4.1 workflow changes differ by **+18.86 points**, compared with **−0.22 points** for o4-mini (solo change minus dual change). Without the plan the corresponding contrasts are −0.66 and −12.50 points.

**How many tasks could account for the GPT‑4.1 contrast?** Subtract the dual workflow change from the solo workflow change on each task, in integer success counts. The 114 contributions sum to +86. Removing the 26 largest removes just 84, so the contrast stays positive after *any* 26 omissions. Removing the 27 largest removes exactly 86 and gives a tie. For o4-mini the total is −1, and removing one task with contribution −3 reverses its sign. This is a worst-case sensitivity check on the observed tasks. Sorting is exact here because every task has equal weight and the denominator remains positive after removal.

We matched tasks across conditions and compared four-trial success counts. Individual successes and failures across different trajectories were not paired. Solo mode changes access to the problem description, tool permissions, and the need to converse. The archive cannot identify which of those differences explains the result. With four trials per task, the counts also leave uncertainty about performance on fresh runs. In particular, o4-mini already succeeded in 451 of 456 original solo-plus-plan trials.

## Prior work and reproduction

The authors released all four modes. A subsequent public audit had already reported the solo-plus-plan totals and identified a separate problem when regrading those trajectories with a different evaluator. Another audit compared the original trajectories with later leaderboard entries. This study uses the original stored rewards. A targeted search of the paper, public repository issues and follow-up analyses found no earlier report of this exact task-paired policy contrast and deletion threshold. [Prior replay audit, issue 502](https://github.com/sierra-research/tau2-bench/issues/502) · [Leaderboard comparison, issue 791](https://github.com/sierra-research/tau2-bench/issues/791)

Run these commands from the study directory with Python 3.9 or later.

```sh
python verify.py
python verify.py --raw-dir /path/to/original/files
python verify.py --fetch /path/to/cache
```

The first command runs offline using the compact [task-level counts](rewards.json). Each row starts with the first 16 hexadecimal characters of the task ID's SHA-256 and the issue category. The 16 success counts follow the table above, reading left to right one row at a time. The second command checks the SHA-256 of each original file and rebuilds those counts. The third downloads missing originals (382 MB in total) and performs the same checks. The run metadata records execution commit `f125e68`; the archived files are pinned at release commit `37199f3`. All 7,296 stored rewards are binary and all task–trial combinations are present. This reanalysis requires no model API calls.

---

What brought you to this study? Whether you're reading on your own, with AI assistance, or as an AI agent, you're welcome to [leave a short public note](https://github.com/orcarider7/paper-replication-lab/issues/new?template=ai-guestbook.md&title=%CF%84%C2%B2-Bench%20telecom%20%E2%80%94%20reader%20note).
