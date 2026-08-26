# Bundled `pitzer.dat` Audit

**Audit date:** 2026-08-26  
**Status:** Reproducible database inventory and version 1 support baseline  
**Not yet provided by this audit:** experimental validation or a complete legal review

## Executive conclusion

The bundled database is an exact, unmodified copy of the official USGS coupled PHREEQC
database repository's `pitzer.dat` at commit
`3ff9be2f12bf44c94b95731c7d8b1ca4a847718c`. Its provenance and checksum are now pinned
and automatically tested.

The database is well suited to a useful major-ion calculator, especially systems based on
Na, K, Mg, Ca, Cl, sulfate, carbonate, H/OH, and selected bromide interactions. It is not a
general periodic-table database. Parameter coverage is interaction-specific, so the app
must assess the complete composition rather than call every listed component universally
"supported."

The most important redox conclusion is definitive: this database contains no redox
couples. Iron is represented by the master component `Fe` whose master species is `Fe+2`.
Fe(III), aluminum, arbitrary pe/Eh calculations, and claims of redox equilibration must not
be exposed in version 1. The application metadata was corrected accordingly.

## Reproducible identity and provenance

| Property | Audited value |
|---|---|
| Repository file | `data/databases/pitzer.dat` |
| Byte length | 37,225 bytes |
| Encoding | Windows-1252 (`cp1252`) |
| SHA-256 | `3640e62aee63a118f800b115b46a2760576e63e05e1792022315a28f75dbe9bb` |
| Upstream | USGS coupled PHREEQC database repository |
| Upstream commit | `3ff9be2f12bf44c94b95731c7d8b1ca4a847718c` |
| Upstream commit date | 2026-01-05 |
| Upstream change description | `Tony's changes, mostly fluoride` |
| Local modifications | None; byte-for-byte match at the audit date |

Primary references:

