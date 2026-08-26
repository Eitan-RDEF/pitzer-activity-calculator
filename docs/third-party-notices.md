# Third-party notices

This file is a release checklist, not yet a complete legal notice.

## PHREEQC / IPHREEQC

The calculation engine is developed by the U.S. Geological Survey. The current binding
reports PHREEQC `3.8.6-17100-x64`. The USGS software page identifies PHREEQC source/usage as
public domain and supplies the official disclaimer. Before public release, reproduce the
applicable notice and disclaimer accurately and record the deployed engine build.

## `phreeqc` Python binding

The Python/C++ binding code is distributed under the MIT License and wraps IPHREEQC. Before
release, include its copyright notice, license text, pinned version, and repository URL.

## `pitzer.dat`

The bundled file is an unmodified copy of the official USGS database repository at commit
`3ff9be2f12bf44c94b95731c7d8b1ca4a847718c`, verified 2026-08-26. Its SHA-256 is
`3640e62aee63a118f800b115b46a2760576e63e05e1792022315a28f75dbe9bb`. See the
[database audit](pitzer-database-audit.md). Before release, reproduce the applicable USGS
notice and disclaimer and explain the engine/database version pairing.

## Streamlit and other dependencies

Generate a dependency inventory before release and preserve all notices required by direct
and redistributed dependencies.
