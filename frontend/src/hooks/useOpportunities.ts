import { useCallback, useEffect, useState } from "react";
import { getOpportunities } from "@/api/opportunities";
import { useOpportunityStore } from "@/store/opportunityStore";
import type { OpportunityListResponse, RadarFilters } from "@/types/opportunity";

export function useOpportunities() {
  const query = useOpportunityStore((state) => state.query);
  const source = useOpportunityStore((state) => state.source);
  const category = useOpportunityStore((state) => state.category);
  const condition = useOpportunityStore((state) => state.condition);
  const minProfit = useOpportunityStore((state) => state.minProfit);
  const minRoi = useOpportunityStore((state) => state.minRoi);
  const maxPrice = useOpportunityStore((state) => state.maxPrice);
  const sort = useOpportunityStore((state) => state.sort);

  const [data, setData] = useState<OpportunityListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const filters: RadarFilters = {
    query: query.trim() || undefined,
    source: source === "all" ? undefined : source,
    category: category === "all" ? undefined : category,
    condition: condition === "all" ? undefined : condition,
    minProfit: minProfit ?? undefined,
    minRoi: minRoi ?? undefined,
    maxPrice: maxPrice ?? undefined,
    sort,
  };

  const refetch = useCallback(async () => {
    setLoading(true);
    try {
      const result = await getOpportunities(filters);
      setData(result);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load opportunities");
    } finally {
      setLoading(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [query, source, category, condition, minProfit, minRoi, maxPrice, sort]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      void refetch();
    }, query ? 200 : 0);
    return () => window.clearTimeout(timer);
  }, [refetch, query]);

  return {
    data,
    items: data?.items ?? [],
    total: data?.total ?? 0,
    loading,
    error,
    refetch,
  };
}
