import { Store } from "lucide-react";
import type { Marketplace } from "@/types/opportunity";

export function MarketplaceBadge({ source }: { source: Marketplace }) {
  return (
    <span className="inline-flex items-center gap-1.5 text-[13px] text-muted">
      <Store className="h-3.5 w-3.5" />
      {source === "facebook" ? "Facebook Marketplace" : "eBay"}
    </span>
  );
}
