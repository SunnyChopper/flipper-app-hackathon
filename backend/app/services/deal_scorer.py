from app.models.deal import Deal, ScoreBreakdown
from app.models.listing import Listing, NormalizedProduct

CATEGORY_RESALE = {
    "electronics": 1.55,
    "home": 1.9,
    "tools": 1.7,
    "general": 1.35,
}

CATEGORY_FEES = {
    "ebay": 0.13,
    "facebook": 0.05,
}


class DealScorer:
    """Estimate resale, repairs, fees, profit, and risk for a normalized listing."""

    def score(self, listing: Listing, product: NormalizedProduct) -> Deal:
        resale_multiple = CATEGORY_RESALE.get(product.category, 1.35)
        estimated_resale = round(listing.price * resale_multiple, 2)
        if product.condition == "for_parts":
            estimated_resale = round(listing.price * 0.9, 2)

        damage = product.attributes.get("damage_hints") or []
        repair_estimate = round(25 * len(damage), 2)
        fees_estimate = round(estimated_resale * CATEGORY_FEES.get(listing.source, 0.1), 2)
        shipping = listing.shipping_cost or 0
        net_profit = round(estimated_resale - listing.price - shipping - repair_estimate - fees_estimate, 2)
        profit_margin = round((net_profit / listing.price) * 100, 1) if listing.price else 0

        risk = min(100, 20 + 15 * len(damage) + (25 if product.condition == "for_parts" else 0))
        overall = int(max(0, min(100, 50 + profit_margin - risk * 0.4)))

        rationale = (
            f"{product.normalized_title} looks like a {product.category} flip. "
            f"Ask {listing.price:.0f}, modeled resale {estimated_resale:.0f}, "
            f"repairs {repair_estimate:.0f}, {listing.source} fees {fees_estimate:.0f}."
        )
        if damage:
            rationale += f" Visible issues: {', '.join(damage)}."

        return Deal(
            listing=listing,
            product=product,
            score=ScoreBreakdown(
                estimated_resale=estimated_resale,
                repair_estimate=repair_estimate,
                fees_estimate=fees_estimate,
                net_profit=net_profit,
                profit_margin=profit_margin,
                risk_score=risk,
                overall_score=overall,
                rationale=rationale,
            ),
        )


deal_scorer = DealScorer()
