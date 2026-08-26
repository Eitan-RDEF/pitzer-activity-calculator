# Supported components and calculation boundaries

**Last updated:** 2026-08-27

**Release:** Version 1

Inputs are analytical component totals on a molality basis, not free-ion concentrations.
PHREEQC determines the aqueous species distribution after the user supplies the composition,
known pH, and temperature.

## Core inputs

These components are shown in the main composition form:

| Input | Interpretation |
|---|---|
| Na+ | Total analytical sodium |
| K+ | Total analytical potassium |
| Mg2+ | Total analytical magnesium |
| Ca2+ | Total analytical calcium |
| Cl- | Total analytical chloride |
| Total S(VI) | Sulfate-family total, including SO4(2-) and HSO4- |
| Total inorganic C(IV) | Carbonate-family total, including CO2(aq), HCO3-, CO3(2-), and defined complexes |

NaCl, KCl, CaCl2, MgCl2, and Na2SO4 have selected published validation evidence. This does
not make every mixture containing those components independently validated.

## Conditional inputs

The extended section exposes components that the bundled database can calculate but for
which interaction coverage is less complete:

| Input | Important limitation |
|---|---|
| Li+ | Carbonate, bicarbonate, and bisulfate interactions are incomplete |
| Sr2+ | Carbonate, hydroxide, and bisulfate interactions are incomplete |
| Ba2+ | Sulfate and carbonate coverage is weak; precipitation is not modeled |
| Total Fe(II) | Fixed Fe(II) only; no redox calculation or Fe(III) conversion |
| Total Mn(II) | Fixed Mn(II) only; no redox calculation |
| Br- | Good binary coverage but fewer multicomponent interaction parameters |
| Total B | Several borate species are represented, but interaction coverage is uneven |
| Total Si | Neutral silica is better supported than deprotonated silicate, especially at high pH |

The app repeats active limitations with the calculation results. A numerical solution does
not override these warnings.

## Unavailable capabilities

Version 1 does not provide:

- Fe(III) or aluminum analytical inputs;
- redox, pe, or Eh calculations;
- mineral precipitation or solid-phase equilibrium;
- gas-phase or atmospheric CO2 equilibrium;
- ion exchange or surface complexation;
- automatic or user-selected charge correction.

For a solution equilibrated with atmospheric or another specified CO2 pressure, users must
determine the resulting pH and total inorganic carbon experimentally or with an appropriate
external equilibrium tool. They may then enter those values here as a closed-system
snapshot. Enter total inorganic carbon—not carbonate ion alone—so PHREEQC can calculate the
distribution among CO2(aq), HCO3-, CO3(2-), and defined complexes.

The calculator reports signed charge balance and a clear quality warning, but it never
changes an ion concentration to force electroneutrality. Investigating and correcting an
imbalanced analytical dataset remains the user's responsibility.

## Operating boundary

- Known pH on the hydrogen-ion activity basis
- Closed aqueous system
- Temperature from 0 to 100 degrees C
- Pressure fixed at 1 atm
- Composition in mol/kg H2O or mmol/kg H2O
- Pitzer activity model
- MacInnes convention for individual-ion activity coefficients

The operating boundary describes inputs accepted by the software. It is broader than the
current independent-validation envelope. See [validation evidence and scope](validation-status.md)
before interpreting a calculation.

For the parameter-level inventory, provenance, checksum, and interaction matrix, see the
full [bundled `pitzer.dat` audit](pitzer-database-audit.md).
