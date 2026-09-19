export type Marketplace = "ebay" | "facebook";

export type Listing = {
  id: string;
  source: Marketplace;
  external_id: string;
  title: string;
  description: string;
  price: number;
  currency: string;
  url: string;
  image_url: string | null;
  location: string | null;
};

export type NormalizedProduct = {
  listing_id: string;
  brand: string | null;
  model: string | null;
  category: string;
  condition: string;
  normalized_title: string;
  attributes: Record<string, unknown>;
};

export type ScoreBreakdown = {
  estimated_resale: number;
  repair_estimate: number;
  fees_estimate: number;
  net_profit: number;
  profit_margin: number;
  risk_score: number;
  overall_score: number;
  rationale: string;
};

export type Deal = {
  listing: Listing;
  product: NormalizedProduct;
  score: ScoreBreakdown;
};

export type DealFilters = {
  q?: string;
  source?: Marketplace | "";
  min_profit?: number;
  max_risk?: number;
};

export type SavedSearch = {
  id: string;
  name: string;
  query: string;
  filters: Record<string, unknown>;
  notify: boolean;
};
