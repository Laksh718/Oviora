import os
import sys

# Resolve model paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "..", "..", "backend")

# Inject backend path so backend app modules are importable
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.services.fallback import fallback_engine
from app.services.formatter import formatter

def predict(file_path: str) -> dict:
    """
    Runs the complete hormone analysis pipeline (OCR -> Normalization -> Rules -> LLM) 
    on a lab report file.
    """
    result = fallback_engine.analyze_file(file_path)
    if not result.get("success"):
        return {"error": result.get("error", "Analysis failed")}
    return formatter.build(result)
