# Baseline and scope pins

| Object | Pin / source |
|---|---|
| Audited original repository | `4b06c519cff2ffcc69a8471f4f861a03f08f93a0` |
| Archived gate | `research/baseline/core.py`, unchanged from that commit |
| Audit reproduction | `python3 tools/audit_baseline.py`; SHA-256 in `evidence/baseline-audit.json` |
| Current experiments | Exact per-file SHA-256 sets in each record under `evidence/` |
| Task | `lock-admin`; policy `admin-requires-auth-v1`; five CLI cases |
| Isolation fixture | `lab/run.py` and `factory/isolated.py`; disposable Linux + bubblewrap |
| Presentation content | Canonical `slides/talk.tex`; compiled Beamer PDF and exported manuscript |

The source hashes identify the executed implementation, including uncommitted record-generation work. They do not pretend a build's initial checkout commit already contains subsequently generated changes. The GitHub commit containing the final records is an additional immutable checkout point.

The intentionally weakened answer-key configuration is a positive detector for a known mechanism. The independent controller is a narrow reference design, not an audited production factory. No proprietary provider, real credential, or customer dataset is in scope.

Optional Boat integration is excluded from the final evidence claim. It is retained for historical reproducibility, not asserted as a fresh cloud run.
