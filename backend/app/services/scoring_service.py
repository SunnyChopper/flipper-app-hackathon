from __future__ import annotations

from app.domain.entities import CatalogProduct
from app.schemas.opportunity import DealScoreResponse
from app.services.valuation_service import roi_percent


def _clamp(value: float, low: float = 0, high: float = 100) -> int:
    return int(round(min(high, max(low, value))))


def score_opportunity(
    *,
    projected_restorer_net: float,
    total_acquisition_and_repair_cost: float,
    projected_harvest_yield: float,
    product: CatalogProduct | None,
    persona: str | None = None,
) -> DealScoreResponse:
    """Derive DealScore from restorer/harvester economics. Not persisted."""
    confidence = product.valuation_confidence_score if product else 0.5
    roi = roi_percent(projected_restorer_net, total_acquisition_and_repair_cost)

    profit_factor = min(45.0, max(0.0, projected_restorer_net / 2.8))
    roi_factor = min(35.0, max(0.0, roi * 0.85))
    confidence_factor = confidence * 20.0
    restorer_score = _clamp(profit_factor + roi_factor + confidence_factor)

    harvest_factor = min(50.0, max(0.0, (projected_harvest_yield + 80) / 4.0))
    harvester_score = _clamp(harvest_factor + confidence_factor)

    total = harvester_score if persona == "harvester" else restorer_score
    return DealScoreResponse(
        total=total,
        restorer_score=restorer_score,
        harvester_score=harvester_score,
        valuation_confidence=confidence,
    )
