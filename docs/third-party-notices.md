# Third-party notices

**Release:** 1.0.0
**Reviewed:** 27 August 2026

The Pitzer Activity Calculator's original source code is licensed separately under the
repository's [MIT License](../LICENSE). The following software and data retain their own
terms, notices, and attribution.

## PHREEQC / IPHREEQC and `pitzer.dat`

PHREEQC and IPHREEQC are developed by the U.S. Geological Survey (USGS). The pinned
`phreeqc==1.1.1` binding reports engine build `3.8.6-17100`; its Windows version string adds
the platform suffix `-x64`. The USGS identifies PHREEQC source and usage as public domain.
The official project and distribution are available from the
[USGS PHREEQC page](https://www.usgs.gov/software/phreeqc-version-3).

The bundled `data/databases/pitzer.dat` is an unmodified copy from the official USGS database
repository at commit `3ff9be2f12bf44c94b95731c7d8b1ca4a847718c`, verified 26 August
2026. Its SHA-256 is
`3640e62aee63a118f800b115b46a2760576e63e05e1792022315a28f75dbe9bb`. Full
provenance is recorded in the [database audit](pitzer-database-audit.md).

The PHREEQC distribution supplies this User Rights Notice in substance:

- The software and related data/documentation are made available by USGS for use in the
  public interest and advancement of science and may be used, copied, modified, or
  distributed without fee, subject to the supplied notice.
- Recipients of redistributed copies or modifications must receive the notice and access to
  the original distribution. Modifications must be clearly identified with their extent,
  author, and date.
- USGS endorsement may not be implied; specific written permission is required to use the
  USGS name in advertising or publicity to endorse a product or commercial entity.
- Authors and USGS should be appropriately acknowledged in publications and products that
  use the software.
- USGS and the United States Government provide no warranty, assume no responsibility, have
  no support obligation, and the user assumes all risk arising from use or performance.

The complete notice accompanies the installed `phreeqc` distribution and the official USGS
distribution. This application does not modify the PHREEQC engine or `pitzer.dat`; it builds
inputs, executes the engine, and presents its outputs.

## `phreeqc` Python binding

The application directly depends on
[`phreeqc` 1.1.1](https://github.com/haohanyang/phreeqc), maintained by Haohan Yang. The
binding is distributed under the MIT License:

> MIT License — Copyright (c) 2024 Haohan Yang. Permission is granted, free of charge, to
> use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
> software, provided the copyright and permission notice are included. The software is
> provided “AS IS”, without warranty; the authors or copyright holders are not liable for
> claims or damages arising from its use.

The complete binding license is included in the installed Python package and its source
repository.

## Streamlit

The user interface directly depends on [Streamlit](https://github.com/streamlit/streamlit),
declared as `streamlit>=1.42,<2`. Streamlit is distributed under the
[Apache License 2.0](https://github.com/streamlit/streamlit/blob/develop/LICENSE). The
dependency is installed by the hosting or local Python environment and is not vendored in
this repository.

## NIST ThermoML reference data

The repository archives selected official ThermoML JSON records from the National Institute
of Standards and Technology Thermodynamics Research Center. They are used to transcribe
published reference values and preserve reproducibility. Each reference case retains the
originating publication citation, source URL, locator, and mapping assumptions. The source
manifest and file hashes are recorded in
[`docs/references/validation/README.md`](references/validation/README.md).

NIST states that data created by NIST employees are generally not subject to copyright in the
United States, may be reused worldwide on a non-exclusive and royalty-free basis, are
provided without warranty, and should be acknowledged; modified works should identify their
changes. See the official [NIST public data license](https://www.nist.gov/open/license).

The calculator is not affiliated with or endorsed by NIST, the Thermodynamics Research
Center, USGS, Streamlit, or the authors of the cited publications.

## Dependency maintenance

Runtime dependency versions are declared in `pyproject.toml` and the hosting requirements
files. Re-review this notice whenever a direct dependency, scientific database, archived
source dataset, or license changes.
