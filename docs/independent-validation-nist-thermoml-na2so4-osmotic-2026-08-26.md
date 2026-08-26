# Independent validation against NIST ThermoML Na2SO4 osmotic-coefficient measurements

**Validation date:** 2026-08-26

**Result:** At two Na2SO4 molalities and 25 degrees C, the current app's osmotic
coefficients were compared with all four measurements in the source record. The mean
absolute relative difference across the four source observations is `1.7926%`; the largest
absolute relative difference is `4.2425%`.

**Evidence class:** Independent experimental reference data

**Important boundary:** This comparison validates only the osmotic coefficient for binary
Na2SO4-water at 0.5 and 1.0 mol/kg H2O and 25 degrees C. It does not validate the app's
Na2SO4 mean activity coefficient, other sulfate salts, mixed electrolytes, or amino-acid
systems.

## Source

Held, C., Reschke, T., Muller, R., Kunz, W., and Sadowski, G. (2014), *Measuring and
modeling aqueous electrolyte/amino-acid solutions with ePC-SAFT*, Journal of Chemical
Thermodynamics, 68, 1-12.

- DOI: <https://doi.org/10.1016/j.jct.2013.08.018>
- NIST ThermoML record:
  <https://trc.nist.gov/ThermoML/10.1016/j.jct.2013.08.018.html>
- Archived source:
  [`nist-thermoml-held-2014-na2so4.json`](references/validation/nist-thermoml-held-2014-na2so4.json)
- Exact locator: pure-or-mixture dataset 81
- Reuse statement: [NIST open-data license](https://www.nist.gov/open/license)

Dataset 81 is the binary Na2SO4-water subset. It reports four direct osmotic-coefficient
measurements made with a commercial Gonotec 070 osmometer: two measurements at 0.5 mol/kg
and two at 1.0 mol/kg. The other datasets in the record include amino acids or different
salts and are not used here.

The repeated values are retained as distinct source observations. They are not averaged,
and neither observation at a given molality is designated as preferred.

## Current calculation environment

| Item | Value |
|---|---|
| PHREEQC engine | `3.8.6-17100-x64` |
| Database | `data/databases/pitzer.dat` |
| Database SHA-256 | `3640e62aee63a118f800b115b46a2760576e63e05e1792022315a28f75dbe9bb` |
| Source temperature | 298.15 K |
| App temperature | 25 degrees C |
| Source pressure | 101 kPa |
| App pressure | 1 atm |
| Composition basis | mol/kg H2O |
| App pH | 7.0, fixed on the hydrogen-ion activity basis |
| Source pH | Not prescribed |
| Activity model | Pitzer |
| Mineral equilibrium and precipitation | Disabled |

The 101 kPa source pressure is mapped to the app's fixed 1 atm. The difference is about
0.3 kPa. The source does not prescribe pH, so pH 7.0 is an explicit app convention rather
than an experimental condition.

## Input mapping

For source Na2SO4 molality `m`, the charge-balanced analytical input is:

- sodium: `Na = 2m`;
- total S(VI): `SO4 = m`.

| Na2SO4 molality, mol/kg H2O | Na input, mol/kg H2O | Total S(VI) input, mol/kg H2O |
|---:|---:|---:|
| 0.5 | 1.0 | 0.5 |
| 1.0 | 2.0 | 1.0 |

## pH mapping sensitivity

Both inputs were recalculated at pH 6, 7, and 8. The largest absolute change in osmotic
coefficient relative to pH 7 was `2.74e-6`, occurring at 0.5 mol/kg. This is much smaller
than the source-to-app differences below. It supports pH 7 as a numerically low-impact
convention for these two cases, but it is not a source condition or a general result for
other sulfate systems.

## Comparison method

For each source observation:

`absolute difference = current app - source`

`relative difference (%) = 100 x (current app - source) / source`

The source `U95` values are compiler-estimated combined expanded uncertainties at 95%
confidence in the ThermoML record. They are retained as source metadata, not used as a
project-defined acceptance tolerance, and no pass/fail status is assigned.

## Side-by-side results

| Molality, mol/kg H2O | Source observation | Source osmotic coefficient | Source U95 | Current app osmotic coefficient | Absolute difference | Relative difference |
|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 1 | 0.717000 | 0.014000 | 0.686581390 | -0.030418610 | -4.2425% |
| 0.5 | 2 | 0.690000 | 0.015000 | 0.686581390 | -0.003418610 | -0.4955% |
| 1.0 | 1 | 0.658000 | 0.016000 | 0.642247026 | -0.015752974 | -2.3941% |
| 1.0 | 2 | 0.642000 | 0.016000 | 0.642247026 | +0.000247026 | +0.0385% |

## Findings

| Finding | Value |
|---|---:|
| Unique app inputs | 2 |
| Source observations | 4 |
| Mean absolute relative difference | 1.7926% |
| Largest absolute relative difference | 4.2425% |
| Largest-difference observation | 0.5 mol/kg, source value 0.717 |
| Numerical differences smaller than source U95 | 3 of 4 |

The two source measurements at each molality differ from one another by more than simple
rounding: `0.027` at 0.5 mol/kg and `0.016` at 1.0 mol/kg. The app result is close to the
lower reported observation at each concentration. At 0.5 mol/kg it is below both source
observations; at 1.0 mol/kg it lies between them.

This spread is important context. It should not be hidden by averaging the observations,
and it prevents the comparison from being summarized by a single source value at each
composition.

## What this validation supports

It is accurate to say that:

- the app's Na2SO4 osmotic coefficient has been independently compared with all four
  binary-water measurements in ThermoML dataset 81;
- at 1.0 mol/kg, the app result lies between the two published observations;
- three of four numerical differences are smaller than the corresponding source-reported
  expanded uncertainty;
- pH 6-8 sensitivity is negligible relative to the observed source-to-app differences for
  these two inputs.

It is not accurate to infer that:

- four different Na2SO4 concentrations were tested;
- the source observations were averaged or one was selected as preferred;
- the app's Na2SO4 mean activity coefficient was independently validated;
- mixed chloride/sulfate, other sulfate salts, or amino-acid systems were validated;
- source uncertainty is an approved project tolerance;
- the complete sulfate operating range is validated.

## Reproducibility and maintenance

The validation-library tests enforce that:

- both selectable inputs preserve the exact source molalities and 2:1 Na/S(VI)
  stoichiometry;
- all four source observations and uncertainties exactly match archived ThermoML dataset
  81;
- the other amino-acid and salt datasets in the record are not imported;
- both inputs run through the normal native PHREEQC engine path.

This is a dated validation snapshot. Recalculate it if the engine, database, source record,
mapping convention, or osmotic-coefficient implementation changes.
