"""Frozen paired keyword retrieval experiment. CPU only, no network at runtime."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
INPUT_SHA = "d07c3160622124a55cbe2b4440c677f9b3afb340afe8bf9473d7a9753558d56a"
REVISION = "c9745ed1d9f207416be6d2e6f8de32d1f16199bf"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def terms(text):
    return re.findall(r"[^\W_]+", text.casefold())


def bm25(documents):
    frequencies = [Counter(terms(document)) for document in documents]
    lengths = [sum(counts.values()) for counts in frequencies]
    count = len(documents)
    average_length = sum(lengths) / count
    document_frequencies = Counter(word for counts in frequencies for word in counts)
    k1, b = 1.2, 0.75

    def compare(query):
        scores = []
        for counts, length in zip(frequencies, lengths):
            norm = k1 * (1 - b + b * length / average_length)
            score = 0.0
            for word in sorted(set(terms(query))):
                df, tf = document_frequencies[word], counts[word]
                if tf:
                    weight = math.log1p((count - df + 0.5) / (df + 0.5))
                    score += weight * tf * (k1 + 1) / (tf + norm)
            scores.append(score)
        return scores

    return compare


def minilm(documents, model_dir):
    sys.path.insert(0, str(ROOT / "deps"))
    import numpy as np
    import onnxruntime as ort
    import tokenizers
    from tokenizers import Tokenizer

    model = model_dir / "model.onnx"
    tokenizer_file = model_dir / "tokenizer.json"
    asset_checksums = {
        model: "b941bf19f1f1283680f449fa6a7336bb5600bdcd5f84d10ddc5cd72218a0fd21",
        tokenizer_file: "be50c3628f2bf5bb5e3a7f17b1f74611b2561a3a27eeab05e5aa30f411572037",
    }
    for asset, expected in asset_checksums.items():
        if sha256(asset) != expected:
            raise ValueError(f"Unexpected asset checksum: {asset.name}")
    tokenizer = Tokenizer.from_file(str(tokenizer_file))
    tokenizer.enable_truncation(max_length=256)
    options = ort.SessionOptions()
    options.intra_op_num_threads = 1
    options.inter_op_num_threads = 1
    session = ort.InferenceSession(str(model), sess_options=options,
                                   providers=["CPUExecutionProvider"])

    def encode(text):
        tokens = tokenizer.encode(text)
        arrays = {
            "input_ids": tokens.ids,
            "attention_mask": tokens.attention_mask,
            "token_type_ids": tokens.type_ids,
        }
        inputs = {info.name: np.array([arrays[info.name]], dtype=np.int64)
                  for info in session.get_inputs()}
        states = session.run(["last_hidden_state"], inputs)[0][0]
        mask = np.array(tokens.attention_mask, dtype=np.float32)
        vector = (states * mask[:, None]).sum(axis=0) / mask.sum()
        return vector / np.linalg.norm(vector)

    embeddings = np.stack([encode(document) for document in documents])
    metadata = {
        "model": "sentence-transformers/all-MiniLM-L6-v2",
        "revision": REVISION,
        "onnx_file": "onnx/model_quint8_avx2.onnx",
        "model_sha256": sha256(model),
        "tokenizer_sha256": sha256(tokenizer_file),
        "numpy": np.__version__,
        "onnxruntime": ort.__version__,
        "tokenizers": tokenizers.__version__,
    }
    return lambda query: (embeddings @ encode(query)).tolist(), metadata


def evaluate(score, ids, pairs):
    details = []
    for pair in pairs:
        target = pair["target"]
        result = {"target": target}
        for form in ("neutral", "keyword"):
            scores = dict(zip(ids, score(pair[form]), strict=True))
            ranked = sorted(ids, key=lambda doc: (-scores[doc], doc))
            result[form] = {
                "rank": ranked.index(target) + 1,
                "top": ranked[0],
                "top_score_tie_size": sum(scores[doc] == scores[ranked[0]] for doc in ranked),
                "target_tie_size": sum(scores[doc] == scores[target] for doc in ranked),
                "scores": {doc: scores[doc] for doc in ranked},
            }
        details.append(result)
    hit_count = {form: sum(row[form]["rank"] == 1 for row in details)
                 for form in ("neutral", "keyword")}
    return {"hits": hit_count, "pairs": details}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lexical-only", action="store_true")
    parser.add_argument("--model-dir", type=Path, default=ROOT / "model")
    args = parser.parse_args()
    frozen = ROOT / "frozen.json"
    if sha256(frozen) != INPUT_SHA:
        raise ValueError("Frozen inputs changed")
    data = json.loads(frozen.read_bytes())
    ids = [doc["id"] for doc in data["documents"]]
    documents = [f"{doc['title']}\n{doc['snippet']}" for doc in data["documents"]]
    pairs = data["pairs"]
    for pair in pairs:
        assert terms(pair["keyword"]) == terms(pair["neutral"]) + terms(pair["cue"])
        assert len(terms(pair["cue"])) == 1

    output = {"input_sha256": INPUT_SHA, "metric": data["metric"]}
    output["bm25"] = evaluate(bm25(documents), ids, pairs)
    if not args.lexical_only:
        scorer, metadata = minilm(documents, args.model_dir)
        output["minilm"] = {"metadata": metadata, **evaluate(scorer, ids, pairs)}
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
