import { FormEvent, useEffect, useState } from "react";
import { createSavedSearch, fetchSavedSearches } from "../lib/api";
import type { SavedSearch } from "../types/deal";

export function SavedSearchesPage() {
  const [items, setItems] = useState<SavedSearch[]>([]);
  const [name, setName] = useState("Weekend tool hunt");
  const [query, setQuery] = useState("dewalt milwaukee");

  async function load() {
    setItems(await fetchSavedSearches());
  }

  useEffect(() => {
    void load().catch(() => setItems([]));
  }, []);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    await createSavedSearch({ name, query });
    await load();
  }

  return (
    <main>
      <h1 className="serif">Saved searches</h1>
      <p className="banner">Alerts land here. Wire Supabase Auth to scope them per user.</p>
      <form className="filters" onSubmit={(event) => void onSubmit(event)}>
        <input value={name} onChange={(event) => setName(event.target.value)} placeholder="Name" />
        <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Query" />
        <button type="submit">Save</button>
      </form>
      <section className="search-list">
        {items.map((item) => (
          <article className="search-item" key={item.id}>
            <div>
              <h2 className="serif">{item.name}</h2>
              <div className="kicker">{item.query || "empty query"}</div>
            </div>
            <span>{item.notify ? "Notify on" : "Silent"}</span>
          </article>
        ))}
      </section>
    </main>
  );
}
