import { create } from "zustand";
import { persist } from "zustand/middleware";

type SavedState = {
  savedIds: string[];
  save: (id: string) => void;
  remove: (id: string) => void;
  toggle: (id: string) => void;
  isSaved: (id: string) => boolean;
};

export const useSavedStore = create<SavedState>()(
  persist(
    (set, get) => ({
      savedIds: [],
      save: (id) => set({ savedIds: Array.from(new Set([...get().savedIds, id])) }),
      remove: (id) => set({ savedIds: get().savedIds.filter((saved) => saved !== id) }),
      toggle: (id) => {
        const { savedIds } = get();
        set({
          savedIds: savedIds.includes(id) ? savedIds.filter((saved) => saved !== id) : [...savedIds, id],
        });
      },
      isSaved: (id) => get().savedIds.includes(id),
    }),
    { name: "dealsniper-saved" },
  ),
);
