import { useEffect, useState } from 'react';
import { useLocale } from '../../lib/useLocale';

const t = {
  heading: { es: 'Flujo de aprovisionamiento de tiendas', en: 'Store provisioning workflow' },
  before: { es: 'ANTES', en: 'BEFORE' },
  after: { es: 'DESPUÉS', en: 'AFTER' },
  petition: { es: 'Solicitud', en: 'Petition' },
  validate: { es: 'Validar', en: 'Validate' },
  validate2: { es: 'Validar 2', en: 'Validate 2' },
  create: { es: 'Crear', en: 'Create' },
  assign: { es: 'Asignar', en: 'Assign' },
  feedback: { es: 'Retroalimentación', en: 'Feedback' },
  templateGen: { es: 'Gen. plantilla', en: 'Template gen' },
  assignCreate: { es: 'Asignar + Crear', en: 'Assign + Create' },
  beforeAnnotation: { es: '6 pasos · 3 sistemas', en: '6 steps · 3 systems' },
  afterAnnotation: { es: '4 pasos · 1 sistema', en: '4 steps · 1 system' },
};

/**
 * Store provisioning workflow — before vs after.
 * Before: 6 steps bouncing between WhatsApp, ERP, and Excel.
 * After: 4 steps, mostly in SaaS (Flask app), with clean handoffs.
 * Larger viewBox (155) for readable text and better contrast.
 */
