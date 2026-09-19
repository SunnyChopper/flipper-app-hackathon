import { useState } from "react";
import { formatCurrency, median } from "@/lib/formatting";
import type { MarketComp } from "@/types/opportunity";
import { ListingImage } from "./ListingImage";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

export function MarketComps({ comps }: { comps: MarketComp[] }) {
  const [open, setOpen] = useState(false);
  const mid = median(comps.map((comp) => comp.price));

  return (
    <>
      <Card className="p-5">
        <div className="mb-3 flex items-center justify-between gap-3">
          <h3 className="text-lg font-semibold tracking-tight">Market Comps (Working Units)</h3>
          <button type="button" onClick={() => setOpen(true)} className="text-[13px] font-medium text-info">
            View all →
          </button>
        </div>
        <ul className="space-y-3">
          {comps.slice(0, 3).map((comp) => (
            <li key={comp.id} className="flex items-center gap-3">
              <ListingImage
                src={comp.imageUrl}
                alt=""
                className="h-11 w-11 rounded-md border border-border"
              />
              <div className="min-w-0 flex-1">
                <div className="truncate text-sm font-medium">{comp.title}</div>
                <div className="text-xs text-muted">{comp.marketplace} • Used</div>
              </div>
              <div className="text-sm font-semibold tabular">{formatCurrency(comp.price)}</div>
            </li>
          ))}
        </ul>
        <div className="mt-4 flex items-center justify-between border-t border-border pt-3 text-sm font-semibold">
          <span>Median working value</span>
          <span className="tabular">{formatCurrency(mid)}</span>
        </div>
      </Card>

      {open ? (
        <div className="fixed inset-0 z-50 grid place-items-center bg-black/30 p-4" onClick={() => setOpen(false)}>
          <Card className="w-full max-w-md p-5" onClick={(event) => event.stopPropagation()}>
            <h3 className="text-lg font-semibold">All comps</h3>
            <ul className="mt-3 space-y-3">
              {comps.map((comp) => (
                <li key={comp.id} className="flex justify-between text-sm">
                  <span>{comp.title}</span>
                  <span className="font-semibold tabular">{formatCurrency(comp.price)}</span>
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
