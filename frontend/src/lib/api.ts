import type { Deal, DealFilters, SavedSearch } from "../types/deal";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
    ...init,
  });
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json() as Promise<T>;
}

export function fetchDeals(filters: DealFilters = {}): Promise<Deal[]> {
  const params = new URLSearchParams();
  if (filters.q) params.set("q", filters.q);
  if (filters.source) params.set("source", filters.source);
  if (filters.min_profit != null) params.set("min_profit", String(filters.min_profit));
  if (filters.max_risk != null) params.set("max_risk", String(filters.max_risk));
  const query = params.toString();
  return request(`/api/deals${query ? `?${query}` : ""}`);
}

export function fetchDeal(id: string): Promise<Deal> {
  return request(`/api/deals/${id}`);
}

export function fetchSavedSearches(): Promise<SavedSearch[]> {
  return request("/api/searches");
}

export function createSavedSearch(body: { name: string; query: string }): Promise<SavedSearch> {
  return request("/api/searches", { method: "POST", body: JSON.stringify(body) });
}

export function ingestEbay(query: string): Promise<Deal[]> {
  return request(`/api/ingest/ebay?query=${encodeURIComponent(query)}`, { method: "POST" });
}

export function ingestFacebook(query: string): Promise<Deal[]> {
  return request(`/api/ingest/facebook?query=${encodeURIComponent(query)}`, { method: "POST" });
}
