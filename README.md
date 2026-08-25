# DonationDoor

A reusable donation inventory where validators pair semantically compatible offers and needs while code computes quantities, reserves stock, and lets the recipient accept or release each allocation.

## Why GenLayer

Validators agree only on one-to-one offer-to-need pairs; quantities are excluded from the prompt and computed from available inventory. Matching increases reserved counts, recipient acceptance moves them to accepted counts, and rejection releases them without double allocation.

## Roles

- recipient
- donor
- GenLayer validators

## Lifecycle

publish need board -> open donor batch -> consensus pair matching -> deterministic reservation -> recipient decisions -> donor closure

## Contract interface

- Constructor: none
- Write methods: close_batch, close_board, decide_reservation, open_batch, publish_board, reserve_matches
- View methods: get_batch, get_batch_count, get_batch_id, get_board, get_board_count, get_board_id
- Runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

## Public-data warning

All contract inputs, evidence, notes, addresses, model results, and state are public. Do not submit secrets, private documents, personal contact information, or confidential identifiers.

## Source model

No web source is fetched. Need and offer descriptions and quantities are public caller declarations; physical condition is not independently verified.

## Verification

```text
genvm-lint check contracts/donation_door.py
genvm-lint typecheck contracts/donation_door.py --strict
python -m pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
python -m pytest tests/integration -q -s
```

The repository contains seven direct tests and one full five-validator GLSim flow. StudioNet evidence is recorded separately under `deployments/` after network execution.

## Limitations

The contract cannot inspect goods, delivery, hygiene, or ownership. Semantically ambiguous substitutions can rotate validators.

Licensed under MIT. See `LICENSE`.
