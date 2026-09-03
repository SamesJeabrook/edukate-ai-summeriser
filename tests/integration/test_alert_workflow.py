from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from edukate_progress_summariser.ai_service import FakeAIProvider
from edukate_progress_summariser.models import InterventionRule
from edukate_progress_summariser.rules import default_rules
from edukate_progress_summariser.summariser import SummaryService
from edukate_progress_summariser.validation import validate_packet


class AlertWorkflowTests(unittest.TestCase):
    def make_packet(self):
        return validate_packet({
            "employer_id": 123,
            "learners": [
                {
                    "name": "Laura Davis",
                    "product": "Example",
                    "otj_hours": 40,
                    "meetings": [],
                    "workshops": [],
                    "days_since_last_meeting": 45,
                },
                {
                    "name": "Charles Fleming",
                    "product": "Example",
                    "otj_hours": 40,
                    "meetings": [],
                    "workshops": [],
                    "days_since_last_meeting": None,
                },
            ],
        })

    def test_summary_contains_multiple_alerts_and_privacy_safe_ai_evidence(self):
        provider = FakeAIProvider()
        result = SummaryService(provider, rules=default_rules()).generate(self.make_packet())
        self.assertEqual(len(result.alerts), 1)
        alert = result.alerts[0]
        self.assertEqual(alert.learner_name, "Laura Davis")
        self.assertTrue(alert.learner_reference)
        self.assertNotEqual(alert.learner_reference, alert.learner_name)
        evidence_text = repr(provider.last_evidence)
        self.assertNotIn("Laura Davis", evidence_text)
        self.assertNotIn("Charles Fleming", evidence_text)
        self.assertEqual(result.alert_payload.alerts, result.alerts)
        self.assertTrue(result.alert_payload.human_review_disclaimer)

    def test_account_manager_output_keeps_name_while_ai_uses_derived_reference(self):
        provider = FakeAIProvider()
        result = SummaryService(provider, rules=default_rules()).generate(self.make_packet())
        output_alert = result.alert_payload.alerts[0]
        ai_learner = provider.last_evidence["learners"][0]
        self.assertEqual(output_alert.learner_name, "Laura Davis")
        self.assertEqual(output_alert.learner_reference, "Laura Davis")
        self.assertEqual(len(ai_learner["learner_reference"]), len("learner-0000000000000000"))
        self.assertNotEqual(ai_learner["learner_reference"], output_alert.learner_reference)


if __name__ == "__main__":
    unittest.main()
