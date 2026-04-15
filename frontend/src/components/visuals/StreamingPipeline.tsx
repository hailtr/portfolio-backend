import { useEffect, useState } from 'react';
import { useLocale } from '../../lib/useLocale';

const t = {
  header: { es: 'Arquitectura de streaming', en: 'Streaming architecture' },
  routingMVs: { es: '7 MVs de ruteo', en: '7 routing MVs' },
  regularViews: { es: '4 VIEWs regulares', en: '4 regular VIEWs' },
  coreAnnotation: { es: 'core.* — 13 tablas ReplacingMergeTree', en: 'core.* — 13 ReplacingMergeTree tables' },
  martAnnotation: { es: 'mart.* — vistas API-ready', en: 'mart.* — API-ready views' },
  schemaObjects: { es: 'objetos de schema', en: 'schema objects' },
  routingMVsStat: { es: 'MVs de ruteo', en: 'routing MVs' },
  eventMart: { es: 'evento → mart', en: 'event → mart' },
} as const;

export default function StreamingPipeline() {
  const locale = useLocale();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const raf = requestAnimationFrame(() => {
      requestAnimationFrame(() => setVisible(true));
    });
    return () => cancelAnimationFrame(raf);
  }, []);

  const core = [
    { l: 'jobs', cx: 12 },
    { l: 'batches', cx: 33 },
    { l: 'tests', cx: 54 },
    { l: 'asserts', cx: 75 },
    { l: 'filters', cx: 96 },
    { l: 'args', cx: 117 },
    { l: 'results', cx: 138 },
  ];

  const marts = [
    { l: 'dl_quality', cx: 22 },
    { l: 'url_quality', cx: 55 },
    { l: 'dl_trends', cx: 95 },
    { l: 'url_trends', cx: 128 },
  ];

  const CW = 16, CH = 7, CY = 50;
  const MW = 24, MH = 7, MY = 68;
  const RCX = 75, FAN_Y = 32;

  const fanCurve = (cx: number) =>
    `M ${RCX} ${FAN_Y} C ${RCX} ${FAN_Y + 8}, ${cx} ${CY - 6}, ${cx} ${CY}`;

  return (
    <div className="my-10 rounded-2xl border border-[var(--color-border)] bg-[var(--color-bg-card)] p-6 md:p-8">
      <div className="flex items-center gap-2 mb-6">
        <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
        <span className="text-xs font-bold uppercase tracking-[0.15em] text-[var(--color-fg-faint)]">
          {t.header[locale]}
        </span>
      </div>

      <div className="relative rounded-xl bg-[var(--color-bg)] border border-[var(--color-border)] overflow-hidden">
        <svg viewBox="0 0 150 82" className="w-full" style={{ height: 'auto', maxHeight: '400px' }}>

          {/* ── QA Platform ── */}
          <g className="transition-all duration-700" style={{ opacity: visible ? 1 : 0 }}>
            <rect x={18} y={3} width={28} height={10} rx={2}
              fill="#f59e0b" opacity={0.1} stroke="#f59e0b" strokeWidth={0.5} />
            <text x={32} y={9.5} textAnchor="middle" fill="#f59e0b"
              fontSize={2.6} fontWeight={700} fontFamily="var(--font-sans)">
              QA Platform
            </text>
          </g>

          {/* Arrow → */}
          <line x1={46} y1={8} x2={58} y2={8}
            stroke="#f59e0b" strokeWidth={0.5} strokeDasharray="1.5 1"
            className="transition-all duration-700"
            style={{ opacity: visible ? 0.5 : 0, transitionDelay: '0.1s' }} />
          {visible && (
            <circle r={0.7} fill="#f59e0b">
              <animate attributeName="cx" values="46;58" dur="1.5s" repeatCount="indefinite" />
              <animate attributeName="cy" values="8;8" dur="1.5s" repeatCount="indefinite" />
              <animate attributeName="opacity" values="0;0.8;0" dur="1.5s" repeatCount="indefinite" />
            </circle>
          )}

          {/* ── Redpanda ── */}
          <g className="transition-all duration-700" style={{ opacity: visible ? 1 : 0, transitionDelay: '0.15s' }}>
            <rect x={58} y={3} width={34} height={10} rx={2}
              fill="#e11d48" opacity={0.08} stroke="#e11d48" strokeWidth={0.5} />
            <text x={75} y={9} textAnchor="middle" fill="#e11d48"
              fontSize={2.6} fontWeight={700} fontFamily="var(--font-sans)">
              Redpanda
            </text>
            <text x={75} y={12} textAnchor="middle" fill="#e11d48"
              fontSize={1.2} fontFamily="var(--font-mono, monospace)" opacity={0.5}>
              streaming-events
            </text>
          </g>

          {/* Arrow ↓ */}
          <line x1={75} y1={13} x2={75} y2={17}
            stroke="#e11d48" strokeWidth={0.5} strokeDasharray="1.5 1"
            className="transition-all duration-700"
            style={{ opacity: visible ? 0.5 : 0, transitionDelay: '0.2s' }} />

          {/* ── raw.streaming_events ── */}
          <g className="transition-all duration-700" style={{ opacity: visible ? 1 : 0, transitionDelay: '0.25s' }}>
            <rect x={25} y={17} width={100} height={9} rx={2}
              fill="#e11d48" opacity={0.05} stroke="#e11d48" strokeWidth={0.5} />
            {visible && (
              <rect x={25} y={17} width={100} height={9} rx={2} fill="#e11d48">
                <animate attributeName="opacity" values="0;0.04;0" dur="2.5s" repeatCount="indefinite" />
              </rect>
            )}
            <text x={75} y={22.5} textAnchor="middle" fill="#e11d48"
              fontSize={2.2} fontWeight={700} fontFamily="var(--font-mono, monospace)">
              raw.streaming_events
            </text>
            <text x={75} y={25} textAnchor="middle" fill="var(--color-fg-faint)"
              fontSize={1.3} fontFamily="var(--font-sans)">
              Kafka Engine → MergeTree
            </text>
          </g>

          {/* ── Divider: 7 routing MVs ── */}
          <line x1={5} y1={30} x2={55} y2={30}
            stroke="#22d3ee" strokeWidth={0.3}
            className="transition-all duration-700"
            style={{ opacity: visible ? 0.25 : 0, transitionDelay: '0.35s' }} />
          <text x={75} y={31} textAnchor="middle" fill="#22d3ee"
            fontSize={1.8} fontWeight={700} fontFamily="var(--font-sans)" letterSpacing={0.3}
            className="transition-all duration-700"
            style={{ opacity: visible ? 0.7 : 0, transitionDelay: '0.35s' }}>
            {t.routingMVs[locale]}
          </text>
          <line x1={95} y1={30} x2={145} y2={30}
            stroke="#22d3ee" strokeWidth={0.3}
            className="transition-all duration-700"
            style={{ opacity: visible ? 0.25 : 0, transitionDelay: '0.35s' }} />

          {/* ── Fan-out bezier curves ── */}
          {core.map((item, i) => (
            <g key={`fan-${i}`}>
              <path d={fanCurve(item.cx)} fill="none" stroke="#22d3ee"
                strokeWidth={3} strokeLinecap="round"
                className="transition-all duration-700"
                style={{ opacity: visible ? 0.04 : 0, transitionDelay: `${0.4 + i * 0.06}s` }} />
              <path d={fanCurve(item.cx)} fill="none" stroke="#22d3ee"
                strokeWidth={0.5} strokeDasharray="2 1" strokeLinecap="round"
                className="transition-all duration-700"
                style={{ opacity: visible ? 0.4 : 0, transitionDelay: `${0.4 + i * 0.06}s` }} />
              {visible && (
                <circle r={0.8} fill="#22d3ee">
                  <animateMotion
                    path={fanCurve(item.cx)}
                    dur={`${1.4 + i * 0.1}s`}
                    repeatCount="indefinite"
                    begin={`${i * 0.18}s`}
                  />
                  <animate attributeName="opacity" values="0;0.8;0"
                    dur={`${1.4 + i * 0.1}s`} repeatCount="indefinite" begin={`${i * 0.18}s`} />
                </circle>
              )}
            </g>
          ))}

          {/* ── Core table boxes ── */}
          {core.map((item, i) => (
            <g key={`core-${i}`} className="transition-all duration-500"
              style={{ opacity: visible ? 1 : 0, transitionDelay: `${0.6 + i * 0.05}s` }}>
              <rect x={item.cx - CW / 2} y={CY} width={CW} height={CH} rx={1.5}
                fill="#22d3ee" opacity={0.06} stroke="#22d3ee" strokeWidth={0.35} strokeOpacity={0.5} />
              <text x={item.cx} y={CY + CH / 2 + 1} textAnchor="middle" fill="#22d3ee"
                fontSize={2} fontWeight={600} fontFamily="var(--font-mono, monospace)" opacity={0.85}>
                {item.l}
              </text>
            </g>
          ))}

          {/* Core annotation */}
          <text x={75} y={CY + CH + 3.5} textAnchor="middle" fill="var(--color-fg-faint)"
            fontSize={1.4} fontFamily="var(--font-sans)"
            className="transition-all duration-700"
            style={{ opacity: visible ? 0.45 : 0, transitionDelay: '0.8s' }}>
            {t.coreAnnotation[locale]}
          </text>

          {/* ── Divider: 4 VIEWs ── */}
          <line x1={5} y1={64} x2={48} y2={64}
            stroke="#fbbf24" strokeWidth={0.3}
            className="transition-all duration-700"
            style={{ opacity: visible ? 0.25 : 0, transitionDelay: '0.85s' }} />
          <text x={75} y={65} textAnchor="middle" fill="#fbbf24"
            fontSize={1.8} fontWeight={700} fontFamily="var(--font-sans)" letterSpacing={0.3}
            className="transition-all duration-700"
            style={{ opacity: visible ? 0.7 : 0, transitionDelay: '0.85s' }}>
            {t.regularViews[locale]}
          </text>
          <line x1={102} y1={64} x2={145} y2={64}
            stroke="#fbbf24" strokeWidth={0.3}
            className="transition-all duration-700"
            style={{ opacity: visible ? 0.25 : 0, transitionDelay: '0.85s' }} />

          {/* ── Mart boxes ── */}
          {marts.map((m, i) => (
            <g key={`mart-${i}`} className="transition-all duration-500"
              style={{ opacity: visible ? 1 : 0, transitionDelay: `${0.9 + i * 0.06}s` }}>
              <rect x={m.cx - MW / 2} y={MY} width={MW} height={MH} rx={1.5}
                fill="#fbbf24" opacity={0.08} stroke="#fbbf24" strokeWidth={0.35} strokeOpacity={0.5} />
              <text x={m.cx} y={MY + MH / 2 + 1} textAnchor="middle" fill="#fbbf24"
                fontSize={1.9} fontWeight={600} fontFamily="var(--font-mono, monospace)" opacity={0.9}>
                {m.l}
              </text>
            </g>
          ))}

          {/* Mart annotation */}
          <text x={75} y={MY + MH + 3.5} textAnchor="middle" fill="var(--color-fg-faint)"
            fontSize={1.4} fontFamily="var(--font-sans)"
            className="transition-all duration-700"
            style={{ opacity: visible ? 0.45 : 0, transitionDelay: '1s' }}>
            {t.martAnnotation[locale]}
          </text>

        </svg>
      </div>

      {/* Stats */}
      <div
        className="mt-5 grid grid-cols-3 gap-4 text-center transition-all duration-700"
        style={{ opacity: visible ? 1 : 0.3, transitionDelay: '1.1s' }}
      >
        <div>
          <p className="text-lg font-extrabold text-[var(--color-accent)]">26</p>
          <p className="text-[0.65rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.schemaObjects[locale]}</p>
        </div>
        <div>
          <p className="text-lg font-extrabold text-[var(--color-accent)]">7</p>
          <p className="text-[0.65rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.routingMVsStat[locale]}</p>
        </div>
        <div>
          <p className="text-lg font-extrabold text-[var(--color-accent)]">NRT</p>
          <p className="text-[0.65rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.eventMart[locale]}</p>
        </div>
      </div>
    </div>
  );
}
