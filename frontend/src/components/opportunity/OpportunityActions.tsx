import { motion } from "framer-motion";
import { ExternalLink, Heart } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/Button";
import { useDealMutations } from "@/hooks/useSavedDeals";
import { useSavedStore } from "@/store/savedStore";

export function OpportunityActions({
  id,
  listingUrl,
  compact,
}: {
  id: string;
  listingUrl: string;
  compact?: boolean;
}) {
  const saved = useSavedStore((state) => state.savedIds.includes(id));
  const { toggle } = useDealMutations();

  return (
    <div className={`flex items-center gap-2 ${compact ? "" : "flex-wrap"}`}>
      <Button variant="secondary" asChild>
        <Link to={`/opportunities/${id}`}>View Details</Link>
      </Button>
      <Button asChild>
        <a href={listingUrl} target="_blank" rel="noopener noreferrer">
          Open Listing
          <ExternalLink className="h-3.5 w-3.5" />
        </a>
      </Button>
      <motion.div animate={saved ? { scale: [1, 1.12, 1] } : { scale: 1 }} transition={{ duration: 0.2 }}>
        <Button
          type="button"
          variant="icon"
          aria-label={saved ? "Remove saved opportunity" : "Save opportunity"}
          onClick={() => void toggle(id)}
        >
          <Heart className={`h-4 w-4 ${saved ? "fill-danger text-danger" : ""}`} />
        </Button>
      </motion.div>
    </div>
  );
}
