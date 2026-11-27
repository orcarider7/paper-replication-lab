# A paired keyword retrieval pilot

Appending one chosen search term changed BM25's top result in one of nine queries. It did not change the top result for the frozen MiniLM encoder. BM25 went from 8/9 to 9/9 correct, while MiniLM was 9/9 in both forms. There were no top-score ties. The BM25 change came from appending "IMO" to "What happens to the medal comparison when one problem is dropped?" The target moved from second to first, ahead of the sandpile note.

## Design

Nine existing notes form the entire candidate corpus. Each candidate includes its README title and first prose paragraph before source links. The inputs store source paths and README hashes. The experiment retrieves those excerpts directly and uses no underlying research datasets or participant data. The nine English query pairs were written for these notes, with one intended target per pair. The second form appends exactly one selected term to the original query. The terms were chosen for relevance to the intended notes.

The corpus, query pairs, intended targets and top-1 metric were frozen in frozen.json before either method scored them. The input SHA-256 is d07c3160622124a55cbe2b4440c677f9b3afb340afe8bf9473d7a9753558d56a. Top-1 is the number of pairs for which the intended target ranks first, reported separately for each form. The runner resolves exact score ties by ascending document ID. The archived JSON also records target ranks and ties, top results and all candidate scores.

BM25 uses case-folded Unicode alphanumeric tokens, k1 = 1.2 and b = 0.75, with each distinct query term scored once. MiniLM tokenizes each text independently, truncates to 256 tokens, mean-pools the final token states with the attention mask, normalizes the pooled vectors and ranks by cosine similarity. We used the CPU execution provider with one intra-op and one inter-op thread. [Pinned MiniLM model and tokenizer revision](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/tree/c9745ed1d9f207416be6d2e6f8de32d1f16199bf)

Eight of the nine added terms are exact case-folded token matches unique to their target excerpt. The other term, "curvature," occurs in none of the excerpts under this tokenization, which treats "curvatures" as a different word. The query writer knew the corpus, and the pilot did not include an irrelevant-term control. Its result therefore describes these selected cues on these nine excerpts. MiniLM's 9/9 neutral baseline leaves no room for improvement on the top-1 metric, even if similarity scores change. These synthetic queries measure retrieval rankings, with no participant data or measurement of model internals, generated answers, or how an interface serves people.

## Reproduce

From this folder, Python 3.11 can run the lexical baseline without any dependencies.

```sh
python -B pilot.py --lexical-only
```

The full run was verified on Windows AMD64 with Python 3.11.9 and an AVX2 CPU model export. The following setup uses Python on both PowerShell and POSIX shells. Other AMD64 environments with AVX2 can install the three pinned runner dependencies; the included requirements file records the full Windows environment.

```sh
python -m pip install --target deps numpy==2.3.4 onnxruntime==1.23.2 tokenizers==0.22.1
python -c "from pathlib import Path; from urllib.request import urlretrieve; root = Path('model'); root.mkdir(exist_ok=True); base = 'https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/c9745ed1d9f207416be6d2e6f8de32d1f16199bf/'; urlretrieve(base + 'onnx/model_quint8_avx2.onnx', root / 'model.onnx'); urlretrieve(base + 'tokenizer.json', root / 'tokenizer.json')"
python -B pilot.py
```

The full run needs no network after setup. It checks the frozen input and both model assets by SHA-256. Use --model-dir to point to an existing folder with both assets. The frozen excerpts are embedded in frozen.json and can be used independently of the original README paths. Repeat runs in the verified environment produced the archived results.json line for line. Floating-point scores may vary across platforms.

## Corpus sources

The nine source titles and excerpts are embedded in `frozen.json`. The source paths and checksums there refer to the preparation checkout. Each link below opens the corresponding public README at the revision used.

- [arndt-compositions-tiling-proof](https://github.com/orcarider7/arndt-compositions-tiling-proof/blob/1a9447ee1a3a08762079fcc1da1ae22acf5a8209/README.md)
- [imo-2024-score-sensitivity](https://github.com/orcarider7/imo-2024-score-sensitivity/blob/13344a22ebcdf5576b0e1e8412755727452c6aa3/README.md)
- [esol-scaffold-split-audit](https://github.com/orcarider7/esol-scaffold-split-audit/blob/0916ee2ead5f636f32c6b205f9aea32610eb71df/README.md)
- [medhelm-ranking-sensitivity](https://github.com/orcarider7/medhelm-ranking-sensitivity/blob/851da9374e4b323a9e5e4e17dcd1dd97b76d0e35/README.md)
- [tree-curvature-and-diameter](https://github.com/orcarider7/tree-curvature-and-diameter/blob/01546e2cab825e0903d035a96a5bef9ab96fd39a/README.md)
- [finite-bracelet-sandpiles](https://github.com/orcarider7/finite-bracelet-sandpiles/blob/67768fd1a9fe83774e4a240c82a0b04edbd876e1/README.md)
- [adelie-penguin-nest-pairs](https://github.com/orcarider7/adelie-penguin-nest-pairs/blob/8d30121bfe454952596e53f6dbb54007dbc3b374/README.md)
- [quantum-well-bandwidth](https://github.com/orcarider7/quantum-well-bandwidth/blob/6deedcb018c1bdf120a593760439a764b3446e65/README.md)
- [tau2-telecom-workflow-audit](https://github.com/orcarider7/tau2-telecom-workflow-audit/blob/868f50a4439ce638509e86be370426edfecad45c/README.md)
