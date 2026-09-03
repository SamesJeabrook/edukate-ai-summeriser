import json
from pathlib import Path
import os
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]


class CLISummaryContractTests(unittest.TestCase):
    def run_cli(self, *arguments):
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(ROOT / "src")
        return subprocess.run(
            [sys.executable, "-m", "edukate_progress_summariser", *arguments],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
        )

    def test_canonical_output_contains_summary_and_metadata(self):
        completed = self.run_cli("data/valid-input.json", "--provider", "fake", "--format", "canonical")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        output = json.loads(completed.stdout)
        self.assertEqual(output["status"], "validated")
        self.assertIn("summary", output)
        self.assertIn("facts", output["summary"])
        self.assertIn("interpretation", output["summary"])
        self.assertIn("alert_payload", output)
        self.assertEqual(output["metadata"]["model"], "fake-model")

    def test_text_output_is_human_readable_and_labelled(self):
        completed = self.run_cli("data/valid-input.json", "--provider", "fake", "--format", "text")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Cohort Progress Summary", completed.stdout)
        self.assertIn("AI-generated interpretation", completed.stdout)
        self.assertIn("Evidence status", completed.stdout)
        self.assertNotIn("Laura Davis", completed.stderr)

    def test_corrected_packet_exposes_sessions_assessments_and_flags(self):
        completed = self.run_cli("data/valid-input.json", "--provider", "fake", "--format", "canonical")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        output = json.loads(completed.stdout)
        facts = output["summary"]["facts"]
        self.assertGreater(facts["sessions_attended"], 0)
        self.assertIsNone(facts["assessments_submitted"])
        self.assertEqual(facts["at_risk_flags"], [])


if __name__ == "__main__":
    unittest.main()
