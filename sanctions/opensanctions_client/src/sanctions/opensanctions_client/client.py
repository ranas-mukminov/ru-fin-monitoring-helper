from typing import Any, Dict, Optional

import requests

from .cache import SimpleCache
from .config import OpenSanctionsConfig
from .models import Entity, SearchResponse


class OpenSanctionsClient:
    def __init__(self, config: Optional[OpenSanctionsConfig] = None) -> None:
        self.config = config or OpenSanctionsConfig()
        self.config.validate()
        self.cache = SimpleCache(self.config.cache_path)

    def _headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {"Accept": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def search_name(self, name: str, params: Optional[Dict[str, Any]] = None) -> SearchResponse:
        cache_key = f"search:{name}:{params}"
        cached = self.cache.get(cache_key)
        if cached:
            return SearchResponse.from_api(cached)

        query_params = {"q": name}
        if params:
            query_params.update(params)
        url = f"{self.config.base_url.rstrip('/')}/search"
        response = requests.get(url, params=query_params, headers=self._headers(), timeout=self.config.timeout)
        response.raise_for_status()
        payload = response.json()
        self.cache.set(cache_key, payload)
        return SearchResponse.from_api(payload)

    def get_entity(self, entity_id: str) -> Entity:
        cache_key = f"entity:{entity_id}"
        cached = self.cache.get(cache_key)
        if cached:
            return Entity.from_api(cached)
        url = f"{self.config.base_url.rstrip('/')}/entities/{entity_id}"
        response = requests.get(url, headers=self._headers(), timeout=self.config.timeout)
        response.raise_for_status()
        payload = response.json()
        self.cache.set(cache_key, payload)
        return Entity.from_api(payload)
