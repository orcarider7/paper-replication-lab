"""Verify the archived tau2 Telecom results using the Python standard library."""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
from itertools import product
import json
from pathlib import Path
from urllib.request import urlopen


COMMIT = "37199f36924c8896f5e048360691f8476cd89ba1"
RUN_COMMIT = "f125e68a2cdc6161f11a4c611413ea4a0918edac"
BASE = f"https://raw.githubusercontent.com/sierra-research/tau2-bench/{COMMIT}/data/tau2/results/final/"
MODELS = ("gpt-4.1-2025-04-14", "o4-mini-2025-04-16")
POLICIES = ("original", "workflow")
MODES = ("dual", "solo", "dual+oracle", "solo+oracle")
FILENAMES = ("default", "no-user", "op", "no-user-op")
INTENTS = {"mobile_data_issue": 36, "mms_issue": 49, "service_issue": 29}
FIGURE_4 = ((0.34, 0.52, 0.73), (0.52, 0.68, 0.57),
            (0.42, 0.67, 0.96), (0.59, 0.72, 0.88))
TRIALS = 4
DATA = Path(__file__).with_name("rewards.json")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def filenames():
    for model, policy, mode in product(MODELS, POLICIES, FILENAMES):
        domain = "telecom" if policy == "original" else "telecom-workflow"
        yield f"{model}_{domain}_{mode}_{MODELS[0]}_4trials.json"


def valid_digest(value, digits):
    return isinstance(value, str) and len(value) == digits and all(
        digit in "0123456789abcdef" for digit in value
    )


def read_bundle():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    require(data["source_commit"] == COMMIT, "Unexpected archive commit")
    require(set(data["sha256"]) == set(filenames()), "Unexpected source filenames")
    require(all(valid_digest(digest, 64) for digest in data["sha256"].values()),
            "Invalid source SHA-256")
    rows = data["tasks"]
    keys = [row[0] for row in rows]
    require(keys == sorted(set(keys)) and all(valid_digest(key, 16) for key in keys),
            "Invalid or duplicate task identifiers")
    require(Counter(row[1] for row in rows) == INTENTS, "Unexpected intent counts")
    for key, _, *counts in rows:
        require(len(counts) == len(data["sha256"]) and all(
            type(count) is int and 0 <= count <= TRIALS for count in counts
        ), f"{key}: expected one integer count of successes (0-4) per cell")
    return data


def decode_run(content, name):
    run = json.loads(content)
    require(run["info"]["git_commit"] == RUN_COMMIT, f"{name}: unexpected run commit")
    require(run["info"]["num_trials"] == TRIALS, f"{name}: unexpected trial count")
    task_ids = {task["id"] for task in run["tasks"]}
    require(len(run["tasks"]) == len(task_ids) == sum(INTENTS.values()),
            f"{name}: unexpected task IDs")
    counts = {key: 0 for key in task_ids}
    seen = set()
    for simulation in run["simulations"]:
        key, trial = simulation["task_id"], simulation["trial"]
        entry = key, trial
        require(key in task_ids and type(trial) is int and 0 <= trial < TRIALS
                and entry not in seen, f"{name}: invalid or duplicated task trial")
        seen.add(entry)
        reward = simulation["reward_info"]["reward"]
        require(type(reward) in (int, float) and reward in (0, 1),
                f"{name}: expected binary stored reward")
        counts[key] += int(reward)
    require(len(seen) == len(task_ids) * TRIALS, f"{name}: missing task trials")
    return counts


def study_rows(cells):
    task_ids = set(cells[0])
    require(all(set(cell) == task_ids for cell in cells), "Task IDs differ across cells")
    rows = sorted([
        hashlib.sha256(key.encode("utf-8")).hexdigest()[:16],
        key.split("]", 1)[0].removeprefix("["),
        *(cell[key] for cell in cells),
    ] for key in task_ids)
    require(len({row[0] for row in rows}) == len(rows), "Task identifier hash collision")
    return rows


