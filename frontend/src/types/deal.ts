export type UserDealStatus = "saved" | "acquired" | "dismissed";

export interface SaveDealRequest {
  status: UserDealStatus;
  notes?: string | null;
}

export interface UserDealSummary {
  id: string;
  listingId?: string;
  status: UserDealStatus;
  notes?: string | null;
  createdAt: string;
  updatedAt?: string;
}

export interface UserDealResponse {
  id: string;
  listingId: string;
  status: UserDealStatus;
  notes?: string | null;
  createdAt: string;
  updatedAt: string;
}
