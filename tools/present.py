#!/usr/bin/env python3
"""Display one act's recorded observations without revealing subsequent acts."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTS = {
    "credentials": ["credentials.before", "credentials.after", "credentials.positive",
                    "credentials.fixture-expired", "credentials.fixture-wrong-audience"],
    "mounts": ["mount.before", "mount.after", "mount.positive"],
    "egress": ["egress.before", "egress.recipient", "egress.payload", "egress.url",
               "egress.no_delivery", "egress.bypass", "egress.positive"],
    "verifier": ["verifier.before", "verifier.after", "verifier.positive"],
    "acceptance": ["gate.invalid", "gate.substitution", "gate.cross_run",
                   "gate.stale_run", "gate.verifier_changed", "gate.forgery",
                   "gate.positive", "gate.replay"],
    "history": ["history.rewrite"],
    "final": ["final.task"],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("act", choices=ACTS)
    parser.add_argument("--record", type=Path, default=ROOT / "evidence/results.json")
    args = parser.parse_args()
    record = json.loads(args.record.read_text())
    if record.get("mode") != "isolated" or record.get("status") != "PASS":
        raise SystemExit("Presentation requires a successful isolated record.")
    sources = record.get("source_sha256", {})
    if set(sources) != {str(p.relative_to(ROOT)) for p in (ROOT / "lab").glob("*.py")}:
        raise SystemExit("Recorded lab source set does not match this checkout.")
    for path, expected in sources.items():
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise SystemExit("Stale evidence: " + path)
    checks = record.get("checks", [])
    if any(c.get("status") != "PASS" for c in checks):
        raise SystemExit("Recorded checks contain a failure or skip.")
    indexed = {c["check"]: c for c in checks}
    names = ["isolation.namespaces", *ACTS[args.act]]
    if any(name not in indexed for name in names):
        raise SystemExit("Record is missing required observations for this act.")

    print("RECORDED LINUX OBSERVATIONS / " + args.act.upper())
    print("Record: " + str(args.record.resolve()))
    print("Lab source hashes match this checkout. No new experiment is running.")
    print("CONFIRMED means the stated observation occurred, including unwanted success.")
    for name in ACTS[args.act]:
        print("\n" + name)
        print("  CONFIRMED: " + indexed[name]["detail"])


if __name__ == "__main__":
    main()
