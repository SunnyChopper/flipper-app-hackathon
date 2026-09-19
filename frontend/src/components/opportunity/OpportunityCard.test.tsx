import { render, screen } from "@testing-library/react";
import * as TooltipPrimitive from "@radix-ui/react-tooltip";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { OpportunityCard } from "@/components/opportunity/OpportunityCard";
import { iphoneSummary } from "@/test/fixtures";

function renderCard() {
  return render(
    <TooltipPrimitive.Provider>
      <MemoryRouter>
        <OpportunityCard opportunity={iphoneSummary} />
      </MemoryRouter>
    </TooltipPrimitive.Provider>,
  );
}

describe("OpportunityCard contract mapping", () => {
  it("renders deal score, asking price, working value, repair cost, and profit from the API DTO", () => {
    renderCard();

    expect(screen.getByText("91")).toBeInTheDocument();
    expect(screen.getByText("$220")).toBeInTheDocument();
    expect(screen.getByText("$425")).toBeInTheDocument();
    expect(screen.getByText("$90")).toBeInTheDocument();
    expect(screen.getByText("$115")).toBeInTheDocument();
    expect(screen.getByText("Asking Price")).toBeInTheDocument();
    expect(screen.getByText("Est. Working Value")).toBeInTheDocument();
    expect(screen.getByText("Est. Repair")).toBeInTheDocument();
  });

  it("routes View Details by Listing.id", () => {
    renderCard();
    const details = screen.getByRole("link", { name: "View Details" });
    expect(details).toHaveAttribute("href", `/opportunities/${iphoneSummary.listingId}`);
  });

  it("shows condition and marketplace badges from Listing fields", () => {
    renderCard();
    expect(screen.getByText("Damaged")).toBeInTheDocument();
    expect(screen.getByText("Facebook Marketplace")).toBeInTheDocument();
  });
});
