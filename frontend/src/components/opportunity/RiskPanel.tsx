import { TriangleAlert } from "lucide-react";

export function RiskPanel({ items }: { items: { id: string; label: string }[] }) {
  return (
    <div className="rounded-card border border-[#fde68a] bg-warning-soft p-5">
      <h3 className="text-lg font-semibold tracking-tight">Unknowns / Risks</h3>
      <p className="mt-1 text-xs text-[#b54708]">Information uncertainty — verify before you buy.</p>
      <ul className="mt-3 space-y-2.5">
        {items.map((item) => (
          <li key={item.id} className="flex items-start gap-2 text-[13px] text-[#7a4a08]">
            <TriangleAlert className="mt-0.5 h-4 w-4 shrink-0 text-warning" />
            {item.label}
          </li>
        ))}
      </ul>
    </div>
  );
}
