import { useEffect } from "react";
import { supabase } from "../lib/supabase";
import type { Deal } from "../types/deal";

export function useRealtimeDeals(onInsert: (hint: string) => void) {
  useEffect(() => {
    if (!supabase) return;
    const channel = supabase
      .channel("deal-snipes")
      .on(
        "postgres_changes",
        { event: "INSERT", schema: "public", table: "deal_scores" },
        (payload) => {
          const listingId = (payload.new as { listing_id?: string }).listing_id;
          onInsert(listingId ?? "new deal");
        },
      )
      .subscribe();
    return () => {
      void supabase?.removeChannel(channel);
    };
  }, [onInsert]);
}

export function mergeDeal(current: Deal[], incoming: Deal): Deal[] {
  return [incoming, ...current.filter((deal) => deal.listing.id !== incoming.listing.id)];
}
