# Baseline and source identity

Reviewed upstream baseline: `4b06c519cff2ffcc69a8471f4f861a03f08f93a0`.

Clean baseline capture: Actions run `35506381406`, packaging commit `418805e2a65cdcb4e9ed9991a18a9278b6c3cbe8`. Only the packaging workflow differed from baseline. Its isolated lab completed 29 assertions and its local factory completed six.

Final active record pins: `evidence/results.json` (lab source map), `evidence/factory-results.json` and `evidence/http-results.json` (complete factory source maps). The final workflow exports its exact commit ID and source archive. Refer to those rather than assuming a mutable branch is a pin.

`factory/` is our reference implementation, not a discovered customer or vendor incident. Its local executor is not an OS security boundary. The fixed task is `lock-admin`, policy `admin-requires-auth-v1`, five explicit cases.

Earlier optional Boat results are retained only in `evidence/archive/factory-before-final.json`. They were not rerun against final source. No cloud credential is required for the final talk, tests or deck. See [DOSSIER.md](DOSSIER.md) for the full scope and classification.
