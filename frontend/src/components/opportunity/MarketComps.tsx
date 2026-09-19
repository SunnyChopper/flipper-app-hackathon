import { useState } from "react";
import { formatCurrency, median } from "@/lib/formatting";
import { conditionLabel, marketCompSourceLabel } from "@/lib/labels";
import type { MarketCompSummary } from "@/types/catalog";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

export function MarketComps({ comps }: { comps: MarketCompSummary[] }) {
  const [open, setOpen] = useState(false);
  const mid = median(comps.map((comp) => comp.totalPrice));

  return (
    <>
      <Card className="p-5">
        <div className="mb-3 flex items-center justify-between gap-3">
          <h3 className="text-lg font-semibold tracking-tight">Market Comps (Working Units)</h3>
          {comps.length > 3 ? (
            <button type="button" onClick={() => setOpen(true)} className="text-[13px] font-medium text-info">
              View all →
            </button>
          ) : null}
        </div>
        {comps.length ? (
          <>
            <ul className="space-y-3">
              {comps.slice(0, 3).map((comp) => (
                <li key={comp.id} className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <div className="truncate text-sm font-medium">{marketCompSourceLabel(comp.source)}</div>
                    <div className="text-xs text-muted">
                      {conditionLabel(comp.itemCondition)} • {comp.soldDate}
                    </div>
                  </div>
                  <div className="text-sm font-semibold tabular">{formatCurrency(comp.totalPrice)}</div>
                </li>
              ))}
            </ul>
            <div className="mt-4 flex items-center justify-between border-t border-border pt-3 text-sm font-semibold">
              <span>Median working value</span>
              <span className="tabular">{formatCurrency(mid)}</span>
            </div>
          </>
        ) : (
          <p className="text-sm text-muted">No sold comps are available yet.</p>
        )}
      </Card>

      {open ? (
        <div className="fixed inset-0 z-50 grid place-items-center bg-black/30 p-4" onClick={() => setOpen(false)}>
          <Card className="w-full max-w-md p-5" onClick={(event) => event.stopPropagation()}>
            <h3 className="text-lg font-semibold">All comps</h3>
            <ul className="mt-3 space-y-3">
              {comps.map((comp) => (
                <li key={comp.id} className="flex justify-between gap-3 text-sm">
                  <span>
                    {marketCompSourceLabel(comp.source)} • {comp.soldDate}
                  </span>
                  <span className="font-semibold tabular">{formatCurrency(comp.totalPrice)}</span>
                </li>
              ))}
            </ul>
            <Button variant="secondary" className="mt-4 w-full" onClick={() => setOpen(false)}>
              Close
            </Button>
          </Card>
        </div>
      ) : null}
    </>
  );
}
