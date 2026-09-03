from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from edukate_progress_summariser.config import AppConfig
from edukate_progress_summariser.models import ActivityRecord, LearnerProgress, ProgressPacket
from edukate_progress_summariser.privacy import build_ai_evidence, derive_learner_reference, redact_sensitive
from edukate_progress_summariser.validation import ValidationError, parse_date, validate_packet


class FoundationTests(unittest.TestCase):
    def test_domain_models_construct_with_typed_values(self):
        activity = ActivityRecord(datetime(2026, 8, 1, tzinfo=timezone.utc), "Coach Meeting", "meeting")
        learner = LearnerProgress("Test Learner", "Example", 10.0, (activity,), (), 3)
        packet = ProgressPacket(123, (learner,))
        self.assertEqual(packet.learners[0].otj_hours, 10.0)
        self.assertEqual(packet.learners[0].meetings[0].kind, "meeting")

    def test_configuration_uses_environment_values_without_exposing_secrets(self):
        config = AppConfig.from_env({
            "EDUKATE_MODEL": "replacement-model",
            "EDUKATE_MAX_LEARNERS": "12",
            "EDUKATE_MAX_ACTIVITY_RECORDS": "100",
            "OPENAI_API_KEY": "must-not-become-a-config-field",
        })
        self.assertEqual(config.model, "replacement-model")
        self.assertEqual(config.max_learners, 12)
        self.assertEqual(config.max_activity_records, 100)
        self.assertFalse(hasattr(config, "api_key"))

    def test_invalid_environment_limits_fall_back_to_safe_defaults(self):
        config = AppConfig.from_env({"EDUKATE_MAX_LEARNERS": "-1", "EDUKATE_MAX_ACTIVITY_RECORDS": "bad"})
        self.assertEqual(config.max_learners, 500)
        self.assertEqual(config.max_activity_records, 5000)

    def test_date_parser_rejects_invalid_and_future_dates(self):
        with self.assertRaises(ValidationError) as invalid:
            parse_date("not-a-date", "packet.learners[0].meetings[0].date_timestamp")
        self.assertIn("invalid date", str(invalid.exception))
        with self.assertRaises(ValidationError) as future:
            parse_date("2099-01-01T00:00:00Z", "activity.date_timestamp", datetime(2026, 9, 3, tzinfo=timezone.utc))
        self.assertIn("future date", str(future.exception))

    def test_reference_is_stable_and_redaction_is_recursive(self):
        first = derive_learner_reference(123, "Test Learner", 0)
        second = derive_learner_reference(123, "Test Learner", 0)
        self.assertEqual(first, second)
        value = {"name": "Test Learner", "nested": {"api_key": "secret", "value": 0}}
        self.assertEqual(redact_sensitive(value), {"name": "[REDACTED]", "nested": {"api_key": "[REDACTED]", "value": 0}})

    def test_ai_evidence_excludes_name_notes_and_credentials(self):
        evidence = build_ai_evidence({
            "employer_id": 123,
            "api_key": "secret",
            "learners": [{
                "name": "Test Learner",
                "product": "Example",
                "otj_hours": 20,
                "meetings": [],
                "workshops": [],
                "days_since_last_meeting": None,
                "notes": "private",
            }],
        })
        evidence_text = str(evidence)
        self.assertNotIn("Test Learner", evidence_text)
        self.assertNotIn("secret", evidence_text)
        self.assertNotIn("private", evidence_text)
        self.assertIn("learner_reference", evidence_text)

    def test_valid_packet_is_normalised(self):
        packet = validate_packet({
            "employer_id": 123,
            "learners": [{
                "name": "Test Learner",
                "product": "Example",
                "otj_hours": 0,
                "meetings": [],
                "workshops": [],
                "days_since_last_meeting": None,
            }],
        })
        self.assertEqual(packet.learners[0].otj_hours, 0.0)
        self.assertIsNone(packet.learners[0].days_since_last_meeting)

    def test_invalid_field_type_reports_field_path(self):
        with self.assertRaises(ValidationError) as context:
            validate_packet({
                "employer_id": 123,
                "learners": [{
                    "name": "Test Learner",
                    "product": "Example",
                    "otj_hours": "forty",
                    "meetings": [],
                    "workshops": [],
                    "days_since_last_meeting": None,
                }],
            })
        self.assertIn("packet.learners[0].otj_hours", str(context.exception))


if __name__ == "__main__":
    unittest.main()
