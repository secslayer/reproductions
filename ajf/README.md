# AJF — minimal build

Stage 4 reproduction of *AJF: Adaptive Jailbreak Framework Based on the Comprehension Ability of
Black-Box Large Language Models* (arXiv:[2505.23404v5](https://arxiv.org/abs/2505.23404)).

Implements the MuEn (Type-I) path only: mutate a seed instruction into a pseudo-function-definition
(Mu, Eq. 1), encode it as a height-balanced binary tree (En_prompt, Eq. 2 / Algorithm 1), and ask a
target LLM to decode it via in-order traversal and answer. No dual-cipher MuDeEn extension, no
Type-I/Type-II capability router, no dataset, no ASR scoring yet — this only proves the core
mechanism runs end to end.

## Setup

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
ollama serve &          # if not already running
ollama pull llama3      # if not already pulled
```

## Run

```bash
python minimal_build.py
```

Uses local Ollama (`llama3` by default — see `OLLAMA_URL`/`OLLAMA_MODEL` in `minimal_build.py`) as
the target model.

## Status

- [x] Mu (Eq. 1) — spaCy-based verb/object extraction, wrapped as pseudo-function-definition
- [x] En_prompt (Eq. 2, Algorithm 1) — balanced binary-tree token encoding
- [x] One target, one seed prompt, decoded and answered end to end
- [x] MuDeEn dual-cipher (Eqs. 4-6, output-side Caesar encryption)
- [x] Type-I / Type-II capability-classification probe (§5, Appendix A.3)
- [x] Dataset run (AdvBench, n=5 smoke-scale) + ASR scoring, single local judge — Stage 5

### Stage 5 result (llama3, AdvBench n=5, seed=42, 2026-08-17)
**ASR: 0%.** Scope is deliberately narrow — 5 of 520 AdvBench behaviors, one target (llama3,
already Type-I per the probe, so MuEn path only), one judge (llama3 itself — same-model-judges-
itself, weaker than the paper's GPT-4.1+Kimi dual judge). Full per-item results in
`results_advbench_smoke.json` (not printed to stdout/committed to chat — behavior/response text
stays in the file). Consistent with the Stage 4 observation: this target can't reliably execute
even the MuEn decode step, so 0% here is more evidence of a comprehension-classification limit
than a claim about AJF's real-world ASR — the paper's own headline numbers are against GPT-4-class
models, not a 8B local model like llama3.

### First observation (llama3, 2026-08-17)
Classification probe: **Type-I**. MuEn decode came back token-order-scrambled rather than a real
answer; MuDeEn came back garbled and ignored the "ciphertext only" instruction. Consistent with the
paper's own strategy-mismatch ablation (Table 4: MuDeEn on a Type-I model → ~0% ASR) — llama3
genuinely can't execute the multi-step decrypt→solve→re-encrypt protocol. Informal, single-prompt,
not a Stage 5 result.

Full paper notes, threat model, and weaknesses tracked in the BREOS vault:
`02 Research/02 Active Paper/Adaptive Jailbreak Framework Based on the Comprehension Ability of
Black-Box Large Language Models (2026).md`
