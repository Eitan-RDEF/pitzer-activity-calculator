# Version 1 Product and Scientific Definition

**Status:** Approved scope baseline  
**Decision date:** 2026-08-26  
**Scope amended:** 2026-08-27 (CO₂ equilibrium and charge correction explicitly excluded)
**Applies to:** First public version of the Pitzer Activity Calculator

## Purpose

This document records the product and scientific decisions made for version 1. It is the
shared implementation baseline for future human contributors and AI agents.

Do not silently broaden, narrow, or reinterpret this scope. If later evidence requires a
change, update this document, explain the reason, add relevant validation evidence, and
record the change in `CHANGELOG.md`.

This is a product definition, not proof that every requested calculation is scientifically
supported by the current database. The `pitzer.dat` audit and validation work described
below must establish the final supported-component list and defensible operating envelope.

## Core promise

Version 1 will be a complete Pitzer activity calculator for supported aqueous species. A
user will enter an aqueous analysis as analytical component totals, select explicit physical
and acid-base assumptions, and receive equilibrium molalities, activities, and activity
coefficients together with diagnostics, water properties, warnings, and reproducible files.

The app is intended to make a rigorous PHREEQC Pitzer calculation accessible without
requiring users to write PHREEQC input or interpret raw solver output.

## Decision register

| # | Topic | Approved decision |
|---:|---|---|
| 1 | Product scope | Complete activity calculator for all supported aqueous species |
| 2 | Composition basis | Analytical component totals |
| 3 | Concentration units | `mol/kg H₂O` and `mmol/kg H₂O` |
| 4 | Acid-base mode | Known pH only |
| 5 | Temperature | 0–100 °C |
| 6 | Pressure | Fixed near atmospheric pressure |
| 7 | Components | Only components supported by a documented `pitzer.dat` audit |
| 8 | Charge handling | Diagnostics and warnings only; no correction |
| 9 | Thermodynamic outputs | Solute results plus water activity and osmotic coefficient |
| 10 | Mean coefficients | Curated, validated electrolyte list |
| 11 | Single-ion convention | MacInnes convention only |
| 12 | Redox | Fixed oxidation-state totals with explicit redox assumptions |
| 13 | Carbonate gas boundary | Closed aqueous system only; no CO₂ equilibrium |
| 14 | Unvalidated coverage | Calculate where technically possible and issue prominent warnings |
| 15 | Solids | No precipitation or equilibration with solids |
| 16 | Known-pH range | pH −2 to 16 |
| 17 | Charge-balance bands | ≤2% good; >2–5% review; >5% significant imbalance |
| 18 | Balancing components | None; the submitted analysis is never modified |
| 19 | External equilibrium states | Enter externally determined pH and total inorganic carbon |
| 20 | Result presentation | Layered summary followed by a complete filterable species table |
| 21 | Downloads | CSV, PHREEQC input, and concise calculation report; optional ZIP |
| 22 | Presets | Curated and validated examples only |
| 23 | Composition UI | Guided fields plus a paste-friendly editable table |
| 24 | Data retention | Stateless; no intentional storage of compositions or results |
| 25 | Explanations | Progressive disclosure |
| 26 | Precision | Adaptive display precision; full precision in downloads |
| 27 | Activity model | Pitzer only |

## Detailed requirements

### 1. Complete activity calculation

The primary result is not limited to H⁺. For every aqueous species returned by PHREEQC
within the supported model, the app should make the following available where defined:

- equilibrium molality;
- activity;
- activity coefficient;
- base-10 logarithms when useful for interpretation or reproduction;
- species name, charge, component association, and unit metadata.

The app must also report ionic strength, pH, charge-balance diagnostics, calculation status,
and the model/database versions used.

### 2. Analytical component totals

Users enter analytical totals such as total Na, Ca, Mg, Cl, S(VI), and inorganic C(IV).
They do not enter guessed equilibrium species distributions. PHREEQC determines speciation
from the totals and selected boundary conditions.

