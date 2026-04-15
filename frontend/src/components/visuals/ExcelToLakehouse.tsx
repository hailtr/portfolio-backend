import { useEffect, useState, useMemo } from 'react';
import { useLocale } from '../../lib/useLocale';

const t = {
  dataConsolidation: { es: 'Consolidación de datos', en: 'Data consolidation' },
  excelFile: { es: 'Archivo Excel de 200 MB', en: '200 MB Excel file' },
  fabricLakehouse: { es: 'Fabric Lakehouse', en: 'Fabric Lakehouse' },
  painAnnotation: {
    es: '23 hojas · 200 MB · días para consolidar · sin control de acceso',
    en: '23 sheets · 200 MB · days to consolidate · zero access control',
  },
  lakehouseSubtitle: {
    es: 'Tablas Delta · Pipelines Automatizados · Acceso Gobernado',
    en: 'Delta Tables · Automated Pipelines · Governed Access',
  },
  sourcesUnified: { es: 'fuentes unificadas', en: 'sources unified' },
  stores: { es: 'tiendas', en: 'stores' },
  pipelines: { es: 'pipelines', en: 'pipelines' },
  automated: { es: 'automatizado', en: 'automated' },
  manual: { es: 'manual', en: 'manual' },
} as const;

/**
 * Excel → Fabric lakehouse migration story.
 * Phase 1 (chaos): 3 sources manually funneled into one overloaded Excel file.
 * Phase 2 (transform): collapse.
 * Phase 3 (clean): same 3 sources, now automated into their own Delta tables.
 */
