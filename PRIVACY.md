# Privacy statement

**Effective date:** 27 August 2026  
**Last updated:** 27 August 2026
**Application owner:** Eitan Elfassy

## Data handled by the calculator

The Pitzer Activity Calculator has no user accounts and does not intentionally persist
submitted compositions or calculation results. Inputs are processed in the active Streamlit
session to run the requested PHREEQC calculation. Download files are generated on demand.

The application does not intentionally log raw compositions or calculation results, and the
owner does not operate advertising or user-tracking analytics in the app. Streamlit usage
statistics are disabled in the repository configuration.

## Hosting data

The planned public hosting environment is Google Cloud Run. Once deployed, Google may process
technical and network information needed to deliver, secure, and operate the service, such as
IP addresses, browser or device information, request metadata, and service logs. That
processing is controlled by Google's own policies. See the
[Google Cloud Privacy Notice](https://cloud.google.com/terms/cloud-privacy-notice).

The application is designed to be stateless and does not intentionally write submitted
compositions or calculation results to Cloud Run storage or application logs. Platform-level
request and infrastructure logs may still be retained according to the configured Google
Cloud logging and retention settings.

## External links and sensitive information

The app links to external resources including GitHub, USGS, NIST, and journal source pages.
Those sites have their own privacy practices.

Do not submit confidential, personal, export-controlled, or otherwise sensitive composition
data to a public hosted calculator. Run the open-source application in an environment you
control when the composition itself is sensitive.

## Contact and changes

Questions about this statement can be sent to
[Eitan Elfassy](mailto:eitan.elfassi@gmail.com). General product and scientific questions may
also be opened in the project's
[GitHub Issues](https://github.com/Eitan-RDEF/pitzer-activity-calculator/issues). Please report
security concerns privately as described in [SECURITY.md](SECURITY.md).

Material changes to this statement will be recorded in the repository and reflected by a new
effective date.
