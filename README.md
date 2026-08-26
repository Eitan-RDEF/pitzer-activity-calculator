# Pitzer Activity Calculator

A free, transparent Streamlit calculator for aqueous-solution activities at high ionic
strength, powered by PHREEQC and its Pitzer database.

> **Project status:** early foundation. The repository currently contains a tested vertical
> slice for H⁺ activity. It is not yet validated or released for production engineering use.

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
coverage, redox constraints, and the initial support matrix.

## Scientific scope

The initial calculator uses molality (`mol/kg H₂O`) and the bundled `pitzer.dat` database.
Individual-ion activity coefficients, including γ(H⁺), depend on an extrathermodynamic
convention; PHREEQC applies the MacInnes convention by default for its Pitzer calculations.
The public app must retain this disclosure near relevant results.

Do not use the current early version as the sole basis for safety-critical, regulatory, or
commercial engineering decisions. The release criteria are tracked in
[Validation plan](docs/validation-plan.md).

## Deployment

The root `streamlit_app.py` and `requirements.txt` follow Streamlit Community Cloud's
repository layout. Deployment steps and the release checklist are documented in
[Deployment](docs/deployment.md).

## License status

The application license has not yet been selected. Do not publish the repository until an
application license and third-party notices have been reviewed and added. PHREEQC, its
Python binding, and the bundled database each require accurate attribution; see
[Third-party notices](docs/third-party-notices.md).
