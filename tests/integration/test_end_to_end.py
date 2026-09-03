import json
import os
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]


class EndToEndTests(unittest.TestCase):
    def run_cli(self, fixture, output_format="canonical"):
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(ROOT / "src")
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "edukate_progress_summariser",
                f"data/{fixture}",
                "--provider",
                "fake",
                "--format",
                output_format,
            ],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
        )

    def test_valid_packet_produces_complete_result_and_traceability_metadata(self):
        completed = self.run_cli("valid-input.json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["status"], "validated")
        self.assertEqual(result["summary"]["facts"]["learner_count"], 100)
        self.assertIsInstance(result["alerts"], list)
        self.assertIn("human_review_disclaimer", result["alert_payload"])
        self.assertEqual(result["metadata"]["model"], "fake-model")
        self.assertEqual(len(result["metadata"]["input_packet_reference"]), 16)
        self.assertNotIn("Laura Davis", completed.stderr)

    def test_provider_fallback_keeps_facts_and_marks_status(self):
        completed = self.run_cli("valid-input.json")
        self.assertEqual(completed.returncode, 0)
        result = json.loads(completed.stdout)
        self.assertIn(result["status"], {"validated", "interpretation_unavailable"})
        self.assertIn("facts", result["summary"])

    def test_invalid_packet_has_no_result(self):
        completed = self.run_cli("invalid-learner-field-types.json")
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "")
        self.assertIn("packet.learners[0].otj_hours", completed.stderr)
        self.assertNotIn("forty", completed.stderr)


if __name__ == "__main__":
    unittest.main()
