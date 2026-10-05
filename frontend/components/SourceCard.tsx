export default function SourceCard({ source, page, content, kind }: {
  source: string; page?: number; content: string; kind: "internal" | "web";
}) {
  const color = kind === "internal" ? "bg-blue-900 text-blue-200" : "bg-purple-900 text-purple-200";
  return (
    <div className="border border-gray-800 rounded p-3 bg-gray-900">
      <div className="flex items-center gap-2 text-xs mb-2">
        <span className={`px-2 py-0.5 rounded ${color}`}>{kind}</span>
        <span className="text-gray-400">{source}{page ? ` p.${page}` : ""}</span>
      </div>
      <p className="text-gray-300 text-sm">{content.slice(0, 200)}...</p>
    </div>
  );
}
