# Pitzer Activity Calculator

A free, transparent Streamlit calculator for aqueous-solution activities at high ionic
strength, powered by PHREEQC and its Pitzer database.

> **Project status:** functional Version 1 foundation. The repository contains a complete,
> tested known-pH workflow for audited core major ions. Selected mean activity coefficients
> and one osmotic-coefficient system have been independently compared with published NIST
> ThermoML references; the full operating range is not validated, and the app is not yet
> released for production engineering use.

## Why this project exists

Most lightweight online activity calculators stop at Debye–Hückel or Davies. This project
aims to make Pitzer calculations accessible without requiring users to install PHREEQC,
write input decks, or interpret raw solver output.

The product priorities are:

1. Scientifically explicit assumptions and conventions.
2. Reliable validation against trusted PHREEQC reference calculations.
3. A focused workflow for engineers and chemists.
4. Reproducible, downloadable inputs and results.
5. A maintainable separation between chemistry and presentation code.

## Run locally

Python 3.12 is the reference development version.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
streamlit run streamlit_app.py
```

Run the fast quality checks with:

```powershell
ruff check .
pytest tests/unit
```

The native PHREEQC integration smoke test is opt-in:

```powershell
$env:RUN_PHREEQC_INTEGRATION = "1"
pytest tests/integration
```

## Repository map

```text
.
├── streamlit_app.py            # Hosting entry point; intentionally thin
├── src/pitzer_calculator/
│   ├── domain/                   # Typed chemistry inputs, outputs, species
│   ├── engine/                   # Validation, input building, PHREEQC adapter
│   └── ui/                       # Streamlit presentation only
├── data/
│   ├── databases/                # Versioned PHREEQC database and provenance
│   └── examples/                 # Reviewed example solution inputs
├── tests/
│   ├── unit/                     # Fast deterministic rules and input tests
│   └── integration/              # Native PHREEQC smoke and reference tests
├── docs/                      # Product, scientific, validation, deployment docs
├── assets/                    # Project-owned visual assets and CSS
├── legacy/                    # Preserved desktop prototype
└── .github/workflows/         # Automated quality checks
```

See [Architecture](docs/architecture.md) for code boundaries and
[Version 1 product definition](docs/version-1-product-definition.md) for the approved
scientific and product behavior. The reproducible
[Pitzer database audit](docs/pitzer-database-audit.md) records provenance, parameter
coverage, redox constraints, and the initial support matrix. The implemented
[core calculation workflow](docs/core-calculation-workflow.md) defines the current input,
result, warning, and export contract.

## Scientific scope

The current calculator accepts `mol/kg H₂O` and `mmol/kg H₂O`, converts internally to
molality, and uses the bundled `pitzer.dat` database. Individual-ion activity coefficients
depend on an extrathermodynamic convention; the generated PHREEQC input explicitly enables
MacInnes scaling, and the app discloses that convention near the results.

Selected outputs have been compared with published USGS and NIST reference data. Validation
does not cover every composition, output, or operating condition. Independently verify
results used for critical engineering decisions. See the current
[validation evidence and scope](docs/validation-status.md) and
[supported components](docs/supported-components.md).

## Deployment

The root `streamlit_app.py` and `requirements.txt` follow Streamlit Community Cloud's
repository layout. Deployment steps and the release checklist are documented in
[Deployment](docs/deployment.md).

## License status

The application license has not yet been selected. Do not publish the repository until an
application license and third-party notices have been reviewed and added. PHREEQC, its
Python binding, and the bundled database each require accurate attribution; see
[Third-party notices](docs/third-party-notices.md).
