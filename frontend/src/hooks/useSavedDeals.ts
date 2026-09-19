import { useCallback, useEffect, useState } from "react";
import { deleteDeal, getDeals, saveDeal } from "@/api/deals";
import type { SavedDealItem } from "@/api/deals";
import { useSavedStore } from "@/store/savedStore";
import { useToastStore } from "@/store/toastStore";

export function useHydrateSavedDeals() {
  const replace = useSavedStore((state) => state.replace);

  useEffect(() => {
    let cancelled = false;
    void getDeals("saved")
      .then((result) => {
        if (!cancelled) replace(result.items.map((item) => item.opportunity.listingId));
      })
      .catch(() => undefined);
    return () => {
      cancelled = true;
    };
  }, [replace]);
}

export function useDealMutations() {
  const savedIds = useSavedStore((state) => state.savedIds);
  const saveLocal = useSavedStore((state) => state.save);
  const removeLocal = useSavedStore((state) => state.remove);
  const showToast = useToastStore((state) => state.show);

  const save = useCallback(
    async (listingId: string) => {
      const wasSaved = savedIds.includes(listingId);
      saveLocal(listingId);
      try {
        await saveDeal(listingId, { status: "saved" });
        if (!wasSaved) showToast("Deal saved");
        return true;
      } catch {
        if (!wasSaved) removeLocal(listingId);
        showToast("Could not save deal");
        return false;
      }
    },
    [removeLocal, saveLocal, savedIds, showToast],
  );

  const remove = useCallback(
    async (listingId: string) => {
      const wasSaved = savedIds.includes(listingId);
      removeLocal(listingId);
      try {
        await deleteDeal(listingId);
        showToast("Removed from saved deals");
        return true;
      } catch {
        if (wasSaved) saveLocal(listingId);
        showToast("Could not remove deal");
        return false;
      }
    },
    [removeLocal, saveLocal, savedIds, showToast],
  );

  const toggle = useCallback(
    async (listingId: string) => {
      if (savedIds.includes(listingId)) return remove(listingId);
      return save(listingId);
    },
    [remove, save, savedIds],
  );

  return { save, remove, toggle, isSaved: (id: string) => savedIds.includes(id) };
}

export function useSavedDeals() {
  const { remove, save, toggle, isSaved } = useDealMutations();
  const [items, setItems] = useState<SavedDealItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refetch = useCallback(async () => {
    setLoading(true);
    try {
      const result = await getDeals("saved");
      setItems(result.items);
      useSavedStore.getState().replace(result.items.map((item) => item.opportunity.listingId));
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load saved deals");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refetch();
  }, [refetch]);

  const removeAndRefresh = useCallback(
    async (listingId: string) => {
      const ok = await remove(listingId);
      if (ok) setItems((current) => current.filter((item) => item.opportunity.listingId !== listingId));
    },
    [remove],
  );

  return {
    items: items.map((item) => item.opportunity),
    count: items.length,
    loading,
    error,
    refetch,
    save,
    remove: removeAndRefresh,
    toggle,
    isSaved,
  };
}
