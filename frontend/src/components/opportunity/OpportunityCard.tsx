import { Link } from "react-router-dom";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Tooltip } from "@/components/ui/Tooltip";
import { formatRelativeTime } from "@/lib/formatting";
import { conditionLabel } from "@/lib/labels";
import type { OpportunitySummary } from "@/types/opportunity";
import { DealScoreBadge } from "./DealScoreBadge";
import { ListingImage } from "./ListingImage";
import { MarketplaceBadge } from "./MarketplaceBadge";
import { MetricRow } from "./MetricRow";
import { OpportunityActions } from "./OpportunityActions";
import { ProfitBadge } from "./ProfitBadge";

export function OpportunityCard({ opportunity }: { opportunity: OpportunitySummary }) {
  const title = opportunity.product?.displayName ?? opportunity.title;

  return (
    <Card className="p-4 hover:-translate-y-0.5 hover:border-border-strong hover:shadow-card-hover md:p-5">
      <div className="flex flex-col gap-4 md:flex-row">
        <Link to={`/opportunities/${opportunity.listingId}`} className="shrink-0">
          <ListingImage
            src={opportunity.imageUrl}
            alt={title}
            className="h-40 w-full rounded-[10px] md:h-[120px] md:w-[120px]"
          />
        </Link>

        <div className="min-w-0 flex-1">
          <div className="flex items-start justify-between gap-3">
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <Tooltip content="Deal Score considers estimated margin, ROI and pricing confidence.">
                  <span>
                    <DealScoreBadge score={opportunity.dealScore} />
                  </span>
                </Tooltip>
                <Link to={`/opportunities/${opportunity.listingId}`} className="truncate text-[16px] font-semibold tracking-tight">
                  {title}
                </Link>
              </div>
              {opportunity.description ? <p className="mt-1 text-sm text-muted">{opportunity.description}</p> : null}
              <div className="mt-2 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-muted">
                <MarketplaceBadge source={opportunity.source} />
                {opportunity.listedAt ? (
                  <>
                    <span>•</span>
                    <span>{formatRelativeTime(opportunity.listedAt)}</span>
                  </>
                ) : null}
              </div>
            </div>
            <ProfitBadge profit={opportunity.projectedRestorerNet} />
          </div>

          <div className="mt-4">
            <MetricRow
              asking={opportunity.price}
              value={opportunity.product?.estimatedWorkingMarketValue ?? 0}
              repair={opportunity.estimatedRepairCost}
            />
          </div>

          <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex flex-wrap gap-1.5">
              <Badge tone="warning">{conditionLabel(opportunity.condition)}</Badge>
              {opportunity.product ? <Badge>{opportunity.product.category}</Badge> : null}
            </div>
            <OpportunityActions id={opportunity.listingId} listingUrl={opportunity.url} />
          </div>
        </div>
      </div>
    </Card>
  );
}
