import type { ReactNode } from "react";
import { cn } from "@/lib/cn";

export function PageContainer({
  children,
  wide,
  className,
}: {
  children: ReactNode;
  wide?: boolean;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "mx-auto w-full px-4 py-4 md:px-6 md:py-8",
        wide ? "max-w-[1320px]" : "max-w-[1280px]",
        className,
      )}
    >
      {children}
    </div>
  );
}
