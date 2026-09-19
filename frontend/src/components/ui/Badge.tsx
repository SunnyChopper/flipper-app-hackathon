import type { HTMLAttributes } from "react";
import { cn } from "@/lib/cn";

type BadgeProps = HTMLAttributes<HTMLSpanElement> & {
  tone?: "neutral" | "success" | "warning" | "info";
};

export function Badge({ className, tone = "neutral", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-1 text-[11px] font-medium",
        tone === "neutral" && "bg-[#f2f4f7] text-[#475467]",
        tone === "success" && "bg-primary-soft text-[#067647]",
        tone === "warning" && "bg-warning-soft text-[#b54708]",
        tone === "info" && "bg-info-soft text-info",
        className,
      )}
      {...props}
    />
  );
}