Labels must distinguish analytical components from equilibrium species. For example, total
S(VI) must not be labeled as though the entire amount necessarily remains free SO₄²⁻.

### 3. Concentration units

Version 1 accepts:

- `mol/kg H₂O`;
- `mmol/kg H₂O`.

Both are molality-based, and their conversion is exact. Version 1 does not accept molarity,
`mg/L`, ppm, or other density-dependent concentration units. Internally, calculations use
`mol/kg H₂O`.

### 4. Acid-base calculation mode

Version 1 provides one explicit mode: **known pH**. The user supplies pH on the H⁺ activity
basis together with analytical component totals. A known pH is required for every
calculation.

The UI must explain that pH is defined from H⁺ activity rather than H⁺ molality.

### 5. Temperature envelope

The exposed version 1 temperature range is 0–100 °C. The database audit must verify
parameter behavior within this range for each supported component and interaction.

The UI must not imply that every supported interaction has equal evidence across the entire
range. Component- or interaction-specific limitations produce warnings.

### 6. Pressure assumption

Version 1 uses a fixed near-atmospheric pressure. It does not expose pressure as an input.
The exact value passed to or assumed by PHREEQC must be documented in the methodology and
calculation report.

Pressurized process systems are outside version 1 scope.

### 7. Audited component coverage

Do not expose every master component merely because it appears in `pitzer.dat`. Create a
documented audit that identifies:

- available aqueous master species and equilibrium species;
- binary, mixing, ternary, and neutral-species interaction parameters;
- temperature dependence and stated parameter ranges;
- known missing parameters or zero-value assumptions;
- redox and complexation implications;
- validation evidence for the intended outputs.

The audit determines the final version 1 input list. Components that cannot be mapped or run
safely are blocked. Components that technically run but have incomplete evidence may be
allowed only under the warning policy in decision 14.

### 8. Charge-balance diagnostics

The app calculates and reports the signed charge-balance error for the original user
analysis. It classifies the magnitude using the documented warning bands, but it does not
offer automatic or user-selected ion adjustment.

The submitted composition is passed to the solver unchanged and retained unchanged in all
downloads. Diagnosing the source of an imbalance and deciding whether any analytical value
should be revised remain the user's responsibility.

### 9. Solute and water outputs

Version 1 includes solute speciation and activity results together with:

- water activity;
- osmotic coefficient.

These water properties are release requirements only if their definitions and extraction
from PHREEQC are independently validated. The osmotic-coefficient extraction now has a
first independent comparison for two binary Na2SO4 inputs at 25 degrees C; water activity
still lacks an independent experimental comparison, and the broader range remains
unvalidated. If validation fails, the app must omit the affected output rather than
approximate it without a reviewed scientific basis.

### 10. Mean electrolyte activity coefficients

The app reports mean activity coefficients, γ±, for a curated list of common neutral
electrolytes. Initial candidates include NaCl, KCl, CaCl₂, MgCl₂, and Na₂SO₄, but the
final list depends on the database and validation audits.

Each electrolyte definition must specify its stoichiometry and equation. Arbitrary cation-
anion pairing is outside version 1 scope.

### 11. MacInnes convention

Individual-ion activity coefficients use PHREEQC's MacInnes convention. Version 1 does not
offer an unscaled alternative.

Because individual-ion activity coefficients are convention-dependent and cannot be
independently measured, this assumption must appear:

- near relevant results;
- in the methodology documentation;
- in the downloadable calculation report.

### 12. Redox-sensitive components

The database audit resolved this decision more narrowly than the initial candidate scope.
The bundled `pitzer.dat` contains no redox couples and cannot simulate redox reactions.

Version 1 may expose fixed Fe(II) total, mapped to the database component `Fe` whose master
species is `Fe+2`, and fixed Mn(II) total after their conditional validation. It must not
expose Fe(III), pe/Eh controls, redox equilibration, or oxidation-state conversion.

