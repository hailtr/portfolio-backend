import { useEffect, useState, useMemo } from 'react';
import { useLocale } from '../../lib/useLocale';

const t = {
  orchestrationOverhaul: { es: 'Reestructuración de orquestación', en: 'Orchestration overhaul' },
  storedProcedures: { es: '+ 124 stored procedures · sin dueño · sin control de versiones', en: '+ 124 stored procedures · no owner · no version control' },
  extract: { es: 'EXTRACCIÓN', en: 'EXTRACT' },
  nineServers: { es: '9 servidores', en: '9 servers' },
  autoIngest: { es: 'auto-ingesta', en: 'auto-ingest' },
  transformHourly: { es: 'TRANSFORM (cada hora a :45)', en: 'TRANSFORM (hourly at :45)' },
  about70Models: { es: '~70 modelos', en: '~70 models' },
  dbtModels: { es: 'modelos dbt', en: 'dbt models' },
  noFullRefresh: { es: 'sin full refresh', en: 'no full refresh' },
  dedupOnWrite: { es: 'dedup en escritura', en: 'dedup on write' },
  versionControlled: { es: 'versionado', en: 'version-controlled' },
};

/**
 * Real architecture: 1,200 Workato recipes → Airflow DAGs.
 *
 * Shows two phases:
 * 1. Chaos — tangled Workato recipes with no governance
 * 2. DAG — real pipeline: 7 parallel extractions (Oracle × 9 servers) → S3 →
 *    ClickPipes → verify → optimize RMT → dbt (EDW → DM → KVAT) → optimize final
 */
