import { AnimatePresence, motion } from "framer-motion";
import { ExternalLink, Trash2 } from "lucide-react";
import { Link } from "react-router-dom";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import type { Opportunity } from "@/types/opportunity";
import { ListingImage } from "./ListingImage";
import { MarketplaceBadge } from "./MarketplaceBadge";
import { MetricRow } from "./MetricRow";
import { ProfitBadge } from "./ProfitBadge";

export function SavedDealCard({
  opportunity,
  onRemove,
}: {
  opportunity: Opportunity;
  onRemove: () => void;
}) {
  return (
    <motion.div
      layout
      initial={{ opacity: 1, height: "auto" }}
      exit={{ opacity: 0, height: 0, marginBottom: 0 }}
      transition={{ duration: 0.2 }}
      className="overflow-hidden"
    >
      <Card className="p-4">
        <div className="flex flex-col gap-4 md:flex-row">
          <ListingImage
            src={opportunity.imageUrl}
            alt={opportunity.title}
            className="h-28 w-full rounded-[10px] md:h-20 md:w-20"
          />
          <div className="min-w-0 flex-1">
            <div className="flex items-start justify-between gap-3">
              <div>
                <Link to={`/opportunities/${opportunity.id}`} className="text-[16px] font-semibold tracking-tight">
                  {opportunity.title}
                </Link>
                <p className="mt-1 text-sm text-muted">{opportunity.subtitle}</p>
                <div className="mt-1">
                  <MarketplaceBadge source={opportunity.source} />
                </div>
              </div>
              <ProfitBadge profit={opportunity.estimatedProfit} />
            </div>
            <div className="mt-3">
              <MetricRow
                asking={opportunity.askingPrice}
                value={opportunity.estimatedWorkingValue}
                repair={opportunity.estimatedRepairCost}
              />
            </div>
            <div className="mt-4 flex flex-wrap items-center gap-2">
              <Button variant="secondary" asChild>
                <Link to={`/opportunities/${opportunity.id}`}>View</Link>
              </Button>
              <Button asChild>
                <a href={opportunity.listingUrl} target="_blank" rel="noopener noreferrer">
                  Open Listing
                  <ExternalLink className="h-3.5 w-3.5" />
                </a>
              </Button>
              <Button type="button" variant="danger" aria-label="Remove saved opportunity" onClick={onRemove}>
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </Card>
    </motion.div>
  );
}

export function SavedDealList({
  items,
  onRemove,
}: {
  items: Opportunity[];
  onRemove: (id: string) => void;
}) {
  return (
    <div className="space-y-3">
      <AnimatePresence initial={false}>
        {items.map((item) => (
          <SavedDealCard key={item.id} opportunity={item} onRemove={() => onRemove(item.id)} />
        ))}
      </AnimatePresence>
    </div>
  );
}
