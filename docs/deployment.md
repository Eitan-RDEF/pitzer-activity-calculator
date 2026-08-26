# Google Cloud Run deployment

## Status and responsibility boundary

The repository is prepared for Google Cloud Run, but deployment is intentionally not part of
this code change. The owner will create and configure the Google Cloud resources separately,
verify the resulting service, and then record its public URL and release revision here.

- Application release: `1.0.0`
- Deployment target: Google Cloud Run service
- Public URL: pending owner deployment and smoke test
- Recommended region: `me-west1` (Tel Aviv)
- Runtime port: Cloud Run's injected `PORT` environment variable, defaulting locally to `8080`

No previous-host URL should be presented as live. Until the Cloud Run service is verified, the
GitHub repository is the canonical project homepage.

## Container contract

The root [Dockerfile](../Dockerfile) is the production runtime definition. It:

- uses the Python 3.12 slim Linux image;
- installs the same package metadata and pinned PHREEQC binding used by local development;
- installs an immutable application wheel and sets `PITZER_PROJECT_ROOT=/app` so the installed
  package can locate its versioned runtime data;
- copies only the application, bundled database, reviewed reference cases, styles, and runtime
  configuration into the image;
- runs as an unprivileged user;
- binds Streamlit to `0.0.0.0` and the injected `PORT`;
- disables usage statistics, development file watching, and run-on-save behavior; and
- preserves normal process signals so Cloud Run can stop an instance cleanly.

The `.dockerignore` file excludes tests, research PDFs, local environments, caches, Git
metadata, and development-only files from the build context. Scientific runtime assets under
`data/databases` and the reviewed cases under `data/examples` remain in the image.

The service is stateless. Do not add code that persists raw user compositions or calculation
results to the container filesystem, Cloud Logging, a database, or analytics without first
updating the privacy statement and obtaining an explicit product decision.

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
`http://localhost:8080/_stcore/health`. GitHub Actions performs the same image build and health
check on every push and pull request.

## Recommended first service configuration

These values suit the calculator's current CPU-bound, single-user calculation model and the
owner's preference for scale-to-zero hosting:

| Setting | Initial value | Reason |
| --- | --- | --- |
| Ingress | All | The calculator is a public website. |
| Authentication | Allow unauthenticated | Visitors should not need a Google account. |
| Billing | Request-based | CPU is needed while handling requests, not while idle. |
| Minimum instances | `0` | Permits scale to zero and avoids a permanently warm instance. |
| Maximum instances | `2` | Provides a simple initial cost and abuse guardrail. |
| CPU | `0.5` vCPU | Conservative initial allocation; increase if calculations feel slow. |
| Memory | `512 MiB` | Appropriate starting point; confirm with Cloud Monitoring. |
| Concurrency | `1` | A Streamlit session can hold state and a PHREEQC calculation is CPU-bound. |
| Execution environment | First generation | Required when using less than 1 vCPU. |
| Startup CPU boost | Enabled | Helps reduce cold-start time. |
| Container port | `8080` | Matches the local default; Cloud Run still injects `PORT`. |

Treat these as initial operating values rather than scientific requirements. During the
side-by-side deployment, confirm them against the current Google Cloud console and pricing
before creating the service. Do not commit Google credentials, service-account keys, project
IDs, billing-account IDs, or generated deployment URLs into source code.

## Post-deployment smoke test

After the owner deploys the service:

1. Confirm the assigned `run.app` URL loads in a signed-out browser.
2. Confirm `/_stcore/health` responds successfully.
3. Load and calculate at least one reviewed NaCl case and one multivalent case.
4. Verify the results tabs, source-data controls, warnings, and every download type.
5. Check desktop and mobile layouts and an initial cold start.
6. Inspect Cloud Logging for startup errors and verify raw compositions are not emitted.
7. Configure a billing budget and alerts; remember that alerts notify but do not hard-cap cost.
8. Record the verified URL, Google Cloud region, deployed revision, and test date in this file
   and in the README.
9. Tag the verified release commit only after the deployment matches that commit.

## Updating and rollback

Cloud Run does not update merely because GitHub changes unless the owner later configures a
continuous-deployment trigger. For the initial manual workflow, build and deploy a new revision
from a reviewed commit, smoke-test the revision, and then direct traffic to it. Cloud Run keeps
older immutable revisions, allowing traffic to be moved back to the last known-good revision if
a deployment fails.

Deployment commands and the choice between source deployment, Cloud Build, and Artifact
Registry will be finalized with the owner during the separate deployment session. This keeps
cloud mutations, billing choices, and authentication decisions out of repository preparation.

## Current operator references

- [Cloud Run container runtime contract](https://cloud.google.com/run/docs/container-contract)
- [CPU limits and fractional-vCPU requirements](https://cloud.google.com/run/docs/configuring/services/cpu)
- [Cloud Run locations](https://cloud.google.com/run/docs/locations)
- [Local container testing](https://cloud.google.com/run/docs/testing/local)
- [Cloud Run pricing](https://cloud.google.com/run/pricing)