export default function ExcelToLakehouse() {
  const locale = useLocale();
  const [phase, setPhase] = useState<'idle' | 'chaos' | 'transform' | 'clean'>('idle');

  useEffect(() => {
    const raf = requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        setPhase('chaos');
        setTimeout(() => setPhase('transform'), 3000);
        setTimeout(() => setPhase('clean'), 4800);
      });
    });
    return () => cancelAnimationFrame(raf);
  }, []);

  // Deterministic pseudo-random for grid cells
  const grid = useMemo(() => {
    let s = 42;
    const rng = () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };

    const COLS = 7, ROWS = 6;
    const cellW = 9.5, cellH = 5.8;
    const startX = 28, startY = 24;
    const highlights = ['', '', '', '#fef3c7', '#fecaca', '#d1fae5', '#dbeafe'];

    return Array.from({ length: COLS * ROWS }, (_, i) => {
      const col = i % COLS, row = Math.floor(i / COLS);
      const isError = rng() < 0.12;
      const isEmpty = rng() < 0.18;
      return {
        id: i, col, row,
        x: startX + col * cellW,
        y: startY + row * cellH,
        w: cellW - 0.3,
        h: cellH - 0.3,
        bg: isError ? '#fecaca' : highlights[Math.floor(rng() * highlights.length)],
        hasContent: !isEmpty,
        isError,
        barW: 2 + rng() * 5.5,
        delay: rng() * 0.4,
      };
    });
  }, []);

  const sources = [
    { label: 'ERP', color: '#7c3aed', y: 18 },
    { label: 'WhatsApp', color: '#22c55e', y: 38 },
    { label: 'Legacy ERP', color: '#f59e0b', y: 58 },
  ];

  const sheetTabs = ['Sheet 1', 'Sheet 2', '...', 'Sheet 23'];

  // Clean phase: Delta tables
  const tables = [
    { label: 'ERP', color: '#7c3aed', x: 5, cols: ['store_id', 'amount', 'region'] },
    { label: 'WhatsApp', color: '#22c55e', x: 37.5, cols: ['store_id', 'status', 'ts'] },
    { label: 'Legacy', color: '#f59e0b', x: 70, cols: ['id', 'value', 'period'] },
  ];

  const isChaos = phase === 'chaos';
  const isClean = phase === 'clean';

  return (
    <div className="my-10 rounded-2xl border border-[var(--color-border)] bg-[var(--color-bg-card)] p-6 md:p-8">
      <div className="flex items-center gap-2 mb-2">
        <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
        <span className="text-xs font-bold uppercase tracking-[0.15em] text-[var(--color-fg-faint)]">
          {t.dataConsolidation[locale]}
        </span>
      </div>

      <div className="flex justify-between mb-4">
        <span className={`text-sm font-bold transition-all duration-500 ${
          isClean ? 'text-[var(--color-fg-faint)] line-through' : 'text-[#ef4444]'
        }`}>
          {t.excelFile[locale]}
        </span>
        <span className={`text-sm font-bold transition-all duration-500 ${
          isClean ? 'text-[var(--color-accent)]' : 'text-[var(--color-fg-faint)]'
        }`}>
          {t.fabricLakehouse[locale]}
        </span>
      </div>

      <div className="relative rounded-xl bg-[var(--color-bg)] border border-[var(--color-border)] overflow-hidden">
        <svg viewBox="0 0 100 82" className="w-full" style={{ height: 'auto', maxHeight: '340px' }}>

          {/* ════════════════════════════════════════════
              CHAOS PHASE — 3 sources → manual merge → Excel
              ════════════════════════════════════════════ */}

          {/* Source boxes (left side) */}
          {sources.map((src, i) => (
            <g key={`src-${src.label}`}>
              <rect
                x={1} y={src.y - 5} width={16} height={10} rx={1.5}
                className="transition-all duration-700"
                style={{
                  fill: src.color, opacity: isChaos ? 0.15 : 0,
                  stroke: src.color, strokeWidth: 0.4, strokeOpacity: isChaos ? 0.4 : 0,
                  transitionDelay: `${i * 0.15}s`,
                }}
              />
              <text
                x={9} y={src.y + 0.5}
                textAnchor="middle" fontSize={2} fontWeight={700}
                fill={src.color} fontFamily="var(--font-sans)"
                className="transition-all duration-700"
                style={{ opacity: isChaos ? 0.9 : 0, transitionDelay: `${i * 0.15}s` }}
              >
                {src.label}
              </text>
              {/* "manual" label on arrow */}
              <text
                x={22} y={src.y - 2}
                textAnchor="middle" fontSize={1.2} fontWeight={500}
                fill="#ef4444" fontFamily="var(--font-sans)"
                className="transition-all duration-700"
                style={{ opacity: isChaos ? 0.5 : 0, transitionDelay: `${0.3 + i * 0.1}s` }}
              >
                {t.manual[locale]}
              </text>
              {/* Arrow from source to Excel area */}
              <line
                x1={17} y1={src.y}
                x2={27} y2={38}
                strokeWidth={0.35} strokeDasharray="1.5 1"
                className="transition-all duration-[1s]"
                style={{
                  stroke: '#ef4444', opacity: isChaos ? 0.3 : 0,
                  transitionDelay: `${0.2 + i * 0.1}s`,
                }}
              />
            </g>
          ))}

          {/* Excel window */}
          {/* Title bar */}
          <rect x={27} y={12} width={70} height={5}
            className="transition-all duration-700"
            style={{ fill: '#217346', opacity: isChaos ? 0.85 : 0 }}
          />
          <text x={30} y={15.5} fontSize={1.8} fill="white" fontWeight={600}
            fontFamily="var(--font-sans)"
            className="transition-all duration-700"
            style={{ opacity: isChaos ? 0.9 : 0 }}
          >
            Book1.xlsx — 200 MB
          </text>
          {/* Window buttons */}
          {[84, 88, 92].map((cx, i) => (
            <circle key={`wb-${i}`} cx={cx} cy={14.5} r={0.7}
              className="transition-all duration-700"
              style={{
                fill: ['#ef4444', '#f59e0b', '#22c55e'][i],
                opacity: isChaos ? 0.5 : 0,
              }}
            />
          ))}

          {/* Formula bar */}
          <rect x={27} y={17} width={70} height={3.5}
            className="transition-all duration-500"
            style={{ fill: 'var(--color-border)', opacity: isChaos ? 0.15 : 0 }}
          />
          <text x={29.5} y={19.3} fontSize={1.3} fill="var(--color-fg-faint)"
            fontFamily="var(--font-mono, monospace)"
            className="transition-all duration-500"
            style={{ opacity: isChaos ? 0.4 : 0 }}
          >
            =VLOOKUP(A2,Sheet12!$A:$F,3,FALSE)
          </text>

          {/* Column headers */}
          {['A', 'B', 'C', 'D', 'E', 'F', 'G'].map((h, i) => (
            <text key={`ch-${h}`}
              x={28 + i * 9.5 + 4.7}
              y={23}
              textAnchor="middle" fontSize={1.5} fontWeight={600}
              fill="var(--color-fg-faint)"
              className="transition-all duration-500"
              style={{ opacity: isChaos ? 0.4 : 0 }}
            >
              {h}
            </text>
          ))}

          {/* Grid cells */}
          {grid.map(cell => (
            <g key={`gc-${cell.id}`}>
              <rect
                x={cell.x} y={cell.y}
                width={cell.w} height={cell.h}
                rx={0.2}
                className="transition-all duration-[1s]"
                style={{
                  fill: cell.bg || 'transparent',
                  stroke: 'var(--color-border)',
                  strokeWidth: 0.12,
                  opacity: isChaos ? 1 : 0,
                  transform: phase === 'transform'
                    ? `translate(${(55 - cell.x) * 0.6}px, ${(45 - cell.y) * 0.5}px) scale(0.15)`
                    : '',
                  transitionDelay: `${cell.delay}s`,
                }}
              />
              {cell.hasContent && (
                <rect
                  x={cell.x + 0.5}
                  y={cell.y + cell.h / 2 - 0.6}
                  width={cell.barW}
                  height={1.2}
                  rx={0.3}
                  className="transition-all duration-[1s]"
                  style={{
                    fill: cell.isError ? '#ef4444' : '#94a3b8',
                    opacity: isChaos ? (cell.isError ? 0.6 : 0.2) : 0,
                    transitionDelay: `${cell.delay}s`,
                  }}
                />
              )}
              {cell.isError && (
                <polygon
                  points={`${cell.x + cell.w - 1.3},${cell.y + 0.2} ${cell.x + cell.w - 0.2},${cell.y + 0.2} ${cell.x + cell.w - 0.2},${cell.y + 1.3}`}
                  className="transition-all duration-700"
                  style={{ fill: '#ef4444', opacity: isChaos ? 0.7 : 0 }}
                />
              )}
            </g>
          ))}

          {/* Sheet tabs */}
          <rect x={27} y={59} width={70} height={4}
            className="transition-all duration-500"
            style={{ fill: 'var(--color-border)', opacity: isChaos ? 0.15 : 0 }}
          />
          {sheetTabs.map((tab, i) => (
            <g key={`tab-${i}`}>
              <rect
                x={29 + i * 15} y={59.5} width={13} height={3} rx={0.5}
                className="transition-all duration-500"
                style={{
                  fill: i === 0 ? 'var(--color-bg)' : 'transparent',
                  stroke: 'var(--color-border)', strokeWidth: 0.15,
                  opacity: isChaos ? 0.4 : 0,
                }}
              />
              <text
                x={29 + i * 15 + 6.5} y={61.5}
                textAnchor="middle" fontSize={1.3}
                fill="var(--color-fg-faint)"
                className="transition-all duration-500"
                style={{ opacity: isChaos ? 0.5 : 0 }}
              >
                {tab}
              </text>
            </g>
          ))}

          {/* Pain annotations */}
          <text x={62} y={67}
            textAnchor="middle" fontSize={1.5} fontWeight={700}
            fill="#ef4444" fontFamily="var(--font-sans)"
            className="transition-all duration-700"
            style={{ opacity: isChaos ? 0.5 : 0, transitionDelay: '0.8s' }}
          >
            {t.painAnnotation[locale]}
          </text>

          {/* ════════════════════════════════════════════
              CLEAN PHASE — 3 automated Delta tables
              ════════════════════════════════════════════ */}

          {tables.map((table, ti) => (
            <g key={table.label}>
              {/* Table header bar */}
              <rect
                x={table.x} y={8}
                width={26} height={7} rx={1.5}
                className="transition-all duration-700"
                style={{ fill: table.color, opacity: isClean ? 0.3 : 0, transitionDelay: `${0.15 * ti}s` }}
              />
              <text
                x={table.x + 13} y={12.5}
                textAnchor="middle" fontSize={2.5} fontWeight={700}
                fill="white" fontFamily="var(--font-sans)"
                className="transition-all duration-700"
                style={{ opacity: isClean ? 1 : 0, transitionDelay: `${0.15 * ti}s` }}
              >
                {table.label}
              </text>

              {/* Column header row */}
              <rect
                x={table.x} y={16} width={26} height={5}
                className="transition-all duration-500"
                style={{ fill: table.color, opacity: isClean ? 0.08 : 0, transitionDelay: `${0.15 * ti + 0.2}s` }}
              />
              {table.cols.map((col, ci) => (
                <text
                  key={`tc-${ti}-${ci}`}
                  x={table.x + 2 + ci * (22 / table.cols.length)}
                  y={19.3}
                  fontSize={1.4} fontWeight={600}
                  fill={table.color} fontFamily="var(--font-mono, monospace)"
                  className="transition-all duration-500"
                  style={{ opacity: isClean ? 0.7 : 0, transitionDelay: `${0.15 * ti + 0.25}s` }}
                >
                  {col}
                </text>
              ))}

              {/* Data rows */}
              {Array.from({ length: 4 }, (_, ri) => (
                <rect
                  key={`tr-${ti}-${ri}`}
                  x={table.x} y={22 + ri * 5.5}
                  width={26} height={4.5} rx={0.5}
                  className="transition-all duration-500"
                  style={{
                    fill: table.color, opacity: isClean ? 0.05 : 0,
                    stroke: table.color, strokeWidth: 0.2,
                    strokeOpacity: isClean ? 0.15 : 0,
                    transitionDelay: `${0.15 * ti + 0.08 * ri + 0.35}s`,
                  }}
                />
              ))}

              {/* Arrow to unified lakehouse */}
              <line
                x1={table.x + 13} y1={45}
                x2={50} y2={58}
                strokeWidth={0.4} strokeDasharray="1.5 1"
                className="transition-all duration-700"
                style={{ stroke: '#22d3ee', opacity: isClean ? 0.3 : 0, transitionDelay: `${0.15 * ti + 0.6}s` }}
              />
              {/* "automated" label */}
              {ti === 1 && (
                <text
                  x={53} y={53}
                  textAnchor="start" fontSize={1.2} fontWeight={500}
                  fill="#22d3ee" fontFamily="var(--font-sans)"
                  className="transition-all duration-700"
                  style={{ opacity: isClean ? 0.5 : 0, transitionDelay: '0.7s' }}
                >
                  {t.automated[locale]}
                </text>
              )}
            </g>
          ))}

          {/* Unified lakehouse box */}
          <rect x={14} y={56} width={72} height={16} rx={2}
            className="transition-all duration-700"
            style={{
              fill: '#22d3ee', opacity: isClean ? 0.08 : 0,
              stroke: '#22d3ee', strokeWidth: 0.5, strokeOpacity: isClean ? 0.4 : 0,
              transitionDelay: '0.9s',
            }}
          />
          <text x={50} y={64} textAnchor="middle" fontSize={3} fontWeight={700}
            fill="#22d3ee" fontFamily="var(--font-sans)"
            className="transition-all duration-700"
            style={{ opacity: isClean ? 1 : 0, transitionDelay: '1s' }}
          >
            Microsoft Fabric Lakehouse
          </text>
          <text x={50} y={68.5} textAnchor="middle" fontSize={1.7}
            fill="#22d3ee" fontFamily="var(--font-sans)"
            className="transition-all duration-700"
            style={{ opacity: isClean ? 0.5 : 0, transitionDelay: '1.1s' }}
          >
            {t.lakehouseSubtitle[locale]}
          </text>
        </svg>
      </div>

      {/* Stats */}
      <div
        className="mt-5 grid grid-cols-3 gap-4 text-center transition-all duration-700"
        style={{ opacity: isClean ? 1 : 0.3 }}
      >
        <div>
          <p className="text-lg font-extrabold text-[var(--color-accent)]">3</p>
          <p className="text-[0.65rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.sourcesUnified[locale]}</p>
        </div>
        <div>
          <p className="text-lg font-extrabold text-[var(--color-accent)]">1,200+</p>
          <p className="text-[0.65rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.stores[locale]}</p>
        </div>
        <div>
          <p className="text-lg font-extrabold text-[var(--color-accent)]">Auto</p>
          <p className="text-[0.65rem] text-[var(--color-fg-faint)] uppercase tracking-wider">{t.pipelines[locale]}</p>
        </div>
      </div>
    </div>
  );
}
