import { useMemo, useState } from "react";
import { DealCard } from "../components/DealCard";
import { FilterBar } from "../components/FilterBar";
import { useDeals } from "../hooks/useDeals";
import { useRealtimeDeals } from "../hooks/useRealtimeDeals";
import { ingestEbay, ingestFacebook } from "../lib/api";
import { formatMoney } from "../lib/format";
import type { DealFilters } from "../types/deal";

export function SearchPage() {
  const [filters, setFilters] = useState<DealFilters>({});
  const { deals, loading, error, reload, setDeals } = useDeals(filters);
  useRealtimeDeals(() => {
    void reload();
  });
  const best = useMemo(
    () => deals.reduce((sum, deal) => sum + Math.max(deal.score.net_profit, 0), 0),
    [deals],
  );

  async function pullFresh() {
    const query = filters.q || "vacuum";
    const [ebay, facebook] = await Promise.all([ingestEbay(query), ingestFacebook(query)]);
    setDeals([...ebay, ...facebook, ...deals]);
    await reload();
  }

  return (
    <main>
      <section className="hero">
        <div>
          <h1>See the spread before you buy the junk.</h1>
          <p>
            Search eBay and Facebook Marketplace, normalize the mess, then rank flips by profit and
            damage risk.
          </p>
        </div>
        <div className="stat-stack">
          <div className="stat">
            <span className="kicker">On this radar</span>
            <b>{deals.length} deals</b>
          </div>
          <div className="stat">
            <span className="kicker">Modeled upside</span>
            <b>{formatMoney(best)}</b>
          </div>
        </div>
      </section>

      <FilterBar filters={filters} onChange={setFilters} onRefresh={() => void reload()} />
      <p className="banner">
        <button type="button" className="ghost" onClick={() => void pullFresh()}>
          Pull marketplace sample
        </button>
      </p>

      {loading && <div className="empty">Scanning listings…</div>}
      {error && <div className="error">API is quiet ({error}). Start the FastAPI server on :8000.</div>}
      {!loading && !deals.length && <div className="empty">No deals matched those filters.</div>}

      <section className="grid">
        {deals.map((deal) => (
          <DealCard key={deal.listing.id} deal={deal} />
        ))}
      </section>
    </main>
  );
}
