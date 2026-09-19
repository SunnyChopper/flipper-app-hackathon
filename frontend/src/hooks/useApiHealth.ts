import { useEffect, useState } from "react";
import { fetchHealth, type ApiHealth } from "@/lib/api";

export function useApiHealth() {
  const [health, setHealth] = useState<ApiHealth | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    void fetchHealth()
      .then((data) => {
        if (!cancelled) {
          setHealth(data);
          setError(null);
        }
      })
      .catch((err: Error) => {
        if (!cancelled) {
          setHealth(null);
          setError(err.message);
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return { health, error, loading };
}
