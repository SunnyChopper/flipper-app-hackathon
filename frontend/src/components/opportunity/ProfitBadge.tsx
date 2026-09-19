import { formatCurrency } from "@/lib/formatting";
import { Tooltip } from "@/components/ui/Tooltip";

export function ProfitBadge({ profit }: { profit: number }) {
  return (
    <Tooltip content="Projected Restorer net after purchase, shipping, and replacement cost.">
      <div className="shrink-0 rounded-[10px] border border-[#d1fae5] bg-primary-soft px-3 py-2 text-right">
        <div className="text-xl font-bold tabular leading-none text-[#067647]">{formatCurrency(profit)}</div>
        <div className="mt-1 text-[11px] text-[#059669]">est. profit</div>
      </div>
    </Tooltip>
  );
}
