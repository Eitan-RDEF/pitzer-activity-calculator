# Contributing

The project is currently in founder-led development. Focus proposed changes on scientific
correctness, transparent assumptions, accessibility, or maintainability.

Before opening a change:

1. Explain the user or scientific problem it solves.
2. Add or update tests for calculation behavior.
3. Record new model assumptions and data provenance.
4. Run `ruff check .` and `pytest tests/unit`.
5. For chemistry changes, include a reproducible reference case and expected tolerance.

Do not add ions, temperature ranges, or outputs merely because PHREEQC accepts them. New
capabilities require evidence that the bundled database supports the relevant interactions
and that the result has been independently checked.

