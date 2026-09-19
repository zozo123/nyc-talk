#!/usr/bin/env python3
"""Check recorded evidence against the current lab source and generate slide labels."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
record = json.loads((ROOT / "evidence/results.json").read_text())
for name, expected in record["source_sha256"].items():
    actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"Evidence is stale for {name}; rerun the lab before building slides.")
if any(x["status"] == "FAIL" for x in record["checks"]):
    raise SystemExit("Recorded checks failed.")
passed = sum(x["status"] == "PASS" for x in record["checks"])
skipped = sum(x["status"] == "SKIP" for x in record["checks"])
isolated = record["mode"] == "isolated" and record["status"] == "PASS" and not skipped
required = {"isolation.namespaces", "mount.before", "mount.after", "mount.positive",
            "egress.bypass", "verifier.after", "gate.substitution", "gate.stale_run",
            "gate.verifier_changed", "final.task"}
if isolated and not required.issubset({r["check"] for r in record["checks"] if r["status"] == "PASS"}):
    raise SystemExit("Missing required isolated checks.")
scope = "Recorded Linux isolation run" if isolated else "Recorded reference run / kernel checks pending"
mount = "Observed with real bind mounts" if isolated else "Expected outcomes / mount check not yet executed"
network = "Direct host-loopback probe: unreachable" if isolated else "Network namespace check: not yet executed"
status = f"{passed} checks passed" + (f", {skipped} integration groups skipped" if skipped else "")
text = "\n".join([
    r"\newcommand{\evidencescope}{" + scope + "}",
    r"\newcommand{\mountscope}{" + mount + "}",
    r"\newcommand{\networkscope}{" + network + "}",
    r"\newcommand{\evidencecount}{" + status + "}",
]) + "\n"
(ROOT / "slides/evidence.tex").write_text(text)
print(scope + ": " + status)
