import { Search } from "lucide-react";
import { useEffect, useRef } from "react";
import { Button } from "@/components/ui/Button";

export function SearchBar({
  value,
  onChange,
  onSubmit,
  disabled = false,
}: {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  disabled?: boolean;
}) {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.key !== "/" || event.metaKey || event.ctrlKey || event.altKey) return;
      const target = event.target as HTMLElement;
      if (target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.isContentEditable) return;
      event.preventDefault();
      inputRef.current?.focus();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <form
      className="flex gap-2"
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit();
      }}
    >
      <label className="relative flex-1">
        <Search className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-subtle" />
        <input
          ref={inputRef}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder="iPhone 13"
          className="h-12 w-full rounded-input border border-border bg-white pl-10 pr-3 text-sm outline-none transition hover:border-border-strong focus:border-primary"
        />
      </label>
        <Button type="submit" className="h-12 px-5" disabled={disabled}>
          {disabled ? "Searching…" : "Search"}
        </Button>
    </form>
  );
}
