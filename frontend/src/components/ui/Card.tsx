import type { HTMLAttributes } from "react";
import { cn } from "@/lib/cn";

export function Card({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "rounded-card border border-border bg-white shadow-card transition duration-[180ms] ease-out",
        className,
      )}
      {...props}
    />
  );
}