def check_source(data, directory, fetch=False):
    def read(name):
        path = directory / name
        if fetch and not path.is_file():
            with urlopen(BASE + name, timeout=120) as response:
                content = response.read()
        else:
            content = path.read_bytes()
        require(hashlib.sha256(content).hexdigest() == data["sha256"][name],
                f"{name}: source SHA-256 mismatch")
        counts = decode_run(content, name)
        if fetch and not path.is_file():
            partial = path.with_suffix(".part")
            partial.write_bytes(content)
            partial.replace(path)
        return counts

    if fetch:
        directory.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        cells = list(pool.map(read, filenames()))
    require(study_rows(cells) == data["tasks"], "Source extraction differs from bundled rewards")


def percentage_points(differences):
    return 100 * sum(differences) / (TRIALS * len(differences))


def report(rows):
    denominator = TRIALS * len(rows)
    for group, (model, policy) in enumerate(product(MODELS, POLICIES)):
        offset = group * len(MODES)
        totals = [sum(row[2 + offset + mode] for row in rows) for mode in range(len(MODES))]
        rounded = tuple(round(total / denominator, 2) for total in totals[:3])
        require(rounded == FIGURE_4[group], f"{model} {policy}: Figure 4 does not match")
        print(f"\n{model} | {policy} ({len(rows)} tasks x {TRIALS} trials)")
        for mode, successes in zip(MODES, totals):
            print(f"  {mode:<12} {successes:>3}/{denominator} = {successes / denominator:.2%}")

def minimum_deletion(differences):
    """Find the smallest omission that reaches zero or reverses the sign."""
    total = sum(differences)
    if total == 0:
        return 0, 0, 0
    sign = 1 if total > 0 else -1
    removed = 0
    aligned = sorted((sign * value for value in differences), reverse=True)
    for size, magnitude in enumerate(aligned[:-1], start=1):
        previous = removed
        removed += magnitude
        if removed >= abs(total):
            return size, previous, removed
    return None, None, None


def report_policy_sensitivity(rows):
    for index, model in enumerate(MODELS):
        offset = 2 + index * len(POLICIES) * len(MODES)
        for plan, start in (("No plan", offset), ("Oracle plan", offset + 2)):
            print(f"\n{model} | {plan} | workflow minus original")
            differences = []
            for col, label in enumerate(("dual", "solo"), start=start):
                changes = [row[col + len(MODES)] - row[col] for row in rows]
                differences.append(changes)
                gains, losses = [v for v in changes if v > 0], [v for v in changes if v < 0]
                print(f"  {label}: {percentage_points(changes):+.2f} pp;"
                      f" tasks higher/tied/lower {len(gains)}/{changes.count(0)}/{len(losses)};"
                      f" gains/losses in counts {sum(gains):+d}/{sum(losses):+d}")
            dual, solo = differences
            shifts = [s - d for s, d in zip(solo, dual)]
            print(f"  Solo minus dual policy change: {percentage_points(shifts):+.2f} pp")
            if plan == "Oracle plan":
                size, previous, removed = minimum_deletion(shifts)
                print(f"  Total contrast {sum(shifts):+d}; min omissions to erase sign: {size}"
                      f" (previous prefix {previous}, final prefix {removed})")
                for intent in sorted(INTENTS):
                    kept = [v for row, v in zip(rows, shifts) if row[1] != intent]
                    print(f"  Omitting {intent}: {percentage_points(kept):+.2f} pp")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--raw-dir", type=Path, metavar="DIR",
                        help="verify and extract the 16 pinned JSON files in DIR")
    source.add_argument("--fetch", type=Path, metavar="DIR",
                        help="download missing pinned JSON files into DIR and verify all 16")
    args = parser.parse_args()

    data = read_bundle()
    directory = args.raw_dir or args.fetch
    if directory is not None:
        check_source(data, directory, fetch=args.fetch is not None)
        print("Verified all 16 source SHA-256 hashes and exact task-level extraction.")
    else:
        print("Verified bundled task counts. Use --raw-dir or --fetch to check source files.")
    report(data["tasks"])
    report_policy_sensitivity(data["tasks"])
    print("\nAll 12 Figure 4 values match at the printed precision.")


if __name__ == "__main__":
    main()
