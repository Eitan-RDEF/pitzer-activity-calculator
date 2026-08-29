# Architecture

## Goal

Keep the chemistry engine independent from Streamlit so it can be validated, reused by a
future API or batch workflow, and tested without a browser.

## Suggested reading order

Future maintainers and coding agents should begin with:

1. `docs/version-1-product-definition.md` for approved scope and non-goals;
2. this file for dependency direction and ownership boundaries;
3. `src/pitzer_calculator/domain/species.py` for exposed components and curated result
   definitions;
4. `src/pitzer_calculator/engine/validation.py`,
   `src/pitzer_calculator/engine/input_builder.py`, and
   `src/pitzer_calculator/engine/phreeqc.py` for the calculation path;
5. `src/pitzer_calculator/reference_cases.py` for the reviewed validation-data boundary;
6. `src/pitzer_calculator/ui/main.py` only after the scientific path is understood; and
7. `gateway/` for the Cloud Run request-routing and inactivity lifecycle.

Module and object docstrings explain ownership and non-obvious contracts. Comments are
reserved for external-library behavior, scientific conventions, or framework workarounds;
they should not restate straightforward code. Tests use descriptive behavior names instead
of repetitive docstrings.

## Dependency direction

```text
browser -> Nginx gateway -> Streamlit /app/
                              |
                              v
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
into application-level `CalculationError` messages. The export module converts domain
results into CSV, Markdown, and ZIP artifacts without depending on Streamlit.

### UI

Owns layout, help text, accessibility, input widgets, and result presentation. It must not
construct PHREEQC syntax or encode hidden scientific rules.

### Runtime gateway

Nginx is an operational boundary inside the same container, not a second service. It serves a
same-origin browser shell at `/`, proxies Streamlit HTTP and WebSocket traffic under `/app/`, and
preserves the established health URL. The shell removes the Streamlit iframe after 10 minutes
without pointer, keyboard, scroll, touch, or tab-return activity. Removing the iframe closes the
WebSocket so Cloud Run can scale to zero.

The shell keeps the latest form state only in the browser tab's `sessionStorage`. On resume it
uses a one-time, 60-second, same-origin cookie to transfer that state into the new Streamlit
session; the UI validates the schema and asks the shell to delete the cookie immediately. No
resume state is written to application storage, URLs, analytics, or logs. Nginx access logging is
disabled to avoid duplicating Cloud Run's platform request logs. If a completed calculation was
current when the session paused, it is recalculated from the restored inputs.

### Data

Databases and reviewed examples are versioned inputs, not source code. Any database update
requires provenance, checksum, release notes, and regression validation.

The reference-case loader is a typed application-data boundary. It reads only the reviewed
production library under `data/examples/`; research candidates are never loaded by the UI.
Selection prefills the existing domain inputs and does not introduce an alternate
calculation path.

## Expected growth

Add modules when real behavior requires them, not in anticipation of every possible feature.
Likely next boundaries are:

- condition-aware database-coverage warnings;
- structured observability without storing user compositions.

The engine accepts a user-supplied known-pH, closed-system state and reports charge-balance
diagnostics without modifying the analysis. Gas-equilibrium and charge-correction strategies
are intentionally not planned product boundaries.

The initial app intentionally has no account system, persistent database, background worker,
or custom backend API.
