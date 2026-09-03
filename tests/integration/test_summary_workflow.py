from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from edukate_progress_summariser.ai_service import FakeAIProvider
from edukate_progress_summariser.summariser import SummaryService
from edukate_progress_summariser.validation import load_json_file, validate_packet


class FailingProvider(FakeAIProvider):
    def interpret(self, evidence):
        self.calls += 1
        self.last_evidence = evidence
        raise RuntimeError("provider unavailable")


class SummaryWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = validate_packet(load_json_file(Path("data/valid-input.json")))

    def test_summary_separates_facts_from_labelled_interpretation(self):
        provider = FakeAIProvider(model="test-model", interpretation="The cohort shows mixed progress.")
        result = SummaryService(provider).generate(self.packet)
        self.assertEqual(result.status.value, "validated")
        self.assertEqual(result.facts.learner_count, 100)
        self.assertEqual(result.interpretation, "The cohort shows mixed progress.")
        self.assertIn("AI", result.interpretation_label)
        self.assertTrue(result.evidence_status)
        self.assertEqual(result.metadata.model, "test-model")
        self.assertEqual(provider.calls, 1)

    def test_model_evidence_has_no_learner_names_and_facts_are_computed_first(self):
        provider = FakeAIProvider()
        result = SummaryService(provider).generate(self.packet)
        evidence_text = str(provider.last_evidence)
        self.assertNotIn(self.packet.learners[0].name, evidence_text)
        self.assertEqual(result.facts.learner_count, len(self.packet.learners))
        self.assertIn("learners", provider.last_evidence)

    def test_provider_failure_preserves_facts_and_marks_interpretation_unavailable(self):
        provider = FailingProvider(model="test-model")
        result = SummaryService(provider).generate(self.packet)
        self.assertEqual(result.status.value, "interpretation_unavailable")
        self.assertIsNone(result.interpretation)
        self.assertEqual(result.facts.learner_count, 100)
        self.assertIn("unavailable", result.evidence_status.lower())

    def test_corrected_fields_and_flags_are_available_to_summary_without_flag_descriptions(self):
        packet = validate_packet({
            "employer_id": 123,
            "learners": [{
                "name": "Flagged Learner",
                "product": "Example",
                "sessions_attended": 4,
                "assessments_submitted": 2,
                "otj_hours": 10,
                "meetings": [],
                "workshops": [],
                "days_since_last_meeting": 1,
                "at_risk_flags": [{"code": "low_attendance", "severity": "high", "description": "Do not send this."}],
            }],
        })
        provider = FakeAIProvider()
        result = SummaryService(provider).generate(packet)
        self.assertEqual(result.facts.sessions_attended, 4)
        self.assertEqual(result.facts.assessments_submitted, 2)
        self.assertEqual(result.facts.at_risk_flags[0].severity, "high")
        self.assertNotIn("Do not send this", repr(provider.last_evidence))


if __name__ == "__main__":
    unittest.main()
