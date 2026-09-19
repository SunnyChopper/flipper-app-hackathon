import { Store } from "lucide-react";
import { marketplaceLabel } from "@/lib/labels";
import type { MarketplaceSource } from "@/types/opportunity";

export function MarketplaceBadge({ source }: { source: MarketplaceSource }) {
  return (
    <span className="inline-flex items-center gap-1.5 text-[13px] text-muted">
      <Store className="h-3.5 w-3.5" />
      {marketplaceLabel(source)}
    </span>
  );
}
