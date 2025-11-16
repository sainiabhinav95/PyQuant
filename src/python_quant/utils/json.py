from pathlib import Path
import json
from typing import Any, Dict, Union

def json_file_to_dict(path: Union[str, Path]) -> Dict[str, Any]:
    """Read JSON from `path` and return as a Python dict.

    Raises:
      FileNotFoundError: if file doesn't exist
      json.JSONDecodeError: if file contains invalid JSON
      ValueError: if JSON is not an object (optional)
    """
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        # optional: enforce that top-level JSON is a dict
        raise ValueError("Expected JSON top-level object to be a dict")
    return data # type: ignore