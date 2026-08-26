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

## Archived machine-readable data

### NIST ThermoML NaCl/KCl record (2016)

- Local file:
  [`nist-thermoml-partanen-2016-nacl-kcl.json`](nist-thermoml-partanen-2016-nacl-kcl.json)
- Title: *Mean Activity Coefficients and Osmotic Coefficients in Dilute Aqueous Sodium or
  Potassium Chloride Solutions at Temperatures from (0 to 70) degrees C*
- Author: J. I. Partanen
- Journal: *Journal of Chemical & Engineering Data* 61(1), 286-306
- DOI: <https://doi.org/10.1021/acs.jced.5b00544>
- ThermoML record: <https://trc.nist.gov/ThermoML/10.1021/acs.jced.5b00544.html>
- Official JSON:
  <https://trc.nist.gov/ThermoML/10.1021/acs.jced.5b00544.json>
- File size: 64,662 bytes
- SHA-256: `e426d0e08cb9d798bbe850a27a24b47a635b0b364173da62faf8c41fa0fac20b`
- Archive decision: included unchanged. The ThermoML dataset metadata identifies the
  [NIST open-data license](https://www.nist.gov/open/license), which permits reuse with
  appropriate acknowledgment.
- Research use: exact transcription source for 16 released evaluated-reference cases:
  NaCl and KCl at 0.1 and 0.5 mol/kg, each at 0, 20, 50, and 70 degrees C.
- Scientific boundary: the values are evaluated mean ionic activity coefficients derived
  from experimental literature. They are independent reference data, not direct
  measurements at every tabulated point and not software benchmarks.

### NIST ThermoML CaCl2 record (2012)

- Local file: [`nist-thermoml-partanen-2012-cacl2.json`](nist-thermoml-partanen-2012-cacl2.json)
- Title: *Traceable Mean Activity Coefficients and Osmotic Coefficients in Aqueous Calcium
  Chloride Solutions at 25 degrees C up to a Molality of 3.0 mol/kg*
- Author: J. I. Partanen
- Journal: *Journal of Chemical & Engineering Data* 57(11), 3247-3257
- DOI: <https://doi.org/10.1021/je300852v>
- ThermoML record: <https://trc.nist.gov/ThermoML/10.1021/je300852v.html>
- Official JSON: <https://trc.nist.gov/ThermoML/10.1021/je300852v.json>
- File size: 13,846 bytes
- SHA-256: `dc86b4f07590ef0257fa8133c8a143fb202a997b5f7a1fd0b11b38a09659dce0`
- Archive decision: included unchanged under the NIST open-data license with attribution.
- Research use: exact transcription source for four released CaCl2 cases at 0.1, 0.5,
  1.0, and 3.0 mol/kg H2O and 25 degrees C.
- Scientific boundary: the ThermoML values use a two-term Debye-Huckel representation of
  traceable experimental literature. They are evaluated reference data rather than direct
  measurements at every selected point.

### NIST ThermoML MgCl2 record (2015)

- Local file:
  [`nist-thermoml-rouhi-bagherinia-2015-mgcl2.json`](nist-thermoml-rouhi-bagherinia-2015-mgcl2.json)
- Title: *Mean activity coefficient measurement and thermodynamic modelling of the ternary
  mixed electrolyte (MgCl2 + glucose + water) system at T = 298.15 K*
- Authors: A. Rouhi and M. A. Bagherinia
- Journal: *Journal of Chemical Thermodynamics* 91, 286-291
- DOI: <https://doi.org/10.1016/j.jct.2015.07.049>
- ThermoML record:
  <https://trc.nist.gov/ThermoML/10.1016/j.jct.2015.07.049.html>
- Official JSON:
  <https://trc.nist.gov/ThermoML/10.1016/j.jct.2015.07.049.json>
- File size: 60,294 bytes
- SHA-256: `74a58b82a5fa377752171d1c6899300bc3fd7295ada228cbaee87b23bf82d9ef`
- Archive decision: included unchanged under the NIST open-data license with attribution.
- Research use: only pure-or-mixture dataset 2, the 15-point binary MgCl2-water subset, is
  eligible for the current app. Four exact points are released at 0.0833, 0.3333, 1.0, and
  2.0 mol/kg H2O and 25 degrees C.
- Scientific boundary: the selected values were calculated from EMF cell-potential
  measurements. The glucose-containing dataset 1 is not mapped or released.

### NIST ThermoML Na2SO4 record (2014)

- Local file:
  [`nist-thermoml-held-2014-na2so4.json`](nist-thermoml-held-2014-na2so4.json)
- Title: *Measuring and modeling aqueous electrolyte/amino-acid solutions with ePC-SAFT*
- Authors: C. Held, T. Reschke, R. Muller, W. Kunz, and G. Sadowski
- Journal: *Journal of Chemical Thermodynamics* 68, 1-12
- DOI: <https://doi.org/10.1016/j.jct.2013.08.018>
- ThermoML record:
  <https://trc.nist.gov/ThermoML/10.1016/j.jct.2013.08.018.html>
- Official JSON:
  <https://trc.nist.gov/ThermoML/10.1016/j.jct.2013.08.018.json>
- File size: 654,223 bytes
- SHA-256: `df1402688908113ef7bd9f6a0103badcb5a111eb04254a175228c015e4338a08`
- Archive decision: included unchanged under the NIST open-data license with attribution.
- Research use: only pure-or-mixture dataset 81, the binary Na2SO4-water subset, is
  eligible for the current app. It supplies two selectable inputs at 0.5 and 1.0 mol/kg
  H2O and two measured osmotic coefficients at each input.
- Scientific boundary: all amino-acid mixtures and other salts in the record are excluded.
  The four measurements represent two unique compositions and are preserved without
  averaging or selecting a preferred replicate.

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
Get-FileHash -Algorithm SHA256 docs/references/validation/*.json
```

The expected hashes above are also the provenance check for future maintainers. If an
official source later changes, preserve the reviewed copy or create a new versioned record;
do not silently replace a file while retaining the old citation and extracted values.
