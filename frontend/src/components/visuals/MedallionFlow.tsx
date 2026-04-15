import { useEffect, useState } from 'react';
import { useLocale } from '../../lib/useLocale';

/* ─── i18n strings ─── */
const t = {
  header: { es: 'Arquitectura de migración del warehouse', en: 'Warehouse migration architecture' },
  objects: { es: 'objetos', en: 'objects' },
  tables: { es: 'tablas', en: 'tables' },
  dataAsProduct: { es: 'Datos como Producto', en: 'Data as a Product' },
  reportsDashboards: { es: 'Reportes y Dashboards', en: 'Reports & Dashboards' },
  objectsMigrated: { es: 'objetos migrados', en: 'objects migrated' },
  fromFullRefresh: { es: 'desde full refresh', en: 'from full refresh' },
  sfChTranslation: { es: 'traducción SF → CH', en: 'SF → CH translation' },
};

/**
 * Warehouse migration architecture — sources through Bronze → Silver → Gold
 * medallion, each layer serving a consumption output:
 *   Bronze (S3) → Middlewares (data as a product)
 *   Silver (ClickHouse) → Segment (ecommerce, Python connector)
 *   Gold (dbt marts) → Power BI reports & dashboards (replacing MicroStrategy)
 */
export default function MedallionFlow() {
  const locale = useLocale();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const raf = requestAnimationFrame(() => {
      requestAnimationFrame(() => setVisible(true));
    });
    return () => cancelAnimationFrame(raf);
  }, []);

  const W = 18;
  const flowY = 28;

  /* ─── Source nodes ─── */
  const sources = [
    { label: 'Oracle × 9', y: 10, color: '#ef4444' },
    { label: 'CSV / TXT', y: 26, color: '#f97316' },
    { label: 'APIs', y: 42, color: '#8b5cf6' },
  ];

  /* ─── Medallion layers (12-unit gaps between columns) ─── */
  const layers = [
    { label: 'Bronze', sub: 'S3 Parquet', detail: 'Hive-partitioned', color: '#cd7f32', x: 22, count: '~1,350', countLabel: t.objects[locale] },
    { label: 'Silver', sub: 'ClickHouse', detail: 'RMT + dedup', color: '#94a3b8', x: 52, count: '~200', countLabel: t.tables[locale] },
    { label: 'Gold', sub: 'dbt marts', detail: '+ projections', color: '#fbbf24', x: 82, count: '~150', countLabel: 'marts' },
  ];

  const bronzeCx = 22 + W / 2;  // 31
  const silverCx = 52 + W / 2;  // 61
  const goldCx   = 82 + W / 2;  // 91

  return (
    <div className="my-10 rounded-2xl border border-[var(--color-border)] bg-[var(--color-bg-card)] p-6 md:p-8">
      {/* Header */}
      <div className="flex items-center gap-2 mb-6">
        <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
        <span className="text-xs font-bold uppercase tracking-[0.15em] text-[var(--color-fg-faint)]">
          {t.header[locale]}
        </span>
      </div>

      {/* SVG Flow */}
      <div className="relative rounded-xl bg-[var(--color-bg)] border border-[var(--color-border)] overflow-hidden">
        <svg viewBox="-1 -3 105 76" className="w-full" style={{ height: 'auto', maxHeight: '400px' }}>

          {/* ── Source boxes (left column) ── */}
          {sources.map((src, i) => (
            <g
              key={src.label}
              className="transition-all duration-700"
              style={{
                opacity: visible ? 1 : 0,
                transform: visible ? 'translateX(0)' : 'translateX(-3px)',
                transitionDelay: `${i * 0.15}s`,
              }}
            >
              <rect
                x={2} y={src.y - 4} width={14} height={10} rx={1.5}
                fill={src.color} opacity={0.1}
                stroke={src.color} strokeWidth={0.4} strokeOpacity={0.4}
              />
              <text
                x={9} y={src.y + 1.5}
                textAnchor="middle"
                fill={src.color}
                fontSize={2.2}
                fontWeight={700}
                fontFamily="var(--font-sans)"
              >
                {src.label}
              </text>
            </g>
          ))}

          {/* ── Fan-in lines: Sources → Bronze ── */}
          {sources.map((src, i) => (
            <line
              key={`fan-${i}`}
              x1={16} y1={src.y}
              x2={22} y2={flowY}
              strokeWidth={0.3}
              strokeDasharray="1.5 1"
              className="transition-all duration-[1s]"
              style={{
                stroke: '#cd7f32',
                opacity: visible ? 0.3 : 0,
                transitionDelay: `${0.3 + i * 0.1}s`,
              }}
            />
          ))}

          {/* ── Medallion layer boxes ── */}
          {layers.map((layer, i) => (
            <g
              key={layer.label}
              className="transition-all duration-700"
              style={{
                opacity: visible ? 1 : 0,
                transform: visible ? 'translateY(0)' : 'translateY(4px)',
                transitionDelay: `${0.4 + i * 0.2}s`,
              }}
            >
              <rect x={layer.x} y={10} width={W} height={36} rx={2}
                fill={layer.color} opacity={0.06} />
              <rect x={layer.x} y={10} width={W} height={36} rx={2}
                fill="none" stroke={layer.color} strokeWidth={0.5} strokeOpacity={0.5} />
              <rect x={layer.x} y={10} width={W} height={4} rx={2}
                fill={layer.color} opacity={0.2} />
              <text x={layer.x + W / 2} y={13}
                textAnchor="middle" fill={layer.color}
                fontSize={2.2} fontWeight={800} fontFamily="var(--font-sans)">
                {layer.label}
              </text>
              <text x={layer.x + W / 2} y={22}
                textAnchor="middle" fill="var(--color-fg-muted)"
                fontSize={2.4} fontWeight={600} fontFamily="var(--font-sans)">
                {layer.sub}
              </text>
              <text x={layer.x + W / 2} y={26}
                textAnchor="middle" fill="var(--color-fg-faint)"
                fontSize={1.8} fontFamily="var(--font-sans)">
                {layer.detail}
              </text>
              <line x1={layer.x + 3} y1={30} x2={layer.x + W - 3} y2={30}
                stroke={layer.color} strokeWidth={0.3} strokeOpacity={0.3} />
              <text x={layer.x + W / 2} y={35}
                textAnchor="middle" fill={layer.color}
                fontSize={3.2} fontWeight={800} fontFamily="var(--font-sans)">
                {layer.count}
              </text>
              <text x={layer.x + W / 2} y={39}
                textAnchor="middle" fill="var(--color-fg-faint)"
                fontSize={1.6} fontFamily="var(--font-sans)">
                {layer.countLabel}
              </text>
            </g>
          ))}

          {/* ── Connection lines between medallion layers ── */}
          {layers.slice(0, -1).map((layer, i) => {
            const next = layers[i + 1];
            return (
              <g key={`conn-${i}`}>
                <line
                  x1={layer.x + W} y1={flowY}
                  x2={next.x} y2={flowY}
                  strokeWidth={0.4}
                  strokeDasharray="1.5 1"
                  className="transition-all duration-[1s]"
                  style={{
                    stroke: next.color,
                    opacity: visible ? 0.4 : 0,
                    transitionDelay: `${0.6 + i * 0.2}s`,
                  }}
                />
                <text
                  x={(layer.x + W + next.x) / 2}
                  y={flowY - 3}
                  textAnchor="middle"
                  fill={next.color}
                  fontSize={1.8}
                  fontWeight={600}
                  fontFamily="var(--font-sans)"
                  className="transition-all duration-700"
                  style={{
                    opacity: visible ? 0.7 : 0,
                    transitionDelay: `${0.8 + i * 0.2}s`,
                  }}
                >
                  {i === 0 ? 'ClickPipes' : 'dbt build'}
                </text>
                {visible && [0, 1].map(p => (
                  <circle key={p} r={0.7} fill={next.color} opacity={0.9}>
                    <animate
                      attributeName="cx"
                      values={`${layer.x + W};${next.x}`}
                      dur={`${1.8 + p * 0.4}s`}
                      repeatCount="indefinite"
                      begin={`${p * 0.9}s`}
                    />
                    <animate
                      attributeName="cy"
                      values={`${flowY};${flowY}`}
                      dur="2s"
                      repeatCount="indefinite"
                    />
                    <animate
                      attributeName="opacity"
                      values="0;0.9;0.9;0"
                      dur={`${1.8 + p * 0.4}s`}
                      repeatCount="indefinite"
                      begin={`${p * 0.9}s`}
                    />
                  </circle>
                ))}
              </g>
            );
          })}

          {/* ═══════════════════════════════════════════════════
              CONSUMPTION OUTPUTS (downward from each layer)
              ═══════════════════════════════════════════════════ */}

          {/* ── Bronze → Middlewares (data as a product) ── */}
          <line
            x1={bronzeCx} y1={46} x2={bronzeCx} y2={55}
            strokeWidth={0.4} strokeDasharray="1.5 1"
            className="transition-all duration-[1s]"
            style={{ stroke: '#f59e0b', opacity: visible ? 0.4 : 0, transitionDelay: '1s' }}
          />
          <g
            className="transition-all duration-700"
            style={{
              opacity: visible ? 1 : 0,
              transform: visible ? 'translateY(0)' : 'translateY(3px)',
              transitionDelay: '1.1s',
            }}
          >
            <rect x={bronzeCx - 9} y={55} width={18} height={13} rx={1.5}
              fill="#f59e0b" opacity={0.08}
              stroke="#f59e0b" strokeWidth={0.4} strokeOpacity={0.3} />
            <text x={bronzeCx} y={60.5}
              textAnchor="middle" fill="#f59e0b"
              fontSize={2.2} fontWeight={700} fontFamily="var(--font-sans)">
              Middlewares
            </text>
            <text x={bronzeCx} y={64.5}
              textAnchor="middle" fill="#f59e0b"
              fontSize={1.3} fontWeight={500} fontFamily="var(--font-sans)"
              opacity={0.6}>
              {t.dataAsProduct[locale]}
            </text>
          </g>
          {visible && (
            <circle r={0.5} fill="#f59e0b" opacity={0.8}>
              <animate attributeName="cx" values={`${bronzeCx};${bronzeCx}`} dur="1.8s" repeatCount="indefinite" />
              <animate attributeName="cy" values="46;55" dur="1.8s" repeatCount="indefinite" />
              <animate attributeName="opacity" values="0;0.8;0.8;0" dur="1.8s" repeatCount="indefinite" />
            </circle>
          )}

          {/* ── Silver → Segment (ecommerce via Python connector) ── */}
          <line
            x1={silverCx} y1={46} x2={silverCx} y2={55}
            strokeWidth={0.4} strokeDasharray="1.5 1"
            className="transition-all duration-[1s]"
            style={{ stroke: '#22c55e', opacity: visible ? 0.4 : 0, transitionDelay: '1.1s' }}
          />
          <text
            x={silverCx + 4} y={51}
            textAnchor="start" fill="#22c55e"
            fontSize={1.4} fontWeight={600} fontFamily="var(--font-sans)"
            className="transition-all duration-700"
            style={{ opacity: visible ? 0.6 : 0, transitionDelay: '1.1s' }}
          >
            Python con
          </text>
          <g
            className="transition-all duration-700"
            style={{
              opacity: visible ? 1 : 0,
              transform: visible ? 'translateY(0)' : 'translateY(3px)',
              transitionDelay: '1.2s',
            }}
          >
            <rect x={silverCx - 9} y={55} width={18} height={13} rx={1.5}
              fill="#22c55e" opacity={0.08}
              stroke="#22c55e" strokeWidth={0.4} strokeOpacity={0.3} />
            <text x={silverCx} y={60.5}
              textAnchor="middle" fill="#22c55e"
              fontSize={2.2} fontWeight={700} fontFamily="var(--font-sans)">
              Segment
            </text>
            <text x={silverCx} y={64.5}
              textAnchor="middle" fill="#22c55e"
              fontSize={1.3} fontWeight={500} fontFamily="var(--font-sans)"
              opacity={0.6}>
              ecommerce
            </text>
          </g>
          {visible && (
            <circle r={0.5} fill="#22c55e" opacity={0.8}>
              <animate attributeName="cx" values={`${silverCx};${silverCx}`} dur="1.8s" repeatCount="indefinite" begin="0.3s" />
              <animate attributeName="cy" values="46;55" dur="1.8s" repeatCount="indefinite" begin="0.3s" />
              <animate attributeName="opacity" values="0;0.8;0.8;0" dur="1.8s" repeatCount="indefinite" begin="0.3s" />
            </circle>
          )}

          {/* ── Gold → Power BI (replacing MicroStrategy) ── */}
          <line
            x1={goldCx} y1={46} x2={goldCx} y2={55}
            strokeWidth={0.4} strokeDasharray="1.5 1"
            className="transition-all duration-[1s]"
            style={{ stroke: '#22d3ee', opacity: visible ? 0.4 : 0, transitionDelay: '1.2s' }}
          />
          {/* Power BI box with MicroStrategy replacement story inside */}
          <g
            className="transition-all duration-700"
            style={{
              opacity: visible ? 1 : 0,
              transform: visible ? 'translateY(0)' : 'translateY(3px)',
              transitionDelay: '1.3s',
            }}
          >
            <rect x={goldCx - 9} y={55} width={18} height={14} rx={1.5}
              fill="#22d3ee" opacity={0.08}
              stroke="#22d3ee" strokeWidth={0.4} strokeOpacity={0.3} />
            {/* MicroStrategy — faded with animated strikethrough */}
            <text x={goldCx} y={59.5}
              textAnchor="middle" fill="#ef4444"
              fontSize={1.4} fontWeight={600} fontFamily="var(--font-sans)">
              <animate attributeName="opacity" values="0;0.5;0.5;0.25" dur="2.5s" fill="freeze" begin="1.5s" />
              MicroStrategy
            </text>
            <line x1={goldCx - 7} y1={59} x2={goldCx - 7} y2={59}
              stroke="#ef4444" strokeWidth={0.35} opacity={0.5}>
              <animate attributeName="x2" values={`${goldCx - 7};${goldCx + 7}`} dur="0.6s" fill="freeze" begin="2s" />
            </line>
            {/* Power BI — active */}
            <text x={goldCx} y={64}
              textAnchor="middle" fill="#22d3ee"
              fontSize={2.2} fontWeight={700} fontFamily="var(--font-sans)">
              Power BI
            </text>
            <text x={goldCx} y={67}
              textAnchor="middle" fill="#22d3ee"
              fontSize={1.1} fontWeight={500} fontFamily="var(--font-sans)"
              opacity={0.6}>
              {t.reportsDashboards[locale]}
            </text>
            <rect x={goldCx - 9} y={55} width={18} height={14} rx={1.5}
              fill="none" stroke="#22d3ee" strokeWidth={0.3}>
              <animate attributeName="stroke-opacity" values="0.15;0.4;0.15" dur="2.5s" repeatCount="indefinite" />
            </rect>
          </g>
          {visible && (
            <circle r={0.5} fill="#22d3ee" opacity={0.8}>
              <animate attributeName="cx" values={`${goldCx};${goldCx}`} dur="1.8s" repeatCount="indefinite" begin="0.6s" />
              <animate attributeName="cy" values="46;55" dur="1.8s" repeatCount="indefinite" begin="0.6s" />
              <animate attributeName="opacity" values="0;0.8;0.8;0" dur="1.8s" repeatCount="indefinite" begin="0.6s" />
            </circle>
          )}

          {/* ── Animated fan-in packets: Sources → Bronze ── */}
          {visible && sources.map((src, i) => (
            <circle key={`pkt-${i}`} r={0.6} fill="#cd7f32" opacity={0.8}>
              <animate
                attributeName="cx"
                values="16;22"
                dur={`${2 + i * 0.3}s`}
                repeatCount="indefinite"
                begin={`${i * 0.5}s`}
              />
              <animate
                attributeName="cy"
                values={`${src.y};${flowY}`}
                dur={`${2 + i * 0.3}s`}
                repeatCount="indefinite"
                begin={`${i * 0.5}s`}
              />
              <animate
                attributeName="opacity"
                values="0;0.8;0.8;0"
                dur={`${2 + i * 0.3}s`}
                repeatCount="indefinite"
                begin={`${i * 0.5}s`}
              />
            </circle>
          ))}
        </svg>
      </div>

      {/* ── Bottom stats ── */}
      <div
        className="mt-5 grid grid-cols-3 gap-3 transition-all duration-700"
        style={{ opacity: visible ? 1 : 0, transitionDelay: '1.2s' }}
      >
        <div className="flex flex-col items-center rounded-xl border border-[rgba(205,127,50,0.15)] bg-[rgba(205,127,50,0.05)] px-3 py-2.5">
          <span className="text-base font-extrabold" style={{ color: '#cd7f32' }}>~1,350</span>
          <span className="text-[0.65rem] text-[var(--color-fg-faint)]">{t.objectsMigrated[locale]}</span>
        </div>
        <div className="flex flex-col items-center rounded-xl border border-[rgba(148,163,184,0.15)] bg-[rgba(148,163,184,0.05)] px-3 py-2.5">
          <span className="text-base font-extrabold" style={{ color: '#94a3b8' }}>→ CDC</span>
          <span className="text-[0.65rem] text-[var(--color-fg-faint)]">{t.fromFullRefresh[locale]}</span>
        </div>
        <div className="flex flex-col items-center rounded-xl border border-[rgba(251,191,36,0.15)] bg-[rgba(251,191,36,0.05)] px-3 py-2.5">
          <span className="text-base font-extrabold" style={{ color: '#fbbf24' }}>~5 days</span>
          <span className="text-[0.65rem] text-[var(--color-fg-faint)]">{t.sfChTranslation[locale]}</span>
        </div>
      </div>
    </div>
  );
}
