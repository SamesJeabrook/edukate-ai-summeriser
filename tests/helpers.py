from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPOSITORY_ROOT / "data"


def load_json_fixture(name: str) -> Any:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))