Inputs and reports must clearly state that these totals retain the fixed oxidation state
represented by the database. The detailed evidence and warnings are recorded in
`docs/pitzer-database-audit.md`.

### 13. Closed carbonate boundary

Version 1 uses a **closed carbonate system**: entered total inorganic carbon remains fixed
and no exchange with atmospheric or another gas phase is modeled. The app does not accept
`pCO₂` or calculate an atmosphere-equilibrated pH or carbon total.

Users who need an open-system state may equilibrate the sample experimentally or use an
appropriate external tool, then enter the resulting pH and total inorganic carbon here.
Total inorganic carbon—not carbonate ion concentration alone—is required because the app
calculates the distribution among CO₂(aq), HCO₃⁻, CO₃²⁻, and defined complexes.

### 14. Outside validated coverage

When PHREEQC can technically calculate a supported composition but the parameter or
validation evidence is incomplete, version 1 may return the result with a prominent warning.

Warnings must be specific. They should identify the affected component, interaction,
temperature, concentration, or other condition and explain why confidence is reduced. A
generic disclaimer is not a substitute.

Numerically invalid inputs, unsupported component identifiers, missing required boundary
conditions, solver failures, and temperatures or pH values outside the exposed version 1
range remain blocking errors.

### 15. No solid-phase equilibration

Version 1 calculates aqueous speciation for the dissolved analytical totals exactly as
entered. It does not add equilibrium phases or precipitate minerals and salts.

A successful result therefore does not prove that the entered composition is physically
stable against precipitation. This limitation must be disclosed, especially for
concentrated and potentially supersaturated solutions.

### 16. Known-pH range

Known-pH mode accepts pH from −2 to 16. This deliberately includes concentrated acidic and
basic systems beyond the conventional 0–14 teaching range.

The database audit and reference suite must establish where results within this exposed
range require additional warnings.

### 17. Charge-balance quality bands

Use the magnitude of the signed PHREEQC charge-balance error for classification:

- **≤2%:** well balanced;
- **>2% to 5%:** review recommended;
- **>5%:** significant imbalance.

The signed numerical value remains visible. These bands do not silently reject or correct a
solution, and the UI must avoid presenting them as universal laboratory acceptance criteria.

### 18. No balancing components

Version 1 exposes no balancing-ion selector. Na⁺, Cl⁻, and every other analytical total
remain exactly as entered. Charge-balance diagnostics inform the user without presenting a
particular correction as chemically justified.

### 19. Externally determined equilibrium states

If pH or total inorganic carbon was established through atmospheric CO₂ equilibration,
another gas boundary, or a separate equilibrium calculation, the user enters the resulting
known pH and total inorganic carbon. The app treats these values as a closed-system snapshot
for aqueous Pitzer calculations; it does not reproduce the preceding equilibration process.

### 20. Layered results

The initial result view shows:

- calculation status and warnings;
- pH, ionic strength, and charge-balance status;
- water activity and osmotic coefficient when validated;
- dominant or user-relevant species;
- requested mean electrolyte coefficients.

A second layer provides the complete aqueous-species table with search, filtering, sorting,
and clear units. Trace species remain accessible rather than being discarded.

### 21. Download package

Version 1 provides:

- the complete tabular result as CSV;
- the reproducible PHREEQC input file;
- a concise human-readable Markdown or plain-text calculation report.

The report contains inputs, units, assumptions, database/model versions, charge-balance
diagnostics, warnings, and key results. The files may also be bundled in a ZIP archive. A
formatted Excel workbook and structured developer JSON are deferred until user demand
justifies them.

### 22. Curated presets

Version 1 includes 30 reviewed reference cases covering published NaCl, KCl, CaCl₂, MgCl₂,
Na₂SO₄, and one mixed NaCl-CaSO₄ aqueous state. Selecting a case prefills the standard
known-pH form; calculation remains under user control and uses the normal result interface.

