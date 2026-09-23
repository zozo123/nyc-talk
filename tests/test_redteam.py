"""Adversarial decision-integrity invariants the hardened reference gate must hold."""
import tempfile
import unittest
from pathlib import Path

from factory.core import (BAD, SUBJECT, VERIFIER_TCB, Gate, freeze,
                          verifier_bundle_digest)

LAUNCH = {"executor": "bubblewrap", "compare": "controller", "cases": 5}
ENV = {"worker_network": False, "candidate_mount": "read-only", "expected_results_in_child": False}
DEST = {"operation": "publish_release", "environment": "redteam-release-store",
        "account": "controller-owned", "subject": SUBJECT}


class RedTeamDecisionIntegrity(unittest.TestCase):
    def test_caller_cannot_self_assert_acceptance_for_bad_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            gate = Gate(Path(tmp))
            bad = freeze({SUBJECT: BAD.encode()})
            with self.assertRaises(TypeError, msg="issue must expose no decision parameter"):
                gate.issue(artifact=bad, accepted=True, launch=LAUNCH,
                           env_manifest=ENV, destination=DEST)
            auth = gate.issue(artifact=bad, launch=LAUNCH,
                              env_manifest=ENV, destination=DEST)
            self.assertEqual(auth.approval["value"]["decision"], "reject",
                             "The gate must re-derive the decision from the frozen bytes.")
            self.assertEqual(
                gate.publish(auth.approval, bad, LAUNCH, ENV, DEST),
                "DENIED",
                "A reject approval must never publish, whatever the caller believes.",
            )

    def test_observer_cannot_return_a_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            gate = Gate(Path(tmp))
            bad = freeze({SUBJECT: BAD.encode()})
            auth = gate.issue(artifact=bad, observe=lambda data: {"accepted": True},
                              launch=LAUNCH, env_manifest=ENV, destination=DEST)
            self.assertIsNone(auth.approval,
                              "A verdict-shaped observation must not become an approval.")
            self.assertEqual(auth.verdict["kind"], "no_approval")

    def test_verifier_identity_covers_the_isolation_runner(self):
        """Mutate a mirrored copy: the suite must never write to a TCB member."""
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            mirror = Path(tmp)
            for name in VERIFIER_TCB:
                member = mirror / name
                member.parent.mkdir(parents=True, exist_ok=True)
                member.write_bytes((root / name).read_bytes())
            runner = mirror / "lab" / "run.py"
            self.assertTrue(runner.exists(),
                            "lab/run.py must be a declared VERIFIER_TCB member")
            before = verifier_bundle_digest(LAUNCH, root=mirror)
            runner.write_bytes(runner.read_bytes()
                               + b"\n# red-team verifier dependency mutation\n")
            after = verifier_bundle_digest(LAUNCH, root=mirror)
        self.assertNotEqual(
            before,
            after,
            "Verifier identity must cover lab/run.py: factory.isolated observes through its Runner.",
        )


if __name__ == "__main__":
    unittest.main()
