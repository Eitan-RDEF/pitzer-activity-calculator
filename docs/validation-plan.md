# Validation plan

This roadmap tracks evidence beyond the current Version 1 validation scope. Completed
comparisons are summarized in [validation evidence and scope](validation-status.md).

## 1. Software correctness

- Unit tests cover validation, species mapping, deterministic PHREEQC input, and output
  parsing failures.
- Native PHREEQC smoke tests run on the deployment Python and Linux environment.
- Every user-visible output has a stable definition, unit, and formatting rule.
- Malformed, extreme, nonfinite, and imbalanced inputs fail or warn predictably.

## 2. Reference calculations

Create versioned fixtures for at least:

- pure or near-pure water;
- dilute and concentrated NaCl;
- CaCl₂ and MgCl₂ brines;
- Na₂SO₄ and mixed chloride/sulfate solutions;
- a seawater-like mixture;
- carbonate-bearing solutions across several pH values;
- one intentionally charge-imbalanced analysis;
- boundary temperatures within the supported range.

For each case, retain the source, exact input, expected output, tolerance, PHREEQC version,
and database checksum.

These tolerances belong to automated regression and scientific validation tests. They are not
part of the public reference library and must not produce user-facing pass/fail judgments.

## 3. Independent comparison

- Compare reproducible cases against PHREEQC run independently of this UI.
- Where compatible, compare mean coefficients or water activity with published data or a
  second trusted implementation.
- Investigate discrepancies instead of widening tolerances without explanation.

## 4. Scientific review

- Confirm database provenance and parameter coverage.
- Review single-ion convention wording.
- Define defensible temperature, pressure, composition, and concentration limits.
- Review charge-balance and redox warnings with an experienced geochemist or chemical
  thermodynamicist.

## 5. Release gate

The first public release requires all critical tests to pass in CI, a completed third-party
notice, an application license, privacy wording, and a visible validation-scope statement.
