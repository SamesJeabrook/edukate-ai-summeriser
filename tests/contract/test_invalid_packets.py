import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from edukate_progress_summariser.validation import ValidationError, load_json_file, validate_packet


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


class InvalidPacketContractTests(unittest.TestCase):
    def test_malformed_json_is_rejected(self):
        with self.assertRaises(ValidationError) as context:
            load_json_file(DATA / "invalid-malformed-json.json")
        self.assertIn("malformed JSON", str(context.exception))

    def test_schema_and_data_type_fixtures_are_rejected_with_field_paths(self):
        expected_fields = {
            "invalid-missing-employer-id.json": "packet.employer_id",
            "invalid-empty-learners.json": "packet.learners",
            "invalid-learner-field-types.json": "packet.learners[0].otj_hours",
            "invalid-inconsistent-dates.json": "packet.learners[0].meetings[0].date_timestamp",
            "invalid-duplicate-learner-references.json": "packet.learners[1]",
        }
        for filename, field_path in expected_fields.items():
            with self.subTest(filename=filename):
                with self.assertRaises(ValidationError) as context:
                    validate_packet(load_json_file(DATA / filename))
                self.assertIn(field_path, str(context.exception))

    def test_insufficient_evidence_fixture_is_valid_but_has_no_complete_risk_basis(self):
        packet = validate_packet(load_json_file(DATA / "invalid-insufficient-evidence.json"))
        learner = packet.learners[0]
        self.assertIsNone(learner.otj_hours)
        self.assertIsNone(learner.days_since_last_meeting)

    def test_all_invalid_fixtures_are_json_files(self):
        fixtures = sorted(DATA.glob("invalid-*.json"))
        self.assertEqual(len(fixtures), 14)
        for fixture in fixtures:
            with self.subTest(fixture=fixture.name):
                if fixture.name != "invalid-malformed-json.json":
                    json.loads(fixture.read_text(encoding="utf-8"))

    def test_new_progress_field_fixtures_are_rejected(self):
        expected_fields = {
            "invalid-sessions-type.json": "sessions_attended",
            "invalid-assessments-negative.json": "assessments_submitted",
            "invalid-at-risk-flag-shape.json": "at_risk_flags[0]",
            "invalid-at-risk-flag-values.json": "at_risk_flags[0].code",
            "invalid-duplicate-at-risk-flags.json": "at_risk_flags[1].code",
        }
        for filename, field in expected_fields.items():
            with self.subTest(filename=filename):
                with self.assertRaises(ValidationError) as context:
                    validate_packet(load_json_file(DATA / filename))
                self.assertIn(field, str(context.exception))


if __name__ == "__main__":
    unittest.main()
