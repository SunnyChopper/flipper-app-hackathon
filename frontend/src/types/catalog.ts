export interface CatalogProductSummary {
  id: string;
  brand: string;
  model: string;
  variant?: string;
  category: string;
  displayName: string;
  estimatedWorkingMarketValue: number;
  valuationConfidenceScore: number;
}

export interface CatalogProductDetail extends CatalogProductSummary {
  lastValuationAt?: string;
}

export interface DefectiveComponent {
  bomItemId: string;
  componentId: string;
  componentName: string;
  requiredSkillSlug: string;
  requiredSkillDisplayName: string;
  avgReplacementCost: number;
  salvageResaleValue: number;
  harvestLiquidityScore: number;
}

export interface RepairSkillSummary {
  slug: string;
  displayName: string;
  category: string;
  userHasSkill: boolean;
}

export interface MarketCompSummary {
  id: string;
  source: string;
  soldPrice: number;
  shippingPrice: number;
  totalPrice: number;
  itemCondition: string;
  soldDate: string;
  listingUrl: string;
}
