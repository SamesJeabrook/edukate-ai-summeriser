import json
from dataclasses import asdict
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from edukate_progress_summariser.alerts import build_alert_payload
from edukate_progress_summariser.models import EscalationAlert


ROOT = Path(__file__).resolve().parents[2]


class AlertPayloadContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / "specs/001-cohort-progress-summary/contracts/output-schema.json").read_text())

    def test_schema_declares_canonical_result_and_payload_fields(self):
        self.assertEqual(self.schema["title"], "Cohort Progress Result")
        self.assertEqual(
            self.schema["required"],
            ["status", "summary", "alerts", "alert_payload", "metadata"],
        )
        self.assertEqual(
            self.schema["properties"]["alert_payload"]["required"],
            ["cohort_context", "alerts", "human_review_disclaimer"],
        )

    def test_payload_contains_required_alert_fields_and_disclaimer(self):
        alert = EscalationAlert(
            learner_reference="learner-abc",
            learner_name="Test Learner",
            severity="high",
            category="contact_recency",
            triggering_evidence=("days_since_last_meeting=45",),
            explanation="Contact is stale.",
            recommended_follow_up="Review contact history.",
            evidence_complete=True,
        )
        payload = build_alert_payload(123, (), (alert,), "AI-generated content supports human review only.")
        serialised = asdict(payload)
        self.assertEqual(serialised["cohort_context"]["employer_id"], 123)
        self.assertEqual(len(serialised["alerts"]), 1)
        self.assertEqual(
            set(serialised["alerts"][0]),
            {
                "learner_reference",
                "learner_name",
                "severity",
                "category",
                "triggering_evidence",
                "explanation",
                "recommended_follow_up",
                "evidence_complete",
            },
        )
        self.assertTrue(serialised["human_review_disclaimer"])

    def test_payload_is_channel_neutral(self):
        source = build_alert_payload(123, (), (), "Review by a human.")
        self.assertNotIn("slack", repr(source).lower())
        self.assertNotIn("email", repr(source).lower())
        self.assertEqual(source.cohort_context, {"employer_id": 123})


if __name__ == "__main__":
    unittest.main()
