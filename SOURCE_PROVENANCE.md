# Source Provenance

## Collection behavior

No web source is fetched. Need and offer descriptions and quantities are public caller declarations; physical condition is not independently verified.

The contract performs no live web request, does not scrape a page, and does not silently claim that a label or URL authenticates its publisher. This avoids validator drift from changing pages. If an application needs live retrieval, that retrieval belongs in a separately reviewed mechanism whose validators independently fetch and normalize the same source.

## Integrity bindings

- Contract source SHA-256: `0eac2ee570bd64543b2fd9b9f8565499bb656c3efb99fbfa7498ec44663cf748`
- ABI SHA-256: `cd67553d67d1917b299205363fc01afbb93c572d4b803a94a0e16f15e1c0f71e`
- Frozen text and canonical JSON records are hashed inside the contract where the workflow needs a content binding.
- Human-readable source references, when present, are expressly marked unverified.

## Fixture policy

Tests use synthetic public fixtures written for this repository. They are not copied production records and do not represent real people.
