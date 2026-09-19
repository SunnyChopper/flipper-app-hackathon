import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { ArrowLeft, ExternalLink, Heart, Info } from "lucide-react";
import { PageContainer } from "@/components/layout/PageContainer";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Tooltip } from "@/components/ui/Tooltip";
import { DefectPanel } from "@/components/opportunity/DefectPanel";
import { DealScoreBadge } from "@/components/opportunity/DealScoreBadge";
import { ListingImage } from "@/components/opportunity/ListingImage";
import { MarketComps } from "@/components/opportunity/MarketComps";
import { MarketplaceBadge } from "@/components/opportunity/MarketplaceBadge";
import { MetricRow } from "@/components/opportunity/MetricRow";
import { RequiredSkillsPanel } from "@/components/opportunity/RequiredSkillsPanel";
import { OpportunityDetailSkeleton } from "@/components/opportunity/Skeletons";
import { useOpportunity } from "@/hooks/useOpportunity";
import { useDealMutations } from "@/hooks/useSavedDeals";
import { formatCurrency, formatRelativeTime, formatRoi } from "@/lib/formatting";
import { conditionLabel } from "@/lib/labels";
import { scoreLabel } from "@/lib/score";
import { useSavedStore } from "@/store/savedStore";
import { NotFoundPage } from "./NotFoundPage";

export function OpportunityPage() {
  const { id } = useParams();
  const { opportunity, loading, error, notFound } = useOpportunity(id);
  const listing = opportunity?.listing;
  const [image, setImage] = useState<string | undefined>(undefined);
  const saved = useSavedStore((state) => (id ? state.savedIds.includes(id) : false));
  const { toggle } = useDealMutations();

  const activeImage = image ?? listing?.imageUrls[0] ?? "";
  const gallery = listing?.imageUrls?.length ? listing.imageUrls : activeImage ? [activeImage] : [];
  const title = opportunity?.product?.displayName ?? listing?.title ?? "";

  if (notFound) return <NotFoundPage />;
  if (loading || !opportunity || !listing) {
    return (
      <PageContainer>
        {error ? (
          <EmptyError message={error} />
        ) : (
          <OpportunityDetailSkeleton />
        )}
      </PageContainer>
    );
  }

  const { financials, dealScore, defects, requiredSkills, marketComps, product } = opportunity;

  return (
    <PageContainer>
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <Link to="/radar" className="inline-flex items-center gap-1.5 text-sm text-muted hover:text-foreground">
          <ArrowLeft className="h-4 w-4" />
          Back to results
        </Link>
        <div className="flex items-center gap-2">
          <Button type="button" variant="secondary" onClick={() => void toggle(listing.id)}>
            <Heart className={`h-4 w-4 ${saved ? "fill-danger text-danger" : ""}`} />
            {saved ? "Saved" : "Save Deal"}
          </Button>
          <Button asChild>
            <a href={listing.url} target="_blank" rel="noopener noreferrer" aria-label="Open external marketplace listing">
              Open Listing
              <ExternalLink className="h-3.5 w-3.5" />
            </a>
          </Button>
        </div>
      </div>

      <div className="grid gap-8 lg:grid-cols-[40%_1fr]">
        <div>
          <div className="overflow-hidden rounded-card border border-border bg-[#F5F6F7]">
            <AnimatePresence mode="wait">
              <motion.div key={activeImage} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.16 }}>
                <ListingImage src={activeImage} alt={title} className="mx-auto aspect-square w-full max-w-[380px]" />
              </motion.div>
            </AnimatePresence>
          </div>
          <div className="mt-3 flex gap-2">
            {gallery.map((src) => (
              <button
                key={src}
                type="button"
                onClick={() => setImage(src)}
                className={`overflow-hidden rounded-lg border-2 ${activeImage === src ? "border-primary" : "border-transparent"}`}
                aria-label="View product photo"
              >
                <ListingImage src={src} alt="" className="h-16 w-16" />
              </button>
            ))}
          </div>
        </div>

        <div>
          <div className="flex items-center gap-3">
            <Tooltip content="Deal Score considers estimated margin, ROI and pricing confidence.">
              <span>
                <DealScoreBadge score={dealScore.total} className="h-10 w-12 text-base" />
              </span>
            </Tooltip>
            <div>
              <div className="text-xs font-medium text-muted">Deal Score</div>
              <Badge tone="success">{scoreLabel(dealScore.total)}</Badge>
            </div>
          </div>
          <h1 className="mt-4 text-[32px] font-bold tracking-[-0.035em]">{title}</h1>
          {listing.description ? <p className="mt-2 text-sm text-muted">{listing.description}</p> : null}
          <div className="mt-3 flex flex-wrap items-center gap-2 text-sm text-muted">
            <MarketplaceBadge source={listing.source} />
            {listing.listedAt ? (
              <>
                <span>•</span>
                <span>{formatRelativeTime(listing.listedAt)}</span>
              </>
            ) : null}
          </div>
          <div className="mt-4 flex flex-wrap gap-1.5">
            {product ? <Badge>{product.category}</Badge> : null}
            <Badge tone="warning">{conditionLabel(listing.condition)}</Badge>
          </div>
        </div>
      </div>

      <Card className="mt-8 p-5">
        <MetricRow
          asking={financials.purchasePrice}
          value={financials.estimatedWorkingMarketValue}
          repair={financials.totalReplacementCost}
        />
      </Card>

      <div className="mt-3 rounded-card border border-primary-border bg-gradient-to-r from-[#ecfdf5] to-[#f0fdf4] px-5 py-5 sm:flex sm:items-end sm:justify-between">
        <div>
          <div className="text-[11px] uppercase tracking-wide text-[#059669]">Potential profit</div>
          <div className="mt-1 text-[30px] font-bold tabular leading-none text-[#067647]">
            {formatCurrency(financials.projectedRestorerNet)}
          </div>
        </div>
        <div className="mt-3 text-right sm:mt-0">
          <div className="text-[11px] uppercase tracking-wide text-muted">ROI</div>
          <div className="text-2xl font-bold tabular">{formatRoi(financials.roiPercent)}</div>
        </div>
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <div className="space-y-4">
          <DefectPanel defects={defects} />
          <RequiredSkillsPanel skills={requiredSkills} />
        </div>
        <MarketComps comps={marketComps} />
      </div>

      <div className="mt-6 flex gap-3 rounded-card border border-[#bfdbfe] bg-info-soft p-4 text-sm text-[#1d4ed8]">
        <Info className="mt-0.5 h-4 w-4 shrink-0" />
        <div>
          <div className="font-medium">This is an estimate, not a guarantee.</div>
          <p className="mt-1 text-[13px] text-[#1e40af]">
            Values are based on recent market data and may vary. Always verify item condition before purchasing.
          </p>
        </div>
      </div>
    </PageContainer>
  );
}

function EmptyError({ message }: { message: string }) {
  return (
    <div className="rounded-card border border-border bg-white p-6 text-sm text-muted">
      Could not load this opportunity. {message}
    </div>
  );
}
