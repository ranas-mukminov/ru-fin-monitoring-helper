from typing import Any, Dict, List, Optional

import requests


class SanctionsNetworkClient:
    """Minimal wrapper for sanctions.network public API."""

    def __init__(self, base_url: str = "https://api.sanctions.network", timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def search(self, name: str, countries: Optional[List[str]] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {"name": name}
        if countries:
            params["countries"] = ",".join(countries)
        response = requests.get(f"{self.base_url}/search", params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
