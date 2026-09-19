import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Search } from "lucide-react";
import { motion } from "framer-motion";
import { SearchBar } from "@/components/filters/SearchBar";
import { RadarFilters } from "@/components/filters/RadarFilters";
import { OpportunityCard } from "@/components/opportunity/OpportunityCard";
import { OpportunityCardSkeleton } from "@/components/opportunity/Skeletons";
import { EmptyState } from "@/components/ui/EmptyState";
import { Button } from "@/components/ui/Button";
import { PageContainer } from "@/components/layout/PageContainer";
import { useOpportunities } from "@/hooks/useOpportunities";
import { useOpportunityStore } from "@/store/opportunityStore";
import { ingestMarketplaces } from "@/api/opportunities";
import { useToastStore } from "@/store/toastStore";
import type { MarketplaceSource, OpportunitySort } from "@/types/opportunity";

export function RadarPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [hydrated, setHydrated] = useState(false);
  const [scanning, setScanning] = useState(false);
  const query = useOpportunityStore((state) => state.query);
  const setQuery = useOpportunityStore((state) => state.setQuery);
  const setFilters = useOpportunityStore((state) => state.setFilters);
  const reset = useOpportunityStore((state) => state.reset);
  const { items, total, loading, error, refetch, applyList } = useOpportunities();
  const showToast = useToastStore((state) => state.show);

  async function scanMarketplaces() {
    const term = query.trim();
    if (!term) {
      showToast("Type something to search, like tvs or iPhone 13.");
      return;
    }
    if (scanning) return;
    setScanning(true);
    try {
      const result = await ingestMarketplaces(term, 5);
      setFilters({
        condition: "all",
        category: "all",
        source: "all",
        minProfit: null,
        minRoi: null,
        maxPrice: null,
      });
      applyList(result);
      showToast(`Found ${result.total} marketplace listing${result.total === 1 ? "" : "s"}`);
    } catch {
      showToast("Marketplace scan failed. Is the API running?");
    } finally {
      setScanning(false);
    }
  }

  useEffect(() => {
    setFilters({
      query: searchParams.get("q") ?? "",
      category: searchParams.get("category") ?? "all",
      source: (searchParams.get("source") as MarketplaceSource | "all") ?? "all",
      condition: searchParams.get("condition") ?? "all",
      minProfit: searchParams.get("minProfit") ? Number(searchParams.get("minProfit")) : null,
      minRoi: searchParams.get("minRoi") ? Number(searchParams.get("minRoi")) : null,
      maxPrice: searchParams.get("maxPrice") ? Number(searchParams.get("maxPrice")) : null,
      sort: (searchParams.get("sort") as OpportunitySort) ?? "score_desc",
    });
    setHydrated(true);
    // Hydrate once from the incoming URL.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const category = useOpportunityStore((state) => state.category);
  const source = useOpportunityStore((state) => state.source);
  const condition = useOpportunityStore((state) => state.condition);
  const minProfit = useOpportunityStore((state) => state.minProfit);
  const minRoi = useOpportunityStore((state) => state.minRoi);
  const maxPrice = useOpportunityStore((state) => state.maxPrice);
  const sort = useOpportunityStore((state) => state.sort);

  useEffect(() => {
    if (!hydrated) return;
    const next = new URLSearchParams();
    if (query) next.set("q", query);
    if (category !== "all") next.set("category", category);
    if (source !== "all") next.set("source", source);
    if (condition !== "all") next.set("condition", condition);
    if (minProfit != null) next.set("minProfit", String(minProfit));
    if (minRoi != null) next.set("minRoi", String(minRoi));
    if (maxPrice != null) next.set("maxPrice", String(maxPrice));
    if (sort !== "score_desc") next.set("sort", sort);
    setSearchParams(next, { replace: true });
  }, [hydrated, query, category, source, condition, minProfit, minRoi, maxPrice, sort, setSearchParams]);

  const resultLabel = query.trim()
    ? `${items.length} result${items.length === 1 ? "" : "s"} for “${query.trim()}”`
    : `${total} opportunit${total === 1 ? "y" : "ies"}`;

  return (
    <PageContainer wide>
      <h1 className="text-[32px] font-bold leading-tight tracking-[-0.035em] text-foreground">Find undervalued items</h1>
      <p className="mt-4 max-w-2xl text-sm text-muted">
        Search marketplaces for damaged and discounted items with real profit potential.
      </p>

      <div className="mt-6">
        <SearchBar
          value={query}
          onChange={setQuery}
          onSubmit={() => void scanMarketplaces()}
          disabled={scanning}
        />
      </div>
      <div className="mt-4">
        <RadarFilters />
      </div>

      <p className="mt-6 flex flex-wrap items-center justify-between gap-3 text-[13px] text-muted">
        <span>{loading || scanning ? "Searching…" : resultLabel}</span>
        <Button type="button" variant="outline" disabled={scanning} onClick={() => void scanMarketplaces()}>
          {scanning ? "Scanning…" : "Scan marketplaces"}
        </Button>
      </p>

      {loading ? (
        <div className="mt-4 space-y-3">
          {Array.from({ length: 4 }).map((_, index) => (
            <OpportunityCardSkeleton key={index} />
          ))}
        </div>
      ) : error ? (
        <EmptyState
          icon={<Search className="h-8 w-8" />}
          title="Could not load opportunities."
          description="The FastAPI service may be offline. Start the backend on port 8000 and try again."
          actionLabel="Retry"
          onAction={() => void refetch()}
        />
      ) : items.length ? (
        <div className="mt-4 space-y-3">
          {items.map((item, index) => (
            <motion.div
              key={item.listingId}
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.18, delay: index * 0.035 }}
            >
              <OpportunityCard opportunity={item} />
            </motion.div>
          ))}
        </div>
      ) : (
        <EmptyState
          icon={<Search className="h-8 w-8" />}
          title="No opportunities match these filters."
          description="No loaded listings match this query and filters. Click Search to scrape eBay."
          actionLabel="Reset Filters"
          onAction={reset}
        />
      )}
    </PageContainer>
  );
}
