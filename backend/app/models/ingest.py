from typing import Literal

from pydantic import BaseModel, Field

MarketplaceSource = Literal["ebay", "facebook", "facebook_marketplace"]


class IngestRequest(BaseModel):
    query: str = "iphone 13"
    location: str = "united-states"
    limit: int = Field(default=8, ge=1, le=50)
    sources: list[MarketplaceSource] = Field(
        default_factory=lambda: ["ebay", "facebook_marketplace"]
    )
