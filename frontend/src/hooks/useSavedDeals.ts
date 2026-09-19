import { mockOpportunities } from "../data/mockOpportunities";
import { useSavedStore } from "../store/savedStore";

export function useSavedDeals() {
  const savedIds = useSavedStore((state) => state.savedIds);
  const remove = useSavedStore((state) => state.remove);
  const toggle = useSavedStore((state) => state.toggle);
  const isSaved = useSavedStore((state) => state.isSaved);

  const items = savedIds
    .map((id) => mockOpportunities.find((item) => item.id === id))
    .filter((item): item is NonNullable<typeof item> => Boolean(item));

  return { items, count: items.length, remove, toggle, isSaved };
}
