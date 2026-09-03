from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from edukate_progress_summariser.metrics import calculate_facts
from edukate_progress_summariser.validation import load_json_file, validate_packet


class MetricsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = validate_packet(load_json_file(Path("data/valid-input.json")))

    def test_calculates_cohort_counts_and_hours(self):
        facts = calculate_facts(self.packet)
        self.assertEqual(facts.learner_count, 100)
        self.assertEqual(facts.meeting_count, 0 + sum(len(learner.meetings) for learner in self.packet.learners))
        self.assertEqual(facts.workshop_count, sum(len(learner.workshops) for learner in self.packet.learners))
        self.assertEqual(facts.total_otj_hours, sum(learner.otj_hours or 0 for learner in self.packet.learners))

    def test_preserves_missing_recency_and_counts_no_activity(self):
        facts = calculate_facts(self.packet)
        self.assertEqual(len(facts.recency_values), facts.learner_count)
        self.assertGreater(facts.learners_without_activity, 0)
        self.assertIn(None, facts.recency_values)

    def test_zero_hours_is_a_valid_measure(self):
        packet = validate_packet({
            "employer_id": 123,
            "learners": [{
                "name": "Zero Hours",
                "product": "Example",
                "otj_hours": 0,
                "meetings": [],
                "workshops": [],
                "days_since_last_meeting": None,
            }],
        })
        facts = calculate_facts(packet)
        self.assertEqual(facts.total_otj_hours, 0)
        self.assertFalse(any("hours" in limitation.lower() for limitation in facts.evidence_limitations))

    def test_missing_hours_is_reported_as_an_evidence_limitation(self):
        packet = validate_packet({
            "employer_id": 123,
            "learners": [{
                "name": "Missing Hours",
                "product": "Example",
                "otj_hours": None,
                "meetings": [],
                "workshops": [],
                "days_since_last_meeting": None,
            }],
        })
        facts = calculate_facts(packet)
        self.assertEqual(facts.total_otj_hours, 0)
        self.assertTrue(any("hours" in limitation.lower() for limitation in facts.evidence_limitations))

    def test_corrected_progress_fields_and_source_flags_are_aggregated(self):
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
                "at_risk_flags": [{"code": "low_attendance", "severity": "high"}],
            }],
        })
        facts = calculate_facts(packet)
        self.assertEqual(facts.sessions_attended, 4)
        self.assertEqual(facts.assessments_submitted, 2)
        self.assertEqual(facts.at_risk_flags[0].code, "low_attendance")


if __name__ == "__main__":
    unittest.main()
