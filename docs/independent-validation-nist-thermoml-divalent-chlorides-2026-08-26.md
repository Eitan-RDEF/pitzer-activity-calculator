# Independent validation against NIST ThermoML divalent-chloride references

**Validation date:** 2026-08-26

**Result:** Across eight CaCl2 and MgCl2 cases at 25 degrees C, the current app's mean
activity coefficients have an overall mean absolute relative difference of `1.1549%` from
the published reference values. The largest relative difference is `1.9942%`.

**Evidence class:** Independent evaluated or experimental-derived reference data

**Important boundary:** This comparison covers only the mean ionic activity coefficients of
CaCl2 and MgCl2 at the eight selected molalities. It does not validate every app output,
component, mixture, concentration, or temperature.

## Sources

### CaCl2

Partanen, J. I. (2012), *Traceable Mean Activity Coefficients and Osmotic Coefficients in
Aqueous Calcium Chloride Solutions at 25 degrees C up to a Molality of 3.0 mol/kg*, Journal
of Chemical & Engineering Data, 57(11), 3247-3257.

- DOI: <https://doi.org/10.1021/je300852v>
- NIST ThermoML record: <https://trc.nist.gov/ThermoML/10.1021/je300852v.html>
- Archived source:
  [`nist-thermoml-partanen-2012-cacl2.json`](references/validation/nist-thermoml-partanen-2012-cacl2.json)

The machine-readable record contains 20 binary CaCl2-water mean ionic activity
coefficients from 0.01 to 3.0 mol/kg H2O at 25 degrees C. The values use a two-term
Debye-Huckel representation of traceable experimental literature. Four points were selected
to span the range and include its upper molality.

### MgCl2

Rouhi, A., and Bagherinia, M. A. (2015), *Mean activity coefficient measurement and
thermodynamic modelling of the ternary mixed electrolyte (MgCl2 + glucose + water) system
at T = 298.15 K*, Journal of Chemical Thermodynamics, 91, 286-291.

- DOI: <https://doi.org/10.1016/j.jct.2015.07.049>
- NIST ThermoML record:
  <https://trc.nist.gov/ThermoML/10.1016/j.jct.2015.07.049.html>
- Archived source:
  [`nist-thermoml-rouhi-bagherinia-2015-mgcl2.json`](references/validation/nist-thermoml-rouhi-bagherinia-2015-mgcl2.json)

The record contains a glucose/water dataset and a separate 15-point binary MgCl2-water
dataset. This validation uses only the pure-water subset. Its mean coefficients were
calculated from EMF cell-potential measurements. The selected molalities are exact source
values and were not interpolated to rounder concentrations.

### Shared repository records

- Validation library:
  [`data/examples/validation_library.json`](../data/examples/validation_library.json)
- Source archive and integrity hashes:
  [`docs/references/validation/README.md`](references/validation/README.md)
