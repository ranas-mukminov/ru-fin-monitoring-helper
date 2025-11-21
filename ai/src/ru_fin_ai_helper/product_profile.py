from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ProductProfile:
    product_type: str
    channels: List[str]
    geography: str
    features: List[str] = field(default_factory=list)
    description: Optional[str] = None
