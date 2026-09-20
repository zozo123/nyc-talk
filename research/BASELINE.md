# Pinned baseline

Audit base: **`4b06c519cff2ffcc69a8471f4f861a03f08f93a0`** in `zozo123/nyc-talk`.

The finalization branch began with a source-capture CI commit, `418805e2a65cdcb4e9ed9991a18a9278b6c3cbe8`. Its retained source archive supplied the cold local checkout. The original laboratory implementation is unchanged by this finalization.

Task: `lock-admin`; policy: `admin-requires-auth-v1`; five command-line cases. `admin:none` and `admin:expired` require 401; `admin:user` requires 403; authenticated admin and public requests require 200.

The final run's exact revision is written into the CI artifact's `build/release/COMMIT.txt`. Per-source SHA-256 values are in the evidence JSON. The source archive and output files are included in the artifact checksum manifest. A hash identifies content, not trustworthiness or successful execution.

This is our reference implementation. The weak report and dependency configurations are deliberately constructed. There is no assertion of an unknown production incident or vendor vulnerability.

Boat is optional infrastructure. It was not rerun for this revision. No cloud credential is required for the default path.
