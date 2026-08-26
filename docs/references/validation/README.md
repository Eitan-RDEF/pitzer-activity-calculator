# Validation source archive

This folder preserves source material used during the scientific-validation research. A file
being archived here does not mean that its data are approved for the public validation
library. Scientific compatibility, reuse rights, transcription, and source-to-app mapping are
separate release gates. The public library will not implement tolerances or pass/fail grading.

## Archived PDFs

### USGS PHRQPITZ report (1988)

- Local file: [`usgs-phrqpitz-1988.pdf`](usgs-phrqpitz-1988.pdf)
- Title: *A computer program incorporating Pitzer's equations for calculation of
  geochemical reactions in brines*
- Authors: L. N. Plummer, D. L. Parkhurst, G. W. Fleming, and S. A. Dunkle
- Report: U.S. Geological Survey Water-Resources Investigations Report 88-4153
- DOI: <https://doi.org/10.3133/wri884153>
- Official PDF: <https://pubs.usgs.gov/wri/1988/4153/report.pdf>
- File size: 3,455,880 bytes
- SHA-256: `149e451fa82af98844590a81d7429105668cf2def783d8ee6568c8f0e0fb551e`
- Archive decision: included. USGS-authored information is generally in the U.S. public
  domain; attribution is requested.
- Research use: source for the four normalized PHRQPITZ implementation benchmarks.

### NSRDS-NBS 24 (1968)

- Local file: [`nsrds-nbs-24-1968.pdf`](nsrds-nbs-24-1968.pdf)
- Title: *Theoretical Mean Activity Coefficients of Strong Electrolytes in Aqueous
  Solutions from 0 to 100 C*
- Author: W. J. Hamer
- Report: NSRDS-NBS 24; NASA-CR-109356
- NTRS record: <https://ntrs.nasa.gov/citations/19700013983>
- File size: 24,136,127 bytes
- SHA-256: `3097aa0593c2e3437ec66c216f94be9f2873b22fdf211ac95b557002aa6203ef`
- Archive decision: included. The NTRS record identifies the work as public-use-permitted.
- Research use: screened source only. It was rejected as independent Pitzer validation
  because it provides theoretical charge-type tables rather than salt-specific experimental
  observations.

## Externally pinned PDF

### NASA/NBS Electrochemical Data Part XIII (1969)

- Repository copy: deliberately not included pending rights clarification
- Title: *Osmotic coefficients and mean activity coefficients of a series of uni-univalent
  electrolytes in aqueous solutions at 25 C*
- Authors: Y.-C. Wu and W. J. Hamer
- Report: NBS Report 10002; NASA-CR-106045
- NTRS record: <https://ntrs.nasa.gov/citations/19690029307>
- Official PDF:
  <https://ntrs.nasa.gov/api/citations/19690029307/downloads/19690029307.pdf>
- Reviewed file size: 6,294,512 bytes
- Reviewed-file SHA-256:
  `05cf33b7e488ff9f04c10e959736f8abe42bac1ff1d81d8fd2d0b7552c643a1c`
- Archive decision: external link and checksum only. The NTRS catalog says “Public Use
  Permitted,” while the report title page contains an older restriction on publication,
  reprinting, and reproduction. Copying it into a public Git repository would itself be
  redistribution, so the conflict must be resolved first.
- Research use: screened source for possible future electrolyte components; not currently
  compatible with the app's exposed analytical anions.

Do not add the PDF to this folder merely because it can be downloaded. First update the
reuse decision in `data/examples/research/validation_sources.json` with explicit supporting
evidence.

## Integrity check

From PowerShell, hashes can be checked with:

```powershell
Get-FileHash -Algorithm SHA256 docs/references/validation/*.pdf
```

The expected hashes above are also the provenance check for future maintainers. If an
official source later changes, preserve the reviewed copy or create a new versioned record;
do not silently replace a file while retaining the old citation and extracted values.
