# Initial independent validation against NIST ThermoML NaCl/KCl references

**Validation date:** 2026-08-26

**Result:** Across 16 dilute NaCl and KCl reference cases from 0 to 70 degrees C, the
current app's mean activity coefficients have a mean absolute relative difference of
`0.2997%` from the published evaluated values. The largest relative difference is `1.1413%`.

**Evidence class:** Independent evaluated reference data derived from experimental
literature

**Important boundary:** This comparison covers only the mean ionic activity coefficients of
NaCl and KCl at 0.1 and 0.5 mol/kg H2O. It is not a validation of every app output,
component, mixture, concentration, or temperature.

## Source

Partanen, J. I. (2016), *Mean Activity Coefficients and Osmotic Coefficients in Dilute
Aqueous Sodium or Potassium Chloride Solutions at Temperatures from (0 to 70) degrees C*,
Journal of Chemical & Engineering Data, 61(1), 286-306.

- DOI: <https://doi.org/10.1021/acs.jced.5b00544>
- NIST ThermoML record:
  <https://trc.nist.gov/ThermoML/10.1021/acs.jced.5b00544.html>
- Archived machine-readable source:
  [`nist-thermoml-partanen-2016-nacl-kcl.json`](references/validation/nist-thermoml-partanen-2016-nacl-kcl.json)
- Library records:
  [`data/examples/validation_library.json`](../data/examples/validation_library.json)
