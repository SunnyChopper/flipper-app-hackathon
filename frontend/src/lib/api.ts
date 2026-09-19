import { API_BASE_URL, apiFetch } from "@/api/apiClient";

export type ApiHealth = {
  status: string;
  service: string;
  supabase: boolean;
  ebay: boolean;
  apify: boolean;
  llm: boolean;
};

export async function fetchHealth(): Promise<ApiHealth> {
  return apiFetch<ApiHealth>("/health");
}

export { API_BASE_URL };
