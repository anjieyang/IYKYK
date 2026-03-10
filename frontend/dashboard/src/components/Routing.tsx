import type { ReactNode } from "react";

import type { ModelStats, Stats } from "../api";

const TIER_DOT: Record<string, string> = {
  SIMPLE: "bg-emerald-400",
  MEDIUM: "bg-sky-400",
  COMPLEX: "bg-orange-400",
  REASONING: "bg-violet-400",
};
const TIER_BAR: Record<string, string> = {
  SIMPLE: "bg-emerald-400/50",
  MEDIUM: "bg-sky-400/50",
  COMPLEX: "bg-orange-400/50",
  REASONING: "bg-violet-400/50",
};
const TIER_LABEL: Record<string, string> = {
  SIMPLE: "text-emerald-300/80",
  MEDIUM: "text-sky-300/80",
  COMPLEX: "text-orange-300/80",
  REASONING: "text-violet-300/80",
};

interface Props {
  stats: Stats | null;
}

export default function Routing({ stats }: Props) {
  const total = stats?.total_requests ?? 1;
  const tiers = ["SIMPLE", "MEDIUM", "COMPLEX", "REASONING"];
  const models = sortUsageBuckets(stats?.by_model);
  const transports = sortUsageBuckets(stats?.by_transport);
  const cacheModes = sortUsageBuckets(stats?.by_cache_mode);
  const methods = Object.entries(stats?.by_method ?? {}).sort(([, a], [, b]) => b - a);
  const cacheFamilies = sortUsageBuckets(stats?.by_cache_family);

  return (
    <div>
      <div className="flex items-end justify-between mb-10">
        <h1 className="text-[18px] font-semibold text-white tracking-tight">Routing</h1>
        <div className="text-right">
          <p className="text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.08em]">Cache Breakpoints</p>
          <p className="text-[20px] font-semibold text-white font-mono tracking-tight">
            {(stats?.total_cache_breakpoints ?? 0).toLocaleString()}
          </p>
        </div>
      </div>

      <section className="mb-12">
        <p className="text-[12px] font-medium text-[#6e6e72] uppercase tracking-[0.08em] mb-5">By Tier</p>
        <table className="w-full">
          <thead>
            <Th><span className="pl-1">Tier</span></Th>
            <Th right w="w-16">Count</Th>
            <Th w="w-[200px]">Distribution</Th>
            <Th right w="w-20">Conf.</Th>
            <Th right w="w-20">Savings</Th>
            <Th right w="w-24">Cost</Th>
          </thead>
          <tbody>
            {tiers.map((tier) => {
              const data = stats?.by_tier?.[tier];
              if (!data) return null;
              const pct = (data.count / total) * 100;
              return (
                <tr key={tier} className="border-b border-white/[0.04] hover:bg-white/[0.02] transition-colors">
                  <td className="py-3">
                    <div className="flex items-center gap-2.5 pl-1">
                      <div className={`h-[8px] w-[8px] rounded-[2px] ${TIER_DOT[tier]}`} />
                      <span className={`text-[13px] font-mono font-medium ${TIER_LABEL[tier]}`}>{tier}</span>
                    </div>
                  </td>
                  <td className="text-right font-mono text-[13px] text-[#b4b4b7] py-3">{data.count}</td>
                  <td className="py-3">
                    <div className="flex items-center gap-3">
                      <div className="flex-1 h-[4px] bg-white/[0.05] rounded-full overflow-hidden">
                        <div className={`h-full rounded-full ${TIER_BAR[tier]}`} style={{ width: `${pct}%` }} />
                      </div>
                      <span className="text-[12px] font-mono text-[#6e6e72] w-10 text-right">{pct.toFixed(0)}%</span>
                    </div>
                  </td>
                  <td className="text-right font-mono text-[13px] text-[#6e6e72] py-3">{data.avg_confidence.toFixed(2)}</td>
                  <td className="text-right font-mono text-[13px] text-[#b4b4b7] py-3">{(data.avg_savings * 100).toFixed(0)}%</td>
                  <td className="text-right font-mono text-[13px] text-[#8b8b8e] py-3">${data.total_cost.toFixed(4)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </section>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-12">
        <UsageTable title="By Model" label="Model" rows={models} total={total} />
        <MethodTable rows={methods} total={total} />
        <UsageTable title="By Transport" label="Transport" rows={transports} total={total} />
        <UsageTable title="By Cache Mode" label="Mode" rows={cacheModes} total={total} />
      </div>

      <section className="mt-12">
        <p className="text-[12px] font-medium text-[#6e6e72] uppercase tracking-[0.08em] mb-5">Cache Family</p>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {cacheFamilies.length === 0 && (
            <div className="md:col-span-2 xl:col-span-3 rounded-xl border border-white/[0.06] bg-white/[0.02] px-4 py-6 text-center text-[13px] text-[#4a4a4d]">
              No data
            </div>
          )}
          {cacheFamilies.map(([name, data]) => (
            <div key={name} className="rounded-xl border border-white/[0.06] bg-white/[0.02] px-4 py-4">
              <p className="text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.08em]">{name}</p>
              <div className="mt-3 flex items-end justify-between">
                <p className="text-[22px] font-semibold text-white font-mono tracking-tight">{data.count}</p>
                <p className="text-[12px] font-mono text-[#8b8b8e]">${data.total_cost.toFixed(4)}</p>
              </div>
              <p className="mt-1 text-[12px] font-mono text-[#5a5a5d]">{((data.count / total) * 100).toFixed(1)}% of routed requests</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function sortUsageBuckets(source: Record<string, ModelStats> | undefined) {
  return Object.entries(source ?? {}).sort(([, a], [, b]) => {
    if (b.count !== a.count) return b.count - a.count;
    return b.total_cost - a.total_cost;
  });
}

function UsageTable({
  title,
  label,
  rows,
  total,
}: {
  title: string;
  label: string;
  rows: [string, ModelStats][];
  total: number;
}) {
  return (
    <section>
      <p className="text-[12px] font-medium text-[#6e6e72] uppercase tracking-[0.08em] mb-5">{title}</p>
      <table className="w-full">
        <thead>
          <Th>{label}</Th>
          <Th right w="w-16">Count</Th>
          <Th right w="w-16">%</Th>
          <Th right w="w-24">Cost</Th>
        </thead>
        <tbody>
          {rows.map(([name, data]) => (
            <tr key={name} className="border-b border-white/[0.04] hover:bg-white/[0.02] transition-colors">
              <td className="font-mono text-[12px] text-[#b4b4b7] py-2.5">{name}</td>
              <td className="text-right font-mono text-[12px] text-[#6e6e72] py-2.5">{data.count}</td>
              <td className="text-right font-mono text-[12px] text-[#6e6e72] py-2.5">{((data.count / total) * 100).toFixed(1)}%</td>
              <td className="text-right font-mono text-[12px] text-[#8b8b8e] py-2.5">${data.total_cost.toFixed(4)}</td>
            </tr>
          ))}
          {rows.length === 0 && <Empty cols={4} />}
        </tbody>
      </table>
    </section>
  );
}

function MethodTable({
  rows,
  total,
}: {
  rows: [string, number][];
  total: number;
}) {
  return (
    <section>
      <p className="text-[12px] font-medium text-[#6e6e72] uppercase tracking-[0.08em] mb-5">By Method</p>
      <table className="w-full">
        <thead>
          <Th>Method</Th>
          <Th right w="w-16">Count</Th>
          <Th right w="w-16">%</Th>
        </thead>
        <tbody>
          {rows.map(([name, count]) => (
            <tr key={name} className="border-b border-white/[0.04] hover:bg-white/[0.02] transition-colors">
              <td className="font-mono text-[12px] text-[#b4b4b7] py-2.5">{name}</td>
              <td className="text-right font-mono text-[12px] text-[#6e6e72] py-2.5">{count}</td>
              <td className="text-right font-mono text-[12px] text-[#6e6e72] py-2.5">{((count / total) * 100).toFixed(1)}%</td>
            </tr>
          ))}
          {rows.length === 0 && <Empty cols={3} />}
        </tbody>
      </table>
    </section>
  );
}

function Th({ children, right, w }: { children: ReactNode; right?: boolean; w?: string }) {
  return (
    <th className={`text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2 border-b border-white/[0.07] ${right ? "text-right" : "text-left"} ${w ?? ""}`}>
      {children}
    </th>
  );
}

function Empty({ cols }: { cols: number }) {
  return <tr><td colSpan={cols} className="py-8 text-center text-[13px] text-[#4a4a4d]">No data</td></tr>;
}
