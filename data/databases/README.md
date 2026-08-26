# PHREEQC databases

`pitzer.dat` is the database bundled with the original desktop prototype. Its upstream
version and exact provenance still need to be verified before public release.

Current repository file SHA-256:

`3640e62aee63a118f800b115b46a2760576e63e05e1792022315a28f75dbe9bb`

Database files are scientific inputs and must be reviewed like code. For every update,
record:

- upstream source and retrieval date;
- upstream and application versions;
- SHA-256 checksum;
- whether the file was modified;
- supported model/species changes;
- regression-test results.

The runtime path is defined once in `pitzer_calculator.config.DEFAULT_DATABASE_PATH`.
