import { Heart } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { PageContainer } from "@/components/layout/PageContainer";
import { Badge } from "@/components/ui/Badge";
import { EmptyState } from "@/components/ui/EmptyState";
import { SavedDealList } from "@/components/opportunity/SavedDealCard";
import { OpportunityCardSkeleton } from "@/components/opportunity/Skeletons";
import { useSavedDeals } from "@/hooks/useSavedDeals";

export function SavedPage() {
  const navigate = useNavigate();
  const { items, count, loading, error, remove, refetch } = useSavedDeals();

  return (
    <PageContainer>
      <div className="mb-6 flex items-end justify-between gap-4">
        <div>
          <h1 className="text-[32px] font-bold tracking-[-0.035em]">Saved Deals</h1>
          <p className="mt-4 text-sm text-muted">Your bookmarked opportunities</p>
        </div>
        <Badge>{count} item{count === 1 ? "" : "s"}</Badge>
      </div>

      {loading ? (
        <div className="space-y-3">
          {Array.from({ length: 2 }).map((_, index) => (
            <OpportunityCardSkeleton key={index} />
          ))}
        </div>
      ) : error ? (
        <EmptyState
          icon={<Heart className="h-8 w-8" />}
          title="Could not load saved deals."
          description="The FastAPI service may be offline. Start the backend on port 8000 and try again."
          actionLabel="Retry"
          onAction={() => void refetch()}
        />
      ) : count ? (
        <SavedDealList items={items} onRemove={(id) => void remove(id)} />
      ) : (
        <EmptyState
          icon={<Heart className="h-8 w-8" />}
          title="No saved deals yet"
          description="Save interesting opportunities from the Radar and they’ll appear here."
          actionLabel="Explore Radar"
          onAction={() => navigate("/radar")}
        />
      )}
    </PageContainer>
  );
}