- [official USGS database file](https://github.com/usgs-coupled-subtrees/phreeqc3-database/blob/3ff9be2f12bf44c94b95731c7d8b1ca4a847718c/pitzer.dat);
- [PHREEQC version 3 software and documentation](https://www.usgs.gov/software/phreeqc-version-3);
- [PHREEQC database descriptions](https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-5.htm).

Run the local audit with:

```powershell
python scripts/audit_pitzer_database.py data/databases/pitzer.dat
python scripts/audit_pitzer_database.py data/databases/pitzer.dat --json
```

The unit suite pins the checksum, byte length, encoding, master-component count, parameter
counts, and exposed input mappings.

## Engine/database pairing

The pinned Python binding is `phreeqc==1.1.1`, and its bundled engine reports
`3.8.6-17100-x64` in the current Windows development environment. The database matches the
USGS repository's 2026-01-05 master file, not the `pitzer.dat` shipped in the PHREEQC 3.8.6
or 3.8.8 release tag.

This mixed pairing loads and executes the audit cases successfully, but that is not enough
to claim complete compatibility. Before public release, choose and document one of these
approaches:

1. align the engine and database to a named upstream release; or
2. retain this newer official database and add regression coverage proving compatibility
   with the deployed engine.

Production must report both the engine version and the database checksum. A database name
alone is not a sufficient version identifier.

## Inventory

### Master components

The database defines 28 master-component rows:

`Alkalinity`, `B`, `Ba`, `Br`, `C`, `C(4)`, `Ca`, `Cl`, `E`, `Fe`, `H`, `H(1)`,
`K`, `Li`, `Mg`, `Mn`, `Na`, `O`, `O(-2)`, `S`, `S(6)`, `Si`, `Sr`, `Hdg`, `Oxg`,
`Mtg`, `Sg`, and `Ntg`.

This list is an inventory, not an input whitelist. Duplicate total/redox-form rows, electron
bookkeeping, and specialized gas pseudo-components are not automatically suitable public
inputs.

### Pitzer parameters

The audit found 268 interaction rows. A row is called temperature-dependent below when it
contains at least one nonzero coefficient after the first coefficient.

| Block | Total rows | Temperature-dependent | Constant-only |
|---|---:|---:|---:|
| B0 | 54 | 26 | 28 |
| B1 | 48 | 27 | 21 |
| B2 | 8 | 5 | 3 |
| C0 | 32 | 16 | 16 |
| THETA | 30 | 3 | 27 |
| LAMBDA | 27 | 9 | 18 |
| ZETA | 10 | 1 | 9 |
| PSI | 59 | 8 | 51 |

A constant-only row is not automatically invalid at temperatures other than 25 °C. It does
mean the database supplies no explicit temperature variation for that row, which must be
considered in the 0–100 °C validation and warning policy. PHREEQC permits up to six
temperature coefficients in Pitzer parameter definitions; omitted coefficients are zero.

### Binary major-ion coverage

Codes in this table identify explicit binary parameter blocks: `0` = B0, `1` = B1,
`2` = B2, and `C` = C0. A dash means no explicit binary row for that pair.

| Cation | Cl− | Br− | OH− | SO₄²− | HSO₄− | HCO₃− | CO₃²− |
|---|---|---|---|---|---|---|---|
| H+ | 01C | 01C | — | 0C | 01 | — | — |
| Li+ | 01C | 01C | 01 | 01C | — | — | — |
| Na+ | 01C | 01C | 01C | 01C | 01 | 012 | 01C |
| K+ | 01C | 01C | 01C | 01C | 01 | 01C | 01C |
| Mg²+ | 01C | 01C | — | 012C | 01 | 01 | — |
| Ca²+ | 012C | 01C | 012 | 012C | 01 | 01 | — |
| Sr²+ | 01C | 01C | — | 012 | — | 0 | — |
| Ba²+ | 01C | 01C | 01 | — | — | — | — |
| Mn²+ | 01C | — | — | 012C | — | — | — |
| Fe²+ | 01C | — | — | 012C | 01 | — | — |

Absence of an explicit pair does not necessarily make PHREEQC fail. It means a relevant
specific-interaction contribution is absent or defaults according to the model, so the app
must not present the result as equally evidenced. Mixing (`THETA`), ternary (`PSI`/`ZETA`),
and neutral-species (`LAMBDA`) coverage also matters for multicomponent solutions.

## Version 1 support classification

This is a product-facing baseline, not the final validation verdict.

| Classification | Components or modes | Required behavior |
|---|---|---|
| Core candidates | Na, K, Mg, Ca, Cl, S(VI), C(IV), alkalinity, H/pH | Expose after reference validation; still evaluate mixture-specific gaps |
| Conditional inputs | Br, Li, Sr, Ba, fixed Fe(II), fixed Mn(II), B, Si | Exposed in a collapsed extended section with permanent component limitations and active condition-specific warnings |
| Explicit boundary | CO₂ | Use only for the user-selected CO₂-equilibrium mode; never assume it silently |
| Excluded | Al, Fe(III), arbitrary redox/pe/Eh, Hdg/Oxg/Mtg/Sg/Ntg inputs, exchange, surface, and phase controls | Do not expose in version 1 |

Important conditional cases include:

- Li has explicit halide, hydroxide, and sulfate pairs, but lacks carbonate, bicarbonate,
  and bisulfate binary rows.
- Sr has halide, sulfate, and one bicarbonate row, but lacks carbonate, hydroxide, and
  bisulfate pairs.
- Ba has halide and hydroxide pairs but lacks sulfate and carbonate-family pairs. Version 1
  also suppresses precipitation, which is especially important for barium systems.
- Fe is fixed Fe(II), with strongest explicit coverage for chloride and sulfate/bisulfate.
  It has no redox couple and sparse coverage outside those systems.
- Mn is fixed Mn(II), with explicit chloride and sulfate pairs only among the audited major
  anions.
- Boron parameters cover several borate species and selected major-ion mixtures, but not a
  uniform set of interactions.
- Neutral `H4SiO4` has selected `LAMBDA` and `ZETA` terms. The deprotonated silicate species
  important at high pH do not have explicit Pitzer rows in this database.
- Bromide has broad binary coverage with several major cations, but less complete ternary
  and trace-metal coverage in complex mixtures.
- Carbonate interactions are strongest for Na and K. Carbonate-rich mixtures containing
  minor divalent metals need explicit coverage warnings.

The initial warning engine inspects active analytical-component combinations and pH for the
documented high-value gaps. Component limitations are also displayed beneath every extended
input and repeated in successful calculation reports. This is deliberately more informative
than a single static "component supported" flag; later validation can refine the rules using
calculated equilibrium-species significance.

## Redox decision

The [official PITZER documentation](https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-37.htm)
states that `pitzer.dat` contains no redox couples and cannot simulate redox reactions.
This audit agrees with the actual master-species inventory.

Version 1 therefore adopts these rules:

- `Fe` input is labeled **Fe(II) total** and maps to the database master component `Fe`;
- Mn is treated as fixed Mn(II) if it is later exposed;
- Fe(III) is unavailable;
- aluminum is unavailable because no `Al` master component exists;
- no redox equilibration, oxidation-state conversion, pe input, or Eh input is implied;
- result reports must repeat these assumptions whenever a redox-sensitive component is
  present.

The previous prototype mappings `Fe(2)`, `Fe(3)`, and `Al` were unsafe: the current binding
can accept such solution lines without a nonzero run status while returning zero totals.
Tests now ensure every public component mapping exists in the audited master list.

## MacInnes and Pitzer options

PHREEQC's documented Pitzer defaults include `-macinnes true`, `-use_etheta true`, and
`-redox false`. MacInnes scaling changes printed individual-ion activity coefficients, not
the equilibrium calculation itself. Version 1 keeps MacInnes scaling and discloses that
individual-ion coefficients are convention-dependent.

The app should emit the selected options explicitly in generated PHREEQC input rather than
depending indefinitely on implicit defaults. Regression cases must pin the resulting
reported coefficients.

## Water properties and mean activity coefficients

The current engine/database pairing successfully exposes:

- `ACT("H2O")` for water activity;
- `OSMOTIC` for the osmotic coefficient;
- `MEANG("electrolyte")` for a database-defined mean activity coefficient.

For a 1 mol/kg water NaCl solution at 25 °C, the integration test currently pins
approximately `γ± = 0.657220`, water activity `0.966825`, and osmotic coefficient
`0.936359`. These are regression values from this exact engine/database pair, not yet an
independent validation against experimental data.

The database contains 21 `MEAN_GAMMAS` definitions:

`CaCl2`, `CaSO4`, `CaCO3`, `Ca(OH)2`, `MgCl2`, `MgSO4`, `MgCO3`, `Mg(OH)2`, `NaCl`,
`Na2SO4`, `NaHCO3`, `Na2CO3`, `NaOH`, `KCl`, `K2SO4`, `HCO3`, `K2CO3`, `KOH`, `HCl`,
`H2SO4`, and `HBr`.

The definition named `HCO3` actually specifies K+ and HCO3− in a 1:1 ratio. Treat it as a
suspected label defect and do not expose it unless the application supplies a reviewed,
tested definition. More generally, a `MEAN_GAMMAS` row defines stoichiometry; it is not by
itself proof of an experimentally validated range.

An initial validation shortlist is NaCl, KCl, CaCl₂, MgCl₂, Na₂SO₄, K₂SO₄, MgSO₄, CaSO₄,
HCl, HBr, and H₂SO₄. Carbonate and hydroxide electrolytes should remain conditional until
their pH/speciation behavior and reference cases are reviewed.

See the official [`MEAN_GAMMAS` documentation](https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/mean_gammas.htm)
and [Basic-function reference](https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-61.htm).

## What this audit does not prove

This inventory does not establish:

- accuracy against experimental data;
- a universal ionic-strength or concentration limit;
- complete validity from 0 to 100 °C for every mixture;
- safety for a process, regulatory, or design decision;
- compatibility of every database feature with the deployed native engine;
- suitability of a component merely because PHREEQC returns a numerical answer.

Those claims require the reference-case program in `docs/validation-plan.md`.

## Required next scientific work

1. Select or formally approve the engine/database version-pairing policy.
2. Build reference cases for core chloride, sulfate, carbonate, acid, and mixed systems over
   the intended temperature and concentration envelope.
3. Independently validate water activity, osmotic coefficient, and the curated mean-γ list.
4. Encode the interaction-aware warning rules described above.
5. Validate the calculated-pH and explicit CO₂-boundary workflows.
6. Review the final support classifications and warnings with a qualified geochemist or
   electrolyte-thermodynamics expert before public promotion.
