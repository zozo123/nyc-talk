"""Adversarial decision-integrity invariants the hardened reference gate must hold."""
import tempfile
import unittest
from pathlib import Path

from factory.core import BAD, SUBJECT, Gate, freeze, verifier_bundle_digest

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
        runner = Path(__file__).resolve().parents[1] / "lab" / "run.py"
        original = runner.read_bytes()
        before = verifier_bundle_digest(LAUNCH)
        try:
            runner.write_bytes(original + b"\n# red-team verifier dependency mutation\n")
            after = verifier_bundle_digest(LAUNCH)
        finally:
            runner.write_bytes(original)
        self.assertNotEqual(
            before,
            after,
            "Verifier identity must cover lab/run.py: factory.isolated observes through its Runner.",
        )


if __name__ == "__main__":
    unittest.main()
