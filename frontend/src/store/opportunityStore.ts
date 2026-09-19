import { create } from "zustand";
import type { MarketplaceSource, OpportunitySort } from "@/types/opportunity";

export type OpportunityFilterState = {
  query: string;
  source: MarketplaceSource | "all";
  category: string;
  condition: string;
  minProfit: number | null;
  minRoi: number | null;
  maxPrice: number | null;
  sort: OpportunitySort;
};

const defaults: OpportunityFilterState = {
  query: "",
  source: "all",
  category: "all",
  condition: "all",
  minProfit: null,
  minRoi: null,
  maxPrice: null,
  sort: "score_desc",
};

type OpportunityState = OpportunityFilterState & {
  setQuery: (query: string) => void;
  setFilters: (patch: Partial<OpportunityFilterState>) => void;
  reset: () => void;
};

export const useOpportunityStore = create<OpportunityState>((set) => ({
  ...defaults,
  setQuery: (query) => set({ query }),
  setFilters: (patch) => set(patch),
  reset: () => set(defaults),
}));