- Reuse statement: [NIST open-data license](https://www.nist.gov/open/license)

The ThermoML record contains 32 KCl and 63 NaCl mean ionic activity coefficients. The
values are evaluated values based on experimental literature and fitted electrolyte
equations; they are not direct measurements at every tabulated temperature and molality.

The validation library selects a compact 16-case grid:

| Electrolyte | Molality, mol/kg H2O | Temperatures |
|---|---:|---|
| NaCl | 0.1 and 0.5 | 0, 20, 50, and 70 degrees C |
| KCl | 0.1 and 0.5 | 0, 20, 50, and 70 degrees C |

Every selected source value and uncertainty is checked against the archived official JSON
by `tests/unit/test_validation_library.py`.

## Current calculation environment

| Item | Value |
|---|---|
| PHREEQC engine | `3.8.6-17100-x64` |
| Database | `data/databases/pitzer.dat` |
| Database SHA-256 | `3640e62aee63a118f800b115b46a2760576e63e05e1792022315a28f75dbe9bb` |
| App pressure | 1 atm |
| Source pressure | 101 kPa |
| Composition basis | mol/kg H2O |
| App pH | 7.0, fixed on the hydrogen-ion activity basis |
| Source pH | Not prescribed for the binary salt-water systems |
| Activity model | Pitzer |
| MacInnes convention | Enabled for individual-ion values |
| Higher-order electrostatic terms | Enabled |
| Redox calculation | Disabled |
| Mineral equilibrium and precipitation | Disabled |

The neutral-electrolyte mean coefficient is independent of the individual-ion MacInnes
scaling convention. The pressure and pH differences are source-to-app mapping assumptions,
not conditions stated by the source.

## pH mapping sensitivity

Because the app requires a known pH while the source does not prescribe one, every selected
case was recalculated at pH 6, 7, and 8. The largest absolute change in the target mean
coefficient relative to pH 7 was `7.25e-6`, for 0.1 mol/kg NaCl at 70 degrees C.

This result supports pH 7 as a numerically low-impact convention for this selected
0.1-0.5 mol/kg grid. It is not a source condition, a comparison tolerance, or evidence that
pH is negligible for lower-concentration or acid-base-active systems.

## Comparison method

For each case:

`absolute difference = current app - source`

`relative difference (%) = 100 x (current app - source) / source`

The mean absolute relative difference is the arithmetic mean of the absolute values of the
16 relative differences.

The ThermoML record reports a compiler-estimated combined expanded uncertainty of `0.05`
at 95% confidence for every selected mean coefficient. It is reproduced below as source
metadata. It is not a project-defined acceptance tolerance, and this document does not assign
pass/fail status.

## Side-by-side results

### NaCl mean activity coefficient

| Temperature, degrees C | Molality, mol/kg H2O | Source gamma | Source U95 | Current app gamma | Absolute difference | Relative difference |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.1 | 0.781300 | 0.050000 | 0.779602804 | -0.001697196 | -0.2172% |
| 0 | 0.5 | 0.672000 | 0.050000 | 0.671796654 | -0.000203346 | -0.0303% |
| 20 | 0.1 | 0.779300 | 0.050000 | 0.778555392 | -0.000744608 | -0.0955% |
| 20 | 0.5 | 0.680800 | 0.050000 | 0.680725168 | -0.000074832 | -0.0110% |
| 50 | 0.1 | 0.770000 | 0.050000 | 0.770493528 | +0.000493528 | +0.0641% |
| 50 | 0.5 | 0.674000 | 0.050000 | 0.676582350 | +0.002582350 | +0.3831% |
| 70 | 0.1 | 0.761000 | 0.050000 | 0.762136485 | +0.001136485 | +0.1493% |
| 70 | 0.5 | 0.659000 | 0.050000 | 0.666520915 | +0.007520915 | +1.1413% |

### KCl mean activity coefficient

| Temperature, degrees C | Molality, mol/kg H2O | Source gamma | Source U95 | Current app gamma | Absolute difference | Relative difference |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.1 | 0.772400 | 0.050000 | 0.769617598 | -0.002782402 | -0.3602% |
| 0 | 0.5 | 0.642900 | 0.050000 | 0.641779888 | -0.001120112 | -0.1742% |
| 20 | 0.1 | 0.770200 | 0.050000 | 0.768637511 | -0.001562489 | -0.2029% |
| 20 | 0.5 | 0.650600 | 0.050000 | 0.648874255 | -0.001725745 | -0.2653% |
| 50 | 0.1 | 0.761000 | 0.050000 | 0.761602811 | +0.000602811 | +0.0792% |
| 50 | 0.5 | 0.644000 | 0.050000 | 0.646328977 | +0.002328977 | +0.3616% |
| 70 | 0.1 | 0.752000 | 0.050000 | 0.754035673 | +0.002035673 | +0.2707% |
| 70 | 0.5 | 0.632000 | 0.050000 | 0.638249186 | +0.006249186 | +0.9888% |

## Aggregate findings

| Finding | Value |
|---|---:|
| Number of cases | 16 |
| Mean absolute relative difference | 0.2997% |
| Largest absolute difference | +0.007520915 |
| Largest relative difference | +1.1413% |
| Case with largest difference | NaCl, 0.5 mol/kg H2O, 70 degrees C |
| Largest pH 6-8 sensitivity relative to pH 7 | `7.25e-6` absolute gamma |

All 16 absolute differences are smaller than the source-reported `U95 = 0.05`. This is a
numerical observation, not a formal acceptance decision.

The sign pattern is systematic in this grid:

- at 0 and 20 degrees C, the app is below the reference for both salts and molalities;
- at 50 and 70 degrees C, the app is above the reference for both salts and molalities;
- the largest differences occur at 70 degrees C and 0.5 mol/kg H2O.

The pH sensitivity is orders of magnitude smaller than the largest comparison differences,
so the fixed-pH convention does not explain the observed temperature pattern. Possible
contributors include differences between the Pitzer parameterization in the current pinned
database and the evaluated equations used by Partanen, as well as source rounding and the
small pressure mapping difference. This document does not assign a single confirmed cause.

## What this validation supports

It is accurate to say that, for the selected grid, the current app's NaCl and KCl mean
activity coefficients agree closely with an independent evaluated reference dataset derived
from experimental literature.

It is not accurate to infer from this comparison that:

- all 95 values in the source have been checked;
- water activity or osmotic coefficient has been independently compared here;
- CaCl2, MgCl2, Na2SO4, carbonate systems, or multicomponent brines are validated;
- the complete 0-100 degrees C app range is validated;
- lower concentrations are insensitive to the imposed pH convention;
- `0.05` is a universal or project-approved tolerance;
- every result produced by the calculator is independently validated.

## Reproducibility and maintenance

The current library tests enforce that:

- all 16 source values and reported uncertainties exactly match the archived ThermoML JSON;
- every mapped input uses supported components and conditions;
- every case runs through the native PHREEQC calculation engine;
- the calculated result contains the requested NaCl or KCl mean coefficient.

At the time of this report:

- `42` unit tests passed;
- `27` native integration tests passed;
- Ruff and repository diff checks passed.

This is a dated scientific-validation snapshot. Recalculate and update it if the engine,
database, source record, mapping convention, or mean-coefficient implementation changes.
