import { useState } from "react";
import { setSpendLimit, clearSpendLimit, type Spend } from "../api";

const WINDOWS = ["per_request", "hourly", "daily", "session"];

interface Props {
  spend: Spend | null;
  onRefresh: () => void;
}

export default function SpendPanel({ spend, onRefresh }: Props) {
  const [window, setWindow] = useState("hourly");
  const [amount, setAmount] = useState("5.00");
  const [busy, setBusy] = useState(false);

  const limits = spend?.limits ?? {};
  const spent = spend?.spent ?? {};
  const remaining = spend?.remaining ?? {};
  const calls = spend?.calls ?? 0;

  const activeWindows = WINDOWS.filter((w) => limits[w] != null);

  async function handleSet() {
    const val = parseFloat(amount);
    if (isNaN(val)) return;
    setBusy(true);
    await setSpendLimit(window, val);
    onRefresh();
    setBusy(false);
  }

  async function handleClear() {
    setBusy(true);
    await clearSpendLimit(window);
    onRefresh();
    setBusy(false);
  }

  return (
    <div>
      <div className="flex items-baseline gap-3 mb-10">
        <h1 className="text-[18px] font-semibold text-white tracking-tight">Spend</h1>
        <span className="text-[13px] font-mono text-[#6e6e72]">{calls} calls</span>
      </div>

      {/* Set limit form */}
      <div className="flex items-end gap-4 mb-12 pb-10 border-b border-white/[0.07]">
        <div>
          <label className="block text-[12px] font-medium text-[#6e6e72] mb-2">Window</label>
          <select
            value={window}
            onChange={(e) => setWindow(e.target.value)}
            className="bg-transparent border border-white/[0.10] text-[#b4b4b7] rounded-lg px-3 py-2 text-[13px] font-mono"
          >
            {WINDOWS.map((w) => <option key={w} value={w} className="bg-[#111113]">{w}</option>)}
          </select>
        </div>
        <div>
          <label className="block text-[12px] font-medium text-[#6e6e72] mb-2">Amount ($)</label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            min={0}
            step={0.5}
            className="bg-transparent border border-white/[0.10] text-[#b4b4b7] rounded-lg px-3 py-2 text-[13px] font-mono w-28"
          />
        </div>
        <button
          disabled={busy}
          onClick={handleSet}
          className="bg-white/90 text-[#111113] px-4 py-2 rounded-lg text-[13px] font-medium hover:bg-white transition-colors disabled:opacity-40"
        >
          Set
        </button>
        <button
          disabled={busy}
          onClick={handleClear}
          className="border border-white/[0.10] text-[#8b8b8e] px-4 py-2 rounded-lg text-[13px] font-medium hover:text-white hover:border-white/20 transition-colors disabled:opacity-40"
        >
          Clear
        </button>
      </div>

      {/* Limits table */}
      <p className="text-[12px] font-medium text-[#6e6e72] uppercase tracking-[0.08em] mb-5">Current Limits</p>
      <table className="w-full">
        <thead>
          <tr className="border-b border-white/[0.07]">
            <th className="text-left text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2">Window</th>
            <th className="text-right text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2 w-24">Limit</th>
            <th className="text-right text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2 w-24">Spent</th>
            <th className="text-right text-[11px] font-medium text-[#5a5a5d] uppercase tracking-[0.06em] py-2 w-28">Remaining</th>
          </tr>
        </thead>
        <tbody>
          {activeWindows.length > 0 ? activeWindows.map((w) => {
            const isLow = remaining[w] != null && remaining[w] < limits[w] * 0.2;
            return (
              <tr key={w} className="border-b border-white/[0.04] hover:bg-white/[0.02] transition-colors">
                <td className="font-mono text-[12px] text-[#b4b4b7] py-3">{w}</td>
                <td className="text-right font-mono text-[12px] text-[#b4b4b7] py-3">${limits[w].toFixed(2)}</td>
                <td className="text-right font-mono text-[12px] text-[#6e6e72] py-3">${(spent[w] ?? 0).toFixed(4)}</td>
                <td className={`text-right font-mono text-[12px] py-3 ${isLow ? "text-red-400/80" : "text-emerald-400/80"}`}>
                  {remaining[w] != null ? `$${remaining[w].toFixed(4)}` : "—"}
                </td>
              </tr>
            );
          }) : (
            <tr><td colSpan={4} className="py-10 text-center text-[13px] text-[#4a4a4d]">No limits set</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
