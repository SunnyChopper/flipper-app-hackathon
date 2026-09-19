import { formatCurrency } from "@/lib/formatting";

export function MetricRow({
  asking,
  value,
  repair,
  fees,
}: {
  asking: number;
  value: number;
  repair: number;
  fees?: number;
}) {
  const items = [
    { label: "Asking", amount: asking },
    { label: "Est. Value", amount: value },
    { label: "Est. Repair", amount: repair },
    ...(fees != null ? [{ label: "Est. Fees", amount: fees }] : []),
  ];

  const columns = items.length > 3 ? "grid-cols-2 md:grid-cols-4" : "grid-cols-3";

  return (
    <div className={`grid gap-3 md:flex md:items-stretch ${columns}`}>
      {items.map((item, index) => (
        <div
          key={item.label}
          className={`min-w-0 ${index > 0 ? "md:border-l md:border-border md:pl-5" : ""} ${fees != null ? "md:flex-1" : ""}`}
        >
          <div className="text-[15px] font-semibold tabular tracking-tight">{formatCurrency(item.amount)}</div>
          <div className="mt-0.5 text-[11px] uppercase tracking-wide text-muted">{item.label}</div>
        </div>
      ))}
    </div>
  );
}
