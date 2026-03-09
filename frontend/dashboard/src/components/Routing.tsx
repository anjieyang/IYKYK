import type { Stats } from "../api";

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
  const models = Object.entries(stats?.by_model ?? {}).sort(([, a], [, b]) => b.count - a.count);
  const methods = Object.entries(stats?.by_method ?? {}).sort(([, a], [, b]) => b - a);

  return (
    <div>
      <h1 className="text-[18px] font-semibold text-white tracking-tight mb-10">Routing</h1>

      {/* Tier table */}
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
            {tiers.map((t) => {
              const d = stats?.by_tier?.[t];
              if (!d) return null;
              const pct = (d.count / total) * 100;
              return (
                <tr key={t} className="border-b border-white/[0.04] hover:bg-white/[0.02] transition-colors">
                  <td className="py-3">
                    <div className="flex items-center gap-2.5 pl-1">
                      <div className={`h-[8px] w-[8px] rounded-[2px] ${TIER_DOT[t]}`} />
                      <span className={`text-[13px] font-mono font-medium ${TIER_LABEL[t]}`}>{t}</span>
                    </div>
                  </td>
                  <td className="text-right font-mono text-[13px] text-[#b4b4b7] py-3">{d.count}</td>
                  <td className="py-3">
                    <div className="flex items-center gap-3">
                      <div className="flex-1 h-[4px] bg-white/[0.05] rounded-full overflow-hidden">
                        <div className={`h-full rounded-full ${TIER_BAR[t]}`} style={{ width: `${pct}%` }} />
                      </div>
                      <span className="text-[12px] font-mono text-[#6e6e72] w-10 text-right">{pct.toFixed(0)}%</span>
                    </div>
                  </td>
                  <td className="text-right font-mono text-[13px] text-[#6e6e72] py-3">{d.avg_confidence.toFixed(2)}</td>
                  <td className="text-right font-mono text-[13px] text-[#b4b4b7] py-3">{(d.avg_savings * 100).toFixed(0)}%</td>
                  <td className="text-right font-mono text-[13px] text-[#8b8b8e] py-3">${d.total_cost.toFixed(4)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </section>

      {/* Model + Method side by side */}
      <div className="grid grid-cols-2 gap-12">
        <section>
          <p className="text-[12px] font-medium text-[#6e6e72] uppercase tracking-[0.08em] mb-5">By Model</p>
          <table className="w-full">
            <thead>
              <Th>Model</Th>
              <Th right w="w-16">Count</Th>
              <Th right w="w-24">Cost</Th>
            </thead>
            <tbody>
              {models.map(([m, d]) => (
                <tr key={m} className="border-b border-white/[0.04] hover:bg-white/[0.02] transition-colors">
                  <td className="font-mono text-[12px] text-[#b4b4b7] py-2.5">{m}</td>
                  <td className="text-right font-mono text-[12px] text-[#6e6e72] py-2.5">{d.count}</td>
                  <td className="text-right font-mono text-[12px] text-[#8b8b8e] py-2.5">${d.total_cost.toFixed(4)}</td>
                </tr>
              ))}
              {models.length === 0 && <Empty cols={3} />}
            </tbody>
          </table>
        </section>

        <section>
          <p className="text-[12px] font-medium text-[#6e6e72] uppercase tracking-[0.08em] mb-5">By Method</p>
          <table className="w-full">
            <thead>
              <Th>Method</Th>
              <Th right w="w-16">Count</Th>
              <Th right w="w-16">%</Th>
            </thead>
            <tbody>
              {methods.map(([m, c]) => (
                <tr key={m} className="border-b border-white/[0.04] hover:bg-white/[0.02] transition-colors">
                  <td className="font-mono text-[12px] text-[#b4b4b7] py-2.5">{m}</td>
                  <td className="text-right font-mono text-[12px] text-[#6e6e72] py-2.5">{c}</td>
                  <td className="text-right font-mono text-[12px] text-[#6e6e72] py-2.5">{((c / total) * 100).toFixed(1)}%</td>
                </tr>
              ))}
              {methods.length === 0 && <Empty cols={3} />}
            </tbody>
          </table>
        </section>
      </div>
    </div>
  );
}

function Th({ children, right, w }: { children: React.ReactNode; right?: boolean; w?: string }) {
  return (
    <th className={`text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2 border-b border-white/[0.07] ${right ? "text-right" : "text-left"} ${w ?? ""}`}>
      {children}
    </th>
  );
}

function Empty({ cols }: { cols: number }) {
  return <tr><td colSpan={cols} className="py-8 text-center text-[13px] text-[#4a4a4d]">No data</td></tr>;
}
