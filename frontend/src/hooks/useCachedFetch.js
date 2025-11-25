import { useState, useEffect } from "react";

const CACHE_DURATION = 1000 * 60 * 5; // 5 Minutes

export const useCachedFetch = (url, cacheKey) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!url) return;

    const fetchData = async () => {
      // 1. Try to load from cache first (Instant load)
      let cachedData = null;
      if (cacheKey) {
        const cachedItem = localStorage.getItem(cacheKey);
        if (cachedItem) {
          try {
            const parsed = JSON.parse(cachedItem);
            console.log(`[Cache Hit] Showing stale data for: ${cacheKey}`);
            setData(parsed.data);
            cachedData = parsed.data;
            setLoading(false); // Show content immediately
          } catch (e) {
            console.error("Cache parse error", e);
            localStorage.removeItem(cacheKey);
          }
        }
      }

      // TEMPORARILY DISABLED FOR PERFORMANCE TESTING
      // 2. Always fetch fresh data in background (Stale-While-Revalidate)
      /*
      try {
        console.log(`[API Call] Validating: ${url}`);
        const res = await fetch(url);
      
        if (!res.ok) {
          // If 404 (Deleted) or other error, clear cache and show error
          if (res.status === 404 && cacheKey) {
            console.log(`[Cache Invalidate] Resource deleted: ${cacheKey}`);
            localStorage.removeItem(cacheKey);
            setData(null); // Clear stale data
          }
      
          if (res.status === 429) throw new Error("RATELIMIT");
          throw new Error(`Error ${res.status}: ${res.statusText}`);
        }
      
        const jsonData = await res.json();
      
        // 3. Update cache and state if data changed
        // Simple comparison to avoid unnecessary re-renders
        if (JSON.stringify(jsonData) !== JSON.stringify(cachedData)) {
          console.log(`[Cache Update] Data refreshed for: ${cacheKey}`);
          if (cacheKey) {
            localStorage.setItem(
              cacheKey,
              JSON.stringify({
                data: jsonData,
                timestamp: Date.now(),
              })
            );
          }
          setData(jsonData);
        }
      
      } catch (err) {
        console.error("Fetch error:", err);
        // Only show error if we don't have cached data (fallback)
        // Or if it was a 404 (explicitly deleted)
        if (!cachedData || err.message.includes("404")) {
          setError(err.message);
            } finally {
              setLoading(false);
            }
            */
      // END TEMPORARY DISABLE
      setLoading(false);
    };

    fetchData();
  }, [url, cacheKey]);

  return { data, loading, error };
};
