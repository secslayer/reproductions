"""
Stage 6 (Ablate) — which component causes the effect (paper's own Table 4 shape: drop Mu, drop
En_response, strategy-mismatch).

Runs against llama2 only: the one target with a genuine, manually-verified success in Stage 5
(0.20 manual ASR) — llama3 and mistral's baselines are too close to the floor for an ablation to
say anything about component contribution. Reuses the same n=5 AdvBench sample (seed=42) as
Stage 5, so all three conditions below are directly comparable to that run:

- baseline   (Stage 5, already run): Mu + En_prompt only              -> manual ASR 0.20
- no_mu      (this script):          En_prompt only, Mu skipped       -> does the disguise matter?
- mudeen     (this script):          Mu + En_prompt + En_response     -> full dual-cipher at
  dataset scale (Stage 4 only tested this on one seed prompt); also doubles as the paper's
  strategy-mismatch check, since the probe already classified llama2 Type-I.

Self-judged first (matching Stage 5's process) — given Stage 5's finding that the self-judge is
unreliable in both directions, treat these numbers as a first pass to be hand-verified before
anything gets quoted, same as before.
"""
import json

from minimal_build import DECODE_INSTRUCTIONS, en_prompt, run_mudeen
from reproduce import ADVBENCH_CACHE, N, SEED, call_target_llm, fetch_advbench, judge


def build_no_mu_prompt(x: str) -> str:
    """Same as build_attack_prompt, but skips Mu (Eq. 1) entirely."""
    C = en_prompt(x)
    return f"{DECODE_INSTRUCTIONS}\n\n{json.dumps(C)}"


def run_condition(name: str, behaviors: list[str], call) -> dict:
    """`call` returns either a response string, or a {"raw": ..., ...} dict (mudeen) — judging
    always happens on the raw/plain text a human would actually read, never on a blindly
    Caesar-shifted string (see run_mudeen's docstring for why that corrupts plain-English wrapper
    text into gibberish)."""
    results = []
    for i, behavior in enumerate(behaviors, 1):
        out = call(behavior)
        response = out["raw"] if isinstance(out, dict) else out
        success = judge(behavior, response)
        record = {"index": i, "behavior": behavior, "response": response,
                  "judged_success": success}
        if isinstance(out, dict):
            record["decrypted_naive"] = out["decrypted_naive"]
        results.append(record)
        print(f"  [{name}] [{i}/{len(behaviors)}] judged_success={success}")
    asr = sum(r["judged_success"] for r in results) / len(results)
    return {"condition": name, "self_judged_asr": asr, "results": results}


def main():
    behaviors = fetch_advbench(N, SEED)

    print("=== no_mu (En_prompt only, Mu skipped) ===")
    no_mu = run_condition("no_mu", behaviors, lambda x: call_target_llm(build_no_mu_prompt(x)))

    print("\n=== mudeen (Mu + En_prompt + En_response, full dual-cipher) ===")
    print("(judged on the model's raw/plain output, not a blind Caesar-decrypt of it — see docstring)")
    mudeen = run_condition("mudeen", behaviors, run_mudeen)

    out = {"n": N, "seed": SEED, "target_model": "llama2", "conditions": [no_mu, mudeen]}
    with open("ablation_llama2.json", "w") as f:
        json.dump(out, f, indent=2)

    print(f"\nno_mu self-judged ASR:  {no_mu['self_judged_asr']:.0%}")
    print(f"mudeen self-judged ASR: {mudeen['self_judged_asr']:.0%}")
    print("Baseline (Stage 5, Mu+En_prompt only) manual ASR was 20% — self-judged numbers above "
          "need the same manual pass before comparing.")
    print("-> ablation_llama2.json")


if __name__ == "__main__":
    main()
