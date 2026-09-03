import os
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
INVALID_FIXTURES = {
    "invalid-malformed-json.json",
    "invalid-missing-employer-id.json",
    "invalid-empty-learners.json",
    "invalid-learner-field-types.json",
    "invalid-inconsistent-dates.json",
    "invalid-duplicate-learner-references.json",
}


class CLIErrorContractTests(unittest.TestCase):
    def run_cli(self, fixture):
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(ROOT / "src")
        return subprocess.run(
            [sys.executable, "-m", "edukate_progress_summariser", f"data/{fixture}", "--provider", "fake"],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
        )

    def test_invalid_packets_fail_without_partial_output_or_sensitive_stderr(self):
        for fixture in INVALID_FIXTURES:
            with self.subTest(fixture=fixture):
                completed = self.run_cli(fixture)
                self.assertNotEqual(completed.returncode, 0)
                self.assertEqual(completed.stdout, "")
                self.assertNotIn("Test Learner", completed.stderr)
                self.assertNotIn("Private Learner", completed.stderr)
                self.assertNotIn("TEST_CREDENTIAL_SHOULD_NOT_BE_LOGGED_OR_SENT", completed.stderr)

    def test_insufficient_evidence_is_not_treated_as_malformed_input(self):
        completed = self.run_cli("invalid-insufficient-evidence.json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotIn("error", completed.stderr.lower())

    def test_untrusted_but_parseable_packets_are_processed_without_sensitive_stderr(self):
        for fixture in ("invalid-credential-like-data.json", "invalid-prompt-injection-content.json"):
            with self.subTest(fixture=fixture):
                completed = self.run_cli(fixture)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertEqual(completed.stderr, "")
                self.assertNotIn("TEST_CREDENTIAL_SHOULD_NOT_BE_LOGGED_OR_SENT", completed.stdout)


if __name__ == "__main__":
    unittest.main()
