import json
from pathlib import Path
from typing import Any, Dict, Optional


class SimpleCache:
    """Tiny file-backed cache to avoid hitting the API repeatedly."""

    def __init__(self, path: Optional[str] = None) -> None:
        self.path = Path(path) if path else Path(".cache_opensanctions.json")
        self._store: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            try:
                self._store = json.loads(self.path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self._store = {}

    def get(self, key: str) -> Optional[Any]:
        return self._store.get(key)

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value
        self.path.write_text(json.dumps(self._store, ensure_ascii=False, indent=2), encoding="utf-8")
