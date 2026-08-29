# Google Cloud Run deployment

## Status and responsibility boundary

The production application is deployed as a public Google Cloud Run service. Google Cloud
resources, billing controls, IAM, and traffic management remain the owner's responsibility;
the repository defines the application container and its continuous-deployment source.

- Application release: `1.0.1`
- Cloud Run service: `pitzer-calculator`
- Public URL:
  [https://pitzer-calculator-584210380580.me-west1.run.app](https://pitzer-calculator-584210380580.me-west1.run.app)
- Region: `me-west1` (Tel Aviv)
- Runtime port: Cloud Run's injected `PORT` environment variable, defaulting locally to `8080`

The Cloud Run URL above is the canonical public application; GitHub remains the source-code and
documentation home. The public root serves an inactivity-aware shell and Streamlit is proxied
under `/app/` within the same service.

## Public discovery page

A separate static presentation page is published at
[https://eitan-rdef.github.io/pitzer-activity-calculator/](https://eitan-rdef.github.io/pitzer-activity-calculator/).
Its purpose is search discovery and project presentation; calculations continue to run only in
the Cloud Run application. The source lives in [`site/`](../site/) and includes conventional HTML,
structured data, a sitemap, robots directives, and social-sharing metadata.

The [GitHub Pages workflow](../.github/workflows/pages.yml) publishes `site/` after relevant pushes
to `main`. It is intentionally independent of the Cloud Build trigger that creates Cloud Run
revisions, so editorial changes to the presentation page do not rebuild the scientific application.

## Container contract

The root [Dockerfile](../Dockerfile) is the production runtime definition. It:

- uses the Python 3.12 slim Linux image;
- installs the same package metadata and pinned PHREEQC binding used by local development;
- installs an immutable application wheel and sets `PITZER_PROJECT_ROOT=/app` so the installed
  package can locate its versioned runtime data;
- copies only the application, bundled database, reviewed reference cases, styles, gateway, and
  runtime configuration into the image;
- runs as an unprivileged user;
- binds Nginx to the injected `PORT` and Streamlit privately to `127.0.0.1:8501/app/`;
- proxies HTTP, health, and WebSocket traffic without creating a second Cloud Run service;
- disables duplicate Nginx access logs while retaining Cloud Run's platform request logs;
- disables usage statistics, development file watching, and run-on-save behavior; and
- supervises both processes and forwards termination signals so Cloud Run can stop cleanly.

The `.dockerignore` file excludes tests, research PDFs, local environments, caches, Git
metadata, and development-only files from the build context. Scientific runtime assets under
`data/databases` and the reviewed cases under `data/examples` remain in the image.

The service is server-stateless. The gateway keeps resume data in the browser tab's
`sessionStorage` and transfers it once through a validated same-origin cookie after an inactivity
pause. The cookie expires after 60 seconds and is deleted earlier after successful consumption.
Do not add code that persists raw user compositions or calculation results to the
container filesystem, Cloud Logging, a database, or analytics without first updating the privacy
statement and obtaining an explicit product decision.

## Inactivity lifecycle

The runtime gateway solves the cost problem created by Streamlit's persistent WebSocket:

1. The browser shell loads Streamlit in a same-origin iframe.
2. Pointer, keyboard, scroll, touch, form-rerun, and tab-return activity reset a 10-minute timer.
3. At expiry the shell replaces the iframe with a pause card, closing the WebSocket.
4. Returning to a hidden tab reconnects automatically; a visible paused page also provides an
   explicit **Resume calculator** button.
5. The new Streamlit session restores validated inputs from browser-tab storage and recalculates
   the last current result when applicable.

The Cloud Run request timeout remains 3600 seconds. Shortening it is not an inactivity control:
Streamlit reconnects timed-out WebSockets while the page remains loaded. For a deterministic
local test, append `?idle_seconds=5` to `http://localhost:8080/`; the override is accepted only on
`localhost` and `127.0.0.1`.

## Validate locally before deployment

Run the normal code checks from a clean Python 3.12 environment:

```powershell
python -m pip install -r requirements-dev.txt
ruff check .
pytest tests/unit
$env:RUN_PHREEQC_INTEGRATION = "1"
pytest tests/integration
```

Then build and run the exact production container:

```powershell
docker build --tag pitzer-calculator:local .
docker run --rm --publish 8080:8080 --env PORT=8080 pitzer-calculator:local
```

Open `http://localhost:8080` and verify the container health endpoint at
`http://localhost:8080/_stcore/health`. Confirm pause/resume quickly at
`http://localhost:8080/?idle_seconds=5`. GitHub Actions performs the same image build and gateway
health check on every push and pull request.

## Verified service configuration

The initial production deployment was verified with these values. They are operational choices,
not scientific requirements:

| Setting | Deployed value | Reason |
| --- | --- | --- |
| Ingress | All | The calculator is a public website. |
| Authentication | Allow unauthenticated | Visitors should not need a Google account. |
| Billing | Request-based | CPU is needed while handling requests, not while idle. |
| Minimum instances | `0` | Permits scale to zero and avoids a permanently warm instance. |
| Maximum instances | `2` | Provides a simple initial cost and abuse guardrail. |
| CPU | `1` vCPU | Matches the deployed revision and gives PHREEQC adequate compute capacity. |
| Memory | `512 MiB` | Matches the deployed revision; review Cloud Monitoring before increasing it. |
| Concurrency | `4` | Current deployed value; increase separately after browser and load testing. |
| Request timeout | `3600` seconds | Matches the deployed revision; normal calculations should finish far sooner. |
| Execution environment | First generation | Matches the deployed revision. |
| Startup CPU boost | Enabled | Helps reduce cold-start time. |
| `_Default` log retention | `30 days` | Confirmed in Cloud Logging; review after material logging changes. |
| Container port | `8080` | Matches the local default; Cloud Run still injects `PORT`. |
| Runtime service account | `pitzer-calculator-runtime` | Dedicated least-privilege identity; no application cloud permissions are required. |
| Encryption | Google-managed key | No customer-managed key is required for this public stateless service. |

The billing account has a separate monthly Cloud Run spend cap. That control is managed in
Google Cloud and is not encoded in this repository. Do not commit Google credentials,
service-account keys, billing-account IDs, or other private cloud configuration into source
code. The public service URL is intentionally documented.

## Verified deployment record

The first fully smoke-tested production baseline was recorded on 2026-08-28:

| Item | Verified value |
| --- | --- |
| Cloud Run revision | `pitzer-calculator-00005-j5d` |
| Source commit | `8a087c3` (`Make downloads independent of Cloud Run routing`) |
| Traffic | `100%` to the latest healthy revision |
| Public access | Application loaded without Google authentication |
| Calculation | A balanced NaCl calculation completed and rendered all result tabs |
| Downloads | CSV, PHREEQC input, Markdown report, and ZIP downloaded through browser-local links |

The revision identifier is a historical verification record. Continuous deployment creates a
new immutable revision after each successful push to `main`; the stable service URL does not
change.

## Smoke test after each production update

After Cloud Build deploys a new revision:

1. Confirm the assigned `run.app` URL loads in a signed-out browser.
2. Confirm `/_stcore/health` responds successfully.
3. Load and calculate at least one reviewed NaCl case and one multivalent case.
4. Verify the results tabs, source-data controls, warnings, and every download type.
5. Check desktop and mobile layouts and an initial cold start.
6. Inspect Cloud Logging for startup errors and verify raw compositions are not emitted.
7. Configure a billing budget and alerts; remember that alerts notify but do not hard-cap cost.
8. Confirm the latest healthy revision receives `100%` of service traffic.
9. Tag a release commit only after the deployed revision matches that commit.

## Updating and rollback

Google Cloud Build is connected to the GitHub repository. A push to the `main` branch triggers
this production workflow:

1. Cloud Build checks out the new `main` commit.
2. It builds the repository's root `Dockerfile` and stores the image in Artifact Registry.
3. It deploys the image as a new immutable `pitzer-calculator` Cloud Run revision.
4. When deployment succeeds, Cloud Run directs production traffic to the new healthy revision.

No separate manual redeployment is normally required after pushing to `main`. A failed build or
failed revision does not require changing the stable public URL. Cloud Run retains older
revisions, so the owner can restore service by moving traffic to the last known-good revision.

Changes to cloud settings, IAM, billing, the build trigger, or traffic allocation are separate
operator actions and are not made by repository code.

## Current operator references

- [Cloud Run container runtime contract](https://cloud.google.com/run/docs/container-contract)
- [CPU limits and fractional-vCPU requirements](https://cloud.google.com/run/docs/configuring/services/cpu)
- [Cloud Run locations](https://cloud.google.com/run/docs/locations)
- [Local container testing](https://cloud.google.com/run/docs/testing/local)
- [Cloud Run pricing](https://cloud.google.com/run/pricing)
