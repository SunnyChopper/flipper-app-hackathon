export type Marketplace = "facebook" | "ebay";

export type RiskSeverity = "low" | "medium" | "high";

export interface RiskItem {
  id: string;
  label: string;
  severity: RiskSeverity;
}

export interface MarketComp {
  id: string;
  title: string;
  price: number;
  marketplace: string;
  imageUrl?: string;
}

export interface Opportunity {
  id: string;
  title: string;
  subtitle?: string;
  source: Marketplace;
  imageUrl: string;
  gallery?: string[];
  askingPrice: number;
  estimatedWorkingValue: number;
  estimatedRepairCost: number;
  estimatedSellingFees: number;
  estimatedProfit: number;
  roiPercent: number;
  dealScore: number;
  category: string;
  subcategory?: string;
  location?: string;
  distanceMiles?: number;
  listedAt: string;
  detectedConditions: string[];
  unknownRisks: RiskItem[];
  marketComps: MarketComp[];
  listingUrl: string;
}

export type SortOption =
  | "best"
  | "profit"
  | "roi"
  | "price"
  | "score"
  | "newest";
