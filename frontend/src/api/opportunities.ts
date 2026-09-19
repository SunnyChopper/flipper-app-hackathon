import { apiFetch } from "./apiClient";
import type { OpportunityDetail, OpportunityListResponse, RadarFilters } from "@/types/opportunity";

export async function getOpportunities(filters: RadarFilters = {}): Promise<OpportunityListResponse> {
  return apiFetch<OpportunityListResponse>("/api/v1/opportunities", {
    params: {
      q: filters.query,
      source: filters.source,
      category: filters.category,
      condition: filters.condition,
      persona: filters.persona,
      minProfit: filters.minProfit,
      minRoi: filters.minRoi,
      maxPrice: filters.maxPrice,
      requiredSkill: filters.requiredSkill,
      sort: filters.sort,
      page: filters.page,
      pageSize: filters.pageSize,
    },
  });
}

export async function getOpportunity(listingId: string): Promise<OpportunityDetail> {
  return apiFetch<OpportunityDetail>(`/api/v1/opportunities/${listingId}`);
}
