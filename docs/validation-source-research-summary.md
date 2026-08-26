# Scientific validation source research summary

**Research date:** 2026-08-26

**Status:** Initial source collection and model reproduction complete; no case is approved
for the public UI yet

**Audience:** Future maintainers, scientific reviewers, and AI coding agents

## Executive summary

The planned validation library is scientifically worthwhile and should remain deliberately
simple for the user:

1. The user selects a reviewed reference case.
2. The app fills the analytical inputs and clearly shows any assumptions.
3. The user presses **Calculate with Pitzer**.
4. The result is compared with the published reference, with a direct source link.

The library must distinguish two evidence classes:

- **Independent reference data** assess agreement with experimental measurements or
  evaluated experimental literature.
- **Implementation benchmarks** assess whether this app reproduces a published Pitzer
  implementation and setup.

An implementation benchmark is useful, but it is not experimental validation. The UI must
never merge these categories under an unexplained “validated” label.

The initial research set contains 16 normalized comparison points:

- four source-cleared USGS implementation benchmarks that have been reproduced with the
  current engine/database pair;
- twelve NaCl and KCl evaluated reference points from Hamer and Wu (1972) that remain
  blocked from public use pending a specific reuse review and a defensible fixed-pH mapping.

All records remain research-only. No comparison tolerance has been approved, and
`release_eligible` is therefore `false` for every case.

## Why source-to-app mapping is not automatic

The calculator currently models a known-pH, closed aqueous solution using analytical totals
on a molality basis. It fixes pressure at 1 atm, suppresses mineral equilibrium and
precipitation, disables redox calculation, enables higher-order electrostatic terms, and uses
the MacInnes single-ion convention.

Consequently, a published value is usable only when its problem definition maps to these
assumptions. Important examples are:

- A binary NaCl-water table normally does not prescribe pH. The app requires one.
- A mineral-solubility calculation is not equivalent to a fixed-composition aqueous
  speciation calculation.
- A source expressed in molarity, mass per volume, or mole fraction cannot be copied into a
  molality input without a documented conversion and, where needed, density data.
- Individual-ion activity coefficients depend on an extrathermodynamic convention. Water
  activity, osmotic coefficient, and neutral-electrolyte mean activity coefficients are more
  suitable comparison properties.
- A successful numerical solution does not prove that the source problem was reproduced.

Any mapping choice introduced by this project must be labeled as an app assumption rather
than attributed to the source.

## Sources evaluated

