# Reviewed examples

This folder contains versioned example and validation data intended for the UI,
documentation, and validation suite. Each public example must include its source, units,
intended lesson, applicable validity limits, published inputs, and published outputs.

The `research` subfolder is deliberately not consumed by the application. Records there are
being evaluated for scientific compatibility and reuse rights before they can become public
examples.

Current research records:

- `research/validation_sources.json`: source provenance, reuse review, and compatibility;
- `research/validation_library_seed.json`: normalized benchmark and candidate data points.

See `docs/validation-data-collection.md` for the collection and release rules.

The public library will not store calculated differences, comparison tolerances, pass/fail
labels, or research-review status. Selecting a case will only prefill the normal calculator
inputs and make the source values available in a compact **Reference data** expander. The
normal calculation and results interface remain unchanged.

Do not add customer or confidential laboratory compositions.
