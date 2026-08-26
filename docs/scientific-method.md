# Scientific method and conventions

## Calculation basis

The initial implementation delegates aqueous speciation and Pitzer activity calculations to
IPHREEQC through the `phreeqc` Python binding. Inputs are analytical totals expressed as
molality (`mol/kg H₂O`) and are evaluated with the versioned database in
`data/databases/pitzer.dat`.

## Individual-ion coefficients

Individual-ion activity coefficients are not independently measurable and require an
extrathermodynamic convention. PHREEQC's Pitzer database uses MacInnes scaling by default.
The UI and exports must disclose the convention whenever individual-ion coefficients are
reported.

Mean electrolyte activity coefficients are generally more suitable for comparison with
experimental measurements. They should be added only with explicit, tested stoichiometric
definitions.

## Input interpretation

- Concentrations are analytical component totals, not necessarily equilibrium species
  concentrations.
- pH is defined from hydrogen-ion activity, not directly from H⁺ molality.
- Sulfur(VI) and inorganic carbon totals are allowed to speciate among database species.
- A successful numerical solve does not guarantee a chemically plausible input.

## Redox boundary

The bundled `pitzer.dat` contains no redox couples. It cannot calculate redox reactions or
convert between entered oxidation states. The only audited iron master component is `Fe`,
with `Fe+2` as its master species, so any exposed iron input is fixed **Fe(II) total**.
Fe(III), pe/Eh controls, and implied redox equilibration are outside version 1.

## Limitations to disclose

- Results depend on database species and interaction-parameter coverage.
- Database validity varies with species, temperature, and concentration.
- Charge imbalance can indicate missing ions, unit errors, or inconsistent analyses.
- Fixed Fe(II) and Mn(II), if exposed, require prominent no-redox warnings.
- Calculations outside the validated envelope must be clearly flagged.

Specific numerical claims and validity ranges will be added only after the validation work
described in `validation-plan.md` is complete.

See the [database audit](pitzer-database-audit.md) for provenance, parameter coverage, and
the component support classification.
