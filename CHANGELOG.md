# Changelog

All notable changes to this project will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project
uses semantic versioning.

## [Unreleased]

### Added

- Add a search-oriented static presentation site with scientific scope, validation evidence,
  FAQs, social-sharing metadata, and an automated GitHub Pages deployment workflow.

## [1.0.1] - 2026-08-28

### Added

- Publish the verified Google Cloud Run endpoint and record its production configuration,
  smoke-test baseline, continuous-deployment workflow, and rollback procedure.

### Changed

- Replace the retired hosted-platform deployment assumptions with a production
  Cloud Run container, stateless runtime contract, container smoke test, and operator guide.
- Disable Streamlit's runtime file watcher and run-on-save behavior in production-oriented
  configuration.
- Use pytest's importlib mode so unit and integration modules with the same descriptive file
  name can be collected together in one full-suite run.
- Start every analytical component at zero; examples remain available through the explicit
  published reference-case selector.
- Replace the standalone species-only download with one rectangular complete-results CSV
  containing summary, balance, mean-coefficient, species, and reproducibility records.
- Embed generated downloads in browser-local links so they remain reliable when Cloud Run
  routes a follow-up request to a different stateless instance.
- Link the author's name in the application sidebar to the public GitHub profile.

### Removed

- Retired the obsolete Tkinter prototype so the repository has one maintained application
  path and one source of scientific behavior.

## [1.0.0] - 2026-08-27

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

[Unreleased]: https://github.com/Eitan-RDEF/pitzer-activity-calculator/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/Eitan-RDEF/pitzer-activity-calculator/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/Eitan-RDEF/pitzer-activity-calculator/releases/tag/v1.0.0
