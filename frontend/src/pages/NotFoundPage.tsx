import { useNavigate } from "react-router-dom";
import { PageContainer } from "@/components/layout/PageContainer";
import { EmptyState } from "@/components/ui/EmptyState";

export function NotFoundPage() {
  const navigate = useNavigate();
  return (
    <PageContainer>
      <EmptyState
        icon={<span className="text-3xl font-bold tracking-tight text-subtle">404</span>}
        title="Opportunity not found."
        description="That listing is no longer on the radar, or the link is incomplete."
        actionLabel="Return to Radar"
        onAction={() => navigate("/radar")}
      />
    </PageContainer>
  );
}
