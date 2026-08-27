import { useEffect, useState } from 'react';
import { useLocale } from '../../lib/useLocale';

const t = {
  header: { es: 'Costo diario de proxies', en: 'Daily proxy cost' },
  before: { es: 'Antes (1 pipeline)', en: 'Before (1 pipeline)' },
  after: { es: 'Después (todos)', en: 'After (all pipelines)' },
  saved: { es: 'ahorro anual', en: 'annual savings' },
  perDay: { es: '/día', en: '/day' },
  reduction: { es: 'reducción', en: 'reduction' },
};

export default function ProxyCostDrop() {
  const locale = useLocale();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const raf = requestAnimationFrame(() => {
      requestAnimationFrame(() => setVisible(true));
    });
    return () => cancelAnimationFrame(raf);
  }, []);

  const beforeCost = 5000;
  const afterCost = 100;
  const annualSaved = Math.round((beforeCost - afterCost) * 365 / 1000);
  const reductionPct = Math.round(((beforeCost - afterCost) / beforeCost) * 100);

  return (
    <div className="my-10 rounded-2xl border border-[var(--color-border)] bg-[var(--color-bg-card)] p-6 md:p-8">
      <div className="flex items-center gap-2 mb-6">
        <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
        <span className="text-xs font-bold uppercase tracking-[0.15em] text-[var(--color-fg-faint)]">
          {t.header[locale]}
        </span>
      </div>

      <div className="space-y-5">
        {/* Before bar */}
        <div>
          <div className="flex items-baseline justify-between mb-2">
            <span className="text-sm font-medium text-[var(--color-fg-muted)]">{t.before[locale]}</span>
            <span className="text-sm font-bold text-[#ef4444]">${beforeCost.toLocaleString()}{t.perDay[locale]}</span>
          </div>
          <div className="h-12 rounded-lg bg-[var(--color-bg)] overflow-hidden">
            <div
              className="h-full rounded-lg flex items-center justify-end pr-3 transition-all duration-[1.5s] ease-out"
              style={{
                width: visible ? '100%' : '0%',
                backgroundColor: '#ef4444',
                opacity: 0.85,
              }}
            >
              <span className="text-xs font-bold text-white/90">BrightData</span>
            </div>
          </div>
        </div>

        {/* After bar */}
        <div>
          <div className="flex items-baseline justify-between mb-2">
            <span className="text-sm font-medium text-[var(--color-fg-muted)]">{t.after[locale]}</span>
            <span className="text-sm font-bold text-[var(--color-accent)]">${afterCost}{t.perDay[locale]}</span>
          </div>
          <div className="h-12 rounded-lg bg-[var(--color-bg)] overflow-hidden">
            <div
              className="h-full rounded-lg flex items-center justify-center transition-all duration-[1.5s] ease-out"
              style={{
                width: visible ? `${(afterCost / beforeCost) * 100}%` : '0%',
                backgroundColor: '#22d3ee',
                transitionDelay: '0.6s',
              }}
            >
              <span className="text-[0.55rem] font-bold text-white/90 whitespace-nowrap">SM</span>
            </div>
          </div>
        </div>
      </div>

      {/* Savings callout */}
      <div
        className="mt-6 flex items-center justify-center gap-3 rounded-xl border border-[rgba(34,211,238,0.15)] bg-[rgba(34,211,238,0.05)] px-4 py-3 transition-all duration-700"
        style={{ opacity: visible ? 1 : 0, transitionDelay: '1.4s' }}
      >
        <svg className="h-5 w-5 text-[var(--color-accent)]" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
        <span className="text-lg font-extrabold text-[var(--color-accent)]">~${annualSaved}K/yr {t.saved[locale]}</span>
        <span className="text-sm text-[var(--color-fg-faint)]">({reductionPct}% {t.reduction[locale]})</span>
      </div>
    </div>
  );
}
