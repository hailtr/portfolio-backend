import { useEffect, useState } from 'react';
import { useLocale } from '../../lib/useLocale';

const t = {
  header: { es: 'Migración Snowflake → ClickHouse', en: 'Snowflake → ClickHouse migration' },
  migrated: { es: 'migradas', en: 'migrated' },
  remaining: { es: 'restantes', en: 'remaining' },
  total: { es: 'tablas totales', en: 'total tables' },
  progress: { es: 'progreso', en: 'progress' },
  alertReduction: { es: 'menos alertas', en: 'fewer alerts' },
  dagFailures: { es: 'fallas de DAGs', en: 'DAG failures' },
  targetSavings: { es: 'ahorro objetivo', en: 'target savings' },
};

export default function MigrationProgress() {
  const locale = useLocale();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const raf = requestAnimationFrame(() => {
      requestAnimationFrame(() => setVisible(true));
    });
    return () => cancelAnimationFrame(raf);
  }, []);

  const migrated = 288;
  const total = 678;
  const pct = Math.round((migrated / total) * 100);

  const segments = [
    { label: 'Spotify', count: 45, color: '#1DB954' },
    { label: 'YouTube', count: 38, color: '#FF0000' },
    { label: 'TikTok', count: 32, color: '#e11d48' },
    { label: 'Shazam', count: 28, color: '#22d3ee' },
    { label: 'Instagram', count: 25, color: '#C13584' },
    { label: locale === 'es' ? 'Otros' : 'Others', count: migrated - 45 - 38 - 32 - 28 - 25, color: '#64748b' },
  ];

  return (
    <div className="my-10 rounded-2xl border border-[var(--color-border)] bg-[var(--color-bg-card)] p-6 md:p-8">
      <div className="flex items-center gap-2 mb-6">
        <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
        <span className="text-xs font-bold uppercase tracking-[0.15em] text-[var(--color-fg-faint)]">
          {t.header[locale]}
        </span>
      </div>

      {/* Progress ring */}
      <div className="flex items-center gap-8">
        <div className="relative flex-shrink-0" style={{ width: 120, height: 120 }}>
          <svg viewBox="0 0 120 120" className="w-full h-full -rotate-90">
            <circle cx={60} cy={60} r={50} fill="none"
              stroke="var(--color-border)" strokeWidth={8} />
            <circle cx={60} cy={60} r={50} fill="none"
              stroke="#22d3ee" strokeWidth={8}
              strokeLinecap="round"
              strokeDasharray={`${2 * Math.PI * 50}`}
              className="transition-all duration-[2s] ease-out"
              style={{
                strokeDashoffset: visible
                  ? `${2 * Math.PI * 50 * (1 - pct / 100)}`
                  : `${2 * Math.PI * 50}`,
              }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-2xl font-extrabold text-[var(--color-accent)]">{pct}%</span>
            <span className="text-[0.55rem] text-[var(--color-fg-faint)] uppercase">{t.progress[locale]}</span>
          </div>
        </div>

        {/* Stacked bar — which sources migrated */}
        <div className="flex-1 space-y-2">
          <div className="h-8 rounded-lg bg-[var(--color-bg)] overflow-hidden flex">
            {segments.map((seg, i) => (
              <div
                key={seg.label}
                className="h-full flex items-center justify-center transition-all duration-[1.5s] ease-out overflow-hidden"
                style={{
                  width: visible ? `${(seg.count / migrated) * 100}%` : '0%',
                  backgroundColor: seg.color,
                  opacity: 0.75,
                  transitionDelay: `${0.5 + i * 0.1}s`,
                }}
              >
                {seg.count > 30 && (
                  <span className="text-[0.45rem] font-bold text-white/80 whitespace-nowrap">{seg.count}</span>
                )}
              </div>
            ))}
          </div>
          <div className="flex flex-wrap gap-x-3 gap-y-1">
            {segments.map(seg => (
              <div key={seg.label} className="flex items-center gap-1">
                <div className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: seg.color }} />
                <span className="text-[0.6rem] text-[var(--color-fg-faint)]">{seg.label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Stats */}
      <div
        className="mt-6 grid grid-cols-4 gap-3 text-center transition-all duration-700"
        style={{ opacity: visible ? 1 : 0.3, transitionDelay: '1.2s' }}
      >
        <div>
          <p className="text-lg font-extrabold text-[var(--color-accent)]">{migrated}</p>
          <p className="text-[0.65rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.migrated[locale]}</p>
        </div>
        <div>
          <p className="text-lg font-extrabold text-[var(--color-accent)]">~$12K</p>
          <p className="text-[0.65rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.targetSavings[locale]}</p>
        </div>
        <div>
          <p className="text-lg font-extrabold text-[#10b981]">60%</p>
          <p className="text-[0.65rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.alertReduction[locale]}</p>
        </div>
        <div>
          <p className="text-lg font-extrabold text-[#10b981]">&lt;20%</p>
          <p className="text-[0.65rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.dagFailures[locale]}</p>
        </div>
      </div>
    </div>
  );
}
