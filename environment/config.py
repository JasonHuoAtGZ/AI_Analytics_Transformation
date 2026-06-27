"""Central configuration for the Customer Analytics Query Agent.

Loads settings from .env and provides typed access to all modules.
"""

from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class OllamaConfig:
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")


@dataclass
class DuckDBConfig:
    path: Path = Path(
        os.getenv("DUCKDB_PATH", "data/generated/customer_analytics.duckdb")
    )


@dataclass
class Settings:
    ollama: OllamaConfig
    duckdb: DuckDBConfig
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    streamlit_port: int = int(os.getenv("STREAMLIT_PORT", "8501"))


settings = Settings(ollama=OllamaConfig(), duckdb=DuckDBConfig())
