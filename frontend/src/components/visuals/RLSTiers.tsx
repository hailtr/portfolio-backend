import { useEffect, useState } from 'react';
import { useLocale } from '../../lib/useLocale';

const t = {
  promoter:       { es: 'Promotor',    en: 'Promoter' },
  supervisor:     { es: 'Supervisor',   en: 'Supervisor' },
  manager:        { es: 'Gerente',      en: 'Manager' },
  ownStores:      { es: 'Solo tiendas propias',  en: 'Own stores only' },
  regionStores:   { es: 'Tiendas de la región',  en: 'Region stores' },
  allStores:      { es: 'Todas las tiendas',     en: 'All stores' },
  dashboardTitle: { es: 'Power BI — Dashboard de Ventas', en: 'Power BI — Sales Dashboard' },
  noRls:          { es: 'Sin RLS — todos ven todo',       en: 'No RLS — everyone sees everything' },
  revenue:        { es: 'Ingresos',       en: 'Revenue' },
  stores:         { es: 'Tiendas',        en: 'Stores' },
  avgStore:       { es: 'Prom / Tienda',  en: 'Avg / Store' },
  growth:         { es: 'Crecimiento',    en: 'Growth' },
  salesByStore:   { es: 'Ventas por tienda',     en: 'Sales by store' },
  regionBreakdown:{ es: 'Desglose por región',   en: 'Region breakdown' },
  myStores:       { es: 'Mis tiendas',           en: 'My stores' },
  regionWest:     { es: 'Región Oeste',           en: 'Region West' },
  regionEast:     { es: 'Región Este',            en: 'Region East' },
  teamStores:     { es: 'Tiendas del equipo',    en: 'Team stores' },
  national:       { es: 'Nacional',               en: 'National' },
  noRlsWarning:   { es: 'Antes: cualquiera con el archivo Excel podía ver todos los datos — sin control de acceso',
                    en: 'Before: anyone with the Excel file could see all data — zero access control' },
  caption:        { es: 'Mismo dashboard, datos diferentes. Haz clic en un rol para ver qué cambia.',
                    en: 'Same dashboard, different data. Click a role to see what changes.' },
};

/**
 * Row-Level Security — simulated Power BI dashboard.
 * Same layout, different data per role. KPIs change, chart bars shift,
 * region rows get restricted. Starts with "No RLS" showing everything.
 */
