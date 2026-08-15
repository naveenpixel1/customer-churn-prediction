import json
import os
from typing import Any, Dict, Optional
from app.utils.config import MODEL_DIR

METRICS_FILE = MODEL_DIR / "metrics.json"

def load_model_metadata() -> Optional[Dict[str, Any]]:
    if not METRICS_FILE.exists():
        return None
    try:
        with open(METRICS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return None
