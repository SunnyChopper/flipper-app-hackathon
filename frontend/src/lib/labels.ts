import type { MarketplaceSource } from "@/types/opportunity";

export const CONDITION_LABELS: Record<string, string> = {
  for_parts: "For Parts",
  damaged: "Damaged",
  used_fair: "Used (Fair)",
  locked: "Locked",
  used_working: "Used (Working)",
};

export function conditionLabel(condition: string): string {
  return CONDITION_LABELS[condition] ?? condition.replaceAll("_", " ");
}

export function marketplaceLabel(source: MarketplaceSource): string {
  return source === "facebook_marketplace" ? "Facebook Marketplace" : "eBay";
}

export function marketCompSourceLabel(source: string): string {
  if (source === "ebay_sold") return "eBay sold";
  return source.replaceAll("_", " ");
}
