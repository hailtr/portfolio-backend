import { useState, useEffect } from "react";

const CACHE_DURATION = 1000 * 60 * 60 * 24; // 24 Horas

export const useCachedFetch = (url, cacheKey) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!url) return;

    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        if (cacheKey) {
          const cachedItem = localStorage.getItem(cacheKey);
          if (cachedItem) {
            const parsed = JSON.parse(cachedItem);
            if (Date.now() - parsed.timestamp < CACHE_DURATION) {
              console.log(`[Cache Hit] Usando datos locales para: ${cacheKey}`);
              setData(parsed.data);
              setLoading(false);
              return;
            }
          }
        }

        console.log(`[API Call] Fetching: ${url}`);
        const res = await fetch(url);

        if (!res.ok) {
          if (res.status === 429) throw new Error("RATELIMIT");
          throw new Error(`Error ${res.status}: ${res.statusText}`);
        }

        const jsonData = await res.json();

        if (cacheKey) {
          localStorage.setItem(
            cacheKey,
            JSON.stringify({
              data: jsonData,
              timestamp: Date.now(),
            }),
          );
        }

        setData(jsonData);
      } catch (err) {
        console.error("Fetch error:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url, cacheKey]);

  return { data, loading, error };
};
