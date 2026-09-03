from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from edukate_progress_summariser.ai_service import FakeAIProvider


class AIServiceTests(unittest.TestCase):
    def test_fake_provider_is_injectable_without_network_or_credentials(self):
        provider = FakeAIProvider(model="test-model", interpretation="Evidence-based test interpretation")
        evidence = {"employer_id": 123, "learners": [{"learner_reference": "learner-abc"}]}
        result = provider.interpret(evidence)
        self.assertEqual(result, "Evidence-based test interpretation")
        self.assertEqual(provider.model, "test-model")
        self.assertEqual(provider.calls, 1)
        self.assertEqual(provider.last_evidence, evidence)


if __name__ == "__main__":
    unittest.main()
