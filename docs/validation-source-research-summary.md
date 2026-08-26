# Scientific validation source research summary

**Research date:** 2026-08-26

**Status:** Initial source collection, USGS reproduction, monovalent/divalent chloride
reference tranches, and the first binary sulfate tranche are complete; no case is connected
to the public UI yet

**Audience:** Future maintainers, scientific reviewers, and AI coding agents

## Executive summary

The planned validation library is scientifically worthwhile and should remain deliberately
simple for the user:

1. The user selects a reviewed reference case.
2. The app fills the analytical inputs and clearly shows any assumptions.
3. The user presses **Calculate with Pitzer**.
4. The normal results appear unchanged. Published values and the direct source link remain
   available in the expandable reference-case section if the user wants to consult them.

Version 1 does not need a comparison screen, calculated differences, tolerances, or pass/fail
judgments.

The library must distinguish two evidence classes:

- **Independent reference data** assess agreement with experimental measurements or
  evaluated experimental literature.
- **Implementation benchmarks** assess whether this app reproduces a published Pitzer
  implementation and setup.

An implementation benchmark is useful, but it is not experimental validation. The UI must
never merge these categories under an unexplained “validated” label.

The current source holdings contain 42 normalized reference cases:

- four source-cleared USGS implementation benchmarks that have been reproduced with the
  current engine/database pair;
- sixteen source-cleared NaCl/KCl evaluated-reference cases transcribed from the NIST
  ThermoML Partanen (2016) record;
- eight source-cleared CaCl2/MgCl2 experimental or evaluated-reference cases transcribed
  from two NIST ThermoML records;
- two source-cleared Na2SO4 inputs retaining four direct osmotic-coefficient measurements
  from a NIST ThermoML binary-water dataset;
- twelve NaCl and KCl evaluated reference points from Hamer and Wu (1972) that remain
  blocked from public use pending a specific reuse review and a defensible fixed-pH mapping.

