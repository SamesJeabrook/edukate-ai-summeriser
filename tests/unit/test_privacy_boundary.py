from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from edukate_progress_summariser.privacy import build_ai_evidence, redact_sensitive


class PrivacyBoundaryTests(unittest.TestCase):
    def test_ai_evidence_excludes_names_direct_identifiers_credentials_and_free_text(self):
        packet = {
            "employer_id": 123,
            "api_key": "TEST_SECRET_VALUE",
            "learners": [{
                "name": "Private Learner",
                "learner_id": "direct-id-123",
                "product": "Example",
                "otj_hours": 20,
                "meetings": [],
                "workshops": [],
                "days_since_last_meeting": None,
                "notes": "Sensitive learner note",
            }],
        }
        evidence = build_ai_evidence(packet)
        evidence_text = repr(evidence)
        for sensitive_value in ("Private Learner", "direct-id-123", "TEST_SECRET_VALUE", "Sensitive learner note"):
            self.assertNotIn(sensitive_value, evidence_text)
        self.assertIn("learner_reference", evidence["learners"][0])

    def test_redaction_removes_sensitive_values_recursively(self):
        value = {
            "name": "Private Learner",
            "nested": {"token": "secret", "safe": "value"},
            "items": [{"notes": "private"}],
        }
        redacted = redact_sensitive(value)
        self.assertEqual(redacted["name"], "[REDACTED]")
        self.assertEqual(redacted["nested"]["token"], "[REDACTED]")
        self.assertEqual(redacted["nested"]["safe"], "value")
        self.assertEqual(redacted["items"][0]["notes"], "[REDACTED]")

    def test_ai_evidence_retains_only_minimum_progress_fields(self):
        evidence = build_ai_evidence({
            "employer_id": 123,
            "learners": [{
                "name": "Private Learner",
                "product": "Example",
                "otj_hours": 20,
                "meetings": [{"private": "detail"}],
                "workshops": [],
                "days_since_last_meeting": 4,
            }],
        })
        self.assertEqual(
            set(evidence["learners"][0]),
            {"learner_reference", "product", "otj_hours", "meeting_count", "workshop_count", "days_since_last_meeting"},
        )


if __name__ == "__main__":
    unittest.main()
