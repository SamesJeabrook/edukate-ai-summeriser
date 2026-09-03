from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from edukate_progress_summariser.alerts import evaluate_alerts
from edukate_progress_summariser.models import InterventionRule
from edukate_progress_summariser.rules import default_rules, select_rules
from edukate_progress_summariser.validation import validate_packet


class AlertRuleTests(unittest.TestCase):
    def make_packet(self):
        return validate_packet({
            "employer_id": 123,
            "learners": [
                {
                    "name": "Stale Learner",
                    "product": "Example",
                    "otj_hours": 40,
                    "meetings": [],
                    "workshops": [],
                    "days_since_last_meeting": 45,
                },
                {
                    "name": "Active Learner",
                    "product": "Example",
                    "otj_hours": 40,
                    "meetings": [],
                    "workshops": [],
                    "days_since_last_meeting": 2,
                },
                {
                    "name": "Unknown Recency",
                    "product": "Example",
                    "otj_hours": 40,
                    "meetings": [],
                    "workshops": [],
                    "days_since_last_meeting": None,
                },
            ],
        })

    def test_defaults_match_stale_contact_and_preserve_severity(self):
        rules = default_rules()
        alerts = evaluate_alerts(self.make_packet(), rules)
        stale = next(alert for alert in alerts if alert.learner_name == "Stale Learner")
        self.assertEqual(stale.severity, "high")
        self.assertTrue(stale.evidence_complete)
        self.assertIn("45", " ".join(stale.triggering_evidence))
        self.assertFalse(any(alert.learner_name == "Active Learner" for alert in alerts))

    def test_employer_override_replaces_matching_default_threshold(self):
        defaults = default_rules()
        override = InterventionRule(
            rule_id="stale-contact",
            version="employer-v2",
            category="contact_recency",
            severity="medium",
            metric="days_since_last_meeting",
            threshold=60,
            operator=">=",
            recommended_follow_up="Review learner contact history.",
        )
        selected = select_rules(defaults, employer_overrides=(override,))
        selected_rule = next(rule for rule in selected if rule.rule_id == "stale-contact")
        self.assertEqual(selected_rule.threshold, 60)
        self.assertEqual(selected_rule.version, "employer-v2")
        alerts = evaluate_alerts(self.make_packet(), selected)
        self.assertFalse(any(alert.learner_name == "Stale Learner" for alert in alerts))

    def test_insufficient_evidence_is_not_emitted_as_a_risk_alert(self):
        alerts = evaluate_alerts(self.make_packet(), default_rules())
        self.assertFalse(any(alert.learner_name == "Unknown Recency" for alert in alerts))

    def test_cohort_override_takes_precedence_over_employer_override(self):
        defaults = default_rules()
        employer = InterventionRule("stale-contact", "employer-v2", "contact_recency", "medium", "days_since_last_meeting", 60, ">=", "Employer follow-up")
        cohort = InterventionRule("stale-contact", "cohort-v3", "contact_recency", "low", "days_since_last_meeting", 30, ">=", "Cohort follow-up")
        selected = select_rules(defaults, employer_overrides=(employer,), cohort_overrides=(cohort,))
        selected_rule = next(rule for rule in selected if rule.rule_id == "stale-contact")
        self.assertEqual(selected_rule.threshold, 30)
        self.assertEqual(selected_rule.version, "cohort-v3")


if __name__ == "__main__":
    unittest.main()
