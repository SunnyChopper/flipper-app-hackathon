import { describe, expect, it } from "vitest";
import { resolveApiBaseUrl } from "./apiClient";

describe("resolveApiBaseUrl", () => {
  it("uses an explicit hosted API URL when set", () => {
    expect(
      resolveApiBaseUrl(
        { VITE_API_BASE_URL: "https://api.example.com/", DEV: false },
        "https://app.vercel.app",
      ),
    ).toBe("https://api.example.com");
  });

  it("uses the page origin when no API URL is set", () => {
    expect(resolveApiBaseUrl({ DEV: false }, "https://deal-sniper.vercel.app")).toBe(
      "https://deal-sniper.vercel.app",
    );
    expect(resolveApiBaseUrl({ DEV: true }, "http://localhost:5173")).toBe("http://localhost:5173");
  });

  it("ignores localhost API URLs outside development so Vercel does not call the local machine", () => {
    expect(
      resolveApiBaseUrl(
        { VITE_API_URL: "http://localhost:8000", DEV: false },
        "https://deal-sniper.vercel.app",
      ),
    ).toBe("https://deal-sniper.vercel.app");
  });

  it("honors a localhost API URL during local development", () => {
    expect(
      resolveApiBaseUrl(
        { VITE_API_URL: "http://localhost:8000", DEV: true },
        "http://localhost:5173",
      ),
    ).toBe("http://localhost:8000");
  });
});
