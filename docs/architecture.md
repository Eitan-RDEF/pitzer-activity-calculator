# Architecture

## Goal

Keep the chemistry engine independent from Streamlit so it can be validated, reused by a
future API or batch workflow, and tested without a browser.

## Dependency direction

```text
streamlit_app.py
        |
        v
       ui  ---> domain
        |         ^
        v         |
      engine -----+
        |
        v
  PHREEQC binding + versioned pitzer.dat
```

Dependencies point inward toward stable domain types:

- `domain` contains no Streamlit or PHREEQC imports.
- `engine` accepts domain inputs and returns domain results.
- `ui` translates human interaction into domain inputs and renders results.
- `streamlit_app.py` only configures the page and invokes the UI.

## Key boundaries

### Domain

Defines solution inputs, calculation results, and supported-component metadata. These types
are the internal contract shared by all interfaces.

### Engine

Validates inputs, creates deterministic PHREEQC input, invokes the native binding, and
parses a deliberately stable set of output headings. Third-party failures are translated
into application-level `CalculationError` messages.

### UI

Owns layout, help text, accessibility, input widgets, and result presentation. It must not
construct PHREEQC syntax or encode hidden scientific rules.

### Data

Databases and reviewed examples are versioned inputs, not source code. Any database update
requires provenance, checksum, release notes, and regression validation.

## Expected growth

Add modules when real behavior requires them, not in anticipation of every possible feature.
Likely next boundaries are:

- tabular result and CSV/XLSX export services;
- solution presets with citations and versioning;
- all-species activity and saturation-index output parsing;
- comparison modes for Davies and Pitzer;
- cached, immutable calculation requests;
- structured observability without storing user compositions.

The initial app intentionally has no account system, persistent database, background worker,
or custom backend API.

