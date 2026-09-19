import { apiFetch } from "./apiClient";
import type { SaveDealRequest, UserDealResponse, UserDealSummary } from "@/types/deal";
import type { OpportunitySummary, UserDealStatus } from "@/types/opportunity";

export interface SavedDealItem {
  userDeal: UserDealSummary;
  opportunity: OpportunitySummary;
}

export interface SavedDealListResponse {
  items: SavedDealItem[];
}

export async function getDeals(status?: UserDealStatus): Promise<SavedDealListResponse> {
  return apiFetch<SavedDealListResponse>("/api/v1/deals", {
    params: { status },
  });
}

export async function saveDeal(listingId: string, payload: SaveDealRequest = { status: "saved" }): Promise<UserDealResponse> {
  return apiFetch<UserDealResponse>(`/api/v1/deals/${listingId}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export async function deleteDeal(listingId: string): Promise<void> {
  await apiFetch<void>(`/api/v1/deals/${listingId}`, { method: "DELETE" });
}
