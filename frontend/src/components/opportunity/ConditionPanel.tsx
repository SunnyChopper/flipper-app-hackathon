import { CircleCheck } from "lucide-react";
import { Card } from "@/components/ui/Card";

export function ConditionPanel({ items }: { items: string[] }) {
  return (
    <Card className="p-5">
      <h3 className="text-lg font-semibold tracking-tight">Detected Condition</h3>
      <ul className="mt-3 space-y-2.5">
        {items.map((item) => (
          <li key={item} className="flex items-start gap-2 text-[13px] text-foreground">
            <CircleCheck className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
            {item}
          </li>
        ))}
      </ul>
    </Card>
  );
}
