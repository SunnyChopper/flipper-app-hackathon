import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Search } from "lucide-react";
import { motion } from "framer-motion";
import { SearchBar } from "@/components/filters/SearchBar";
import { RadarFilters } from "@/components/filters/RadarFilters";
import { OpportunityCard } from "@/components/opportunity/OpportunityCard";
import { OpportunityCardSkeleton } from "@/components/opportunity/Skeletons";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageContainer } from "@/components/layout/PageContainer";
import { useOpportunities } from "@/hooks/useOpportunities";
import { useOpportunityStore } from "@/store/opportunityStore";
import type { Marketplace, SortOption } from "@/types/opportunity";

export function RadarPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [booting, setBooting] = useState(true);
  const [hydrated, setHydrated] = useState(false);
  const query = useOpportunityStore((state) => state.query);
  const setQuery = useOpportunityStore((state) => state.setQuery);
  const setFilters = useOpportunityStore((state) => state.setFilters);
  const reset = useOpportunityStore((state) => state.reset);
  const { results } = useOpportunities();

  useEffect(() => {
    setFilters({
      query: searchParams.get("q") ?? "",
      category: searchParams.get("category") ?? "all",
      marketplace: (searchParams.get("marketplace") as Marketplace | "all") ?? "all",
      minProfit: searchParams.get("minProfit") ? Number(searchParams.get("minProfit")) : null,
      maxPrice: searchParams.get("maxPrice") ? Number(searchParams.get("maxPrice")) : null,
      sort: (searchParams.get("sort") as SortOption) ?? "best",
    });
    setHydrated(true);
    const timer = window.setTimeout(() => setBooting(false), 420);
    return () => window.clearTimeout(timer);
    // Hydrate once from the incoming URL.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const category = useOpportunityStore((state) => state.category);
  const marketplace = useOpportunityStore((state) => state.marketplace);
  const minProfit = useOpportunityStore((state) => state.minProfit);
  const maxPrice = useOpportunityStore((state) => state.maxPrice);
  const sort = useOpportunityStore((state) => state.sort);

  useEffect(() => {
    if (!hydrated) return;
    const next = new URLSearchParams();
    if (query) next.set("q", query);
    if (category !== "all") next.set("category", category);
    if (marketplace !== "all") next.set("marketplace", marketplace);
    if (minProfit != null) next.set("minProfit", String(minProfit));
    if (maxPrice != null) next.set("maxPrice", String(maxPrice));
    if (sort !== "best") next.set("sort", sort);
    setSearchParams(next, { replace: true });
  }, [hydrated, query, category, marketplace, minProfit, maxPrice, sort, setSearchParams]);

  const resultLabel = query.trim()
    ? `${results.length} result${results.length === 1 ? "" : "s"} for “${query.trim()}”`
    : `${results.length} opportunit${results.length === 1 ? "y" : "ies"}`;

  return (
    <PageContainer wide>
      <h1 className="text-[32px] font-bold leading-tight tracking-[-0.035em] text-foreground">Find undervalued items</h1>
      <p className="mt-4 max-w-2xl text-sm text-muted">
        Search marketplaces for damaged and discounted items with real profit potential.
      </p>

      <div className="mt-6">
        <SearchBar value={query} onChange={setQuery} onSubmit={() => undefined} />
      </div>
      <div className="mt-4">
        <RadarFilters />
      </div>

      <p className="mt-6 text-[13px] text-muted">{resultLabel}</p>

      {booting ? (
        <div className="mt-4 space-y-3">
          {Array.from({ length: 4 }).map((_, index) => (
            <OpportunityCardSkeleton key={index} />
          ))}
        </div>
      ) : results.length ? (
        <div className="mt-4 space-y-3">
          {results.map((item, index) => (
            <motion.div
              key={item.id}
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
          description="Try lowering your minimum profit or increasing your maximum purchase price."
          actionLabel="Reset Filters"
          onAction={reset}
        />
      )}
    </PageContainer>
  );
}
