# Initial validation against published USGS PHRQPITZ benchmarks

**Validation date:** 2026-08-26

**Result:** The current app closely reproduces four published USGS PHRQPITZ aqueous-state
benchmarks for concentrated NaCl and NaCl-CaSO4 solutions from 0 to 100 degrees C.

**Evidence class:** Published software-implementation benchmark

**Important boundary:** This is the first implementation validation of the app. It is not yet
independent validation against experimental measurements, and it does not validate every
component, mixture, concentration, or temperature offered by the calculator.

## Source

Plummer, L. N., Parkhurst, D. L., Fleming, G. W., and Dunkle, S. A. (1988), *A computer
program incorporating Pitzer's equations for calculation of geochemical reactions in brines*,
U.S. Geological Survey Water-Resources Investigations Report 88-4153.

- DOI: <https://doi.org/10.3133/wri884153>
- Archived source: [`docs/references/validation/usgs-phrqpitz-1988.pdf`](references/validation/usgs-phrqpitz-1988.pdf)
- Library data: [`data/examples/validation_library.json`](../data/examples/validation_library.json)

The source cases are PHRQPITZ test problems 3 and 4. Their original calculations include
mineral-equilibrium paths. The current app intentionally disables solids, so this validation
re-enters each published **final aqueous composition** and compares the resulting aqueous
properties. It does not claim to reproduce the mineral-equilibrium path, halite solubility, or
the gypsum-anhydrite boundary calculation itself.

## Current calculation environment

| Item | Value |
|---|---|
| PHREEQC engine | `3.8.6-17100-x64` |
| Database | `data/databases/pitzer.dat` |
| Database SHA-256 | `3640e62aee63a118f800b115b46a2760576e63e05e1792022315a28f75dbe9bb` |
| Pressure | 1 atm |
| Composition basis | mol/kg H2O |
| pH mode | Known pH, defined from hydrogen-ion activity |
| Activity model | Pitzer |
| MacInnes convention | Enabled |
| Higher-order electrostatic terms | Enabled |
| Redox calculation | Disabled |
| Mineral equilibrium and precipitation | Disabled |

The current database is a pinned official USGS repository file dated 2026-01-05. It is much
newer than the database used to produce the 1988 PHRQPITZ output, so small differences are
expected and should not automatically be interpreted as calculation errors.

## Inputs

| Case | Temperature | Known pH | Analytical components, mol/kg H2O | Source locator |
|---|---:|---:|---|---|
| Concentrated NaCl-CaSO4 | 25 degrees C | 6.7203 | Na 5.573737; Cl 5.573737; Ca 0.04801542; S(VI) 0.04801542 | Test problem 3, table 11, printed pages 75-82 |
| NaCl final state | 0 degrees C | 7.0322 | Na 6.093272; Cl 6.093272 | Test problem 4, table 13, printed pages 83-89 |
| NaCl final state | 25 degrees C | 6.5971 | Na 6.099676; Cl 6.099676 | Test problem 4, table 13, printed pages 90-91 |
| NaCl final state | 100 degrees C | 5.6149 | Na 6.624753; Cl 6.624753 | Test problem 4, table 13, printed pages 92-93 |

## Side-by-side results

Relative difference is calculated here for this scientific review as:

`100 x (current app - USGS source) / USGS source`

The public reference-library feature does not need to calculate or display this difference.

### 1. Concentrated NaCl-CaSO4 solution at 25 degrees C

| Property | USGS source | Current app | Relative difference |
|---|---:|---:|---:|
| Water activity | 0.777300 | 0.777317 | +0.0021% |
| Osmotic coefficient | 1.243600 | 1.243650 | +0.0040% |
| Ionic strength, mol/kg H2O | 5.765800 | 5.765799 | -0.00002% |
| Mean activity coefficient, NaCl | 0.942280 | 0.945198 | +0.310% |

The app also calculated mean coefficients for CaCl2 and Na2SO4, but the selected source
comparison retains only the published NaCl mean coefficient.

