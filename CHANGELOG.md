# Changelog

All notable changes to this project will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project
intends to use semantic versioning once public releases begin.

## [Unreleased]

### Added

- Production-minded Streamlit repository scaffold.
- In-app selector for 30 reviewed USGS and NIST reference cases, with automatic prefilling
  of the normal calculation form.
- Collapsible **Load a published reference case (optional)** section with published values,
  uncertainty where supplied, evidence class, citation, direct source link, locator, and
  mapping assumptions behind two closed-by-default show/hide controls.
- Complete known-pH, closed-system PHREEQC workflow for audited core major ions.
- Full active-species molality, activity, activity-coefficient, and logarithmic results.
- Water activity, osmotic coefficient, alkalinity, charge diagnostics, and curated mean
  activity coefficients.
- Molal and millimolal composition entry with deterministic internal conversion.
- Species CSV, exact PHREEQC input, calculation report, and complete ZIP downloads.
- Database provenance audit, parameter inventory, support matrix, and version 1 definition.
- Unit-test, integration-test, CI, documentation, and deployment foundations.
- Preserved Tkinter prototype under `legacy/`.

### Changed

- Restricted the Version 1 workflow to audited core components while conditional ions await
  targeted validation and warning rules.
- Restricted the acid-base workflow to user-supplied known pH and defined atmospheric or
  specified-CO2 equilibrium as outside the product scope; users may enter externally
  determined pH and total inorganic carbon as a closed aqueous-system snapshot.
- Defined charge handling as diagnostics and warnings only; the calculator never adjusts a
  submitted component concentration to force charge balance.
- Made 1 atm pressure and the Pitzer, MacInnes, electrostatic-mixing, and no-redox assumptions
  explicit in generated PHREEQC input.
