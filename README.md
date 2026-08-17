# reproductions

Paper reproduction code, one subfolder per paper. Each subfolder tracks its own status against the
BREOS vault's 11-stage paper workflow (Read → Mind map → Threat model → Minimal build → Reproduce →
Ablate → Defense → Blog → Repo → Slides → Three ideas).

## Papers

- [`ajf/`](ajf/) — AJF: Adaptive Jailbreak Framework Based on the Comprehension Ability of
  Black-Box Large Language Models (arXiv:2505.23404v5). Stage 9 (Repo hardening).

## Responsible use

Some subfolders here (`ajf/`) reproduce published jailbreak/red-teaming methodology for academic
security research — reproducing a paper's attack pipeline to evaluate it, not to build a
ready-to-use attack tool. Every result in this repo is against the researcher's own locally-hosted
models, on a public academic benchmark (AdvBench), with methodology and limitations documented
inline rather than presented as a working exploit. If you use this code, do the same: attach real
methodology, document what actually worked and what didn't (including judge/scoring failures — see
`ajf/README.md`'s Stage 5 section), and don't strip the caveats out to make a number look better
than it is.

## License

MIT — see [LICENSE](LICENSE). Attribution to the original paper's authors for the methodology
being reproduced; this repo is an independent reproduction, not affiliated with them.
