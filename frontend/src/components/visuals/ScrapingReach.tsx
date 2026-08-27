import { useEffect, useState } from 'react';
import { useLocale } from '../../lib/useLocale';

const t = {
  header: { es: 'Alcance de scraping', en: 'Scraping reach' },
  artists: { es: 'artistas rastreados', en: 'artists tracked' },
  platforms: { es: 'plataformas', en: 'platforms' },
  resilience: { es: 'resiliencia', en: 'resilience' },
  recovered: { es: 'recuperado', en: 'recovered' },
};

const platforms = [
  { name: 'Ticketmaster', difficulty: 98, color: '#ef4444', label: 'Hardest' },
  { name: 'TikTok', difficulty: 90, color: '#e11d48', label: 'Outage recovered' },
  { name: 'Genius', difficulty: 72, color: '#f97316', label: '' },
  { name: 'Shazam', difficulty: 65, color: '#f59e0b', label: '' },
  { name: 'Discogs', difficulty: 60, color: '#eab308', label: '' },
  { name: 'Tunefind', difficulty: 55, color: '#facc15', label: '' },
];

export default function ScrapingReach() {
  const locale = useLocale();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const raf = requestAnimationFrame(() => {
      requestAnimationFrame(() => setVisible(true));
    });
    return () => cancelAnimationFrame(raf);
  }, []);

  return (
    <div className="my-10 rounded-2xl border border-[var(--color-border)] bg-[var(--color-bg-card)] p-6 md:p-8">
      <div className="flex items-center gap-2 mb-6">
        <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
        <span className="text-xs font-bold uppercase tracking-[0.15em] text-[var(--color-fg-faint)]">
          {t.header[locale]}
        </span>
      </div>

      <div className="space-y-3">
        {platforms.map((p, i) => (
          <div key={p.name}>
            <div className="flex items-baseline justify-between mb-1">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-[var(--color-fg)]">{p.name}</span>
                {p.label && (
                  <span className="text-[0.6rem] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded-full"
                    style={{ color: p.color, backgroundColor: `${p.color}15` }}>
                    {p.label}
                  </span>
                )}
              </div>
              <span className="text-xs text-[var(--color-fg-faint)]">{p.difficulty}%</span>
            </div>
            <div className="h-6 rounded-md bg-[var(--color-bg)] overflow-hidden">
              <div
                className="h-full rounded-md transition-all duration-[1.5s] ease-out"
                style={{
                  width: visible ? `${p.difficulty}%` : '0%',
                  backgroundColor: p.color,
                  opacity: 0.7,
                  transitionDelay: `${i * 0.12}s`,
                }}
              />
            </div>
          </div>
        ))}
      </div>

      <div className="mt-2 text-right">
        <span className="text-[0.6rem] text-[var(--color-fg-faint)] italic">
          {locale === 'es' ? 'dificultad anti-scraping relativa' : 'relative anti-scraping difficulty'}
        </span>
      </div>

      {/* Stats */}
      <div
        className="mt-6 grid grid-cols-3 gap-4 text-center transition-all duration-700"
        style={{ opacity: visible ? 1 : 0.3, transitionDelay: '1s' }}
      >
        <div>
          <p className="text-lg font-extrabold text-[var(--color-accent)]">15M+</p>
          <p className="text-[0.65rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.artists[locale]}</p>
        </div>
        <div>
          <p className="text-lg font-extrabold text-[var(--color-accent)]">6+</p>
          <p className="text-[0.65rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.platforms[locale]}</p>
        </div>
        <div>
          <p className="text-lg font-extrabold text-[var(--color-accent)]">100%</p>
          <p className="text-[0.65rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.resilience[locale]}</p>
        </div>
      </div>
    </div>
  );
}
