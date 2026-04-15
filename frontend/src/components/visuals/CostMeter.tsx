import { useEffect, useState } from 'react';
import { useLocale } from '../../lib/useLocale';

const t = {
  monthlyDataStackCost: { es: 'Costo mensual del stack de datos', en: 'Monthly data stack cost' },
  before: { es: 'Antes', en: 'Before' },
  after: { es: 'Después', en: 'After' },
  otherTools: { es: 'Otras herramientas', en: 'Other tools' },
  saved: { es: 'ahorrados', en: 'saved' },
  reduction: { es: 'reducci\u00f3n', en: 'reduction' },
};

/**
 * Stacked cost breakdown — shows WHERE the $83K went vs the $23K replacement.
 * Each segment animates in sequentially to reveal the cost structure.
 */
export default function CostMeter() {
  const locale = useLocale();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const raf = requestAnimationFrame(() => {
      requestAnimationFrame(() => setVisible(true));
    });
    return () => cancelAnimationFrame(raf);
  }, []);

  const beforeSegs = [
    { label: 'Snowflake', value: 30, color: '#29b5e8' },
    { label: 'Workato', value: 30, color: '#f97316' },
    { label: t.otherTools[locale], value: 23, color: '#64748b' },
  ];

  const afterSegs = [
    { label: 'ClickHouse', value: 12, color: '#facc15' },
    { label: 'S3', value: 3, color: '#f97316' },
    { label: 'Airflow', value: 5, color: '#10b981' },
    { label: 'Ops', value: 3, color: '#64748b' },
  ];

  const beforeTotal = beforeSegs.reduce((s, x) => s + x.value, 0);
  const afterTotal = afterSegs.reduce((s, x) => s + x.value, 0);
  const saved = beforeTotal - afterTotal;

  return (
    <div className="my-10 rounded-2xl border border-[var(--color-border)] bg-[var(--color-bg-card)] p-6 md:p-8">
      <div className="flex items-center gap-2 mb-6">
        <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
        <span className="text-xs font-bold uppercase tracking-[0.15em] text-[var(--color-fg-faint)]">
          {t.monthlyDataStackCost[locale]}
        </span>
      </div>

      <div className="space-y-6">
        {/* Before */}
        <div>
          <div className="flex items-baseline justify-between mb-2">
            <span className="text-sm font-medium text-[var(--color-fg-muted)]">{t.before[locale]}</span>
            <span className="text-sm font-bold text-[var(--color-fg)]">${beforeTotal}K/mo</span>
          </div>
          <div className="h-11 rounded-lg bg-[var(--color-bg)] overflow-hidden flex">
            {beforeSegs.map((seg, i) => (
              <div
                key={seg.label}
                className="h-full flex items-center justify-center transition-all duration-[1.2s] ease-out overflow-hidden"
                style={{
                  width: visible ? `${(seg.value / beforeTotal) * 100}%` : '0%',
                  backgroundColor: seg.color,
                  transitionDelay: `${i * 0.15}s`,
                }}
              >
                <span className="text-[0.5rem] font-bold text-white/80 whitespace-nowrap px-0.5">
                  ${seg.value}K
                </span>
              </div>
            ))}
          </div>
          <div className="flex gap-3 mt-1.5 flex-wrap">
            {beforeSegs.map(seg => (
              <div key={seg.label} className="flex items-center gap-1">
                <div className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: seg.color }} />
                <span className="text-[0.6rem] text-[var(--color-fg-faint)]">{seg.label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* After */}
        <div>
          <div className="flex items-baseline justify-between mb-2">
            <span className="text-sm font-medium text-[var(--color-fg-muted)]">{t.after[locale]}</span>
            <span className="text-sm font-bold text-[var(--color-accent)]">${afterTotal}K/mo</span>
          </div>
          <div className="h-11 rounded-lg bg-[var(--color-bg)] overflow-hidden flex">
            {afterSegs.map((seg, i) => (
              <div
                key={seg.label}
                className="h-full flex items-center justify-center transition-all duration-[1.2s] ease-out overflow-hidden"
                style={{
                  // Scale to same total width as "before" for visual comparison
                  width: visible ? `${(seg.value / beforeTotal) * 100}%` : '0%',
                  backgroundColor: seg.color,
                  transitionDelay: `${0.6 + i * 0.15}s`,
                }}
              >
                <span className="text-[0.5rem] font-bold text-white/80 whitespace-nowrap px-0.5">
                  ${seg.value}K
                </span>
              </div>
            ))}
          </div>
          <div className="flex gap-3 mt-1.5 flex-wrap">
            {afterSegs.map(seg => (
              <div key={seg.label} className="flex items-center gap-1">
                <div className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: seg.color }} />
                <span className="text-[0.6rem] text-[var(--color-fg-faint)]">{seg.label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Savings callout */}
      <div
        className="mt-6 flex items-center justify-center gap-3 rounded-xl border border-[rgba(34,211,238,0.15)] bg-[rgba(34,211,238,0.05)] px-4 py-3 transition-all duration-700"
        style={{ opacity: visible ? 1 : 0, transitionDelay: '1.2s' }}
      >
        <svg className="h-5 w-5 text-[var(--color-accent)]" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
        <span className="text-lg font-extrabold text-[var(--color-accent)]">${saved}K/mo {t.saved[locale]}</span>
        <span className="text-sm text-[var(--color-fg-faint)]">({Math.round((saved / beforeTotal) * 100)}% {t.reduction[locale]})</span>
      </div>
    </div>
  );
}
