import { useCallback, useEffect, useRef, useState } from "react";
import { getOpportunities } from "@/api/opportunities";
import { RADAR_PAGE_SIZE, useOpportunityStore } from "@/store/opportunityStore";
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
  const page = useOpportunityStore((state) => state.page);
  const setPage = useOpportunityStore((state) => state.setPage);

  const [data, setData] = useState<OpportunityListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const requestId = useRef(0);

  const filters: RadarFilters = {
    query: query.trim() || undefined,
    source: source === "all" ? undefined : source,
    category: category === "all" ? undefined : category,
    condition: condition === "all" ? undefined : condition,
    minProfit: minProfit ?? undefined,
    minRoi: minRoi ?? undefined,
    maxPrice: maxPrice ?? undefined,
    sort,
    page,
    pageSize: RADAR_PAGE_SIZE,
  };

  const refetch = useCallback(async () => {
    const id = ++requestId.current;
    setLoading(true);
    try {
      const result = await getOpportunities(filters);
      if (id !== requestId.current) return;
      const pageCount = Math.max(1, Math.ceil(result.total / RADAR_PAGE_SIZE));
      if (page > pageCount) {
        setPage(pageCount);
        return;
      }
      setData(result);
      setError(null);
    } catch (err) {
      if (id !== requestId.current) return;
      setError(err instanceof Error ? err.message : "Failed to load opportunities");
    } finally {
      if (id === requestId.current) setLoading(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [query, source, category, condition, minProfit, minRoi, maxPrice, sort, page, setPage]);

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
    page: data?.page ?? page,
    pageSize: data?.pageSize ?? RADAR_PAGE_SIZE,
    loading,
    error,
    refetch,
    applyList: setData,
  };
}
