# PHREEQC databases

`pitzer.dat` is an unmodified, byte-for-byte copy of the official USGS coupled PHREEQC
database repository file at commit
`3ff9be2f12bf44c94b95731c7d8b1ca4a847718c` (2026-01-05). It was verified against the
[upstream file](https://github.com/usgs-coupled-subtrees/phreeqc3-database/blob/3ff9be2f12bf44c94b95731c7d8b1ca4a847718c/pitzer.dat)
on 2026-08-26.

File identity:

- size: 37,225 bytes;
- encoding: Windows-1252 (`cp1252`);
- SHA-256: `3640e62aee63a118f800b115b46a2760576e63e05e1792022315a28f75dbe9bb`.

The current Python binding reports PHREEQC `3.8.6-17100-x64`, while this database is newer
than the database shipped in that named engine release. The pairing loads and passes the
current regression tests, but release approval still requires either version alignment or
explicit compatibility validation.

See the full [database audit](../../docs/pitzer-database-audit.md) for parameter inventory,
support classification, redox constraints, and remaining validation work.

Database files are scientific inputs and must be reviewed like code. For every update,
record:

- upstream source and retrieval date;
- upstream and application versions;
- SHA-256 checksum;
- whether the file was modified;
- supported model/species changes;
- regression-test results.

The runtime path is defined once in `pitzer_calculator.config.DEFAULT_DATABASE_PATH`.
