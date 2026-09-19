import { Heart } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { PageContainer } from "@/components/layout/PageContainer";
import { Badge } from "@/components/ui/Badge";
import { EmptyState } from "@/components/ui/EmptyState";
import { SavedDealList } from "@/components/opportunity/SavedDealCard";
import { useSavedDeals } from "@/hooks/useSavedDeals";
import { useToastStore } from "@/store/toastStore";

export function SavedPage() {
  const navigate = useNavigate();
  const { items, count, remove } = useSavedDeals();
  const showToast = useToastStore((state) => state.show);

  return (
    <PageContainer>
      <div className="mb-6 flex items-end justify-between gap-4">
        <div>
          <h1 className="text-[32px] font-bold tracking-[-0.035em]">Saved Deals</h1>
          <p className="mt-4 text-sm text-muted">Your bookmarked opportunities</p>
        </div>
        <Badge>{count} item{count === 1 ? "" : "s"}</Badge>
      </div>

      {count ? (
        <SavedDealList
          items={items}
          onRemove={(id) => {
            remove(id);
            showToast("Removed from saved deals");
          }}
        />
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