Every preset must record provenance, purpose, units, applicable validity limits, and expected
results. The collapsed **Load a published reference case (optional)** section presents the
evidence class, published values, citation, direct source link, locator, and mapping
assumptions. Published source details and mapping limitations are each hidden until requested.
The app does not calculate differences or assign pass/fail. Presets are educational starting
points, not universal reference compositions.

### 23. Composition entry experience

Use guided controls for calculation mode, temperature, pH or carbonate variables, and other
boundary conditions. Use an editable table for composition totals.

The composition table must support:

- adding and removing rows;
- selecting only audited components;
- entering one approved unit per row or using a clearly defined table-wide unit;
- pasting multiple rows from spreadsheet software;
- immediate row-level validation.

Version 1 does not include a separate CSV-upload workflow.

### 24. Stateless data handling

The app does not intentionally persist user compositions or calculation results. Data exists
only for the active Streamlit session and downloadable files are generated on demand.

Version 1 has no accounts, saved calculations, composition database, or raw-composition
analytics. Repository-level Streamlit usage statistics are disabled. The hosting provider
may process technical data required to operate and secure the public service, as described
in the public privacy statement.

### 25. Progressive disclosure

Keep the main workflow concise while placing explanations where decisions occur. Use
expandable help for:

- analytical totals and molality;
- known-pH and closed-carbonate assumptions;
- charge-balance diagnostics;
- MacInnes scaling;
- redox assumptions;
- water properties and mean coefficients;
- database coverage and warnings;
- no-precipitation behavior.

A separate methodology page provides the full scientific explanation and references.

### 26. Numerical precision

The interface uses adaptive significant figures and scientific notation based on magnitude.
Avoid both false precision and values rounded to zero.

Downloads preserve the full practical numerical precision returned by the engine. The
formatting layer must not modify values used in calculations or exports.

### 27. Pitzer-only model

Version 1 runs the Pitzer model only. It does not compare against Debye–Hückel or Davies and
does not automatically select a model based on ionic strength.

The methodology may explain why Pitzer is appropriate, but the result interface must not
imply that different activity models are interchangeable.

## Version 1 non-goals

The following are explicitly outside this release:

- arbitrary PHREEQC input submitted by public users;
- molarity, `mg/L`, ppm, or density-based input conversions;
- variable pressure and pressurized-process modeling;
- atmospheric or user-specified CO₂/gas equilibrium;
- automatic or user-selected charge correction;
- full user-controlled pe/Eh calculations;
- arbitrary mean-electrolyte pairing;
- mineral precipitation or equilibrium-with-solids calculations;
- Debye–Hückel, Davies, or automatic model comparisons;
- CSV file upload;
- accounts, saved calculations, or persistent composition storage;
- formatted Excel or developer JSON exports.

## Required work before implementation is considered complete

1. ~~Audit the bundled `pitzer.dat` and publish the component/interaction support matrix.~~
   Baseline completed 2026-08-26; interaction-aware warning implementation remains.
2. ~~Verify the database's exact upstream version, provenance, and checksum.~~ Completed
   2026-08-26; final third-party notice review remains.
3. Define the exact near-atmospheric pressure value and redox assumptions.
4. Validate water activity and osmotic-coefficient extraction.
5. Validate the curated mean-electrolyte equations and list.
6. Define condition-specific coverage warnings.
7. ~~Build the first reviewed reference library and connect it to the UI.~~ Completed
   2026-08-27 with 30 cases; broader composition and property coverage remains future
   scientific work.
8. Run native PHREEQC integration tests in the deployment Linux environment.
9. ~~Complete public methodology, privacy, licensing, attribution, and limitation wording.~~
   Completed for release 1.0.0 on 2026-08-27; review again when hosting, data handling,
   dependencies, or scientific scope changes.
10. Conduct a small expert review before broader promotion for engineering use.

## Change control

Future changes to these decisions should include:

- the decision number being changed;
- the old and new behavior;
- the user or scientific reason;
- validation or usability evidence;
- migration effects on inputs, results, presets, exports, and documentation.
