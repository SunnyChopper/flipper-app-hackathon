import { create } from "zustand";
import type { MarketplaceSource, OpportunitySort } from "@/types/opportunity";

export const RADAR_PAGE_SIZE = 20;

export type OpportunityFilterState = {
  query: string;
  source: MarketplaceSource | "all";
  category: string;
  condition: string;
  minProfit: number | null;
  minRoi: number | null;
  maxPrice: number | null;
  sort: OpportunitySort;
  page: number;
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
  page: 1,
};

type OpportunityState = OpportunityFilterState & {
  setQuery: (query: string) => void;
  setPage: (page: number) => void;
  setFilters: (patch: Partial<OpportunityFilterState>) => void;
  reset: () => void;
};

export const useOpportunityStore = create<OpportunityState>((set) => ({
  ...defaults,
  setQuery: (query) => set({ query, page: 1 }),
  setPage: (page) => set({ page: Math.max(1, page) }),
  setFilters: (patch) => set({ page: 1, ...patch }),
  reset: () => set(defaults),
}));
