import { scoreTone } from "@/lib/score";
import { cn } from "@/lib/cn";

export function DealScoreBadge({ score, className }: { score: number; className?: string }) {
  const tone = scoreTone(score);
  return (
    <span
      className={cn(
        "inline-flex h-8 w-10 items-center justify-center rounded-md text-[15px] font-bold tabular",
        tone === "high" && "bg-primary-soft text-[#067647]",
        tone === "mid" && "bg-warning-soft text-[#b54708]",
        tone === "low" && "bg-[#f2f4f7] text-[#667085]",
        className,
      )}
    >
      {score}
    </span>
  );
}