The 30 source-cleared records are loaded by the Streamlit reference-case selector. The
twelve Hamer-Wu candidates remain research-only and are not available to the runtime.

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
| [Partanen NaCl/KCl ThermoML record (2016)](https://trc.nist.gov/ThermoML/10.1021/acs.jced.5b00544.html) ([local JSON](references/validation/nist-thermoml-partanen-2016-nacl-kcl.json)) | 95 evaluated mean ionic activity coefficients over temperature and molality, with compiler-estimated uncertainty | ThermoML metadata identifies the NIST open-data license; attribution and the originating citation are retained | Release a compact 16-case subset with explicit pH and pressure mapping assumptions |
| [Partanen CaCl2 ThermoML record (2012)](https://trc.nist.gov/ThermoML/10.1021/je300852v.html) ([local JSON](references/validation/nist-thermoml-partanen-2012-cacl2.json)) | 20 traceable evaluated CaCl2 mean coefficients at 25 degrees C up to 3 mol/kg | ThermoML metadata identifies the NIST open-data license | Release four range-spanning binary cases with exact 1:2 Ca/Cl mapping |
| [Rouhi and Bagherinia MgCl2 ThermoML record (2015)](https://trc.nist.gov/ThermoML/10.1016/j.jct.2015.07.049.html) ([local JSON](references/validation/nist-thermoml-rouhi-bagherinia-2015-mgcl2.json)) | 15 pure-water MgCl2 mean coefficients calculated from EMF measurements, plus a separate glucose-containing dataset | ThermoML metadata identifies the NIST open-data license | Release four exact points from the pure-water subset only; exclude glucose mixtures |
| [Held et al. Na2SO4 ThermoML record (2014)](https://trc.nist.gov/ThermoML/10.1016/j.jct.2013.08.018.html) ([local JSON](references/validation/nist-thermoml-held-2014-na2so4.json)) | Four measured osmotic coefficients for binary Na2SO4-water, representing two observations at each of two molalities | ThermoML metadata identifies the NIST open-data license | Release two binary inputs, preserve all four observations without averaging, and exclude amino-acid mixtures |

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
expected and are retained as internal scientific findings rather than public UI behavior.

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
- These comparisons show successful reproduction of the overall states. The public library
  will not turn this observation into a pass/fail judgment.
- Likely contributors include database revisions, parameter temperature dependence,
  historical implementation details, source rounding, and the conversion from an equilibrium
  path to a re-entered fixed final state. These are internal scientific questions and do not
  require a user-facing comparison feature.

## Source-cleared NIST ThermoML NaCl/KCl references

The Partanen (2016) ThermoML record supplies independent evaluated reference values derived
from experimental literature. It contains 32 KCl and 63 NaCl mean ionic activity
coefficients. A compact subset was selected for the public-data shape:

| Electrolyte | Molality, mol/kg H2O | Temperatures |
|---|---:|---|
| KCl | 0.1 and 0.5 | 0, 20, 50, and 70 degrees C |
| NaCl | 0.1 and 0.5 | 0, 20, 50, and 70 degrees C |

This produces 16 cases. Every value is checked automatically against the archived official
ThermoML JSON. The record reports a compiler-estimated combined expanded uncertainty of
`0.05` at 95% confidence for each selected mean coefficient; this value is retained as
source metadata and must not be interpreted as a project-defined acceptance tolerance.

The source conditions are binary salt-water solutions at 101 kPa. No pH is prescribed.
The current app requires a fixed pH and pressure of 1 atm, so each released record clearly
states that pH 7.0 and 1 atm are app-side mapping conventions. Only the mean ionic activity
coefficient and its reported uncertainty are reference outputs. Water activity, osmotic
coefficient, ionic strength, and species-level outputs calculated by the app are not source
values for these records.

On 2026-08-26, all 16 mapped inputs were run successfully with the pinned engine/database.
An internal pH sensitivity check recalculated every case at pH 6, 7, and 8. The maximum
absolute change in the target mean coefficient relative to pH 7 was `7.25e-6`, occurring
for 0.1 mol/kg NaCl at 70 degrees C. This supports the convention for the selected grid but
does not convert pH 7 into a source condition or establish a general tolerance.

The archived ThermoML metadata points to the NIST open-data license. The project retains
the official record unchanged, acknowledges NIST/TRC, and cites the originating journal
article. This release finding applies to this record; it is not a blanket approval for every
ThermoML candidate.

## Source-cleared NIST ThermoML CaCl2/MgCl2 references

The second independent tranche extends the library from 1:1 electrolytes to 2:1
electrolytes at 25 degrees C:

| Electrolyte | Selected source molalities, mol/kg H2O | Source property |
|---|---|---|
| CaCl2 | 0.1, 0.5, 1.0, and 3.0 | Traceable evaluated mean ionic activity coefficient |
| MgCl2 | 0.0833, 0.3333, 1.0, and 2.0 | Mean ionic activity coefficient calculated from EMF measurements |

The CaCl2 record contains 20 binary points from 0.01 to 3.0 mol/kg. Four values were chosen
to span the range and include the upper source molality. Its reported compiler-estimated 95%
expanded uncertainty is `0.001` for every selected point.

The MgCl2 record contains a 75-point glucose/water dataset and a separate 15-point
MgCl2-water dataset. Only the pure-water dataset is compatible with the current app. The
selected molalities are exact source values; 0.0833 and 0.3333 mol/kg are retained instead
of silently substituting or interpolating 0.1 and 0.5 mol/kg. The reported 95% expanded
uncertainty varies with concentration and is stored for each case.

Every source molality is mapped stoichiometrically as `Ca = m, Cl = 2m` or
`Mg = m, Cl = 2m`. The sources do not prescribe pH, so pH 7.0 remains an app-side
convention. CaCl2 source pressure is 101 kPa; MgCl2 source pressure is 101.325 kPa, exactly
1 atm. The app uses 1 atm for both.

All eight inputs ran through the pinned native engine. An internal pH sensitivity check at
pH 6, 7, and 8 found maximum absolute changes relative to pH 7 of `4.81e-5` for CaCl2 and
`2.86e-4` for MgCl2. This supports the selected mapping but is not a source condition,
tolerance, or general statement for lower concentrations or other chemical systems.

Unit tests directly compare every released value and uncertainty with the archived official
ThermoML JSON files. The source files and their integrity hashes are recorded in
`docs/references/validation/README.md`.

## Source-cleared NIST ThermoML Na2SO4 reference

The third independent tranche validates a different property and ion type: directly
measured osmotic coefficients for binary Na2SO4-water at 25 degrees C. Only ThermoML
pure-or-mixture dataset 81 from Held et al. (2014) is used. The publication's amino-acid
mixtures and other salts are excluded.

The dataset has four measurements but only two unique compositions:

| Na2SO4 molality, mol/kg H2O | Source osmotic coefficients | Source U95 values |
|---:|---|---|
| 0.5 | 0.717 and 0.690 | 0.014 and 0.015 |
| 1.0 | 0.658 and 0.642 | 0.016 and 0.016 |

The library therefore adds two selectable cases and retains both observations at each
composition. It does not average the measurements or present either one as preferred.
Each molality maps as `Na = 2m` and `SO4 = m`. The source conditions are 298.15 K and
101 kPa; pH is not prescribed. The app uses 25 degrees C, 1 atm, and pH 7.0, with pressure
and pH explicitly identified as app-side conventions.

Both inputs ran through the pinned native engine. A pH 6-8 sensitivity check found a
maximum absolute change of `2.74e-6` in osmotic coefficient relative to pH 7. The dated
side-by-side comparison reports a mean absolute relative difference of `1.7926%` across
the four source observations and a largest absolute relative difference of `4.2425%`.
Three of the four numerical differences are smaller than their source-reported expanded
uncertainties. These are observations, not project-defined tolerances or pass/fail results.

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

The implemented public workflow is a reference-case selector, not an automatic validation
engine. Selecting a case:

- fills only the normal calculator fields;
- leaves calculation under the user's control;
- leaves the existing results interface unchanged;
- provides a collapsed **Load a published reference case (optional)** section containing the
  evidence class and conditions, with published source details and app-added assumptions
  available through separate closed-by-default controls;
- links directly to the source.

The app should not calculate differences, show a side-by-side comparison table, assign
tolerances, or declare pass/fail. The user decides whether and how to consult the reference
values.

Recommended labels are **Experimental/evaluated reference** and **Software benchmark**.
Avoid labels such as “certified,” “proven,” or an unqualified “validated.”

## What can and cannot currently be claimed

It is accurate to say:

- the application reproduces selected published PHRQPITZ aqueous-state results closely for
  several reported properties;
- the exact engine version and database checksum are recorded;
- discrepancies are preserved and awaiting scientific review;
- a source-review and release-gate process exists.
- selected NaCl, KCl, CaCl2, MgCl2, and Na2SO4 properties have been independently compared
  with NIST ThermoML experimental or evaluated-reference data within explicitly documented
  conditions.

It is not accurate to say:

- the calculator is independently validated across its full component, property,
  concentration, and temperature range;
- the full 0-100 degrees C range is validated;
- a universal concentration or ionic-strength limit has been established;
- the selected USGS cases prove mineral-equilibrium capability;
- every value hosted by NIST or NASA is automatically free to redistribute;
- the current historical/current-model differences have a single confirmed cause.

## Required release gate

The 30 production cases satisfy these gates. The same checks remain mandatory before any
additional record is moved from research into the UI-loaded production library.

Before any case is loaded by the UI, record all of the following:

- full citation and stable URL;
- exact table, page, figure, or data-record identifier;
- explicit reuse status appropriate for a free public app;
- property definition and concentration basis;
- temperature, pressure, and full analytical composition;
- exact source-to-app mapping;
- all app-added pH, redox, charge-balance, and phase assumptions;
- independently checked transcription;
- a successful internal smoke calculation with the pinned engine/database pair;
- evidence-class label and concise user warning.

Internal scientific records may retain engine version, database checksum, and reproduction
notes. Those fields do not belong in the public case file or user interface.

Until every gate is complete, keep a candidate in the research library and do not make the
runtime load the record.

## Recommended next work

1. Explain the USGS historical/current deltas, especially the 0 degrees C NaCl mean
   coefficient.
2. Decide whether to align the engine and database to one named PHREEQC release or retain
   the current pairing with explicit regression evidence.
3. Retain the documented pH sensitivity evidence and repeat it if lower concentrations or
   different acid-base components are selected.
4. Decide whether the blocked Hamer-Wu concentration extension adds enough value to justify
   a separate redistribution determination.
5. Locate a clean fixed-composition mixed chloride/sulfate record without solids or
   saturation, now that the binary Na2SO4 mapping is established.
6. Investigate the systematic negative CaCl2/MgCl2 differences as internal scientific work,
   especially the three CaCl2 points outside the narrow source-reported uncertainty.
7. Add seawater-like and carbonate-bearing cases only after the pH, alkalinity or total
   inorganic carbon, charge-balance, and phase mappings are exact.
8. Have the final classifications and source-to-app mappings reviewed by a qualified
   electrolyte-thermodynamics or geochemistry specialist.
9. Maintain automated loader, prefill, and source-display tests as the public library grows.

## Repository records

- First dated implementation-validation result:
  `docs/initial-validation-usgs-phrqpitz-2026-08-26.md`
- First dated independent evaluated-reference validation result:
  `docs/initial-independent-validation-nist-thermoml-2026-08-26.md`
- First dated divalent-chloride independent-validation result:
  `docs/independent-validation-nist-thermoml-divalent-chlorides-2026-08-26.md`
- First dated sulfate osmotic-coefficient independent-validation result:
  `docs/independent-validation-nist-thermoml-na2so4-osmotic-2026-08-26.md`
- Production source cases loaded by Streamlit:
  `data/examples/validation_library.json`
- Source metadata and rights review:
  `data/examples/research/validation_sources.json`
- Normalized inputs, reference values, and internal reproduction notes:
  `data/examples/research/validation_library_seed.json`
- Collection and release rules: `docs/validation-data-collection.md`
- Broader validation plan: `docs/validation-plan.md`
- Calculation assumptions: `docs/scientific-method.md`
- Database identity and parameter audit: `docs/pitzer-database-audit.md`
- Archived source files and external-source manifest:
  `docs/references/validation/README.md`

The JSON files are the machine-readable source of record. This document explains their
scientific meaning and must be updated when a source decision, mapping assumption,
reproduction result, or release status changes.
