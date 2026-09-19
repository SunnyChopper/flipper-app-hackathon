import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { Pagination } from "@/components/filters/Pagination";

describe("Pagination", () => {
  it("hides when every result fits on one page", () => {
    const { container } = render(
      <Pagination page={1} pageSize={20} total={6} onPageChange={vi.fn()} />,
    );
    expect(container).toBeEmptyDOMElement();
  });

  it("shows the current range and moves between pages", () => {
    const onPageChange = vi.fn();
    render(<Pagination page={2} pageSize={20} total={47} onPageChange={onPageChange} />);

    expect(screen.getByText("Showing 21–40 of 47")).toBeInTheDocument();
    expect(screen.getByText("Page 2 of 3")).toBeInTheDocument();

    screen.getByRole("button", { name: "Previous page" }).click();
    expect(onPageChange).toHaveBeenCalledWith(1);

    screen.getByRole("button", { name: "Next page" }).click();
    expect(onPageChange).toHaveBeenCalledWith(3);
  });
});
