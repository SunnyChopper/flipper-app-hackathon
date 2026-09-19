import type { MarketplaceSource } from "./opportunity";

export interface ListingDetail {
  id: string;
  source: MarketplaceSource;
  externalId: string;
  url: string;
  title: string;
  description?: string;
  price: number;
  shippingCost: number;
  condition: string;
  imageUrls: string[];
  listedAt?: string;
  createdAt: string;
  projectedRestorerNet: number;
  projectedHarvestYield: number;
}
