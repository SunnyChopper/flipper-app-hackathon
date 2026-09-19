import type { InputHTMLAttributes } from "react";
import { cn } from "@/lib/cn";

type InputProps = InputHTMLAttributes<HTMLInputElement> & {
  label: string;
};

export function Input({ label, id, className, ...props }: InputProps) {
  const inputId = id ?? props.name;
  return (
    <label className="block">
      <span className="mb-1.5 block text-[13px] font-medium text-foreground">{label}</span>
      <input
        id={inputId}
        className={cn(
          "h-11 w-full rounded-input border border-border bg-white px-3 text-sm outline-none transition hover:border-border-strong focus:border-primary",
          className,
        )}
        {...props}
      />
    </label>
  );
}