export default function PipelineCollapse() {
  const locale = useLocale();
  const [phase, setPhase] = useState<'idle' | 'chaos' | 'collapsing' | 'dag'>('idle');

  useEffect(() => {
    const raf = requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        setPhase('chaos');
        setTimeout(() => setPhase('collapsing'), 1800);
        setTimeout(() => setPhase('dag'), 3200);
      });
    });
    return () => cancelAnimationFrame(raf);
  }, []);

  // ─── REAL DAG: EXTRACTION LAYER (top) ───
  const extractTables = [
    'TRANSACTIONS', 'LINE_ITEMS', 'CUSTOMERS', 'CUST_ATTRS',
    'STORES', 'PAYMENTS', 'CARD_DETAIL',
  ];
  const eNodeW = 13, eNodeH = 3.2;
  const eStartY = 2;
  const eGap = 0.6;
  const eX = 17;

  const extractNodes = extractTables.map((t, i) => ({
    label: t,
    x: eX,
    y: eStartY + i * (eNodeH + eGap),
    color: '#f59e0b',
  }));

  // Extract center Y for connections
  const eCenterY = eStartY + ((extractTables.length - 1) * (eNodeH + eGap)) / 2 + eNodeH / 2;

  // ─── REAL DAG: TRANSFORM CHAIN (bottom) ───
  const transformNodes = [
    { label: 'Verify', sub: 'ClickPipes', x: 3, color: '#10b981' },
    { label: 'Optimize', sub: 'RMT dedup', x: 19, color: '#06b6d4' },
    { label: 'dbt EDW', sub: t.about70Models[locale], x: 35, color: '#a855f7' },
    { label: 'dbt DM', sub: '~60 pre-aggs', x: 51, color: '#a855f7' },
    { label: 'Marts', sub: '~10 final', x: 67, color: '#fbbf24' },
    { label: 'Optimize', sub: 'final', x: 83, color: '#10b981' },
  ];
  const tNodeW = 14, tNodeH = 8;
  const tY = 42;

  // ─── SPAGHETTI CHAOS ───
  const chaosNodes = useMemo(() =>
    Array.from({ length: 45 }, (_, i) => ({
      id: i,
      x: 4 + (i * 19.3 + i * i * 3.1) % 88,
      y: 3 + (i * 11.7 + i * i * 2.9) % 58,
      r: 0.6 + (i % 4) * 0.4,
      color: ['#ef4444', '#f97316', '#dc2626', '#b91c1c'][i % 4],
    })),
  []);
  const chaosEdges = useMemo(() =>
    Array.from({ length: 65 }, (_, i) => {
      const a = chaosNodes[i % chaosNodes.length];
      const b = chaosNodes[(i * 7 + 5) % chaosNodes.length];
      return { id: i, x1: a.x, y1: a.y, x2: b.x, y2: b.y };
    }),
  []);
  const chaosLabels = [
    { x: 8, y: 14, text: 'recipe_sales_daily_v3' },
    { x: 52, y: 7, text: 'recipe_inv_COPY(2)' },
    { x: 25, y: 40, text: 'recipe_FINAL_DO_NOT_EDIT' },
    { x: 68, y: 48, text: 'recipe_customer_OLD' },
    { x: 40, y: 25, text: 'recipe_tender_???' },
    { x: 78, y: 18, text: 'recipe_guyana_manual' },
    { x: 14, y: 55, text: 'recipe_refund_SAP_bak' },
  ];

  return (
    <div className="my-10 rounded-2xl border border-[var(--color-border)] bg-[var(--color-bg-card)] p-6 md:p-8">
      <div className="flex items-center gap-2 mb-2">
        <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
        <span className="text-xs font-bold uppercase tracking-[0.15em] text-[var(--color-fg-faint)]">
          {t.orchestrationOverhaul[locale]}
        </span>
      </div>

      <div className="flex justify-between mb-4">
        <span className={`text-sm font-bold transition-colors duration-500 ${
          phase === 'dag' ? 'text-[var(--color-fg-faint)] line-through' : 'text-[#ef4444]'
        }`}>
          1,200 Workato recipes
        </span>
        <span className={`text-sm font-bold transition-all duration-500 ${
          phase === 'dag' ? 'text-[var(--color-accent)]' : 'text-[var(--color-fg-faint)]'
        }`}>
          Airflow DAGs
        </span>
      </div>

      <div className="relative rounded-xl bg-[var(--color-bg)] border border-[var(--color-border)] overflow-hidden">
        <svg viewBox="0 0 100 66" className="w-full" style={{ height: 'auto', maxHeight: '380px' }}>
          <defs>
            <marker id="arr" markerWidth="3.5" markerHeight="2.5" refX="3.2" refY="1.25" orient="auto">
              <path d="M0,0 L3.5,1.25 L0,2.5" fill="#22d3ee" opacity={0.6} />
            </marker>
          </defs>

          {/* ════════ CHAOS LAYER ════════ */}
          {chaosEdges.map((e, i) => (
            <line key={`ce-${e.id}`}
              x1={e.x1} y1={e.y1} x2={e.x2} y2={e.y2}
              strokeWidth={0.18}
              className="transition-all duration-[1.5s]"
              style={{ stroke: '#ef4444', opacity: phase === 'chaos' ? 0.15 : 0, transitionDelay: `${(i % 12) * 0.03}s` }}
            />
          ))}
          {chaosNodes.map(n => (
            <circle key={`cn-${n.id}`} cx={n.x} cy={n.y} r={n.r}
              className="transition-all duration-[1.5s]"
              style={{
                fill: n.color,
                opacity: phase === 'chaos' ? 0.45 : phase === 'collapsing' ? 0.2 : 0,
                transform: phase === 'collapsing' ? `translate(${(50 - n.x) * 0.7}px, ${(33 - n.y) * 0.7}px)` : '',
                transitionDelay: `${(n.id % 10) * 0.04}s`,
              }}
            />
          ))}
          {chaosLabels.map((l, i) => (
            <text key={`cl-${i}`} x={l.x} y={l.y}
              fontSize={1.35} fontFamily="var(--font-mono, monospace)"
              className="transition-all duration-[1.2s]"
              style={{ fill: '#ef4444', opacity: phase === 'chaos' ? 0.3 : 0, transitionDelay: `${i * 0.08}s` }}
            >
              {l.text}
            </text>
          ))}
          {phase === 'chaos' && (
            <text x={50} y={63} textAnchor="middle" fontSize={1.8} fontWeight={600}
              fill="#ef4444" opacity={0.25} fontFamily="var(--font-sans)">
              {t.storedProcedures[locale]}
            </text>
          )}
          {phase === 'collapsing' && (
            <circle cx={50} cy={33} r={3} fill="#f59e0b" opacity={0.06}>
              <animate attributeName="r" values="2;14;2" dur="1.4s" fill="freeze" />
              <animate attributeName="opacity" values="0.12;0.02;0" dur="1.4s" fill="freeze" />
            </circle>
          )}

          {/* ════════ DAG LAYER ════════ */}

          {/* ── Section label: Extract ── */}
          <text x={1} y={eCenterY + 0.5} fontSize={1.3} fontWeight={700} fill="var(--color-fg-faint)"
            fontFamily="var(--font-sans)" writingMode="tb" textAnchor="middle"
            className="transition-all duration-700"
            style={{ opacity: phase === 'dag' ? 0.4 : 0, transitionDelay: '0.1s' }}
          >
            {t.extract[locale]}
          </text>

          {/* ── Oracle source ── */}
          <g className="transition-all duration-700"
            style={{ opacity: phase === 'dag' ? 1 : 0, transitionDelay: '0s' }}>
            <rect x={4} y={eCenterY - 7} width={10} height={14} rx={1.5}
              fill="#f59e0b" opacity={0.08} stroke="#f59e0b" strokeWidth={0.35} />
            <text x={9} y={eCenterY - 1.5} textAnchor="middle" fill="#f59e0b"
              fontSize={2} fontWeight={700} fontFamily="var(--font-sans)">Oracle</text>
            <text x={9} y={eCenterY + 2} textAnchor="middle" fill="var(--color-fg-faint)"
              fontSize={1.3} fontFamily="var(--font-sans)">{t.nineServers[locale]}</text>
          </g>

          {/* ── 7 parallel extract tasks ── */}
          {extractNodes.map((node, i) => (
            <g key={`en-${node.label}`}
              className="transition-all duration-500"
              style={{ opacity: phase === 'dag' ? 1 : 0, transitionDelay: `${0.05 * i + 0.1}s` }}
            >
              <rect x={node.x} y={node.y} width={eNodeW} height={eNodeH}
                rx={1} fill={node.color} opacity={0.08} stroke={node.color} strokeWidth={0.3} />
              <text x={node.x + eNodeW / 2} y={node.y + eNodeH / 2 + 0.6}
                textAnchor="middle" fill={node.color}
                fontSize={1.5} fontWeight={700} fontFamily="var(--font-mono, monospace)">
                {node.label}
              </text>
            </g>
          ))}

          {/* ── Oracle → extract edges (fan-out) ── */}
          {extractNodes.map((node, i) => (
            <line key={`oe-${i}`}
              x1={14} y1={eCenterY} x2={node.x} y2={node.y + eNodeH / 2}
              strokeWidth={0.25} markerEnd="url(#arr)"
              className="transition-all duration-500"
              style={{ stroke: '#f59e0b', opacity: phase === 'dag' ? 0.25 : 0, transitionDelay: `${0.05 * i}s` }}
            />
          ))}

          {/* ── S3 (fan-in target) ── */}
          <g className="transition-all duration-700"
            style={{ opacity: phase === 'dag' ? 1 : 0, transitionDelay: '0.3s' }}>
            <rect x={35} y={eCenterY - 6} width={11} height={12} rx={1.5}
              fill="#22d3ee" opacity={0.08} stroke="#22d3ee" strokeWidth={0.35} />
            <text x={40.5} y={eCenterY - 1} textAnchor="middle" fill="#22d3ee"
              fontSize={1.8} fontWeight={700} fontFamily="var(--font-sans)">S3</text>
            <text x={40.5} y={eCenterY + 2} textAnchor="middle" fill="var(--color-fg-faint)"
              fontSize={1.2} fontFamily="var(--font-sans)">Parquet</text>
          </g>

          {/* ── extract → S3 edges (fan-in) ── */}
          {extractNodes.map((node, i) => (
            <line key={`es-${i}`}
              x1={node.x + eNodeW} y1={node.y + eNodeH / 2} x2={35} y2={eCenterY}
              strokeWidth={0.2} markerEnd="url(#arr)"
              className="transition-all duration-500"
              style={{ stroke: '#22d3ee', opacity: phase === 'dag' ? 0.2 : 0, transitionDelay: `${0.05 * i + 0.2}s` }}
            />
          ))}

          {/* ── Fan labels ── */}
          {phase === 'dag' && (
            <>
              <text x={14.5} y={1.5} fontSize={1.1} fill="#f59e0b" opacity={0.45}
                fontFamily="var(--font-sans)" fontStyle="italic">fan-out (×7)</text>
              <text x={31.5} y={1.5} fontSize={1.1} fill="#22d3ee" opacity={0.45}
                fontFamily="var(--font-sans)" fontStyle="italic">fan-in</text>
            </>
          )}

          {/* ── Extract → S3 animated packets ── */}
          {phase === 'dag' && extractNodes.map((node, i) => (
            <circle key={`pk-e-${i}`} r={0.5} fill="#f59e0b">
              <animate attributeName="cx" values={`${node.x + eNodeW};35`}
                dur={`${1.4 + i * 0.15}s`} repeatCount="indefinite" begin={`${0.08 * i}s`} />
              <animate attributeName="cy" values={`${node.y + eNodeH / 2};${eCenterY}`}
                dur={`${1.4 + i * 0.15}s`} repeatCount="indefinite" begin={`${0.08 * i}s`} />
              <animate attributeName="opacity" values="0;0.7;0"
                dur={`${1.4 + i * 0.15}s`} repeatCount="indefinite" begin={`${0.08 * i}s`} />
            </circle>
          ))}

          {/* ── ClickPipes ── */}
          <g className="transition-all duration-700"
            style={{ opacity: phase === 'dag' ? 1 : 0, transitionDelay: '0.4s' }}>
            <rect x={50} y={eCenterY - 6} width={13} height={12} rx={1.5}
              fill="#22d3ee" opacity={0.08} stroke="#22d3ee" strokeWidth={0.35} />
            <text x={56.5} y={eCenterY - 1} textAnchor="middle" fill="#22d3ee"
              fontSize={1.6} fontWeight={700} fontFamily="var(--font-sans)">ClickPipes</text>
            <text x={56.5} y={eCenterY + 2} textAnchor="middle" fill="var(--color-fg-faint)"
              fontSize={1.1} fontFamily="var(--font-sans)">{t.autoIngest[locale]}</text>
          </g>

          {/* S3 → ClickPipes */}
          <line x1={46} y1={eCenterY} x2={50} y2={eCenterY}
            strokeWidth={0.35} markerEnd="url(#arr)"
            className="transition-all duration-700"
            style={{ stroke: '#22d3ee', opacity: phase === 'dag' ? 0.35 : 0, transitionDelay: '0.35s' }}
          />

          {/* ── Divider line ── */}
          <line x1={2} y1={37} x2={98} y2={37}
            strokeWidth={0.15} strokeDasharray="2 1.5"
            className="transition-all duration-700"
            style={{ stroke: 'var(--color-border)', opacity: phase === 'dag' ? 0.4 : 0, transitionDelay: '0.5s' }}
          />
          <text x={50} y={39.5} textAnchor="middle" fontSize={1.2} fontWeight={600}
            fill="var(--color-fg-faint)" fontFamily="var(--font-sans)"
            className="transition-all duration-700"
            style={{ opacity: phase === 'dag' ? 0.4 : 0, transitionDelay: '0.5s' }}>
            {t.transformHourly[locale]}
          </text>

          {/* ── Transform chain ── */}
          {transformNodes.map((node, i) => (
            <g key={`tn-${node.label}-${i}`}
              className="transition-all duration-500"
              style={{ opacity: phase === 'dag' ? 1 : 0, transitionDelay: `${0.5 + 0.08 * i}s` }}
            >
              <rect x={node.x} y={tY} width={tNodeW} height={tNodeH} rx={1.5}
                fill={node.color} opacity={0.08} stroke={node.color} strokeWidth={0.35} />
              <text x={node.x + tNodeW / 2} y={tY + 3.5}
                textAnchor="middle" fill={node.color}
                fontSize={1.7} fontWeight={700} fontFamily="var(--font-sans)">
                {node.label}
              </text>
              <text x={node.x + tNodeW / 2} y={tY + 6}
                textAnchor="middle" fill="var(--color-fg-faint)"
                fontSize={1.1} fontFamily="var(--font-sans)">
                {node.sub}
              </text>
            </g>
          ))}

          {/* ── Transform chain edges ── */}
          {transformNodes.slice(0, -1).map((node, i) => {
            const next = transformNodes[i + 1];
            return (
              <line key={`te-${i}`}
                x1={node.x + tNodeW} y1={tY + tNodeH / 2}
                x2={next.x} y2={tY + tNodeH / 2}
                strokeWidth={0.3} markerEnd="url(#arr)"
                className="transition-all duration-500"
                style={{ stroke: '#22d3ee', opacity: phase === 'dag' ? 0.3 : 0, transitionDelay: `${0.55 + 0.08 * i}s` }}
              />
            );
          })}

          {/* ── Transform chain packets ── */}
          {phase === 'dag' && transformNodes.slice(0, -1).map((node, i) => {
            const next = transformNodes[i + 1];
            return (
              <circle key={`pk-t-${i}`} r={0.5} fill={next.color}>
                <animate attributeName="cx"
                  values={`${node.x + tNodeW};${next.x}`}
                  dur={`${1.6 + i * 0.12}s`} repeatCount="indefinite" begin={`${0.15 * i}s`} />
                <animate attributeName="cy"
                  values={`${tY + tNodeH / 2};${tY + tNodeH / 2}`}
                  dur={`${1.6 + i * 0.12}s`} repeatCount="indefinite" />
                <animate attributeName="opacity"
                  values="0;0.7;0" dur={`${1.6 + i * 0.12}s`}
                  repeatCount="indefinite" begin={`${0.15 * i}s`} />
              </circle>
            );
          })}

          {/* ── Vertical connector: ClickPipes → Verify ── */}
          <line x1={56.5} y1={eCenterY + 6} x2={10} y2={tY}
            strokeWidth={0.3} strokeDasharray="1.5 1" markerEnd="url(#arr)"
            className="transition-all duration-700"
            style={{ stroke: '#22d3ee', opacity: phase === 'dag' ? 0.2 : 0, transitionDelay: '0.45s' }}
          />
        </svg>
      </div>

      {/* Bottom stats */}
      <div
        className="mt-5 grid grid-cols-4 gap-3 text-center transition-all duration-700"
        style={{ opacity: phase === 'dag' ? 1 : 0.3 }}
      >
        <div>
          <p className="text-lg font-extrabold text-[var(--color-accent)]">~140</p>
          <p className="text-[0.6rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.dbtModels[locale]}</p>
        </div>
        <div>
          <p className="text-lg font-extrabold text-[var(--color-accent)]">CDC</p>
          <p className="text-[0.6rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.noFullRefresh[locale]}</p>
        </div>
        <div>
          <p className="text-lg font-extrabold text-[var(--color-accent)]">RMT</p>
          <p className="text-[0.6rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.dedupOnWrite[locale]}</p>
        </div>
        <div>
          <p className="text-lg font-extrabold text-[var(--color-accent)]">Git</p>
          <p className="text-[0.6rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.versionControlled[locale]}</p>
        </div>
      </div>
    </div>
  );
}
