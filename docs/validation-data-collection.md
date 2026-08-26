# Validation data collection

## Purpose

The future validation library will let a user select a sourced composition, load it into the
calculator, press **Calculate with Pitzer**, and compare the app result with the published
reference. The calculation remains user-triggered; the library supplies reviewed inputs,
reference values, definitions, and source links.

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
- reproduction result using the pinned PHREEQC version and bundled `pitzer.dat` checksum;
- a justified comparison tolerance that reflects source precision and model differences;
- a user-facing explanation of whether the record is experimental evidence or a software
  benchmark.

If any item is missing, `release_eligible` remains `false` or the status remains
`source_cleared_pending_reproduction`.

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
The seed records both current outputs and app-minus-reference deltas. No pass/fail tolerance
has been assigned yet: the largest observed difference is in the 0 degrees C saturated-NaCl
mean coefficient, while water activity and osmotic-coefficient results remain close. This must
be investigated as a database/version or method difference before a release threshold is set.

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

1. Investigate the historical/current-model deltas and define evidence-based tolerances for
   the four USGS cases.
2. Locate source-cleared experimental NaCl and KCl data with explicit property definitions
   and uncertainty.
3. Add CaCl2, MgCl2, Na2SO4, and mixed chloride/sulfate cases.
4. Add seawater-like and carbonate-bearing cases only when pH, alkalinity or total carbon,
   charge balance, and phase assumptions map exactly to the app.
5. Expose only reviewed cases in the UI, with a direct source link beside the comparison.
