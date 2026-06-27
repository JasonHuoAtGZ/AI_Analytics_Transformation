"""Query Engine — converts natural language to SQL using Ollama LLM.

Sends the knowledge-base-augmented prompt to the local Ollama model
and extracts the generated SQL from the response.
"""

import re

from openai import OpenAI

from environment.config import settings
from src.agent.knowledge_base import build_system_prompt
from src.db.connection import db


class QueryEngine:
    """Converts natural language questions into DuckDB SQL via Ollama."""

    def __init__(self) -> None:
        self._client = OpenAI(
            base_url=settings.ollama.base_url + "/v1",
            api_key="ollama",
        )
        self._model = settings.ollama.model
        self._system_prompt = build_system_prompt()

    def generate_sql(self, question: str) -> str:
        """Send question to Ollama and return the generated SQL."""
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.1,      # Low temperature for deterministic SQL
            max_tokens=500,
        )
        raw = response.choices[0].message.content.strip()
        return self._extract_sql(raw)

    @staticmethod
    def _extract_sql(raw: str) -> str:
        """Extract clean SQL from the LLM response.

        Handles common LLM output patterns:
        - SQL wrapped in ```sql ... ``` blocks
        - SQL wrapped in ``` ... ``` blocks
        - Plain SQL text
        """
        # Try fenced code block first
        match = re.search(r"```(?:sql)?\s*\n?(.*?)\n?```", raw, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Fallback: assume the whole response is SQL
        return raw.strip()

    @property
    def model_name(self) -> str:
        return self._model


# Singleton instance
query_engine = QueryEngine()
