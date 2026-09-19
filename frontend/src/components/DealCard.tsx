import { Link } from "react-router-dom";
import { formatMoney, profitTone, riskLabel } from "../lib/format";
import type { Deal } from "../types/deal";

export function DealCard({ deal }: { deal: Deal }) {
  const tone = profitTone(deal.score.net_profit);
  return (
    <Link className="card" to={`/deals/${deal.listing.id}`}>
      <img src={deal.listing.image_url ?? ""} alt="" />
      <div className="card-body">
        <div className="kicker">
          {deal.listing.source} · {deal.listing.location ?? "unknown"}
        </div>
        <h2>{deal.product.normalized_title}</h2>
        <div className="metrics">
          <span>Ask {formatMoney(deal.listing.price)}</span>
          <span className={tone}>Profit {formatMoney(deal.score.net_profit)}</span>
          <span className={deal.score.risk_score >= 65 ? "hot" : "mid"}>{riskLabel(deal.score.risk_score)}</span>
        </div>
      </div>
    </Link>
  );
}
