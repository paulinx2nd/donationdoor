# Reviewer Guide

## Mechanism in one sentence

A reusable donation inventory where validators pair semantically compatible offers and needs while code computes quantities, reserves stock, and lets the recipient accept or release each allocation.

## What consensus actually decides

Validators agree only on one-to-one offer-to-need pairs; quantities are excluded from the prompt and computed from available inventory.

## What code settles afterward

Matching increases reserved counts, recipient acceptance moves them to accepted counts, and rejection releases them without double allocation.

## Why this is distinct

Its primitive is inventory reservation with recipient settlement, not a single stored classification.

## Fast review path

1. Confirm the pinned dependency on the first source line.
2. Inspect the custom validator and verify it reruns the substantive task.
3. Trace role checks and terminal-state guards in each write method.
4. Run lint, strict type checking, seven direct tests, and the five-validator integration test.
5. Compare `abi.json` and the StudioNet manifest to the committed source hash.

## Known limitations

The contract cannot inspect goods, delivery, hygiene, or ownership. Semantically ambiguous substitutions can rotate validators.
