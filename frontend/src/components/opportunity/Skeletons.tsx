import { Card } from "@/components/ui/Card";
import { Skeleton } from "@/components/ui/Skeleton";

export function OpportunityCardSkeleton() {
  return (
    <Card className="p-5">
      <div className="flex gap-4">
        <Skeleton className="h-[120px] w-[120px] shrink-0" />
        <div className="min-w-0 flex-1 space-y-3">
          <Skeleton className="h-5 w-2/3" />
          <Skeleton className="h-4 w-1/2" />
          <div className="flex gap-6 pt-2">
            <Skeleton className="h-8 w-20" />
            <Skeleton className="h-8 w-20" />
            <Skeleton className="h-8 w-20" />
          </div>
        </div>
      </div>
    </Card>
  );
}

export function OpportunityDetailSkeleton() {
  return (
    <div className="space-y-5">
      <Skeleton className="h-8 w-40" />
      <div className="grid gap-6 lg:grid-cols-[40%_1fr]">
        <Skeleton className="aspect-square w-full" />
        <div className="space-y-3">
          <Skeleton className="h-8 w-3/4" />
          <Skeleton className="h-5 w-1/2" />
          <Skeleton className="h-24 w-full" />
        </div>
      </div>
      <Skeleton className="h-28 w-full" />
      <div className="grid gap-4 md:grid-cols-2">
        <Skeleton className="h-40 w-full" />
        <Skeleton className="h-40 w-full" />
      </div>
    </div>
  );
}
