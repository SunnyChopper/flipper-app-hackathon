const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export type ApiHealth = {
  status: string;
  service: string;
  supabase: boolean;
  ebay: boolean;
  apify: boolean;
  llm: boolean;
};

export async function fetchHealth(): Promise<ApiHealth> {
  const response = await fetch(`${API_URL}/health`);
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json() as Promise<ApiHealth>;
}
