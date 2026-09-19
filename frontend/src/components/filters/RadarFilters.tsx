import { FilterSelect } from "./FilterSelect";
import { useOpportunityStore } from "@/store/opportunityStore";
import type { Marketplace, SortOption } from "@/types/opportunity";

const categories = [
  { label: "All Categories", value: "all" },
  { label: "Electronics", value: "Electronics" },
  { label: "Gaming", value: "Gaming" },
  { label: "Tools", value: "Tools" },
  { label: "Appliances", value: "Appliances" },
  { label: "Computers", value: "Computers" },
  { label: "Phones", value: "Phones" },
];

const marketplaces = [
  { label: "All Marketplaces", value: "all" },
  { label: "Facebook Marketplace", value: "facebook" },
  { label: "eBay", value: "ebay" },
];

const minProfits = [
  { label: "Any profit", value: "" },
  { label: "$50+", value: "50" },
  { label: "$100+", value: "100" },
  { label: "$150+", value: "150" },
  { label: "$250+", value: "250" },
];

const maxPrices = [
  { label: "Any price", value: "" },
  { label: "Under $100", value: "100" },
  { label: "Under $250", value: "250" },
  { label: "Under $500", value: "500" },
  { label: "Under $1000", value: "1000" },
];

const sorts = [
  { label: "Best Match", value: "best" },
  { label: "Highest Profit", value: "profit" },
  { label: "Highest ROI", value: "roi" },
  { label: "Lowest Price", value: "price" },
  { label: "Highest Deal Score", value: "score" },
  { label: "Newest", value: "newest" },
];

export function RadarFilters() {
  const category = useOpportunityStore((state) => state.category);
  const marketplace = useOpportunityStore((state) => state.marketplace);
  const minProfit = useOpportunityStore((state) => state.minProfit);
  const maxPrice = useOpportunityStore((state) => state.maxPrice);
  const sort = useOpportunityStore((state) => state.sort);
  const setFilters = useOpportunityStore((state) => state.setFilters);

  return (
    <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
      <div className="flex flex-wrap gap-2">
        <FilterSelect
          label="Category"
          value={category}
          options={categories}
          onChange={(value) => setFilters({ category: value })}
        />
        <FilterSelect
          label="Marketplace"
          value={marketplace}
          options={marketplaces}
          onChange={(value) => setFilters({ marketplace: value as Marketplace | "all" })}
        />
        <FilterSelect
          label="Minimum profit"
          value={minProfit == null ? "" : String(minProfit)}
          options={minProfits}
          onChange={(value) => setFilters({ minProfit: value ? Number(value) : null })}
        />
        <FilterSelect
          label="Maximum price"
          value={maxPrice == null ? "" : String(maxPrice)}
          options={maxPrices}
          onChange={(value) => setFilters({ maxPrice: value ? Number(value) : null })}
        />
      </div>
      <div className="flex items-center gap-2 text-[13px] text-muted">
        <span>Sort by:</span>
        <FilterSelect
          label="Sort"
          value={sort}
          options={sorts}
          onChange={(value) => setFilters({ sort: value as SortOption })}
        />
      </div>
    </div>
  );
}