| Source | Scientific value | Reuse finding | Current decision |
|---|---|---|---|
| [USGS PHRQPITZ report (1988)](https://doi.org/10.3133/wri884153) ([local PDF](references/validation/usgs-phrqpitz-1988.pdf)) | Published Pitzer test problems with inputs and outputs | USGS-authored information is generally in the U.S. public domain; attribution requested | Use selected final aqueous states as implementation benchmarks |
| [Hamer and Wu (1972)](https://doi.org/10.1063/1.3253108) | Evaluated osmotic and mean activity coefficients for uni-univalent electrolytes at 25 degrees C | Exact redistribution status of the journal/reference-data compilation still requires confirmation | Retain selected values as blocked research candidates |
| [NASA/NBS Part XIII (1969)](https://ntrs.nasa.gov/citations/19690029307) ([local manifest](references/validation/README.md#nasanbs-electrochemical-data-part-xiii-1969)) | Evaluated uni-univalent electrolyte tables | NTRS says public use permitted, but the report title page contains an older reproduction restriction | Keep an official link and checksum; do not redistribute the PDF until the conflicting notices are resolved |
| [NSRDS-NBS 24](https://ntrs.nasa.gov/citations/19700013983) ([local PDF](references/validation/nsrds-nbs-24-1968.pdf)) | Theoretical activity-coefficient tables from 0 to 100 degrees C | NTRS marks the report public-use-permitted | Screened out as independent evidence because it is theoretical and charge-type-based, not salt-specific experimental validation |
| [NIST ThermoML Archive](https://trc.nist.gov/ThermoML/Browse) | Promising machine-readable discovery source with property metadata | Rights and suitability must be checked record by record | Continue searching; do not bulk-import without review |

Relevant rights guidance:

- [USGS copyright and attribution FAQ](https://www.usgs.gov/faqs/are-usgs-reportspublications-copyrighted)
- [NIST copyright, fair-use, and licensing distinctions](https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-software-and-technical-series-publications)

Government hosting alone is not sufficient proof of unrestricted redistribution. The rights
statement for the exact work or dataset must be recorded.

The repository source archive and integrity hashes are documented in
[`docs/references/validation/README.md`](references/validation/README.md). The USGS report
and NSRDS-NBS 24 are stored locally. NASA/NBS Part XIII remains externally pinned by its
official URL, file size, and SHA-256 because placing the PDF in a public repository would be
redistribution while its notices remain contradictory.

## Source-cleared USGS benchmarks

The selected records come from test problems 3 and 4 of the 1988 PHRQPITZ report. The
original calculations include mineral-equilibrium paths. The present app cannot reproduce
those paths because it intentionally does not enable solids. Instead, the published **final
aqueous states** are re-entered as fixed-composition cases.

This is an implementation comparison only. It must not be presented as a halite-solubility or
gypsum-anhydrite equilibrium capability of the app.

### Normalized inputs

| Case | Temperature | Known pH | Analytical components, mol/kg H2O |
|---|---:|---:|---|
| Test problem 3 final NaCl-CaSO4 state | 25 degrees C | 6.7203 | Na 5.573737; Cl 5.573737; Ca 0.04801542; S(VI) 0.04801542 |
| Test problem 4 halite-saturated final state | 0 degrees C | 7.0322 | Na 6.093272; Cl 6.093272 |
| Test problem 4 halite-saturated final state | 25 degrees C | 6.5971 | Na 6.099676; Cl 6.099676 |
| Test problem 4 halite-saturated final state | 100 degrees C | 5.6149 | Na 6.624753; Cl 6.624753 |

### Reproduction environment

All four cases were run on 2026-08-26 with:

- PHREEQC engine: `3.8.6-17100-x64`
- database SHA-256:
  `3640e62aee63a118f800b115b46a2760576e63e05e1792022315a28f75dbe9bb`
- database file: `data/databases/pitzer.dat`
- pressure: 1 atm
- MacInnes scaling: enabled
- redox calculation: disabled
- phase equilibrium: disabled

The database is the pinned 2026-01-05 USGS repository file, not the database originally
distributed with the older PHRQPITZ report. Historical/current differences are therefore
expected and must be investigated rather than concealed with a broad tolerance.

### Reference and current results

`Delta` below means current app result minus published reference.

| Case | Property | Reference | Current app | Delta |
|---|---|---:|---:|---:|
| NaCl-CaSO4, 25 degrees C | Water activity | 0.7773 | 0.7773165546 | +0.0000165546 |
|  | Osmotic coefficient | 1.2436 | 1.2436496071 | +0.0000496071 |
|  | Ionic strength, mol/kg H2O | 5.7658 | 5.7657987320 | -0.0000012680 |
|  | Mean gamma NaCl | 0.94228 | 0.9451978378 | +0.0029178378 |
| Saturated NaCl, 0 degrees C | Water activity | 0.7577 | 0.7579162008 | +0.0002162008 |
|  | Osmotic coefficient | 1.2641 | 1.2625356427 | -0.0015643573 |
|  | Ionic strength, mol/kg H2O | 6.0933 | 6.0932720183 | -0.0000279817 |
|  | Mean gamma NaCl | 0.92781 | 0.9136458156 | -0.0141641844 |
| Saturated NaCl, 25 degrees C | Water activity | 0.7546 | 0.7543301465 | -0.0002698535 |
|  | Osmotic coefficient | 1.2813 | 1.2827898765 | +0.0014898765 |
|  | Ionic strength, mol/kg H2O | 6.0997 | 6.0996760620 | -0.0000239380 |
|  | Mean gamma NaCl | 0.99929 | 1.0039294064 | +0.0046394064 |
| Saturated NaCl, 100 degrees C | Water activity | 0.7442 | 0.7438994537 | -0.0003005463 |
|  | Osmotic coefficient | 1.2375 | 1.2394512241 | +0.0019512241 |
|  | Ionic strength, mol/kg H2O | 6.6248 | 6.6247535348 | -0.0000464652 |
|  | Mean gamma NaCl | 0.91012 | 0.9128035504 | +0.0026835504 |

### Interpretation

- Water activity agrees closely in all four cases.
- Osmotic-coefficient differences are small but nonzero.
- Ionic-strength differences are consistent with source rounding.
- The largest observed discrepancy is the NaCl mean coefficient at 0 degrees C:
  `-0.0141641844` in absolute gamma.
- These comparisons show successful reproduction of the overall states, but they do not yet
  justify pass/fail thresholds.
- Likely contributors include database revisions, parameter temperature dependence,
  historical implementation details, source rounding, and the conversion from an equilibrium
  path to a re-entered fixed final state. Each must be checked before assigning tolerances.

## Blocked Hamer-Wu reference candidates

These values are attractive because they are evaluated reference data derived from
experimental literature and cover concentrations useful for the app. They are retained only
in the research dataset and must not yet appear in the public UI.

### NaCl at 25 degrees C — table 16

| Molality, mol/kg H2O | Osmotic coefficient | Mean activity coefficient |
|---:|---:|---:|
| 0.1 | 0.933 | 0.779 |
| 0.5 | 0.921 | 0.681 |
| 1.0 | 0.936 | 0.657 |
| 2.0 | 0.984 | 0.668 |
| 4.0 | 1.116 | 0.783 |
| 6.0 | 1.270 | 0.986 |

### KCl at 25 degrees C — table 28

| Molality, mol/kg H2O | Osmotic coefficient | Mean activity coefficient |
|---:|---:|---:|
| 0.1 | 0.927 | 0.768 |
| 0.5 | 0.900 | 0.649 |
| 1.0 | 0.898 | 0.604 |
| 2.0 | 0.912 | 0.573 |
| 4.0 | 0.965 | 0.576 |
| 4.803 | 0.990 | 0.589 |

The 4.803 mol/kg H2O KCl row is identified by the source as saturation.

Two blockers apply to every value above:

1. Confirm that the selected values may be redistributed in a free public application.
2. Define the app's fixed-pH mapping. The source describes binary electrolyte-water
   solutions without prescribing pH. Silently selecting pH 7 would alter the problem, even
   if a later sensitivity analysis shows the numerical effect is negligible.

## Product and UX conclusions

The lowest-burden credible implementation is a reference-case selector, not an automatic
validation engine. Selecting a case should:

- fill only the normal calculator fields;
- show the source, evidence class, conditions, and app-added assumptions;
- leave calculation under the user's control;
- show reference and calculated values side by side after calculation;
- display absolute and relative differences without declaring pass/fail until an approved
  tolerance exists;
- link directly to the source;
- keep limitations visible but concise.

Recommended labels are **Experimental/evaluated reference** and **Software benchmark**.
Avoid labels such as “certified,” “proven,” or an unqualified “validated.”

## What can and cannot currently be claimed

It is accurate to say:

- the application reproduces selected published PHRQPITZ aqueous-state results closely for
  several reported properties;
- the exact engine version and database checksum are recorded;
- discrepancies are preserved and awaiting scientific review;
- a source-review and release-gate process exists.

It is not yet accurate to say:

- the calculator has been independently validated against experimental data;
- the full 0-100 degrees C range is validated;
- a universal concentration or ionic-strength limit has been established;
- the selected USGS cases prove mineral-equilibrium capability;
- every value hosted by NIST or NASA is automatically free to redistribute;
- the current differences pass an accepted scientific tolerance.

## Required release gate

Before any case is loaded by the UI, record all of the following:

- full citation and stable URL;
- exact table, page, figure, or data-record identifier;
- explicit reuse status appropriate for a free public app;
- property definition and concentration basis;
- temperature, pressure, and full analytical composition;
- exact source-to-app mapping;
- all app-added pH, redox, charge-balance, and phase assumptions;
- independently checked transcription;
- current PHREEQC engine version and database checksum;
- reproduced outputs and deltas;
- evidence-based tolerances;
- evidence-class label and concise user warning.

Until every gate is complete, keep `release_eligible: false` and do not make the runtime load
the record.

## Recommended next work

1. Explain the USGS historical/current deltas, especially the 0 degrees C NaCl mean
   coefficient.
2. Decide whether to align the engine and database to one named PHREEQC release or retain
   the current pairing with explicit regression evidence.
3. Obtain a clear redistribution determination for the selected Hamer-Wu values.
4. Quantify the effect of the app-required pH convention on binary NaCl and KCl cases.
5. Find source-cleared experimental data with uncertainties for NaCl and KCl.
6. Extend collection to CaCl2, MgCl2, Na2SO4, and mixed chloride/sulfate solutions.
7. Add seawater-like and carbonate-bearing cases only after the pH, alkalinity or total
   inorganic carbon, charge-balance, and phase mappings are exact.
8. Have the final classifications and tolerances reviewed by a qualified electrolyte-
   thermodynamics or geochemistry specialist.
9. Only then connect approved records to the Streamlit case selector and comparison view.

## Repository records

- Source metadata and rights review:
  `data/examples/research/validation_sources.json`
- Normalized inputs, reference values, reproduction outputs, and deltas:
  `data/examples/research/validation_library_seed.json`
- Collection and release rules: `docs/validation-data-collection.md`
- Broader validation plan: `docs/validation-plan.md`
- Calculation assumptions: `docs/scientific-method.md`
- Database identity and parameter audit: `docs/pitzer-database-audit.md`
- Archived source PDFs and external-source manifest:
  `docs/references/validation/README.md`

The JSON files are the machine-readable source of record. This document explains their
scientific meaning and must be updated when a source decision, mapping assumption,
reproduction result, or release status changes.
