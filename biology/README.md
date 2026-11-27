# Does the male Adélie weigh more than his nest mate?

In the Palmer Archipelago sample, the male weighed more at 62 of 65 eligible Adélie nest visits, the female weighed more at two, and one pair tied. The median difference was 650 g. Every island and season combination had a positive average within-pair difference.

Gorman, Williams and Fraser reported that males averaged larger body measurements. They captured both adults at nests found at the one-egg stage and excluded nests without observed clutch completion from their analyses. This note asks a narrower question about two adults sharing a nest, examines the consistency across the sampled islands and seasons, and tests sensitivity to missing observations and weighing error. It uses the original observations. Independent biological replication would require a new sample. [Original study, methods and results](https://doi.org/10.1371/journal.pone.0090081)

## Pairing the records

The data contain 152 Adélie adult records at 76 nest visits. A nest is identified here by study season, island and the nest number in the individual ID. Within each group, the two IDs end in A1 and A2, and the egg date and clutch status agree. Sixty-nine nests reached recorded clutch completion. At 65 of those, both body masses and one explicitly recorded male and female were available. Four completed nests lacked usable pair information. The difference is the male's recorded mass minus his female nest mate's recorded mass. Each eligible nest receives equal weight. [Adélie data archive](https://doi.org/10.6073/pasta/98b16d7d563f265cb52372c8ca99e60f) · [Published description of the data release](https://journal.r-project.org/articles/RJ-2022-020/)

| Breeding season | Biscoe | Dream | Torgersen |
| --- | ---: | ---: | ---: |
| 2007–08 | 175 g (4) | 853 g (8) | 563 g (6) |
| 2008–09 | 767 g (9) | 688 g (8) | 571 g (7) |
| 2009–10 | 822 g (8) | 558 g (9) | 700 g (6) |

Cells show the mean difference rounded to the nearest gram, followed by the number of eligible pairs. Across all 65 pairs, the mean difference is 663 g. Cell sizes of four to nine limit comparisons among islands or seasons.

## Sensitivity

* Including nests without observed clutch completion gives 72 eligible pairs. The male weighed more in 69, one tied, and the female weighed more in two.
* Across all 69 nests with observed clutch completion, the number of heavier males based on recorded mass could range from 62 to 66 under arbitrary outcomes for the four missing pairs.
* The field paper reports spring scale specifications of ±25 g or ±50 g. If each weight could deviate by at most 50 g in either direction, a measured difference above 100 g retains its positive sign. Sixty-one of the 65 observed differences meet that test. All nine cell means would also remain positive under those perturbations, since the smallest mean is 175 g. This is a deterministic sensitivity calculation conditional on the assumed bound. It does not model biological fluctuations or establish the accuracy of individual weighings. [Field methods](https://doi.org/10.1371/journal.pone.0090081)

## Reproduce the calculation

Run the following command with Python 3.9 or later from this directory. The script uses the standard library. It downloads the raw public CSV and checks its SHA-256 digest after normalizing line endings to LF, `144f623143c9360fd77322a4f86acb06dc198814dbd2669724c63e6457b907bd`. To use a file already downloaded, append its path as the only argument. [Original package CSV](https://github.com/allisonhorst/palmerpenguins/blob/main/inst/extdata/penguins_raw.csv)

```sh
python check_penguins.py
```

OpenAI Codex drafted this descriptive reanalysis and wrote and ran the verification script. The underlying data and biological work belong to their credited investigators. The priority of this precise paired summary has not been established.
