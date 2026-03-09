import type { Health, Stats } from "../api";

const TIER_BAR: Record<string, string> = {
  SIMPLE: "bg-emerald-400/70",
  MEDIUM: "bg-sky-400/70",
  COMPLEX: "bg-orange-400/70",
  REASONING: "bg-violet-400/70",
};
const TIER_DOT: Record<string, string> = {
  SIMPLE: "bg-emerald-400",
  MEDIUM: "bg-sky-400",
  COMPLEX: "bg-orange-400",
  REASONING: "bg-violet-400",
};
const TIER_LABEL: Record<string, string> = {
  SIMPLE: "text-emerald-300/80",
  MEDIUM: "text-sky-300/80",
  COMPLEX: "text-orange-300/80",
  REASONING: "text-violet-300/80",
};

interface Props {
  stats: Stats | null;
  health: Health | null;
}

export default function Overview({ stats, health }: Props) {
  const total = stats?.total_requests ?? 0;

  if (total === 0) return <Onboarding />;

  const savings = stats?.avg_savings != null ? `${(stats.avg_savings * 100).toFixed(0)}%` : "—";
  const latency = stats?.avg_latency_us != null ? `${Math.round(stats.avg_latency_us)}µs` : "—";
  const sessionCount = health?.sessions?.count ?? 0;
  const cost = stats?.total_actual_cost != null ? `$${stats.total_actual_cost.toFixed(2)}` : "—";

  const tiers = ["SIMPLE", "MEDIUM", "COMPLEX", "REASONING"]
    .map((t) => ({ name: t, count: stats?.by_tier?.[t]?.count ?? 0 }))
    .filter((t) => t.count > 0);

  const models = Object.entries(stats?.by_model ?? {})
    .sort(([, a], [, b]) => b.count - a.count)
    .slice(0, 6);
  const maxModelCount = models.length > 0 ? models[0][1].count : 1;

  return (
    <div>
      {/* Hero */}
      <div className="mb-12">
        <p className="text-[12px] font-medium text-[#6e6e72] uppercase tracking-[0.08em] mb-3">Average Savings</p>
        <p className="text-[56px] font-bold text-white leading-none tracking-tighter">{savings}</p>
      </div>

      {/* Stats strip */}
      <div className="flex gap-10 mb-14 pb-8 border-b border-white/[0.07]">
        <Stat label="Requests" value={total.toLocaleString()} />
        <Stat label="Total Cost" value={cost} />
        <Stat label="Avg Latency" value={latency} />
        <Stat label="Sessions" value={sessionCount.toString()} />
      </div>

      {/* Tier breakdown */}
      <section className="mb-14">
        <p className="text-[12px] font-medium text-[#6e6e72] uppercase tracking-[0.08em] mb-5">Tier Distribution</p>

        <div className="h-[6px] w-full rounded-full overflow-hidden flex bg-white/[0.06] mb-5">
          {tiers.map((t) => (
            <div
              key={t.name}
              className={`h-full ${TIER_BAR[t.name]} first:rounded-l-full last:rounded-r-full`}
              style={{ width: `${(t.count / total) * 100}%` }}
            />
          ))}
        </div>

        <div className="flex flex-wrap gap-x-6 gap-y-2">
          {tiers.map((t) => (
            <div key={t.name} className="flex items-center gap-2">
              <div className={`h-[8px] w-[8px] rounded-[2px] ${TIER_DOT[t.name]}`} />
              <span className={`text-[13px] font-medium ${TIER_LABEL[t.name]}`}>{t.name}</span>
              <span className="text-[13px] font-mono text-[#6e6e72]">{t.count}</span>
              <span className="text-[13px] font-mono text-[#4a4a4d]">
                {((t.count / total) * 100).toFixed(0)}%
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* Model usage */}
      <section>
        <p className="text-[12px] font-medium text-[#6e6e72] uppercase tracking-[0.08em] mb-5">Model Usage</p>
        <div className="space-y-5">
          {models.map(([name, d]) => (
            <div key={name}>
              <div className="flex items-baseline justify-between mb-2">
                <span className="text-[14px] font-mono text-[#b4b4b7]">{name}</span>
                <div className="flex items-baseline gap-4">
                  <span className="text-[14px] font-mono text-[#8b8b8e]">{d.count}</span>
                  <span className="text-[12px] font-mono text-[#5a5a5d]">${d.total_cost.toFixed(4)}</span>
                </div>
              </div>
              <div className="h-[4px] w-full bg-white/[0.05] rounded-full overflow-hidden">
                <div
                  className="h-full bg-white/[0.18] rounded-full"
                  style={{ width: `${(d.count / maxModelCount) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-[12px] text-[#5a5a5d] mb-1">{label}</p>
      <p className="text-[20px] font-semibold text-white font-mono tracking-tight">{value}</p>
    </div>
  );
}

function Onboarding() {
  return (
    <div className="max-w-lg pt-8">
      <h1 className="text-[22px] font-semibold text-white tracking-tight mb-3">Waiting for requests</h1>
      <p className="text-[14px] text-[#8b8b8e] leading-relaxed mb-10">
        Point your client to the proxy and set the model to <code className="font-mono text-[#b4b4b7]">uncommon-route/auto</code>.
      </p>
      <pre className="text-[12px] font-mono text-[#7a7a7d] leading-[1.7] bg-[#0c0c0e] border border-white/[0.06] rounded-lg p-5 overflow-x-auto">
{`from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8403/v1",
    api_key="your-upstream-key",
)
resp = client.chat.completions.create(
    model="uncommon-route/auto",
    messages=[{"role": "user", "content": "hello"}],
)`}
      </pre>
    </div>
  );
}