export default function RLSTiers() {
  const locale = useLocale();
  const [activeRole, setActiveRole] = useState<number>(-1);

  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    const raf = requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        const t1 = setTimeout(() => setActiveRole(0), 2500);
        interval = setInterval(() => {
          setActiveRole((prev) => (prev + 1) % 3);
        }, 3000);
        return () => clearTimeout(t1);
      });
    });
    return () => {
      cancelAnimationFrame(raf);
      clearInterval(interval);
    };
  }, []);

  const roles = [
    {
      name: t.promoter[locale],
      color: '#22d3ee',
      desc: t.ownStores[locale],
      revenue: '$12.4K',
      stores: '3',
      avg: '$4.1K',
      growth: '+8%',
      bars: [65, 45, 80],
      regions: [
        { name: t.myStores[locale], value: '$12,400', ok: true },
        { name: t.regionWest[locale], value: '—', ok: false },
        { name: t.regionEast[locale], value: '—', ok: false },
      ],
    },
    {
      name: t.supervisor[locale],
      color: '#f59e0b',
      desc: t.regionStores[locale],
      revenue: '$89.2K',
      stores: '8',
      avg: '$11.2K',
      growth: '+12%',
      bars: [65, 45, 80, 55, 70, 40, 60, 50],
      regions: [
        { name: t.teamStores[locale], value: '$52,100', ok: true },
        { name: t.regionWest[locale], value: '$37,100', ok: true },
        { name: t.regionEast[locale], value: '—', ok: false },
      ],
    },
    {
      name: t.manager[locale],
      color: '#a855f7',
      desc: t.allStores[locale],
      revenue: '$341K',
      stores: '15',
      avg: '$22.7K',
      growth: '+18%',
      bars: [65, 45, 80, 55, 70, 40, 60, 50, 75, 35, 90, 48, 62, 55, 42],
      regions: [
        { name: t.national[locale], value: '$341,000', ok: true },
        { name: t.regionWest[locale], value: '$187,200', ok: true },
        { name: t.regionEast[locale], value: '$153,800', ok: true },
      ],
    },
  ];

  const isNoRLS = activeRole === -1;
  const active = isNoRLS ? roles[2] : roles[activeRole]; // No RLS shows Manager's data
  const accent = isNoRLS ? '#ef4444' : active.color;

  return (
    <div className="my-10 rounded-2xl border border-[var(--color-border)] bg-[var(--color-bg-card)] p-6 md:p-8">
      <div className="flex items-center gap-2 mb-6">
        <span className="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
        <span className="text-xs font-bold uppercase tracking-[0.15em] text-[var(--color-fg-faint)]">
          Row-Level Security
        </span>
      </div>

      {/* Role selector */}
      <div className="flex gap-2 mb-5">
        {roles.map((role, i) => (
          <button
            key={role.name}
            onClick={() => setActiveRole(i)}
            className="flex-1 rounded-lg px-3 py-2 text-xs font-bold uppercase tracking-wider transition-all duration-300 border cursor-pointer"
            style={{
              borderColor: activeRole === i ? role.color : 'var(--color-border)',
              backgroundColor: activeRole === i ? `${role.color}15` : 'transparent',
              color: activeRole === i ? role.color : 'var(--color-fg-faint)',
            }}
          >
            {role.name}
          </button>
        ))}
      </div>

      {/* Dashboard simulation */}
      <div className="rounded-xl bg-[var(--color-bg)] border border-[var(--color-border)] overflow-hidden">

        {/* Dashboard header */}
        <div className="flex items-center justify-between px-4 py-2.5 border-b border-[var(--color-border)]">
          <div className="flex items-center gap-2">
            <div
              className="h-2 w-2 rounded-full transition-colors duration-300"
              style={{ backgroundColor: accent }}
            />
            <span className="text-[0.65rem] font-bold text-[var(--color-fg-muted)]">
              {t.dashboardTitle[locale]}
            </span>
          </div>
          <span
            className="text-[0.55rem] font-semibold uppercase tracking-wider transition-all duration-300"
            style={{ color: accent }}
          >
            {isNoRLS ? t.noRls[locale] : active.desc}
          </span>
        </div>

        <div className="p-4 space-y-4">

          {/* KPI Cards */}
          <div className="grid grid-cols-4 gap-2">
            {[
              { label: t.revenue[locale], value: active.revenue },
              { label: t.stores[locale], value: active.stores },
              { label: t.avgStore[locale], value: active.avg },
              { label: t.growth[locale], value: active.growth },
            ].map((kpi) => (
              <div key={kpi.label}
                className="rounded-lg border px-2.5 py-2 transition-all duration-500"
                style={{
                  borderColor: `${accent}20`,
                  backgroundColor: `${accent}08`,
                }}
              >
                <p className="text-[0.5rem] uppercase tracking-wider text-[var(--color-fg-faint)] mb-0.5">
                  {kpi.label}
                </p>
                <p
                  className="text-sm font-extrabold transition-all duration-500"
                  style={{ color: accent }}
                >
                  {kpi.value}
                </p>
              </div>
            ))}
          </div>

          {/* Bar chart */}
          <div className="rounded-lg border border-[var(--color-border)] p-3">
            <p className="text-[0.5rem] uppercase tracking-wider text-[var(--color-fg-faint)] mb-2">
              {t.salesByStore[locale]}
            </p>
            <div className="flex items-end gap-[3px]" style={{ height: '48px' }}>
              {Array.from({ length: 15 }, (_, i) => {
                const hasBar = i < active.bars.length;
                const height = hasBar ? active.bars[i] : 0;
                return (
                  <div
                    key={i}
                    className="flex-1 rounded-t-sm transition-all duration-500"
                    style={{
                      height: `${height}%`,
                      backgroundColor: hasBar ? accent : 'transparent',
                      opacity: hasBar ? 0.5 : 0.05,
                      transitionDelay: `${i * 20}ms`,
                    }}
                  />
                );
              })}
            </div>
          </div>

          {/* Region breakdown */}
          <div className="space-y-1">
            <p className="text-[0.5rem] uppercase tracking-wider text-[var(--color-fg-faint)] mb-1.5">
              {t.regionBreakdown[locale]}
            </p>
            {active.regions.map((region) => (
              <div key={region.name}
                className="flex items-center justify-between rounded-md px-2.5 py-1.5 transition-all duration-400"
                style={{
                  backgroundColor: region.ok ? `${accent}08` : 'transparent',
                  opacity: region.ok ? 1 : 0.35,
                }}
              >
                <span className="text-[0.6rem] font-medium text-[var(--color-fg-muted)]">
                  {region.name}
                </span>
                <span
                  className="text-[0.65rem] font-bold transition-all duration-500"
                  style={{ color: region.ok ? accent : 'var(--color-fg-faint)' }}
                >
                  {region.value}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* No RLS warning bar */}
        {isNoRLS && (
          <div className="px-4 py-2 border-t border-[#ef444420] bg-[#ef444408]">
            <p className="text-[0.55rem] text-center font-semibold text-[#ef4444]" style={{ opacity: 0.7 }}>
              {t.noRlsWarning[locale]}
            </p>
          </div>
        )}
      </div>

      {/* Caption */}
      <p className="mt-4 text-center text-xs text-[var(--color-fg-faint)]">
        {t.caption[locale]}
      </p>
    </div>
  );
}
