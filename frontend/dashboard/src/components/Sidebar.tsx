interface Props {
  current: string;
  onChange: (page: string) => void;
  upstream: string;
  isUp: boolean;
  version: string;
  feedbackPending: number;
}

const NAV = [
  { id: "overview", label: "Overview" },
  { id: "routing", label: "Routing" },
  { id: "config", label: "Config" },
  { id: "models", label: "Models" },
  { id: "sessions", label: "Sessions" },
  { id: "spend", label: "Spend" },
  { id: "feedback", label: "Feedback" },
];

export default function Sidebar({ current, onChange, upstream, isUp, version, feedbackPending }: Props) {
  return (
    <aside className="fixed top-0 left-0 h-full w-[220px] border-r border-white/[0.08] bg-[linear-gradient(180deg,_#141518_0%,_#101114_100%)] flex flex-col z-50">
      {/* Logo */}
      <div className="px-5 h-14 flex items-center border-b border-white/[0.08]">
        <span className="text-[15px] font-semibold text-[#f1f1f3] tracking-tight">UncommonRoute</span>
      </div>

      {/* Nav */}
      <nav className="flex-1 py-4 px-3">
        {NAV.map((item) => (
          <button
            key={item.id}
            onClick={() => onChange(item.id)}
            className={`w-full text-left px-3 py-2 rounded-lg text-[14px] transition-colors flex items-center justify-between mb-0.5 ${
              current === item.id
                ? "text-[#f1f1f3] bg-[#1b1d21] font-medium"
                : "text-[#94969d] hover:text-[#dedfe3] hover:bg-[#17191d]"
            }`}
          >
            {item.label}
            {item.id === "feedback" && feedbackPending > 0 && (
              <span className="text-[11px] font-mono font-semibold bg-blue-500/80 text-white rounded-full h-5 min-w-5 flex items-center justify-center px-1.5">
                {feedbackPending}
              </span>
            )}
          </button>
        ))}
      </nav>

      {/* Footer */}
      <div className="px-5 py-4 border-t border-white/[0.08]">
        <div className="flex items-center gap-2 text-[12px] text-[#6c6f76]">
          <div className={`h-[7px] w-[7px] rounded-full flex-shrink-0 ${isUp ? "bg-emerald-400/80" : "bg-[#5a5a5d]"}`} />
          <span className="truncate">{upstream || "No upstream"}</span>
        </div>
        <div className="text-[11px] font-mono text-[#4d5057] mt-1.5">v{version}</div>
      </div>
    </aside>
  );
}
