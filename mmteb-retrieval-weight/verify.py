"""Re-aggregate rounded task-category scores in MMTEB Table 2."""
import csv
from fractions import Fraction
from pathlib import Path

TABLE = Path(__file__).with_name("table2.csv")
LEADER = "multilingual-e5-large-instruct"
GRIT = "GritLM-7B"
MISTRAL = "e5-mistral-7b-instruct"
ERROR = Fraction("0.05")  # half a displayed decimal unit


def load_table():
    with TABLE.open(newline="", encoding="ascii") as handle:
        rows = list(csv.DictReader(handle))
    categories = tuple(rows[0])[2:]
    published = {row["model"]: Fraction(row["published_category"]) for row in rows}
    scores = {row["model"]: {cat: Fraction(row[cat]) for cat in categories}
              for row in rows}
    return categories, published, scores


def mean(values):
    values = tuple(values)
    return sum(values) / len(values)


def means(scores, categories):
    return {model: mean(row[cat] for cat in categories)
            for model, row in scores.items()}


def rank(totals):
    return sorted(totals, key=lambda model: (-totals[model], model))


def describe(model, totals):
    return f"{model} {float(totals[model]):.6f}"


def main():
    categories, published, scores = load_table()
    assert len(scores) == 12 and len(categories) == 8
    overall = means(scores, categories)
    for model in rank(overall):
        rounded = Fraction((10 * overall[model] + Fraction(1, 2)) // 1, 10)
        # All scores are positive. Round an exact half up at one decimal.
        assert rounded == published[model], (model, rounded)
        print(f"{describe(model, overall)} (printed {float(published[model]):.1f})")
    assert rank(overall)[:3] == [LEADER, GRIT, MISTRAL]
    assert overall[GRIT] - overall[MISTRAL] > 2 * ERROR

    print("\nLeave one category out, winner and runner-up:")
    for dropped in categories:
        reduced = means(scores, [cat for cat in categories if cat != dropped])
        winner, second, third, *_ = rank(reduced)
        assert winner == LEADER
        assert reduced[winner] - reduced[second] > 2 * ERROR
        assert second == (MISTRAL if dropped == "retrieval" else GRIT)
        robust = reduced[second] - reduced[third] > 2 * ERROR
        print(f"{dropped:20} {describe(winner, reduced)} / "
              f"{describe(second, reduced)} (runner-up rounding robust: {robust})")

    nonretrieval = means(scores, [cat for cat in categories if cat != "retrieval"])
    reversal = nonretrieval[MISTRAL] - nonretrieval[GRIT]
    assert reversal > 2 * ERROR
    print(f"Without retrieval, Mistral leads Grit by {reversal} "
          f"({float(reversal):.6f}) percentage points")

    retrieval = {model: row["retrieval"] for model, row in scores.items()}
    # All other models lie strictly below E5 at both endpoints, even with rounding.
    for model in scores.keys() - {LEADER, GRIT}:
        assert nonretrieval[LEADER] - nonretrieval[model] > 2 * ERROR
        assert retrieval[LEADER] - retrieval[model] > 2 * ERROR

    lead = nonretrieval[LEADER] - nonretrieval[GRIT]
    advantage = retrieval[GRIT] - retrieval[LEADER]
    threshold = lead / (lead + advantage)
    earliest = (lead - 2 * ERROR) / (lead + advantage)
    latest = (lead + 2 * ERROR) / (lead + advantage)
    assert 0 < earliest < threshold < latest < 1
    print(f"Retrieval-weight crossover: {threshold} = {float(threshold):.4%}")
    print(f"Rounding range: {float(earliest):.4%} to {float(latest):.4%}")


if __name__ == "__main__":
    main()
