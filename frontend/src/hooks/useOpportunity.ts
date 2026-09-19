import { useEffect, useState } from "react";
import { getOpportunity } from "@/api/opportunities";
import { ApiError } from "@/api/apiClient";
import type { OpportunityDetail } from "@/types/opportunity";

export function useOpportunity(listingId: string | undefined) {
  const [opportunity, setOpportunity] = useState<OpportunityDetail | null>(null);
  const [loading, setLoading] = useState(Boolean(listingId));
  const [error, setError] = useState<string | null>(null);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    if (!listingId) return;
    let cancelled = false;
    setLoading(true);
    setNotFound(false);
    void getOpportunity(listingId)
      .then((result) => {
        if (cancelled) return;
        setOpportunity(result);
        setError(null);
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        setOpportunity(null);
        if (err instanceof ApiError && err.status === 404) {
          setNotFound(true);
          setError(null);
        } else {
          setError(err instanceof Error ? err.message : "Failed to load opportunity");
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [listingId]);

  return { opportunity, loading, error, notFound };
}
