import { getAccessToken } from "@/lib/supabase";

export type ApiEnv = {
  VITE_API_BASE_URL?: string;
  VITE_API_URL?: string;
  DEV?: boolean | string;
};

function stripTrailingSlash(url: string): string {
  return url.replace(/\/$/, "");
}

function isLocalhostUrl(url: string): boolean {
  try {
    const host = new URL(url).hostname;
    return host === "localhost" || host === "127.0.0.1";
  } catch {
    return false;
  }
}

export function resolveApiBaseUrl(
  env: ApiEnv = import.meta.env,
  origin = typeof window !== "undefined" ? window.location.origin : "http://localhost:8000",
): string {
  const configured = (env.VITE_API_BASE_URL || env.VITE_API_URL || "").trim();
  const isDev = env.DEV === true || env.DEV === "true";
  if (configured && (isDev || !isLocalhostUrl(configured))) {
    return stripTrailingSlash(configured);
  }
  return stripTrailingSlash(origin);
}

export const API_BASE_URL = resolveApiBaseUrl();

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

function buildUrl(path: string, params?: Record<string, string | number | undefined | null>): string {
  const url = new URL(path, API_BASE_URL);
  if (params) {
    for (const [key, value] of Object.entries(params)) {
      if (value === undefined || value === null || value === "") continue;
      url.searchParams.set(key, String(value));
    }
  }
  return url.toString();
}

export async function apiFetch<T>(
  path: string,
  init?: RequestInit & { params?: Record<string, string | number | undefined | null> },
): Promise<T> {
  const { params, ...requestInit } = init ?? {};
  const token = await getAccessToken();
  const response = await fetch(buildUrl(path, params), {
    ...requestInit,
    headers: {
      Accept: "application/json",
      ...(requestInit.body ? { "Content-Type": "application/json" } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...requestInit.headers,
    },
  });

  if (response.status === 204) {
    return undefined as T;
  }

  if (!response.ok) {
    throw new ApiError(`Request failed (${response.status})`, response.status);
  }

  return response.json() as Promise<T>;
}
