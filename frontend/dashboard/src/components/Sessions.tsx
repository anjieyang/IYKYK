import type { Session } from "../api";

const TIER_LABEL: Record<string, string> = {
  SIMPLE: "text-emerald-300/80",
  MEDIUM: "text-sky-300/80",
  COMPLEX: "text-orange-300/80",
  REASONING: "text-violet-300/80",
};

function fmtAge(s: number): string {
  if (s < 60) return `${s}s`;
  if (s < 3600) return `${Math.floor(s / 60)}m`;
  return `${Math.floor(s / 3600)}h`;
}

interface Props {
  data: { count: number; sessions: Session[] } | null;
}

export default function Sessions({ data }: Props) {
  const count = data?.count ?? 0;
  const sessions = data?.sessions ?? [];

  return (
    <div>
      <div className="flex items-baseline gap-3 mb-10">
        <h1 className="text-[18px] font-semibold text-white tracking-tight">Sessions</h1>
        <span className="text-[13px] font-mono text-[#6e6e72]">{count} active</span>
      </div>

      <table className="w-full">
        <thead>
          <tr className="border-b border-white/[0.07]">
            <th className="text-left text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2">ID</th>
            <th className="text-left text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2">Model</th>
            <th className="text-left text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2 w-24">Tier</th>
            <th className="text-right text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2 w-20">Requests</th>
            <th className="text-right text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2 w-16">Age</th>
          </tr>
        </thead>
        <tbody>
          {sessions.map((s) => (
            <tr key={s.id} className="border-b border-white/[0.04] hover:bg-white/[0.02] transition-colors">
              <td className="font-mono text-[12px] text-[#b4b4b7] py-3">{s.id}</td>
              <td className="font-mono text-[12px] text-[#6e6e72] py-3">{s.model}</td>
              <td className={`font-mono text-[12px] py-3 ${TIER_LABEL[s.tier] ?? "text-[#6e6e72]"}`}>{s.tier}</td>
              <td className="text-right font-mono text-[12px] text-[#b4b4b7] py-3">{s.requests}</td>
              <td className="text-right font-mono text-[12px] text-[#6e6e72] py-3">{fmtAge(s.age_s)}</td>
            </tr>
          ))}
          {sessions.length === 0 && (
            <tr><td colSpan={5} className="py-10 text-center text-[13px] text-[#4a4a4d]">No active sessions</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
