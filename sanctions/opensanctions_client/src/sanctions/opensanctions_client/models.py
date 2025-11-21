from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Entity:
    id: str
    name: str
    datasets: List[str] = field(default_factory=list)
    score: Optional[float] = None

    @classmethod
    def from_api(cls, payload: dict) -> "Entity":
        return cls(
            id=payload.get("id", ""),
            name=payload.get("name", ""),
            datasets=list(payload.get("datasets") or []),
            score=payload.get("score"),
        )


@dataclass
class SearchResponse:
    results: List[Entity]

    @classmethod
    def from_api(cls, payload: dict) -> "SearchResponse":
        raw_results = payload.get("results") or []
        entities = [Entity.from_api(item) for item in raw_results]
        return cls(results=entities)
