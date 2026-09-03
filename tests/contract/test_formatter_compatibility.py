from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from edukate_progress_summariser.ai_service import FakeAIProvider
from edukate_progress_summariser.summariser import SummaryService
from edukate_progress_summariser.validation import validate_packet


class FormatterCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = validate_packet({
            "employer_id": 123,
            "learners": [{
                "name": "Needs Follow-up",
                "product": "Example",
                "otj_hours": 20,
                "meetings": [],
                "workshops": [],
                "days_since_last_meeting": 45,
            }],
        })

    def test_canonical_payload_can_be_rendered_without_changing_evidence(self):
        result = SummaryService(FakeAIProvider()).generate(self.packet)
        payload = result.alert_payload
        rendered = "\n".join(
            f"{alert.severity.upper()}: {alert.learner_reference} | {alert.category} | {alert.explanation}"
            for alert in payload.alerts
        )
        self.assertIn("HIGH: Needs Follow-up", rendered)
        self.assertEqual(payload.alerts, result.alerts)
        self.assertIn("human review", payload.human_review_disclaimer.lower())

    def test_future_formatter_can_consume_same_structured_fields(self):
        result = SummaryService(FakeAIProvider()).generate(self.packet)
        payload = result.alert_payload

        def future_formatter(alert_payload):
            return {
                "title": f"Cohort {alert_payload.cohort_context['employer_id']}",
                "items": [alert.category for alert in alert_payload.alerts],
                "disclaimer": alert_payload.human_review_disclaimer,
            }

        formatted = future_formatter(payload)
        self.assertEqual(formatted["title"], "Cohort 123")
        self.assertEqual(formatted["items"], ["contact_recency"])
        self.assertTrue(formatted["disclaimer"])


if __name__ == "__main__":
    unittest.main()
