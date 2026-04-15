import { useState, useEffect } from 'react';

export type Locale = 'es' | 'en';

/** Detect locale from URL. Safe for SSR (defaults to 'es', updates after mount). */
export function useLocale(): Locale {
  const [locale, setLocale] = useState<Locale>('es');
  useEffect(() => {
    if (window.location.pathname.startsWith('/en/') || window.location.pathname === '/en') {
      setLocale('en');
    }
  }, []);
  return locale;
}
