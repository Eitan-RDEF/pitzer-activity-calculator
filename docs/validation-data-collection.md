# Validation data collection

## Purpose

The future reference library will let a user select a sourced composition, load it into the
calculator, and press **Calculate with Pitzer**. The normal result interface remains
unchanged. Published values, definitions, assumptions, and a direct source link remain
available in a compact **Reference data** expander for users who want to consult them.

Version 1 will not add a comparison view, show calculated differences, assign tolerances,
or declare pass/fail. Interpretation remains with the user.

The research records are stored under `data/examples/research/`. They are not loaded by the
application until every release gate below is satisfied.

## Two evidence classes

The UI must label these classes separately:

1. **Independent reference data** — experimental observations or evaluated values derived
   from experimental literature. These test scientific agreement.
2. **Implementation benchmarks** — published outputs from PHRQPITZ, PHREEQC, or another
   implementation. These test model setup, database compatibility, parsing, and numerical
   reproduction; they are not experimental validation.

Neither class should be described simply as “validated” without naming what was compared.

## Release gates for each case

A case can enter the public library only when all of the following are recorded:

- stable source URL and full citation;
- page, table, figure, or machine-readable record identifier;
- explicit reuse status suitable for a free public app;
- property definition, concentration basis, temperature, pressure, and composition;
- exact mapping from the source composition to the app's analytical inputs;
- any app-added assumption, especially fixed pH, redox state, charge treatment, or absence
  of solids;
- independently checked transcription;
- a user-facing explanation of whether the record is experimental evidence or a software
  benchmark;
- a successful internal smoke calculation confirming that the mapped input is accepted by
  the pinned engine/database pair.

Research-only status and reproduction notes may be retained outside the public library to
support maintainers. They are not part of the user-facing case format.

The approved production record should contain only:

- case identifier, name, and short description;
- input conditions and analytical composition;
- published reference outputs;
- evidence class;
- citation, direct source link, and exact table/page/record locator;
- assumptions and limitations.

It should not contain calculated differences, tolerances, pass/fail labels, or research status.

A production case should follow this conceptual shape:

```json
{
  "id": "source_case_identifier",
  "title": "Human-readable case name",
  "evidence_type": "experimental_or_evaluated_reference",
  "source": {
    "citation": "Full citation",
    "url": "https://source.example",
    "locator": "Table 1, page 10"
  },
  "input": {
    "temperature_c": 25.0,
    "pressure_atm": 1.0,
    "known_ph": 7.0,
    "composition_unit": "mol/kg_H2O",
    "components": {"Na": 1.0, "Cl": 1.0}
  },
  "published_outputs": {
    "mean_activity_coefficients": {"NaCl": 0.657},
    "water_activity": 0.9668,
    "osmotic_coefficient": 0.936
  },
  "assumptions": ["Any mapping assumption added by the app"]
}
```

Selecting this case prefills `input`. The **Reference data** expander renders
`published_outputs`, `source`, and `assumptions`. Pressing **Calculate with Pitzer** follows
the existing calculation path and renders the existing results interface.

## Initial collection (2026-08-26)

The first normalized seed contains:

- four public-domain USGS implementation benchmarks: one concentrated NaCl-CaSO4 final
  state and three halite-saturated NaCl final states at 0, 25, and 100 degrees C;
- twelve NaCl and KCl evaluated reference points from Hamer and Wu (1972), retained as
  blocked research candidates until redistribution rights and the app's required fixed-pH
  convention are resolved.

All four USGS states were reproduced on 2026-08-26 with PHREEQC
`3.8.6-17100-x64` and database SHA-256
`3640e62aee63a118f800b115b46a2760576e63e05e1792022315a28f75dbe9bb`.
The seed currently retains internal reproduction outputs for scientific traceability. These
are research metadata and will not be copied into the public library. The observed historical
differences are documented in `validation-source-research-summary.md`; the app will neither
calculate nor display them.

The USGS records are good first engineering benchmarks because their reported final aqueous
states can be re-entered using components already exposed by the app. The original mineral
equilibrium paths are not reproduced by the current product and must not be implied.

The Hamer-Wu records are scientifically useful, but a binary electrolyte table does not define
the fixed pH required by this calculator. Choosing pH 7 without documenting and testing its
effect would silently change the reference problem. Their reuse status also requires a more
specific review than a general assumption that all government-hosted material is unrestricted.

The NASA/NBS Part XIII report was reviewed but its salts require analytical components not
currently exposed by the app. The NTRS catalog marks it public-use-permitted, while the
report itself carries an older reproduction restriction; it is therefore not a release source
until that conflict is resolved.

NSRDS-NBS 24 was screened out as independent evidence because it tabulates theoretical
charge-type equations rather than salt-specific experimental values. NIST ThermoML remains
a promising discovery source, but every record needs its own scientific and rights review.

## Next collection priority

1. Investigate the historical/current-model differences as internal scientific work; do not
   turn them into a public pass/fail feature.
2. Locate source-cleared experimental NaCl and KCl data with explicit property definitions
   and uncertainty.
3. Add CaCl2, MgCl2, Na2SO4, and mixed chloride/sulfate cases.
4. Add seawater-like and carbonate-bearing cases only when pH, alkalinity or total carbon,
   charge balance, and phase assumptions map exactly to the app.
5. Expose only reviewed cases in the selector, with their source values and link in a compact
   **Reference data** expander.
