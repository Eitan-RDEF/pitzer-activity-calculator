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

The first production-shaped records are stored in
`data/examples/validation_library.json`. They contain four USGS software benchmarks and 26
NIST ThermoML experimental/evaluated-reference cases. They are not connected to the
Streamlit UI yet.

Their first side-by-side implementation-validation result is recorded in
`docs/initial-validation-usgs-phrqpitz-2026-08-26.md`.

The first side-by-side independent evaluated-reference comparison is recorded in
`docs/initial-independent-validation-nist-thermoml-2026-08-26.md`.

The first divalent-chloride independent-reference comparison is recorded in
`docs/independent-validation-nist-thermoml-divalent-chlorides-2026-08-26.md`.

The first independent sulfate osmotic-coefficient comparison is recorded in
`docs/independent-validation-nist-thermoml-na2so4-osmotic-2026-08-26.md`.

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

If a source reports repeated observations at an identical input, preserve those observations
as a source-value list with their individual uncertainties. Do not create misleading duplicate
mixtures, silently average the observations, or select a preferred value unless the source
itself defines that treatment.

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
- sixteen NIST ThermoML evaluated-reference cases: NaCl and KCl at 0.1 and 0.5 mol/kg,
  each at 0, 20, 50, and 70 degrees C;
- eight NIST ThermoML divalent-chloride cases at 25 degrees C: CaCl2 at 0.1, 0.5, 1.0,
  and 3.0 mol/kg, plus MgCl2 at the exact source molalities 0.0833, 0.3333, 1.0, and
  2.0 mol/kg;
- two NIST ThermoML binary Na2SO4 inputs at 0.5 and 1.0 mol/kg and 25 degrees C, each
  retaining two direct osmotic-coefficient measurements from the source rather than an
  invented average;
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

The Partanen (2016) ThermoML record resolves the immediate need for a source-cleared,
machine-readable independent tranche. Its two datasets contain 32 KCl and 63 NaCl mean
ionic activity coefficients. The released subset deliberately uses only 16 points so the
future selector remains manageable. Each selected value retains the compiler-estimated 95%
expanded uncertainty of `0.05` reported in ThermoML. The source specifies 101 kPa and no
pH; the app mapping uses 1 atm and pH 7.0 and labels both as project assumptions. Only the
mean coefficient and its reported uncertainty are reference outputs for these cases.

An internal sensitivity check on 2026-08-26 recalculated all 16 cases at pH 6, 7, and 8.
The largest absolute change in the target mean coefficient relative to pH 7 was
`7.25e-6`. This supports pH 7 as a numerically low-impact mapping convention for this
selected 0.1-0.5 mol/kg grid. It is not a source condition, comparison tolerance, or general
claim for lower-concentration solutions.

The archived JSON is retained byte-for-byte under `docs/references/validation/`, and a unit
test verifies every released value directly against it. The ThermoML dataset metadata points
to the NIST open-data license, so reuse requires acknowledgment of NIST/TRC and citation of
the originating publication.

The CaCl2 tranche uses the Partanen (2012) binary record, which contains 20 traceable mean
coefficients at 25 degrees C from 0.01 to 3.0 mol/kg. Four values span that range, including
the upper source molality. The MgCl2 tranche uses only the 15-point pure-water subset of the
Rouhi and Bagherinia (2015) record; the glucose-containing dataset is deliberately excluded.
Its exact available molalities are preserved rather than interpolated. Every MCl2 input maps
the source molality as cation = m and chloride = 2m.

All eight inputs ran successfully through the pinned native engine. Recalculation at pH 6,
7, and 8 produced maximum absolute changes relative to pH 7 of `4.81e-5` for CaCl2 and
`2.86e-4` for MgCl2. These values support pH 7 as a low-impact mapping convention for the
selected cases, but they are not source conditions or acceptance tolerances.

The Held et al. (2014) ThermoML record contains many amino-acid/electrolyte systems, but
only pure-or-mixture dataset 81 is a binary Na2SO4-water system compatible with the app.
It contains four observations but only two unique input compositions: two measurements at
0.5 mol/kg and two at 1.0 mol/kg. The public library therefore adds two selectable cases
and preserves both measurements and their compiler-estimated 95% expanded uncertainties
inside each case. It does not average the replicate observations.

The source molality maps as `Na = 2m` and `SO4 = m`. Source temperature is 298.15 K and
source pressure is 101 kPa; the app uses 25 degrees C and 1 atm. The source does not
prescribe pH, so pH 7 remains an explicit app mapping convention. A pH 6-8 sensitivity
check produced a largest absolute change of `2.74e-6` in osmotic coefficient relative to
pH 7. Both inputs ran successfully through the pinned native engine.

The NASA/NBS Part XIII report was reviewed but its salts require analytical components not
currently exposed by the app. The NTRS catalog marks it public-use-permitted, while the
report itself carries an older reproduction restriction; it is therefore not a release source
until that conflict is resolved.

NSRDS-NBS 24 was screened out as independent evidence because it tabulates theoretical
charge-type equations rather than salt-specific experimental values. Additional NIST
ThermoML candidates still require the same record-by-record scientific and rights review
applied to the Partanen record.

## Next collection priority

1. Investigate the historical/current-model differences as internal scientific work; do not
   turn them into a public pass/fail feature.
2. Retain pH 7 as an explicit app-side convention for the released binary NaCl/KCl grid;
   repeat the sensitivity check if lower concentrations are selected later.
3. Locate a clean, fixed-composition mixed chloride/sulfate record without solids or
   saturation after establishing the binary Na2SO4 mapping.
4. Extend binary sulfate coverage to another supported salt only when its analytical
   components, property definition, and no-solids assumptions map exactly to the app.
5. Add seawater-like and carbonate-bearing cases only when pH, alkalinity or total carbon,
   charge balance, and phase assumptions map exactly to the app.
6. Expose only reviewed cases in the selector, with their source values and link in a compact
   **Reference data** expander.
