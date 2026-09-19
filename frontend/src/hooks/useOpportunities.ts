import { useMemo } from "react";
import { mockOpportunities } from "../data/mockOpportunities";
import { useOpportunityStore } from "../store/opportunityStore";
import type { Opportunity, SortOption } from "../types/opportunity";

function sortOpportunities(items: Opportunity[], sort: SortOption): Opportunity[] {
  const next = [...items];
  switch (sort) {
    case "profit":
      return next.sort((a, b) => b.estimatedProfit - a.estimatedProfit);
    case "roi":
      return next.sort((a, b) => b.roiPercent - a.roiPercent);
    case "price":
      return next.sort((a, b) => a.askingPrice - b.askingPrice);
    case "score":
      return next.sort((a, b) => b.dealScore - a.dealScore);
    case "newest":
      return next.sort((a, b) => +new Date(b.listedAt) - +new Date(a.listedAt));
    default:
      return next.sort((a, b) => b.dealScore - a.dealScore);
  }
}

export function useOpportunities() {
  const query = useOpportunityStore((state) => state.query);
  const category = useOpportunityStore((state) => state.category);
  const marketplace = useOpportunityStore((state) => state.marketplace);
  const minProfit = useOpportunityStore((state) => state.minProfit);
  const maxPrice = useOpportunityStore((state) => state.maxPrice);
  const sort = useOpportunityStore((state) => state.sort);

  const results = useMemo(() => {
    const needle = query.trim().toLowerCase();
    const filtered = mockOpportunities.filter((item) => {
      const matchesQuery =
        !needle ||
        item.title.toLowerCase().includes(needle) ||
        item.category.toLowerCase().includes(needle) ||
        (item.subcategory ?? "").toLowerCase().includes(needle);
      const matchesCategory = category === "all" || item.category === category || item.subcategory === category;
      const matchesMarket = marketplace === "all" || item.source === marketplace;
      const matchesProfit = minProfit == null || item.estimatedProfit >= minProfit;
      const matchesPrice = maxPrice == null || item.askingPrice <= maxPrice;
      return matchesQuery && matchesCategory && matchesMarket && matchesProfit && matchesPrice;
    });
    return sortOpportunities(filtered, sort);
  }, [query, category, marketplace, minProfit, maxPrice, sort]);

  return { results, total: mockOpportunities.length };
}

export function getOpportunity(id: string): Opportunity | undefined {
  return mockOpportunities.find((item) => item.id === id);
}
