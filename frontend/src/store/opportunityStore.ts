import { create } from "zustand";
import type { Marketplace, SortOption } from "../types/opportunity";

export type OpportunityFilters = {
  query: string;
  category: string;
  marketplace: Marketplace | "all";
  minProfit: number | null;
  maxPrice: number | null;
  sort: SortOption;
};

const defaults: OpportunityFilters = {
  query: "",
  category: "all",
  marketplace: "all",
  minProfit: null,
  maxPrice: null,
  sort: "best",
};

type OpportunityState = OpportunityFilters & {
  setQuery: (query: string) => void;
  setFilters: (patch: Partial<OpportunityFilters>) => void;
  reset: () => void;
};

export const useOpportunityStore = create<OpportunityState>((set) => ({
  ...defaults,
  setQuery: (query) => set({ query }),
  setFilters: (patch) => set(patch),
  reset: () => set(defaults),
}));
