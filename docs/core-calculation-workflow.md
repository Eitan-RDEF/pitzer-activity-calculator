# Core Known-pH Calculation Workflow

**Implementation status:** complete Version 1 workflow

**Implemented:** 2026-08-26

**Validation status:** software regression tested; selected properties independently compared

## Scope

This is the Version 1 end-to-end calculation contract. It implements a focused known-pH
workflow with a default major-ion core and a clearly separated conditional-component mode.
Calculated-pH, CO₂-equilibrium, and charge-correction modes remain future work.

The workflow is:

- known pH on the hydrogen-ion activity basis;
- closed aqueous system with no gas-phase equilibrium;
- fixed pressure of 1 atm;
- 0–100 °C;
- analytical totals in `mol/kg H₂O` or `mmol/kg H₂O`;
- default inputs Na, K, Mg, Ca, Cl, total S(VI), and total inorganic C(IV);
- conditional inputs Br, Li, Sr, Ba, B, Si, fixed Fe(II), and fixed Mn(II), with static and
  mixture-aware database-coverage warnings;
- Pitzer model with MacInnes scaling and electrostatic mixing terms enabled;
- redox disabled;
- no minerals, precipitation, exchange, surfaces, or solid solutions.

## Domain contract

The UI converts `mmol/kg H₂O` to `mol/kg H₂O` before constructing `SolutionInput`.
PHREEQC always receives `mol/kgw` and exactly 1 kg of water.

`CalculationResult` returns:

- pH, temperature, and pressure;
- ionic strength and calculated alkalinity;
- water mass, water activity, and osmotic coefficient;
- signed charge balance and percent charge-balance error;
- every active aqueous solute species possible from the exposed inputs;
- molality, activity, activity coefficient, and base-10 logarithms for each species;
- available curated mean activity coefficients;
- PHREEQC engine version, database SHA-256, and exact PHREEQC input.

## Species extraction

PHREEQC `USER_PUNCH` calls `MOL`, `ACT`, `GAMMA`, `LM`, `LA`, and `LG` for the audited
species list. Output headings use stable indexed identifiers rather than chemical formulas,
so formulas containing punctuation cannot destabilize the Python mapping.

PHREEQC reports a sentinel molality of `1e-99` for defined but absent species in this output
path. The adapter excludes values at or below `1e-90`; this rule is covered by integration
tests. It does not hide any physically meaningful species within the calculator's intended
numerical envelope.

The extraction functions are documented in the official
[PHREEQC Basic-function reference](https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-61.htm).

## Mean coefficients

The initial curated set is:

- NaCl;
- KCl;
- CaCl₂;
- MgCl₂;
- Na₂SO₄;
- HBr.

A mean coefficient is displayed only when both constituent equilibrium ions have active
molality. Values are calculated with PHREEQC's `MEANG` function and the stoichiometry in the
database's `MEAN_GAMMAS` block. This is a software extraction contract, not yet proof of an
experimental validity range.

## Charge-balance interpretation

No automatic correction is performed. The signed PHREEQC error is retained, while the UI
uses the approved absolute-error bands:

- `≤2%`: good;
- `>2%` and `≤5%`: review recommended;
- `>5%`: significant imbalance.

## Exports

Every successful calculation provides:

- full-precision active-species CSV;
- exact PHREEQC `.pqi` input;
- human-readable Markdown report;
- ZIP containing all three files.

The report records inputs, warnings, results, conventions, exclusions, engine version, and
database checksum. Export generation is stateless and does not write the user's composition
to the server filesystem.

## Current evidence and next scientific work

The integration suite pins a 1 molal NaCl result at 25 °C and exercises a mixed
chloride/sulfate/carbonate system at 60 °C. The Streamlit test submits the default NaCl case
and confirms that the complete result interface renders without exceptions.

These regression cases detect software changes. Separate NIST ThermoML comparisons now
provide independent evidence for selected NaCl, KCl, CaCl2, MgCl2, and Na2SO4 properties;
USGS cases provide implementation benchmarks. See
[validation evidence and scope](validation-status.md) for the current results and the
[validation plan](validation-plan.md) for remaining priorities.
