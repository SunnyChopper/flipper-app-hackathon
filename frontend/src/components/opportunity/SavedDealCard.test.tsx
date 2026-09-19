import { render, screen } from "@testing-library/react";
import * as TooltipPrimitive from "@radix-ui/react-tooltip";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { SavedDealCard } from "@/components/opportunity/SavedDealCard";
import { iphoneSummary } from "@/test/fixtures";

describe("SavedDealCard", () => {
  it("displays saved listing projections from OpportunitySummary", () => {
    render(
      <TooltipPrimitive.Provider>
        <MemoryRouter>
          <SavedDealCard opportunity={iphoneSummary} onRemove={() => undefined} />
        </MemoryRouter>
      </TooltipPrimitive.Provider>,
    );

    expect(screen.getByText("Apple iPhone 13 128GB Unlocked")).toBeInTheDocument();
    expect(screen.getByText("$220")).toBeInTheDocument();
    expect(screen.getByText("$115")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "View" })).toHaveAttribute(
      "href",
      `/opportunities/${iphoneSummary.listingId}`,
    );
  });
});
