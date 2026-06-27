"""Query Engine -- converts natural language to SQL using Ollama LLM.

Sends the knowledge-base-augmented prompt to the local Ollama model
and extracts the generated SQL, reasoning, and chart type from the response.
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
            temperature=0.1,
            max_tokens=800,
        )
        raw = response.choices[0].message.content.strip()
        return self._extract_sql(raw)

    @staticmethod
    def _extract_sql(raw: str) -> str:
        """Extract SQL from the LLM response.

        Handles:
        - Fenced `sql ... ` blocks
        - Fenced ` ... ` blocks
        - Plain SQL text (fallback)
        """
        # Priority 1: fenced code block
        m = re.search(
            r"`(?:sql)?\s*\n(.+?)\n?`",
            raw, re.DOTALL,
        )
        if m:
            return m.group(1).strip()

        # Priority 2: look for SELECT statement in the text
        m = re.search(r"(SELECT\s+.+?(?:;|$))", raw, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1).strip().rstrip(";")

        # Fallback: return as-is, validation will catch issues
        return raw.strip()


    @property
    def model_name(self) -> str:
        return self._model


# Singleton instance
query_engine = QueryEngine()
