# Validation evidence and scope

**Last updated:** 2026-08-27

**Release:** Version 1

Selected outputs have been compared with published USGS and NIST reference data for NaCl,
KCl, CaCl2, MgCl2, and Na2SO4. Validation does not cover every composition, output, or
operating condition. Independently verify results used for critical engineering decisions.

## Evidence summary

The current reference library contains 30 source-cleared cases. Experimental or evaluated
references are kept separate from software implementation benchmarks. The app's selector
can load every case into the normal calculation form and exposes its published source values,
citation, evidence class, locator, and assumptions in a collapsed optional section.

| Evidence | Cases or observations | Compared property | Conditions | Result summary |
|---|---:|---|---|---|
| NIST ThermoML NaCl and KCl | 16 cases | Mean ionic activity coefficient | 0.1 and 0.5 mol/kg H2O; 0, 20, 50, and 70 degrees C | Mean absolute relative difference 0.2997%; maximum 1.1413% |
| NIST ThermoML CaCl2 | 4 cases | Mean ionic activity coefficient | 0.1, 0.5, 1.0, and 3.0 mol/kg H2O; 25 degrees C | Mean absolute relative difference 0.6281%; maximum 0.8400% |
| NIST ThermoML MgCl2 | 4 cases | Mean ionic activity coefficient | 0.0833, 0.3333, 1.0, and 2.0 mol/kg H2O; 25 degrees C | Mean absolute relative difference 1.6817%; maximum 1.9942% |
| NIST ThermoML Na2SO4 | 2 inputs, 4 observations | Osmotic coefficient | 0.5 and 1.0 mol/kg H2O; 25 degrees C | Mean absolute relative difference 1.7926%; maximum 4.2425% |
| USGS PHRQPITZ | 4 cases | Water activity, osmotic coefficient, ionic strength, and selected mean coefficients | Published concentrated aqueous states from 0 to 100 degrees C | Close implementation reproduction; not independent experimental validation |

Source-reported expanded uncertainties are retained with the NIST reference values. They
are source metadata, not project-defined acceptance tolerances, and the app does not assign
pass/fail status.

## What this evidence supports

Within the conditions above, it is accurate to say that selected app outputs have been
compared with published independent references and published Pitzer implementation
benchmarks. Source values, mapping assumptions, engine identity, database checksum, and
side-by-side results are recorded in the repository.

The app also checks every reference input through the normal PHREEQC calculation path.
At the date of this page, the suite contains 45 unit tests and 37 native integration tests.

## What is not yet covered

The current evidence does not establish:

- accuracy for every possible mixture or concentration;
- independent validation of water activity;
- independent multicomponent-brine validation;
- carbonate-system validation;
- broad temperature validation for CaCl2, MgCl2, or Na2SO4;
- independent validation of conditional components such as Li, Sr, Ba, Br, B, Si,
  fixed Fe(II), or fixed Mn(II);
- mineral precipitation, gas equilibrium, charge-correction, or redox capability, which
  Version 1 intentionally does not model;
- suitability as the sole basis for a safety-critical, regulatory, or commercial decision.

## Detailed reports

- [USGS PHRQPITZ implementation comparison](initial-validation-usgs-phrqpitz-2026-08-26.md)
- [NIST ThermoML NaCl/KCl comparison](initial-independent-validation-nist-thermoml-2026-08-26.md)
- [NIST ThermoML CaCl2/MgCl2 comparison](independent-validation-nist-thermoml-divalent-chlorides-2026-08-26.md)
- [NIST ThermoML Na2SO4 osmotic-coefficient comparison](independent-validation-nist-thermoml-na2so4-osmotic-2026-08-26.md)
- [Source archive and integrity hashes](references/validation/README.md)
- [Reference-data collection and release rules](validation-data-collection.md)

The broader [validation plan](validation-plan.md) records future evidence priorities. It is
a roadmap, not the current validation-status page.
