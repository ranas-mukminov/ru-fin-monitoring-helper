from dataclasses import dataclass, field
from typing import Optional


def _default_base_url() -> str:
    return "https://api.opensanctions.org"


@dataclass
class OpenSanctionsConfig:
    base_url: str = field(default_factory=_default_base_url)
    timeout: int = 10
    api_key: Optional[str] = None
    rate_limit_per_minute: int = 60
    cache_path: Optional[str] = None

    def validate(self) -> None:
        if not self.base_url:
            raise ValueError("base_url must be set")
        if not isinstance(self.timeout, (int, float)) or self.timeout <= 0:
            raise ValueError("timeout must be positive")
        if not isinstance(self.rate_limit_per_minute, int) or self.rate_limit_per_minute <= 0:
            raise ValueError("rate_limit_per_minute must be positive")
