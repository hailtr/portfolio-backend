import { useEffect, useState } from 'react';
import { useLocale } from '../../lib/useLocale';

const t = {
  heading: {
    es: 'Por qué materialized views',
    en: 'Why materialized views',
  },
  batchReprocess: {
    es: 'Reprocesamiento batch',
    en: 'Batch reprocess',
  },
  mvCascade: {
    es: 'Cascada MV',
    en: 'MV cascade',
  },
  batchStep1: {
    es: 'Nuevo evento llega',
    en: 'New event arrives',
  },
  batchStep2: {
    es: 'Esperar batch programado',
    en: 'Wait for scheduled batch',
  },
  batchStep3: {
    es: 'Escanear TODOS los 64K+ eventos raw',
    en: 'Scan ALL 64K+ raw events',
  },
  batchStep4: {
    es: 'Re-agregar desde cero',
    en: 'Re-aggregate from scratch',
  },
  batchStep5: {
    es: 'Sobrescribir toda la tabla de salida',
    en: 'Overwrite entire output table',
  },
  hours: {
    es: 'Horas',
    en: 'Hours',
  },
  untilDashboard: {
    es: 'hasta que el dashboard refleje datos nuevos',
    en: 'until dashboard reflects new data',
  },
  cascadeStep1: {
    es: 'Nuevo evento llega a raw',
    en: 'New event lands in raw',
  },
  cascadeStep2: {
    es: 'MV de ruteo dispara automáticamente',
    en: 'Routing MV fires automatically',
  },
  cascadeStep3: {
    es: 'Solo la fila nueva llega a tabla core',
    en: 'Only the new row hits core table',
  },
  cascadeStep4: {
    es: 'VIEW hace join de datos frescos al leer',
    en: 'VIEW joins fresh data on read',
  },
  cascadeStep5: {
    es: 'Dashboard lo refleja al instante',
    en: 'Dashboard reflects it instantly',
  },
  subSecond: {
    es: 'Sub-segundo',
    en: 'Sub-second',
  },
  eventToMart: {
    es: 'evento a mart consultable',
    en: 'event to queryable mart',
  },
  bottomCallout: {
    es: 'Los VIEWs de mart usan VIEWs regulares (no MVs) para evitar race conditions de joins — los joins ocurren al momento del query sobre datos ya deduplicados en ReplacingMergeTree',
    en: 'Mart VIEWs use regular VIEWs (not MVs) to avoid join race conditions — joins happen at query time on already-deduplicated ReplacingMergeTree data',
  },
};

/**
 * Materialized View chain — shows how 1 insert into the landing table
 * triggers a cascade: raw → routing MV → core table → mart VIEW ready.
 * Contrasts batch (scan everything) vs MV chain (process only the delta).
 */
