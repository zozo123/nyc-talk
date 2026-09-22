"""Adversarial security invariants. These are expected to fail until the reference gate is hardened."""
import tempfile
import unittest
from pathlib import Path

from factory.core import BAD, SUBJECT, Gate, freeze, verifier_bundle_digest

LAUNCH = {"executor": "bubblewrap", "compare": "controller", "cases": 5}
ENV = {"worker_network": False, "candidate_mount": "read-only", "expected_results_in_child": False}


class RedTeamDecisionIntegrity(unittest.TestCase):
    def test_caller_cannot_self_assert_acceptance_for_bad_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            gate = Gate(Path(tmp))
            bad = freeze({SUBJECT: BAD.encode()})
            approval = gate.issue(
                artifact=bad,
                accepted=True,
                launch=LAUNCH,
                env_manifest=ENV,
            )
            self.assertEqual(
                gate.publish(approval, bad, LAUNCH, ENV),
                "DENIED",
                "Gate.issue currently trusts caller-supplied accepted=True instead of a verifier-owned decision.",
            )

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
            "Verifier identity ignores lab/run.py even though factory.isolated uses Runner from that file.",
        )


if __name__ == "__main__":
    unittest.main()
