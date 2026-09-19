import { formatCurrency } from "@/lib/formatting";

export function MetricRow({
  asking,
  value,
  repair,
}: {
  asking: number;
  value: number;
  repair: number;
  fees?: number;
}) {
  const items = [
    { label: "Asking Price", amount: asking },
    { label: "Est. Working Value", amount: value },
    { label: "Est. Repair", amount: repair },
  ];

  return (
    <div className="grid grid-cols-3 gap-3 md:flex md:items-stretch">
      {items.map((item, index) => (
        <div key={item.label} className={`min-w-0 ${index > 0 ? "md:border-l md:border-border md:pl-5" : ""}`}>
          <div className="text-[15px] font-semibold tabular tracking-tight">{formatCurrency(item.amount)}</div>
          <div className="mt-0.5 text-[11px] uppercase tracking-wide text-muted">{item.label}</div>
        </div>
      ))}
    </div>
  );
}
