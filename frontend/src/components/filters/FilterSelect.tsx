import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/cn";

export function FilterSelect({
  label,
  value,
  onChange,
  options,
}: {
  label?: string;
  value: string;
  onChange: (value: string) => void;
  options: { label: string; value: string }[];
}) {
  return (
    <label className="relative inline-flex">
      {label ? <span className="sr-only">{label}</span> : null}
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className={cn(
          "h-9 appearance-none rounded-full border border-border bg-white py-0 pl-3 pr-8 text-[13px]",
          "transition hover:border-border-strong hover:bg-[#fafafa]",
        )}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      <ChevronDown className="pointer-events-none absolute right-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-subtle" />
    </label>
  );
}
