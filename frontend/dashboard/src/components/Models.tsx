import { useState } from "react";
import type { Mapping } from "../api";

type Filter = "all" | "available" | "not_found";

interface Props {
  mapping: Mapping | null;
}

export default function Models({ mapping }: Props) {
  const [filter, setFilter] = useState<Filter>("all");

  const discovered = mapping?.discovered ?? false;
  const upCount = mapping?.upstream_model_count ?? 0;
  const mapped = mapping?.mappings?.filter((r) => r.mapped).length ?? 0;
  const unresolved = mapping?.unresolved?.length ?? 0;
  const rows = mapping?.mappings ?? [];

  const filtered = rows.filter((r) => {
    if (filter === "available") return r.available === true;
    if (filter === "not_found") return r.available === false;
    return true;
  });

  return (
    <div>
      {/* Header */}
      <div className="flex items-baseline justify-between mb-10">
        <h1 className="text-[18px] font-semibold text-white tracking-tight">Models</h1>
        <div className="flex items-baseline gap-3 text-[13px] font-mono">
          <span className="text-[#8b8b8e]">{upCount} upstream</span>
          <span className="text-[#3a3a3d]">/</span>
          <span className="text-[#8b8b8e]">{mapped} mapped</span>
          <span className="text-[#3a3a3d]">/</span>
          <span className={unresolved > 0 ? "text-red-400/80" : "text-[#8b8b8e]"}>{unresolved} unresolved</span>
          {mapping?.provider && (
            <>
              <span className="text-[#3a3a3d]">/</span>
              <span className="text-[#6e6e72]">{mapping.provider}{mapping.is_gateway ? " (gw)" : ""}</span>
            </>
          )}
        </div>
      </div>

      {!discovered && (
        <div className="mb-8 border border-white/[0.07] rounded-lg p-5 bg-white/[0.02]">
          <p className="text-[14px] text-[#8b8b8e]">Discovery pending. Check upstream configuration.</p>
        </div>
      )}

      {/* Filter */}
      <div className="flex items-center gap-1 mb-5">
        {(["all", "available", "not_found"] as Filter[]).map((f) => {
          const count = f === "all" ? rows.length : f === "available" ? rows.filter(r => r.available).length : rows.filter(r => r.available === false).length;
          return (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 text-[13px] rounded-lg transition-colors ${
                filter === f
                  ? "text-white bg-white/[0.08] font-medium"
                  : "text-[#6e6e72] hover:text-[#b4b4b7] hover:bg-white/[0.03]"
              }`}
            >
              {f === "all" ? "All" : f === "available" ? "Available" : "Not Found"}
              <span className="ml-1.5 font-mono text-[12px] text-[#5a5a5d]">{count}</span>
            </button>
          );
        })}
      </div>

      {/* Table */}
      <table className="w-full">
        <thead>
          <tr className="border-b border-white/[0.07]">
            <th className="text-left text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2">Internal Name</th>
            <th className="text-left text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2">Resolved (Upstream)</th>
            <th className="text-right text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2 w-24">Status</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((r) => (
            <tr
              key={r.internal}
              className={`border-b border-white/[0.04] transition-colors ${
                r.available === false ? "bg-red-500/[0.04] hover:bg-red-500/[0.07]" : "hover:bg-white/[0.02]"
              }`}
            >
              <td className="font-mono text-[12px] text-[#b4b4b7] py-3">{r.internal}</td>
              <td className={`font-mono text-[12px] py-3 ${r.mapped ? "text-white/90" : "text-[#5a5a5d]"}`}>
                {r.resolved}
              </td>
              <td className="text-right py-3">
                {r.available === true && <span className="text-[11px] font-mono text-emerald-400/70">available</span>}
                {r.available === false && <span className="text-[11px] font-mono text-red-400/70">not found</span>}
                {r.available === null && <span className="text-[11px] font-mono text-[#4a4a4d]">unknown</span>}
              </td>
            </tr>
          ))}
          {filtered.length === 0 && (
            <tr><td colSpan={3} className="py-10 text-center text-[13px] text-[#4a4a4d]">No models match filter</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
