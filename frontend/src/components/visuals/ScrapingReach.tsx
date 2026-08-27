import { useEffect, useState } from 'react';
import { useLocale } from '../../lib/useLocale';

const t = {
  header: { es: 'Plataformas conquistadas', en: 'Platforms conquered' },
  artists: { es: 'artistas rastreados', en: 'artists tracked' },
  platforms: { es: 'plataformas', en: 'platforms' },
  resilience: { es: 'resiliencia', en: 'resilience' },
};

const platforms = [
  {
    name: 'Ticketmaster',
    challenge: { es: 'Considerado imposible', en: 'Considered impossible' },
    result: { es: 'Funcionando a escala', en: 'Running at scale' },
    color: '#ef4444',
  },
  {
    name: 'Discogs',
    challenge: { es: '7 meses sin resolver por otro ingeniero', en: '7 months unsolved by another engineer' },
    result: { es: '5 scrapers coordinados', en: '5 scrapers coordinated' },
    color: '#e11d48',
  },
  {
    name: 'TikTok',
    challenge: { es: 'Apagón total de datos', en: 'Total data outage' },
    result: { es: '$1,500 → $50/mes', en: '$1,500 → $50/mo' },
    color: '#f97316',
  },
  {
    name: 'Tunefind',
    challenge: { es: 'Alineación API + HTML a escala', en: 'API + HTML alignment at scale' },
    result: { es: '2 pipelines → 1 unificado', en: '2 pipelines → 1 unified' },
    color: '#f59e0b',
  },
  {
    name: 'Shazam',
    challenge: { es: 'Millones de requests, costo masivo', en: 'Millions of requests, massive cost' },
    result: { es: 'Costo optimizado, PG + CH', en: 'Cost-optimized, PG + CH' },
    color: '#eab308',
  },
  {
    name: 'Genius',
    challenge: { es: 'Equilibrio de throttling preciso', en: 'Precise throttle balancing' },
    result: { es: 'Presupuesto por token', en: 'Per-token budgeting' },
    color: '#facc15',
  },
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
          <div
            key={p.name}
            className="flex items-center gap-4 rounded-xl border border-[var(--color-border)] bg-[var(--color-bg)] px-4 py-3 transition-all duration-700"
            style={{
              opacity: visible ? 1 : 0,
              transform: visible ? 'translateX(0)' : 'translateX(-12px)',
              transitionDelay: `${i * 0.1}s`,
            }}
          >
            {/* Color indicator */}
            <div
              className="h-10 w-1 rounded-full flex-shrink-0"
              style={{ backgroundColor: p.color }}
            />

            {/* Platform info */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="text-sm font-bold text-[var(--color-fg)]">{p.name}</span>
              </div>
              <span className="text-xs text-[var(--color-fg-faint)]">{p.challenge[locale]}</span>
            </div>

            {/* Result */}
            <div className="flex-shrink-0 text-right">
              <span
                className="text-xs font-semibold px-2.5 py-1 rounded-full"
                style={{ color: p.color, backgroundColor: `${p.color}12` }}
              >
                {p.result[locale]}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Stats */}
      <div
        className="mt-6 grid grid-cols-3 gap-4 text-center transition-all duration-700"
        style={{ opacity: visible ? 1 : 0.3, transitionDelay: '0.8s' }}
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
