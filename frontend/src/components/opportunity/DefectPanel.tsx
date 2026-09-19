import { CircleCheck } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { formatCurrency } from "@/lib/formatting";
import type { DefectiveComponent } from "@/types/catalog";

export function DefectPanel({ defects }: { defects: DefectiveComponent[] }) {
  return (
    <Card className="p-5">
      <h3 className="text-lg font-semibold tracking-tight">Detected Condition</h3>
      {defects.length ? (
        <ul className="mt-3 space-y-3">
          {defects.map((defect) => (
            <li key={defect.bomItemId} className="flex items-start gap-2 text-[13px] text-foreground">
              <CircleCheck className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
              <div>
                <div className="font-medium">{defect.componentName}</div>
                <div className="text-muted">Estimated replacement: {formatCurrency(defect.avgReplacementCost)}</div>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-3 text-sm text-muted">No defective components were detected.</p>
      )}
    </Card>
  );
}
