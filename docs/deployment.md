# Deployment

## Target

The initial host is Streamlit Community Cloud. It executes `streamlit run` from the repository
root, so the deployment entry point is `streamlit_app.py` and Python dependencies are exposed
through `requirements.txt`.

## Reference environment

- Python 3.12
- Dependencies declared in `pyproject.toml`
- `phreeqc` native wheel available for the target Linux/Python combination
- Bundled database at `data/databases/pitzer.dat`

## Pre-deployment checklist

1. Install from a clean environment with `python -m pip install -r requirements-dev.txt`.
2. Run `ruff check .` and `pytest tests/unit`.
3. Run native integration tests with `RUN_PHREEQC_INTEGRATION=1`.
4. Start `streamlit run streamlit_app.py` and exercise all reference cases.
5. Verify mobile and desktop layouts, keyboard navigation, units, and error messages.
6. Confirm no user compositions, secrets, or IP addresses are intentionally persisted.
7. Add the selected license, third-party notices, privacy statement, and owner contact.
8. Deploy from a tagged commit and record the app URL in this document.

## Operational posture

The calculator should be stateless. Do not log raw user compositions. Store only anonymous,
aggregate product analytics if a future privacy policy explicitly permits it.

If native-wheel installation fails on the target platform, treat that as a deployment blocker;
do not silently switch scientific engines.

