export default function PipelineTrace({ trace }: { trace: string[] }) {
  if (!trace || !trace.length) return null;
  return (
    <div className="border border-gray-800 rounded p-4 bg-gray-900">
      <h3 className="text-sm text-gray-400 uppercase tracking-wide mb-3">Routing trace</h3>
      <ol className="space-y-2">
        {trace.map((step, i) => (
          <li key={i} className="flex items-center gap-2 text-sm">
            <span className="w-6 h-6 rounded-full bg-emerald-900 text-emerald-300 flex items-center justify-center text-xs">
              {i + 1}
            </span>
            <span className="font-mono">{step}</span>
          </li>
        ))}
      </ol>
    </div>
  );
}
