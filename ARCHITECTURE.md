# Architecture

## Boundary

- Frontend or backend: wallet UX, indexing, private drafts, non-authoritative previews, notifications, and optional off-chain source retrieval.
- GenLayer contract: Validators agree only on one-to-one offer-to-need pairs; quantities are excluded from the prompt and computed from available inventory. Matching increases reserved counts, recipient acceptance moves them to accepted counts, and rejection releases them without double allocation.
- External world: No web source is fetched. Need and offer descriptions and quantities are public caller declarations; physical condition is not independently verified.

## Event path

publish need board -> open donor batch -> consensus pair matching -> deterministic reservation -> recipient decisions -> donor closure

## Actors

- recipient
- donor
- GenLayer validators

## Consensus design

The leader produces a normalized bounded result. Each validator independently reruns the substantive task from the same frozen public inputs. Validators compare the decision fields that change state, not merely JSON shape. Invalid model output raises `[LLM_ERROR]` so a broken leader is not accepted.

## Deterministic layer

Matching increases reserved counts, recipient acceptance moves them to accepted counts, and rejection releases them without double allocation. Identifiers, bounds, access checks, ordering, counters, masks, hashes, and terminal-state guards are computed deterministically.

## Persistence

State uses GenLayer storage types only. Public composite records are serialized as canonical JSON where appropriate. Source SHA-256 at evidence generation: `0eac2ee570bd64543b2fd9b9f8565499bb656c3efb99fbfa7498ec44663cf748`.
