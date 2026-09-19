import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Search } from "lucide-react";
import { motion } from "framer-motion";
import { SearchBar } from "@/components/filters/SearchBar";
import { RadarFilters } from "@/components/filters/RadarFilters";
import { Pagination } from "@/components/filters/Pagination";
import { OpportunityCard } from "@/components/opportunity/OpportunityCard";
import { OpportunityCardSkeleton } from "@/components/opportunity/Skeletons";
import { EmptyState } from "@/components/ui/EmptyState";
import { Button } from "@/components/ui/Button";
import { PageContainer } from "@/components/layout/PageContainer";
import { useOpportunities } from "@/hooks/useOpportunities";
import { RADAR_PAGE_SIZE, useOpportunityStore } from "@/store/opportunityStore";
import type { MarketplaceSource, OpportunitySort } from "@/types/opportunity";

export function RadarPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [hydrated, setHydrated] = useState(false);
  const query = useOpportunityStore((state) => state.query);
  const setQuery = useOpportunityStore((state) => state.setQuery);
  const setFilters = useOpportunityStore((state) => state.setFilters);
  const setPage = useOpportunityStore((state) => state.setPage);
  const reset = useOpportunityStore((state) => state.reset);
  const { items, total, page, pageSize, loading, error, refetch } = useOpportunities();

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
      page: Math.max(1, Number(searchParams.get("page") || "1") || 1),
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
  const storePage = useOpportunityStore((state) => state.page);

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
    if (storePage > 1) next.set("page", String(storePage));
    setSearchParams(next, { replace: true });
  }, [hydrated, query, category, source, condition, minProfit, minRoi, maxPrice, sort, storePage, setSearchParams]);

  const resultLabel = query.trim()
    ? `${total} result${total === 1 ? "" : "s"} for “${query.trim()}”`
    : `${total} opportunit${total === 1 ? "y" : "ies"}`;

  return (
    <PageContainer wide>
      <h1 className="text-[32px] font-bold leading-tight tracking-[-0.035em] text-foreground">Find undervalued items</h1>
      <p className="mt-4 max-w-2xl text-sm text-muted">
        The backend crawls phones, TVs, electronics, and other categories every minute, and only
        keeps broken or badly damaged listings. Search filters what has already been scored.
      </p>

      <div className="mt-6">
        <SearchBar value={query} onChange={setQuery} onSubmit={() => void refetch()} />
      </div>
      <div className="mt-4">
        <RadarFilters />
      </div>

      <p className="mt-6 flex flex-wrap items-center justify-between gap-3 text-[13px] text-muted">
        <span>{loading ? "Loading…" : resultLabel}</span>
        <Button type="button" variant="outline" disabled={loading} onClick={() => void refetch()}>
          Refresh
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
          <Pagination
            page={page}
            pageSize={pageSize || RADAR_PAGE_SIZE}
            total={total}
            disabled={loading}
            onPageChange={(nextPage) => {
              setPage(nextPage);
              window.scrollTo({ top: 0, behavior: "smooth" });
            }}
          />
        </div>
      ) : (
        <EmptyState
          icon={<Search className="h-8 w-8" />}
          title="No opportunities match these filters."
          description="No crawled listings match this query and filters. New marketplace items land here automatically."
          actionLabel="Reset Filters"
          onAction={reset}
        />
      )}
    </PageContainer>
  );
}
