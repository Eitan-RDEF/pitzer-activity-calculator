# Changelog

All notable changes to this project will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project
intends to use semantic versioning once public releases begin.

## [Unreleased]

### Added

- Production-minded Streamlit repository scaffold.
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

- Restricted the functional beta to the audited core components while conditional ions await
  targeted validation and warning rules.
- Made 1 atm pressure and the Pitzer, MacInnes, electrostatic-mixing, and no-redox assumptions
  explicit in generated PHREEQC input.
