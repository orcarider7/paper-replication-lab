# When does retrieval weight change the MMTEB leader?

Using the printed scores, GritLM-7B and multilingual-e5-large-instruct tie when retrieval receives **57/85 of the total weight (about 67.06%)** and the other seven categories split the balance equally. Above that weight GritLM-7B leads. With eight equal weights multilingual-e5-large-instruct leads, and it stays first under every single-category omission. This calculation covers all 12 models in the MTEB(Multilingual) block of Enevoldsen et al.'s ICLR 2025 Table 2. [Published paper, Table 2, p. 8](https://proceedings.iclr.cc/paper_files/paper/2025/file/fc0e3f908a2116ba529ad0a1530a3675-Paper-Conference.pdf#page=8)

## Reproduction

The mean of the eight printed category scores reproduces the reported category mean for every model when rounded to one decimal, with exact halves rounded up. The three leading means are 62.1000 for multilingual-e5-large-instruct, 60.1125 for GritLM-7B and 59.9000 for e5-mistral-7b-instruct. These means give each category equal weight. The paper also reports an all-task mean and a separate task-level Borda ranking. Table 2 omits instruction retrieval from the category mean because of limited model support. We use the category scores from the publication and perform no new embedding inference. [Paper, sections 3.2 and 3.3](https://arxiv.org/html/2502.13595#S3)

## Sensitivity to the task mix

- Omitting standard retrieval gives e5-mistral-7b-instruct second place with 60.4857, ahead of GritLM-7B at 60.3714. The 0.1143-point gap exceeds the maximum 0.10-point gap error from one-decimal rounding of both rows. Dropping any of the other seven categories leaves GritLM-7B second in the printed-score calculation. The runner-up gap after dropping classification alone is small enough that rounding could change its order.
- With retrieval weight *w*, each other category gets weight *(1 - w)/7*. From the printed scores, multilingual-e5-large-instruct leads GritLM-7B by 2.4429 points at *w* = 0, while GritLM-7B leads by 1.2 points at *w* = 1. Their straight lines cross at 57/85, or 67.0588%. All ten other models are below multilingual-e5-large-instruct at both endpoints, so they cannot lead anywhere along this weighting path.
- Each printed category score can differ from its underlying value by up to 0.05. If A denotes E5's non-retrieval lead and B denotes GritLM's retrieval advantage, the crossover is A/(A+B). Either gap can differ by at most 0.10. Inserting the smallest A and largest B gives 164/255. Reversing those choices gives 178/255. Thus **64.31% to 69.80%** describes the outer rounding bounds, displayed to two decimal places. This uses cell precision alone. Variation across tasks, languages or evaluation runs would require separate data.

## Run

Run python verify.py with Python 3.9 or newer. The standard-library script reads table2.csv, a transcription of the eight category values and published category mean for each of the 12 multilingual rows. It computes exact rational means, checks the published decimals, reports the eight omissions, and checks the crossover and its rounding bounds. The input contains only numbers and model names from the published table.

## Related work and attribution

The MMTEB authors already identify GritLM's strong retrieval performance. A subsequent audit documents how rankings vary across languages and studies language-balanced aggregation. The calculation here asks a narrower question about the weight on retrieval in the 2025 table. A November 2026 search pairing MMTEB and GritLM with retrieval weight, category omission and leaderboard sensitivity did not locate this particular crossover. Historical priority remains open. [MMTEB paper](https://arxiv.org/abs/2502.13595) · [AACL 2026 audit of language-specific rank inversions](https://aclanthology.org/2026.aacl-short.28/)

Research note maintained by Yingbo Sun (orcarider7). This analysis has not undergone journal or conference peer review. [Friendly, public reader guestbook](../ai-guestbook/)
