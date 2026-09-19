import { FilterSelect } from "./FilterSelect";
import { useOpportunityStore } from "@/store/opportunityStore";
import type { MarketplaceSource, OpportunitySort } from "@/types/opportunity";

const categories = [
  { label: "All Categories", value: "all" },
  { label: "Smartphones", value: "smartphones" },
  { label: "Gaming consoles", value: "gaming_consoles" },
  { label: "Laptops", value: "laptops" },
];

const sources = [
  { label: "All Marketplaces", value: "all" },
  { label: "Facebook Marketplace", value: "facebook_marketplace" },
  { label: "eBay", value: "ebay" },
];

const conditions = [
  { label: "Any condition", value: "all" },
  { label: "Damaged", value: "damaged" },
  { label: "For Parts", value: "for_parts" },
  { label: "Used (Fair)", value: "used_fair" },
  { label: "Locked", value: "locked" },
];

const minProfits = [
  { label: "Any profit", value: "" },
  { label: "$50+", value: "50" },
  { label: "$100+", value: "100" },
  { label: "$150+", value: "150" },
  { label: "$250+", value: "250" },
];

const minRois = [
  { label: "Any ROI", value: "" },
  { label: "20%+", value: "20" },
  { label: "40%+", value: "40" },
  { label: "60%+", value: "60" },
];

const maxPrices = [
  { label: "Any price", value: "" },
  { label: "Under $100", value: "100" },
  { label: "Under $250", value: "250" },
  { label: "Under $500", value: "500" },
  { label: "Under $1000", value: "1000" },
];

const sorts = [
  { label: "Highest Deal Score", value: "score_desc" },
  { label: "Highest Profit", value: "profit_desc" },
  { label: "Highest ROI", value: "roi_desc" },
  { label: "Lowest Price", value: "price_asc" },
  { label: "Newest", value: "newest" },
];

export function RadarFilters() {
  const category = useOpportunityStore((state) => state.category);
  const source = useOpportunityStore((state) => state.source);
  const condition = useOpportunityStore((state) => state.condition);
  const minProfit = useOpportunityStore((state) => state.minProfit);
  const minRoi = useOpportunityStore((state) => state.minRoi);
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
          value={source}
          options={sources}
          onChange={(value) => setFilters({ source: value as MarketplaceSource | "all" })}
        />
        <FilterSelect
          label="Condition"
          value={condition}
          options={conditions}
          onChange={(value) => setFilters({ condition: value })}
        />
        <FilterSelect
          label="Minimum profit"
          value={minProfit == null ? "" : String(minProfit)}
          options={minProfits}
          onChange={(value) => setFilters({ minProfit: value ? Number(value) : null })}
        />
        <FilterSelect
          label="Minimum ROI"
          value={minRoi == null ? "" : String(minRoi)}
          options={minRois}
          onChange={(value) => setFilters({ minRoi: value ? Number(value) : null })}
        />
        <FilterSelect
          label="Maximum price"
          value={maxPrice == null ? "" : String(maxPrice)}
          onChange={(value) => setFilters({ maxPrice: value ? Number(value) : null })}
          options={maxPrices}
        />
      </div>
      <div className="flex items-center gap-2 text-[13px] text-muted">
        <span>Sort by:</span>
        <FilterSelect
          label="Sort"
          value={sort}
          options={sorts}
          onChange={(value) => setFilters({ sort: value as OpportunitySort })}
        />
      </div>
    </div>
  );
}
