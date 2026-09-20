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
factory = json.loads((ROOT / "evidence/factory-results.json").read_text())
for name, expected in factory["source_sha256"].items():
    actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"Factory evidence is stale for {name}; rerun make record-factory.")
local = factory["local"]
if local["status"] != "PASS" or any(x["status"] == "FAIL" for x in local["checks"]):
    raise SystemExit("Recorded factory checks failed.")
passed = sum(x["status"] == "PASS" for x in record["checks"])
skipped = sum(x["status"] == "SKIP" for x in record["checks"])
factory_passed = sum(x["status"] == "PASS" for x in local["checks"])
isolated = record["mode"] == "isolated" and record["status"] == "PASS" and not skipped
required = {"isolation.namespaces", "mount.before", "mount.after", "mount.positive",
            "egress.bypass", "verifier.after", "gate.substitution", "gate.stale_run",
            "gate.verifier_changed", "final.task"}
if isolated and not required.issubset({r["check"] for r in record["checks"] if r["status"] == "PASS"}):
    raise SystemExit("Missing required isolated checks.")
scope = "Recorded Linux isolation run + factory" if isolated else "Recorded reference run + factory"
mount = "Observed with real bind mounts" if isolated else "Expected outcomes / mount check not yet executed"
network = "Direct host-loopback probe: unreachable" if isolated else "Network namespace check: not yet executed"
status = f"{passed} lab checks passed, {factory_passed} factory checks passed" + (
    f", {skipped} lab integration groups skipped" if skipped else "")
text = "\n".join([
    r"\newcommand{\evidencescope}{" + scope + "}",
    r"\newcommand{\mountscope}{" + mount + "}",
    r"\newcommand{\networkscope}{" + network + "}",
    r"\newcommand{\evidencecount}{" + status + "}",
]) + "\n"
(ROOT / "slides/evidence.tex").write_text(text)
print(scope + ": " + status)