- Reuse statement: [NIST open-data license](https://www.nist.gov/open/license)

Every selected source value and reported uncertainty is checked against the archived
official JSON by `tests/unit/test_validation_library.py`.

## Current calculation environment

| Item | Value |
|---|---|
| PHREEQC engine | `3.8.6-17100-x64` |
| Database | `data/databases/pitzer.dat` |
| Database SHA-256 | `3640e62aee63a118f800b115b46a2760576e63e05e1792022315a28f75dbe9bb` |
| App pressure | 1 atm |
| CaCl2 source pressure | 101 kPa |
| MgCl2 source pressure | 101.325 kPa, equivalent to 1 atm |
| Composition basis | mol/kg H2O |
| App pH | 7.0, fixed on the hydrogen-ion activity basis |
| Source pH | Not prescribed for the binary salt-water systems |
| Activity model | Pitzer |
| MacInnes convention | Enabled for individual-ion values |
| Higher-order electrostatic terms | Enabled |
| Redox calculation | Disabled |
| Mineral equilibrium and precipitation | Disabled |

The neutral-electrolyte mean coefficient is independent of the individual-ion MacInnes
scaling convention. The source-to-app pH and CaCl2 pressure mappings are explicit project
assumptions, not conditions stated by the sources.

## Inputs

Each MCl2 source molality `m` maps to a charge-balanced analytical input:

- divalent cation: `M = m`;
- chloride: `Cl = 2m`.

| Electrolyte | Source molality, mol/kg H2O | App analytical components, mol/kg H2O |
|---|---:|---|
| CaCl2 | 0.1 | Ca 0.1; Cl 0.2 |
| CaCl2 | 0.5 | Ca 0.5; Cl 1.0 |
| CaCl2 | 1.0 | Ca 1.0; Cl 2.0 |
| CaCl2 | 3.0 | Ca 3.0; Cl 6.0 |
| MgCl2 | 0.0833 | Mg 0.0833; Cl 0.1666 |
| MgCl2 | 0.3333 | Mg 0.3333; Cl 0.6666 |
| MgCl2 | 1.0 | Mg 1.0; Cl 2.0 |
| MgCl2 | 2.0 | Mg 2.0; Cl 4.0 |

## pH mapping sensitivity

Because the app requires a known pH while the sources do not prescribe one, every selected
case was recalculated at pH 6, 7, and 8.

| Electrolyte | Largest absolute change relative to pH 7 | Case |
|---|---:|---|
| CaCl2 | `4.81e-5` | 3.0 mol/kg H2O |
| MgCl2 | `2.86e-4` | 2.0 mol/kg H2O |

These sensitivities are much smaller than the source-to-app differences reported below.
They support pH 7 as a numerically low-impact convention for these selected cases, but they
are not source conditions, comparison tolerances, or general results for other systems.

## Comparison method

For each case:

`absolute difference = current app - source`

`relative difference (%) = 100 x (current app - source) / source`

The mean absolute relative difference is the arithmetic mean of the absolute values of the
relative differences. Source `U95` values are compiler-estimated combined expanded
uncertainties at 95% confidence stored in the ThermoML records.

The uncertainty is displayed as source metadata. It is not a project-defined acceptance
tolerance, and this document does not assign pass/fail status.

## Side-by-side results

### CaCl2 mean activity coefficient

| Molality, mol/kg H2O | Source gamma | Source U95 | Current app gamma | Absolute difference | Relative difference |
|---:|---:|---:|---:|---:|---:|
| 0.1 | 0.517000 | 0.001000 | 0.516083594 | -0.000916406 | -0.1773% |
| 0.5 | 0.449000 | 0.001000 | 0.445346297 | -0.003653703 | -0.8137% |
| 1.0 | 0.502000 | 0.001000 | 0.498579577 | -0.003420423 | -0.6814% |
| 3.0 | 1.490000 | 0.001000 | 1.477483433 | -0.012516567 | -0.8400% |

CaCl2 has a mean absolute relative difference of `0.6281%`. The 0.1 mol/kg result is
numerically inside the source-reported `U95 = 0.001`; the differences at 0.5, 1.0, and
3.0 mol/kg are larger than that particularly narrow uncertainty.

### MgCl2 mean activity coefficient

| Molality, mol/kg H2O | Source gamma | Source U95 | Current app gamma | Absolute difference | Relative difference |
|---:|---:|---:|---:|---:|---:|
| 0.0833 | 0.548500 | 0.029500 | 0.540406712 | -0.008093288 | -1.4755% |
| 0.3333 | 0.479600 | 0.029700 | 0.470665686 | -0.008934314 | -1.8629% |
| 1.0 | 0.577600 | 0.033300 | 0.566081537 | -0.011518463 | -1.9942% |
| 2.0 | 1.069500 | 0.085100 | 1.054589903 | -0.014910097 | -1.3941% |

MgCl2 has a mean absolute relative difference of `1.6817%`. All four absolute differences
are smaller than their source-reported expanded uncertainties.

## Aggregate findings

| Finding | Value |
|---|---:|
| Number of cases | 8 |
| Overall mean absolute relative difference | 1.1549% |
| CaCl2 mean absolute relative difference | 0.6281% |
| MgCl2 mean absolute relative difference | 1.6817% |
| Largest absolute difference | -0.014910097 |
| Case with largest absolute difference | MgCl2, 2.0 mol/kg H2O |
| Largest relative difference | -1.9942% |
| Case with largest relative difference | MgCl2, 1.0 mol/kg H2O |
| Differences smaller than source U95 | 5 of 8 |

The current app is below the reference value in all eight cases. This consistent sign is a
scientific observation worth retaining for future database and parameter reviews.

The comparison has two different uncertainty contexts:

- CaCl2 has small percentage differences, but its reported `U95 = 0.001` is unusually
  narrow; three of four differences are larger than it.
- MgCl2 has larger percentage differences, but all four remain smaller than the broader
  source-reported uncertainties.

Because no project acceptance tolerance has been established, neither observation is
converted into a pass/fail label.

## Interpretation

The pH sensitivity is too small to explain the observed differences. Possible contributors
include differences between the current `pitzer.dat` parameterization and the equations or
experimental interpretation used by the sources, source rounding, and the small CaCl2
pressure mapping difference. For MgCl2, the uncertainty attached to EMF-derived values is
also substantially larger than for the evaluated CaCl2 record.

This comparison does not establish a single confirmed cause for the systematic negative
difference. The result should be revisited if the database or engine is updated.

## What this validation supports

It is accurate to say that, for the selected 25 degrees C cases:

- the app's CaCl2 mean coefficients differ from the traceable evaluated references by less
  than `0.85%`;
- the app's MgCl2 mean coefficients differ from the EMF-derived references by less than
  `2.0%`;
- all MgCl2 differences and one CaCl2 difference are smaller than their source-reported
  expanded uncertainties;
- the remaining three CaCl2 differences are small in percentage terms but larger than the
  source's narrow reported uncertainty.

It is not accurate to infer that:

- every CaCl2 or MgCl2 point in the sources has been checked;
- water activity or osmotic coefficient has been independently compared here;
- the source uncertainty is an approved project tolerance;
- Na2SO4, carbonate systems, or multicomponent brines are validated;
- the full 0-100 degrees C app range is validated for divalent chlorides;
- every result produced by the calculator is independently validated.

## Reproducibility and maintenance

The validation-library tests enforce that:

- all eight source values and uncertainties exactly match the archived ThermoML JSON;
- every input preserves exact source molality and 1:2 cation/chloride stoichiometry;
- every mapped case uses supported components and conditions;
- every case runs through the native PHREEQC engine;
- the calculated result contains the requested CaCl2 or MgCl2 mean coefficient.

At the time of this report:

- `44` unit tests passed;
- `35` native integration tests passed;
- Ruff, JSON parsing, and repository diff checks passed.

This is a dated scientific-validation snapshot. Recalculate and update it if the engine,
database, source record, mapping convention, or mean-coefficient implementation changes.
