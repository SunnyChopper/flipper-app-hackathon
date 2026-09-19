import { API_BASE_URL, apiFetch } from "@/api/apiClient";

export type ApiHealth = {
  status: string;
  service: string;
  supabase: boolean;
  ebay: boolean;
  apify: boolean;
  llm: boolean;
  crawl?: {
    enabled: boolean;
    intervalSeconds: number;
    running: boolean;
    lastCategory: string | null;
    lastQuery: string | null;
    lastInserted: number;
    lastSkipped: number;
    lastRejected: number;
    lastError: string | null;
    lastRunAt: string | null;
    nextCategory: string | null;
  };
};

export async function fetchHealth(): Promise<ApiHealth> {
  return apiFetch<ApiHealth>("/health");
}

export { API_BASE_URL };