export default function MatViewChain() {
  const locale = useLocale();
  const [visible, setVisible] = useState(false);
  const [phase, setPhase] = useState<'batch' | 'cascade'>('batch');

  useEffect(() => {
    const raf = requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        setVisible(true);
        setTimeout(() => setPhase('cascade'), 2800);
      });
    });
    return () => cancelAnimationFrame(raf);
  }, []);

  const isCascade = phase === 'cascade';

  return (
    <div className="my-10 rounded-2xl border border-[var(--color-border)] bg-[var(--color-bg-card)] p-6 md:p-8">
      <div className="flex items-center gap-2 mb-6">
        <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
        <span className="text-xs font-bold uppercase tracking-[0.15em] text-[var(--color-fg-faint)]">
          {t.heading[locale]}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

        {/* ── Batch side ── */}
        <div
          className="rounded-xl border p-4 transition-all duration-700"
          style={{
            borderColor: !isCascade ? '#ef4444' : 'var(--color-border)',
            backgroundColor: !isCascade ? 'rgba(239,68,68,0.05)' : 'var(--color-bg)',
            opacity: visible ? 1 : 0,
          }}
        >
          <div className="flex items-center gap-2 mb-3">
            <div className="h-2 w-2 rounded-full" style={{ backgroundColor: '#ef4444' }} />
            <span className="text-xs font-bold uppercase tracking-wider text-[#ef4444]">
              {t.batchReprocess[locale]}
            </span>
          </div>

          <div className="space-y-1.5">
            {[
              { step: t.batchStep1[locale], icon: '1' },
              { step: t.batchStep2[locale], icon: '2' },
              { step: t.batchStep3[locale], icon: '3' },
              { step: t.batchStep4[locale], icon: '4' },
              { step: t.batchStep5[locale], icon: '5' },
            ].map((s, i) => (
              <div key={i}
                className="flex items-center gap-2.5 rounded-md px-2.5 py-1.5 transition-all duration-500"
                style={{
                  backgroundColor: !isCascade ? 'rgba(239,68,68,0.06)' : 'transparent',
                  opacity: visible ? 1 : 0,
                  transitionDelay: `${0.1 * i}s`,
                }}
              >
                <span className="flex-shrink-0 w-4 h-4 rounded-full flex items-center justify-center text-[0.55rem] font-bold"
                  style={{ backgroundColor: 'rgba(239,68,68,0.12)', color: '#ef4444' }}>
                  {s.icon}
                </span>
                <span className="text-xs text-[var(--color-fg-muted)]">{s.step}</span>
              </div>
            ))}
          </div>

          <div className="mt-4 rounded-lg px-3 py-2 text-center"
            style={{ backgroundColor: 'rgba(239,68,68,0.06)' }}>
            <span className="text-lg font-extrabold text-[#ef4444]">{t.hours[locale]}</span>
            <p className="text-[0.6rem] text-[var(--color-fg-faint)] uppercase tracking-wider">
              {t.untilDashboard[locale]}
            </p>
          </div>
        </div>

        {/* ── MV Cascade side ── */}
        <div
          className="rounded-xl border p-4 transition-all duration-700"
          style={{
            borderColor: isCascade ? '#22d3ee' : 'var(--color-border)',
            backgroundColor: isCascade ? 'rgba(34,211,238,0.05)' : 'var(--color-bg)',
            opacity: visible ? 1 : 0,
            transitionDelay: '0.2s',
          }}
        >
          <div className="flex items-center gap-2 mb-3">
            <div className="h-2 w-2 rounded-full" style={{ backgroundColor: '#22d3ee' }} />
            <span className="text-xs font-bold uppercase tracking-wider text-[#22d3ee]">
              {t.mvCascade[locale]}
            </span>
          </div>

          <div className="space-y-1.5">
            {[
              { step: t.cascadeStep1[locale], tag: 'INSERT' },
              { step: t.cascadeStep2[locale], tag: 'MV' },
              { step: t.cascadeStep3[locale], tag: 'DELTA' },
              { step: t.cascadeStep4[locale], tag: 'VIEW' },
              { step: t.cascadeStep5[locale], tag: 'NRT' },
            ].map((s, i) => (
              <div key={i}
                className="flex items-center gap-2.5 rounded-md px-2.5 py-1.5 transition-all duration-500"
                style={{
                  backgroundColor: isCascade ? 'rgba(34,211,238,0.06)' : 'transparent',
                  opacity: visible ? 1 : 0,
                  transitionDelay: `${0.1 * i + 0.3}s`,
                }}
              >
                <span className="flex-shrink-0 rounded px-1.5 py-0.5 text-[0.5rem] font-bold font-mono"
                  style={{ backgroundColor: 'rgba(34,211,238,0.12)', color: '#22d3ee' }}>
                  {s.tag}
                </span>
                <span className="text-xs text-[var(--color-fg-muted)]">{s.step}</span>
              </div>
            ))}
          </div>

          <div className="mt-4 rounded-lg px-3 py-2 text-center"
            style={{ backgroundColor: 'rgba(34,211,238,0.06)' }}>
            <span className="text-lg font-extrabold text-[#22d3ee]">{t.subSecond[locale]}</span>
            <p className="text-[0.6rem] text-[var(--color-fg-faint)] uppercase tracking-wider">
              {t.eventToMart[locale]}
            </p>
          </div>
        </div>
      </div>

      {/* Bottom callout */}
      <div
        className="mt-5 rounded-xl border px-4 py-3 text-center transition-all duration-700"
        style={{
          borderColor: isCascade ? 'rgba(34,211,238,0.15)' : 'transparent',
          backgroundColor: isCascade ? 'rgba(34,211,238,0.04)' : 'transparent',
          opacity: isCascade ? 1 : 0,
          transitionDelay: '0.5s',
        }}
      >
        <p className="text-xs text-[var(--color-fg-muted)]">
          {t.bottomCallout[locale]}
        </p>
      </div>
    </div>
  );
}