### 2. NaCl final state at 0 degrees C

| Property | USGS source | Current app | Relative difference |
|---|---:|---:|---:|
| Water activity | 0.757700 | 0.757916 | +0.0285% |
| Osmotic coefficient | 1.264100 | 1.262536 | -0.124% |
| Ionic strength, mol/kg H2O | 6.093300 | 6.093272 | -0.00046% |
| Mean activity coefficient, NaCl | 0.927810 | 0.913646 | -1.527% |

### 3. NaCl final state at 25 degrees C

| Property | USGS source | Current app | Relative difference |
|---|---:|---:|---:|
| Water activity | 0.754600 | 0.754330 | -0.0358% |
| Osmotic coefficient | 1.281300 | 1.282790 | +0.116% |
| Ionic strength, mol/kg H2O | 6.099700 | 6.099676 | -0.00039% |
| Mean activity coefficient, NaCl | 0.999290 | 1.003929 | +0.464% |

### 4. NaCl final state at 100 degrees C

| Property | USGS source | Current app | Relative difference |
|---|---:|---:|---:|
| Water activity | 0.744200 | 0.743899 | -0.0404% |
| Osmotic coefficient | 1.237500 | 1.239451 | +0.158% |
| Ionic strength, mol/kg H2O | 6.624800 | 6.624754 | -0.00070% |
| Mean activity coefficient, NaCl | 0.910120 | 0.912804 | +0.295% |

## Consolidated assessment

| Property family | Largest absolute relative difference observed |
|---|---:|
| Water activity | approximately 0.0404% |
| Osmotic coefficient | approximately 0.158% |
| Ionic strength | approximately 0.00070% |
| Mean activity coefficient, NaCl | approximately 1.527% |

Agreement is strong across all four concentrated-solution cases:

- Water activity differs by no more than approximately 0.04%.
- Osmotic coefficient differs by no more than approximately 0.16%.
- Ionic strength is effectively identical at the precision reported by the source.
- Three of the four NaCl mean coefficients differ by approximately 0.29-0.46%.
- The largest difference is the NaCl mean coefficient at 0 degrees C, at approximately
  1.53% below the published PHRQPITZ value.

The 0 degrees C mean-coefficient difference deserves follow-up, but it is not currently
evidence of an app defect. Plausible contributors include updates to Pitzer interaction
parameters, temperature-dependence terms, database revisions, source rounding, and
implementation differences between 1988 PHRQPITZ and the current PHREEQC engine/database
pair.

## Validation conclusion

These results provide credible first evidence that:

- the app maps concentrated analytical inputs correctly into PHREEQC;
- the app extracts water activity, osmotic coefficient, ionic strength, and mean NaCl
  activity coefficients correctly;
- the current engine/database pair produces results closely aligned with published USGS
  PHRQPITZ output at 0, 25, and 100 degrees C;
- the stored reference-library inputs run successfully through the normal calculation path.

This evidence does **not** yet establish:

- independent agreement with experimental measurements;
- a universal validity limit for concentration or ionic strength;
- validation of KCl, CaCl2, MgCl2, sulfate, carbonate, seawater-like mixtures, or extended
  components;
- mineral-equilibrium, precipitation, redox, or calculated-pH capabilities;
- complete validation of the entire 0-100 degrees C operating range for arbitrary mixtures.

The next validation priority is source-cleared experimental or evaluated data for NaCl and
KCl, followed by CaCl2, MgCl2, Na2SO4, and mixed major-ion solutions.

## Reproducibility

The library structure and stored component keys are checked by
`tests/unit/test_validation_library.py`. Each stored input is also run through the native
PHREEQC engine by `tests/integration/test_validation_library.py` when
`RUN_PHREEQC_INTEGRATION=1`.

This document records a scientific review snapshot. If the engine, database, source mapping,
or stored values change, rerun the four cases and create an updated dated result rather than
silently overwriting the historical conclusion.
