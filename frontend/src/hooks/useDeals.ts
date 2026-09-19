import { useCallback, useEffect, useState } from "react";
import { fetchDeals } from "../lib/api";
import type { Deal, DealFilters } from "../types/deal";

export function useDeals(filters: DealFilters) {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const reload = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setDeals(await fetchDeals(filters));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load deals");
    } finally {
      setLoading(false);
    }
  }, [filters.q, filters.source, filters.min_profit, filters.max_risk]);

  useEffect(() => {
    void reload();
  }, [reload]);

  return { deals, loading, error, reload, setDeals };
}
