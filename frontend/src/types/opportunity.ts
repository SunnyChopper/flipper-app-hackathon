import type { CatalogProductDetail, CatalogProductSummary, DefectiveComponent, MarketCompSummary, RepairSkillSummary } from "./catalog";
import type { UserDealStatus, UserDealSummary } from "./deal";
import type { ListingDetail } from "./listing";

export type MarketplaceSource = "ebay" | "facebook_marketplace";

export type { UserDealStatus };

export type OpportunitySort = "score_desc" | "profit_desc" | "roi_desc" | "price_asc" | "newest";

export interface RadarFilters {
  query?: string;
  source?: MarketplaceSource;
  category?: string;
  minProfit?: number;
  minRoi?: number;
  maxPrice?: number;
  condition?: string;
  requiredSkill?: string;
  persona?: string;
  sort?: OpportunitySort;
  page?: number;
  pageSize?: number;
}

export interface DealScore {
  total: number;
  restorerScore: number;
  harvesterScore: number;
  valuationConfidence: number;
}

export interface OpportunityFinancials {
  purchasePrice: number;
  shippingCost: number;
  totalReplacementCost: number;
  totalAcquisitionAndRepairCost: number;
  estimatedWorkingMarketValue: number;
  projectedRestorerNet: number;
  projectedHarvestYield: number;
  roiPercent: number;
}

export interface OpportunitySummary {
  listingId: string;
  source: MarketplaceSource;
  title: string;
  description?: string;
  url: string;
  price: number;
  shippingCost: number;
  imageUrl?: string;
  condition: string;
  listedAt?: string;
  product?: CatalogProductSummary;
  requiredRepairSkills: string[];
  projectedRestorerNet: number;
  projectedHarvestYield: number;
  estimatedRepairCost: number;
  dealScore: number;
  userDealStatus: UserDealStatus | null;
}

export interface OpportunityListResponse {
  items: OpportunitySummary[];
  page: number;
  pageSize: number;
  total: number;
}

export interface OpportunityDetail {
  listing: ListingDetail;
  product: CatalogProductDetail | null;
  defects: DefectiveComponent[];
  requiredSkills: RepairSkillSummary[];
  marketComps: MarketCompSummary[];
  financials: OpportunityFinancials;
  dealScore: DealScore;
  userDeal: UserDealSummary | null;
}
