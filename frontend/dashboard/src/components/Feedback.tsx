import { useCallback, useEffect, useState } from "react";
import {
  fetchRecent,
  submitFeedback,
  type RecentRequest,
  type FeedbackResult,
} from "../api";

const TIER_LABEL: Record<string, string> = {
  SIMPLE: "text-emerald-300/80",
  MEDIUM: "text-sky-300/80",
  COMPLEX: "text-orange-300/80",
  REASONING: "text-violet-300/80",
};

function fmtTime(ts: number): string {
  return new Date(ts * 1000).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

export default function Feedback() {
  const [requests, setRequests] = useState<RecentRequest[]>([]);
  const [submitted, setSubmitted] = useState<Record<string, FeedbackResult>>({});
  const [busy, setBusy] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    const data = await fetchRecent();
    if (data) setRequests(data);
  }, []);

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, 5000);
    return () => clearInterval(id);
  }, [refresh]);

  async function handle(requestId: string, signal: "ok" | "weak" | "strong") {
    setBusy(requestId);
    const result = await submitFeedback(requestId, signal);
    if (result) setSubmitted((prev) => ({ ...prev, [requestId]: result }));
    setBusy(null);
  }

  const pendingCount = requests.filter((r) => r.feedback_pending && !submitted[r.request_id]).length;

  return (
    <div>
      <div className="flex items-baseline gap-3 mb-2">
        <h1 className="text-[18px] font-semibold text-white tracking-tight">Feedback</h1>
        {pendingCount > 0 && (
          <span className="text-[13px] font-mono text-blue-400/80">{pendingCount} awaiting</span>
        )}
      </div>
      <p className="text-[14px] text-[#6e6e72] mb-10">
        Rate routing decisions to improve the classifier. All training happens locally.
      </p>

      <table className="w-full">
        <thead>
          <tr className="border-b border-white/[0.07]">
            <th className="text-left text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2 w-20">Time</th>
            <th className="text-left text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2">Prompt</th>
            <th className="text-left text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2 w-24">Tier</th>
            <th className="text-left text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2">Model</th>
            <th className="text-right text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2 w-20">Cost</th>
            <th className="text-right text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2 w-[240px]"></th>
          </tr>
        </thead>
        <tbody>
          {requests.length === 0 ? (
            <tr><td colSpan={6} className="py-10 text-center text-[13px] text-[#4a4a4d]">No routed requests yet</td></tr>
          ) : (
            requests.map((r) => {
              const fb = submitted[r.request_id];
              const isPending = r.feedback_pending && !fb;
              const isBusy = busy === r.request_id;

              return (
                <tr key={r.request_id} className="border-b border-white/[0.04] hover:bg-white/[0.02] transition-colors">
                  <td className="text-[12px] font-mono text-[#5a5a5d] py-3.5">{fmtTime(r.timestamp)}</td>
                  <td className="py-3.5">
                    <div className="max-w-[300px] truncate text-[14px] text-[#b4b4b7]" title={r.prompt_preview}>
                      {r.prompt_preview || "—"}
                    </div>
                  </td>
                  <td className={`text-[12px] font-mono py-3.5 ${TIER_LABEL[r.tier] ?? "text-[#6e6e72]"}`}>
                    {r.tier}
                  </td>
                  <td className="font-mono text-[12px] text-[#6e6e72] py-3.5">{r.model}</td>
                  <td className="text-right font-mono text-[12px] text-[#6e6e72] py-3.5">${r.cost.toFixed(4)}</td>
                  <td className="text-right py-3.5">
                    {fb ? (
                      <span className={`text-[12px] font-mono ${fb.action === "updated" ? "text-sky-400/80" : "text-emerald-400/80"}`}>
                        {fb.action === "updated" ? `${fb.from_tier} → ${fb.to_tier}` : "confirmed"}
                      </span>
                    ) : !isPending ? (
                      <span className="text-[12px] font-mono text-[#3a3a3d]">expired</span>
                    ) : (
                      <div className="flex justify-end gap-2">
                        <button
                          disabled={isBusy}
                          onClick={() => handle(r.request_id, "strong")}
                          className="px-3.5 py-1.5 rounded-full text-[12px] font-medium border border-white/[0.10] text-[#8b8b8e] hover:text-white hover:border-white/[0.20] hover:bg-white/[0.04] transition-all disabled:opacity-30"
                        >
                          Cheaper
                        </button>
                        <button
                          disabled={isBusy}
                          onClick={() => handle(r.request_id, "ok")}
                          className="px-3.5 py-1.5 rounded-full text-[12px] font-medium bg-white/90 text-[#111113] hover:bg-white transition-all disabled:opacity-30"
                        >
                          Right
                        </button>
                        <button
                          disabled={isBusy}
                          onClick={() => handle(r.request_id, "weak")}
                          className="px-3.5 py-1.5 rounded-full text-[12px] font-medium border border-white/[0.10] text-[#8b8b8e] hover:text-white hover:border-white/[0.20] hover:bg-white/[0.04] transition-all disabled:opacity-30"
                        >
                          Stronger
                        </button>
                      </div>
                    )}
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
}
