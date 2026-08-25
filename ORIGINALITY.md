# Originality

## Mechanism fingerprint

Its primitive is inventory reservation with recipient settlement, not a single stored classification.

Lifecycle: publish need board -> open donor batch -> consensus pair matching -> deterministic reservation -> recipient decisions -> donor closure.

Consensus boundary: Validators agree only on one-to-one offer-to-need pairs; quantities are excluded from the prompt and computed from available inventory.

Settlement boundary: Matching increases reserved counts, recipient acceptance moves them to accepted counts, and rejection releases them without double allocation.

## Review-cohort defense

Names, prompts, labels, and method names are not the basis of the distinction. The actor topology, stored state, allowed transitions, validator decision, and deterministic settlement described above are the reusable mechanism. A full-workspace structural scan is run before publication; its JSON report is retained outside the repository-wide source tree and summarized in `AUDIT.md` after the final pass.