export default function StoreWorkflow() {
  const locale = useLocale();
  const [visible, setVisible] = useState(false);
  const [showAfter, setShowAfter] = useState(false);

  useEffect(() => {
    const raf = requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        setVisible(true);
        setTimeout(() => setShowAfter(true), 2000);
      });
    });
    return () => cancelAnimationFrame(raf);
  }, []);

  const systems = [
    { label: 'WhatsApp', x: 22, color: '#22c55e' },
    { label: 'ERP', x: 58, color: '#a78bfa' },
    { label: 'Excel', x: 94, color: '#ef4444' },
    { label: 'SaaS', x: 130, color: '#22d3ee' },
  ];

  const beforeSteps = [
    { sys: 0, y: 24, label: t.petition[locale] },
    { sys: 1, y: 33, label: t.validate[locale] },
    { sys: 2, y: 42, label: t.validate2[locale] },
    { sys: 1, y: 51, label: t.create[locale] },
    { sys: 2, y: 60, label: t.assign[locale] },
    { sys: 0, y: 69, label: t.feedback[locale] },
  ];

  const afterSteps = [
    { sys: 3, y: 82, label: t.petition[locale] },
    { sys: 3, y: 91, label: t.templateGen[locale] },
    { sys: 1, y: 100, label: t.assignCreate[locale] },
    { sys: 0, y: 109, label: t.feedback[locale] },
  ];

  const R = 3.5;
  const LABEL_OFF = 6.5;
  const MID_X = 78;

  return (
    <div className="my-10 rounded-2xl border border-[var(--color-border)] bg-[var(--color-bg-card)] p-6 md:p-8">
      <div className="flex items-center gap-2 mb-6">
        <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
        <span className="text-xs font-bold uppercase tracking-[0.15em] text-[var(--color-fg-faint)]">
          {t.heading[locale]}
        </span>
      </div>

      <div className="relative rounded-xl bg-[var(--color-bg)] border border-[var(--color-border)] overflow-hidden">
        <svg viewBox="0 0 155 115" className="w-full" style={{ height: 'auto', maxHeight: '520px' }}>

          {/* ── System column headers ── */}
          {systems.map((sys, i) => (
            <g key={sys.label}>
              <text x={sys.x} y={9}
                textAnchor="middle" fontSize={2.6} fontWeight={700}
                fill={sys.color} fontFamily="var(--font-sans)"
                className="transition-all duration-500"
                style={{ opacity: visible ? 0.9 : 0, transitionDelay: `${i * 0.1}s` }}
              >
                {sys.label}
              </text>
              <line x1={sys.x} y1={13} x2={sys.x} y2={112}
                strokeWidth={0.2} strokeDasharray="3 3"
                className="transition-all duration-700"
                style={{ stroke: sys.color, opacity: visible ? 0.18 : 0, transitionDelay: `${i * 0.1}s` }}
              />
            </g>
          ))}

          {/* ── BEFORE label ── */}
          <text x={5} y={46.5}
            textAnchor="middle" fontSize={1.8} fontWeight={700}
            fill="#ef4444" fontFamily="var(--font-sans)" letterSpacing={0.3}
            transform="rotate(-90, 5, 46.5)"
            className="transition-all duration-500"
            style={{ opacity: visible ? 0.6 : 0, transitionDelay: '0.3s' }}
          >
            {t.before[locale]}
          </text>

          {/* ── Before connecting lines (zig-zag) ── */}
          {beforeSteps.slice(0, -1).map((step, i) => {
            const next = beforeSteps[i + 1];
            const sx = systems[step.sys].x;
            const nx = systems[next.sys].x;
            return (
              <line key={`bl-${i}`}
                x1={sx} y1={step.y + R}
                x2={nx} y2={next.y - R}
                strokeWidth={0.6} strokeDasharray="2 1.2"
                className="transition-all duration-700"
                style={{
                  stroke: '#ef4444',
                  opacity: visible ? 0.3 : 0,
                  transitionDelay: `${0.3 + i * 0.12}s`,
                }}
              />
            );
          })}

          {/* ── Before step nodes ── */}
          {beforeSteps.map((step, i) => {
            const sys = systems[step.sys];
            const labelRight = sys.x < MID_X;
            return (
              <g key={`bs-${i}`}>
                <circle cx={sys.x} cy={step.y} r={R}
                  className="transition-all duration-500"
                  style={{
                    fill: sys.color, opacity: visible ? 0.18 : 0,
                    stroke: sys.color, strokeWidth: 0.5, strokeOpacity: visible ? 0.6 : 0,
                    transitionDelay: `${0.2 + i * 0.12}s`,
                  }}
                />
                <text x={sys.x} y={step.y + 1}
                  textAnchor="middle" fontSize={2.2} fontWeight={700}
                  fill={sys.color} fontFamily="var(--font-sans)"
                  className="transition-all duration-500"
                  style={{ opacity: visible ? 0.95 : 0, transitionDelay: `${0.2 + i * 0.12}s` }}
                >
                  {i + 1}
                </text>
                <text
                  x={labelRight ? sys.x + LABEL_OFF : sys.x - LABEL_OFF}
                  y={step.y + 0.8}
                  textAnchor={labelRight ? 'start' : 'end'}
                  fontSize={2} fontWeight={500}
                  fill="var(--color-fg-faint)" fontFamily="var(--font-sans)"
                  className="transition-all duration-500"
                  style={{ opacity: visible ? 0.7 : 0, transitionDelay: `${0.2 + i * 0.12}s` }}
                >
                  {step.label}
                </text>
              </g>
            );
          })}

          {/* Before annotation */}
          <text x={148} y={16}
            textAnchor="end" fontSize={1.8} fontWeight={600}
            fill="#ef4444" fontFamily="var(--font-sans)"
            className="transition-all duration-500"
            style={{ opacity: visible ? 0.55 : 0, transitionDelay: '1s' }}
          >
            {t.beforeAnnotation[locale]}
          </text>

          {/* ── Divider ── */}
          <line x1={12} y1={75.5} x2={143} y2={75.5}
            strokeWidth={0.4}
            className="transition-all duration-700"
            style={{
              stroke: 'var(--color-border)',
              opacity: showAfter ? 0.5 : 0,
              transitionDelay: '1.8s',
            }}
          />

          {/* ── AFTER label ── */}
          <text x={5} y={95.5}
            textAnchor="middle" fontSize={1.8} fontWeight={700}
            fill="#22d3ee" fontFamily="var(--font-sans)" letterSpacing={0.3}
            transform="rotate(-90, 5, 95.5)"
            className="transition-all duration-500"
            style={{ opacity: showAfter ? 0.6 : 0, transitionDelay: '2s' }}
          >
            {t.after[locale]}
          </text>

          {/* ── After connecting lines ── */}
          {afterSteps.slice(0, -1).map((step, i) => {
            const next = afterSteps[i + 1];
            const sx = systems[step.sys].x;
            const nx = systems[next.sys].x;
            return (
              <line key={`al-${i}`}
                x1={sx} y1={step.y + R}
                x2={nx} y2={next.y - R}
                strokeWidth={0.6} strokeDasharray="2 1.2"
                className="transition-all duration-700"
                style={{
                  stroke: '#22d3ee',
                  opacity: showAfter ? 0.4 : 0,
                  transitionDelay: `${2 + i * 0.15}s`,
                }}
              />
            );
          })}

          {/* ── After step nodes ── */}
          {afterSteps.map((step, i) => {
            const sys = systems[step.sys];
            const labelRight = sys.x < MID_X;
            return (
              <g key={`as-${i}`}>
                <circle cx={sys.x} cy={step.y} r={R}
                  className="transition-all duration-500"
                  style={{
                    fill: sys.color, opacity: showAfter ? 0.18 : 0,
                    stroke: sys.color, strokeWidth: 0.5, strokeOpacity: showAfter ? 0.6 : 0,
                    transitionDelay: `${2 + i * 0.15}s`,
                  }}
                />
                <text x={sys.x} y={step.y + 1}
                  textAnchor="middle" fontSize={2.2} fontWeight={700}
                  fill={sys.color} fontFamily="var(--font-sans)"
                  className="transition-all duration-500"
                  style={{ opacity: showAfter ? 0.95 : 0, transitionDelay: `${2 + i * 0.15}s` }}
                >
                  {i + 1}
                </text>
                <text
                  x={labelRight ? sys.x + LABEL_OFF : sys.x - LABEL_OFF}
                  y={step.y + 0.8}
                  textAnchor={labelRight ? 'start' : 'end'}
                  fontSize={2} fontWeight={500}
                  fill="var(--color-fg-faint)" fontFamily="var(--font-sans)"
                  className="transition-all duration-500"
                  style={{ opacity: showAfter ? 0.7 : 0, transitionDelay: `${2 + i * 0.15}s` }}
                >
                  {step.label}
                </text>
              </g>
            );
          })}

          {/* After annotation */}
          <text x={148} y={78}
            textAnchor="end" fontSize={1.8} fontWeight={600}
            fill="#22d3ee" fontFamily="var(--font-sans)"
            className="transition-all duration-500"
            style={{ opacity: showAfter ? 0.55 : 0, transitionDelay: '2.8s' }}
          >
            {t.afterAnnotation[locale]}
          </text>

        </svg>
      </div>
    </div>
  );
}
