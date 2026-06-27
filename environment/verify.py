"""Environment health check — validates all components are correctly configured.

Usage:
    python environment/verify.py
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECKS: list[dict] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    CHECKS.append({"name": name, "ok": ok, "detail": detail})


# --- Python version ---
py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
check("Python >= 3.12", sys.version_info >= (3, 12), py_ver)

# --- Virtual environment ---
in_venv = sys.prefix != sys.base_prefix
check("Virtual env active", in_venv, sys.prefix if in_venv else "not in venv")

# --- Core packages ---
for pkg in ("duckdb", "openai", "streamlit", "pandas", "pydantic", "dotenv"):
    try:
        __import__(pkg)
        check(f"Package: {pkg}", True)
    except ImportError:
        check(f"Package: {pkg}", False, "not installed")

# --- Config loads ---
try:
    sys.path.insert(0, str(REPO_ROOT))
    from environment.config import settings

    check("Config loaded", True)
    check("  Ollama URL", bool(settings.ollama.base_url), settings.ollama.base_url)
    check("  Ollama model", bool(settings.ollama.model), settings.ollama.model)
    check("  DuckDB path", bool(str(settings.duckdb.path)), str(settings.duckdb.path))
except Exception as e:
    check("Config loaded", False, str(e))

# --- Required directories ---
for d in ("data/raw", "data/generated", "scripts", "src/agent", "src/db",
          "src/ui", "tests", "skills", "lessons_learned", "docs"):
    exists = (REPO_ROOT / d).is_dir()
    check(f"Directory: {d}", exists, "ok" if exists else "missing")

# --- DuckDB functional ---
try:
    import duckdb

    con = duckdb.connect(":memory:")
    con.execute("SELECT 1 AS test")
    check("DuckDB functional", True)
    con.close()
except Exception as e:
    check("DuckDB functional", False, str(e))

# --- Ollama reachable ---
try:
    from openai import OpenAI

    client = OpenAI(base_url=settings.ollama.base_url + "/v1", api_key="ollama")
    models = client.models.list()
    model_ids = [m.id for m in models]
    check("Ollama reachable", True)
    check(
        f"  Model {settings.ollama.model}",
        settings.ollama.model in model_ids,
        "available" if settings.ollama.model in model_ids else f"not found in {model_ids}",
    )
except Exception as e:
    check("Ollama reachable", False, str(e))

# --- Report ---
print("\n" + "=" * 60)
print("  ENVIRONMENT VERIFICATION")
print("=" * 60)
passed = 0
failed = 0
for c in CHECKS:
    name = c["name"]
    if c["ok"]:
        passed += 1
        print(f"  [OK]    {name}")
    else:
        failed += 1
        print(f"  [FAIL]  {name}  —  {c.get('detail', '')}")

print("-" * 60)
print(f"  {passed} passed, {failed} failed")
if failed:
    print("\n  Fix failures above before proceeding.")
else:
    print("\n  All checks passed. Environment is ready.")
print("=" * 60 + "\n")
