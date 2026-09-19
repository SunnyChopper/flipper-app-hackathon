import type { DealFilters } from "../types/deal";

type Props = {
  filters: DealFilters;
  onChange: (filters: DealFilters) => void;
  onRefresh: () => void;
};

export function FilterBar({ filters, onChange, onRefresh }: Props) {
  return (
    <form
      className="filters"
      onSubmit={(event) => {
        event.preventDefault();
        onRefresh();
      }}
    >
      <input
        placeholder="Search titles, brands, damage notes"
        value={filters.q ?? ""}
        onChange={(event) => onChange({ ...filters, q: event.target.value })}
      />
      <select
        value={filters.source ?? ""}
        onChange={(event) => onChange({ ...filters, source: event.target.value as DealFilters["source"] })}
      >
        <option value="">All markets</option>
        <option value="ebay">eBay</option>
        <option value="facebook">Facebook</option>
      </select>
      <input
        type="number"
        placeholder="Min profit"
        value={filters.min_profit ?? ""}
        onChange={(event) =>
          onChange({ ...filters, min_profit: event.target.value ? Number(event.target.value) : undefined })
        }
      />
      <input
        type="number"
        placeholder="Max risk"
        value={filters.max_risk ?? ""}
        onChange={(event) =>
          onChange({ ...filters, max_risk: event.target.value ? Number(event.target.value) : undefined })
        }
      />
      <button type="submit">Snipe</button>
    </form>
  );
}
