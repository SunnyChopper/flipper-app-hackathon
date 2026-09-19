import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { ProfitRiskPanel } from "../components/ProfitRiskPanel";
import { fetchDeal } from "../lib/api";
import type { Deal } from "../types/deal";

export function DealDetailPage() {
  const { dealId } = useParams();
  const [deal, setDeal] = useState<Deal | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!dealId) return;
    void fetchDeal(dealId)
      .then(setDeal)
      .catch((err: Error) => setError(err.message));
  }, [dealId]);

  if (error) return <div className="error">{error}</div>;
  if (!deal) return <div className="empty">Loading deal…</div>;

  return (
    <main className="detail">
      <section>
        <img src={deal.listing.image_url ?? ""} alt="" />
        <p className="kicker">
          {deal.listing.source} · {deal.product.category} · {deal.product.condition}
        </p>
        <h1 className="serif">{deal.product.normalized_title}</h1>
        <p>{deal.listing.description}</p>
      </section>
      <ProfitRiskPanel deal={deal} />
    </main>
  );
}
