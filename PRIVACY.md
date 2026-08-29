# Privacy statement

**Effective date:** 27 August 2026

**Last updated:** 29 August 2026

**Data controller and application owner:** Eitan Elfassy

**Contact:** [eitan.elfassi@gmail.com](mailto:eitan.elfassi@gmail.com)

## Scope

This statement describes data handling by the public Pitzer Activity Calculator, its Google
Cloud Run hosting environment, and the project's public GitHub Pages presentation site. The
calculator has no user accounts, advertising, profiling, or user-tracking analytics.

## Calculator inputs and results

Submitted compositions, physical conditions, and selected reference cases are processed in the
active Streamlit session only to perform the requested PHREEQC calculation. Generated download
files are created on demand. The application does not intentionally persist those inputs,
calculation results, or downloads in an application database, container filesystem, analytics
service, or application log.

Chemical compositions are not normally personal data. Users must not enter names, contact
details, or other personal information into calculator fields. They must also not submit
confidential, export-controlled, or otherwise sensitive formulations to the public service.

## Inactivity recovery storage

The application pauses after 10 minutes without browser activity to close abandoned WebSocket
connections. To avoid losing work, the latest form values are stored in that tab's browser
`sessionStorage` until the tab is closed. They are not available to other browser tabs.

When the user resumes, a same-origin cookie named `pitzer_resume_state` transfers the validated
form state once into the new Streamlit session. The cookie:

- is restricted to the `/app/` path;
- uses `SameSite=Strict` and `Secure` on the public HTTPS service;
- expires after at most 60 seconds; and
- is normally deleted earlier, immediately after successful consumption.

This storage is used only to provide the calculator's inactivity-recovery function. It is not
used for identification, advertising, analytics, or cross-site tracking.

## Technical service data, purposes, and legal basis

Google Cloud Run and Cloud Logging necessarily process limited technical service data needed to
deliver, secure, diagnose, and operate the public service. This may include IP addresses,
timestamps, requested paths, response status, browser or device information, and infrastructure
or error metadata. Duplicate Nginx access logging is disabled in the application container.

Where the GDPR or a comparable law applies, the legal basis for processing this limited
technical data is the owner's legitimate interest in providing, securing, preventing abuse of,
and troubleshooting the free scientific service. The data is not used for direct marketing,
behavioral advertising, or decisions about individuals.

## Service providers, location, and retention

The calculator is hosted on Google Cloud Run. Eitan Elfassy determines the purposes and means of
the application's processing and is the data controller; Google acts as a cloud service provider
and, for customer personal data, as a processor under the
[Google Cloud Data Processing Addendum](https://cloud.google.com/terms/data-processing-addendum/).
Google may use subprocessors and may process technical data outside the user's country subject
to its contractual transfer safeguards. See the
[Google Cloud Privacy Notice](https://cloud.google.com/terms/cloud-privacy-notice) and
[Google Cloud subprocessors](https://cloud.google.com/terms/subprocessors).

The application does not retain calculator inputs or results after the active server session.
Browser recovery data follows the periods stated above. The Google Cloud project's `_Default`
log bucket is configured to retain logs for 30 days. Required administrative and system audit
logs are governed by Google Cloud's separate mandatory retention rules. See
[Cloud Logging storage and retention](https://cloud.google.com/logging/docs/storage).

The public presentation site and source repository are hosted by GitHub. GitHub may process
ordinary request and device data when those pages are visited under the
[GitHub Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).

## External links

The app links to GitHub, USGS, NIST, and journal or publisher pages. Visiting an external link
causes the destination site to process the request under its own privacy practices. The
calculator does not receive information about a user's subsequent activity on those sites.

## Individual rights

Depending on applicable law, users may have rights to request access, correction, deletion,
restriction, or objection concerning their personal data, and to complain to a competent data
protection authority. Requests can be sent to
[eitan.elfassi@gmail.com](mailto:eitan.elfassi@gmail.com). To help locate a relevant technical log
entry, a request may need to include the approximate access time and IP address involved.

Form-recovery data is controlled directly by the user: closing the browser tab removes its
`sessionStorage`. The application performs no profiling or automated decision-making about
individuals.

## Security, questions, and changes

The public service uses HTTPS, a same-origin recovery design, short-lived restricted cookies, an
unprivileged container, and validated state restoration. No Internet service can guarantee
absolute security. Users with sensitive compositions should run the open-source application in
an environment they control.

General product and scientific questions may be opened in the project's
[GitHub Issues](https://github.com/Eitan-RDEF/pitzer-activity-calculator/issues). Security concerns
should be reported privately as described in [SECURITY.md](SECURITY.md).

Material changes to this statement will be recorded in the repository and reflected by an
updated date.
