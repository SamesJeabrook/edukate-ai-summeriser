from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol


class AIProvider(Protocol):
    @property
    def model(self) -> str:
        ...

    def interpret(self, evidence: Mapping[str, Any]) -> str:
        ...


@dataclass
class OpenAIProvider:
    model: str
    api_key: str

    def interpret(self, evidence: Mapping[str, Any]) -> str:
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)
        response = client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": "Interpret only the supplied de-identified learner progress evidence. Do not invent facts.",
                },
                {"role": "user", "content": str(dict(evidence))},
            ],
        )
        return response.output_text


@dataclass
class FakeAIProvider:
    model: str = "fake-model"
    interpretation: str = "Fake interpretation"
    calls: int = 0
    last_evidence: Mapping[str, Any] = None

    def interpret(self, evidence: Mapping[str, Any]) -> str:
        self.calls += 1
        self.last_evidence = evidence
        return self.interpretation
