from enum import Enum
from typing import Literal

MarketplaceSource = Literal["ebay", "facebook_marketplace"]
UserDealStatus = Literal["saved", "acquired", "dismissed"]
Persona = Literal["restorer", "harvester"]


class OpportunitySort(str, Enum):
    score_desc = "score_desc"
    profit_desc = "profit_desc"
    roi_desc = "roi_desc"
    price_asc = "price_asc"
    newest = "newest"
