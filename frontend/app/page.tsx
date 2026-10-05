"use client";
import { useState } from "react";
import QueryInput from "@/components/QueryInput";
import PipelineTrace from "@/components/PipelineTrace";
import ReportView from "@/components/ReportView";
import SourceCard from "@/components/SourceCard";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);

  async function runSearch() {
    if (!query.trim()) return;
    setLoading(true);
    setData(null);
    try {
      const res = await fetch(`${API}/research`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const json = await res.json();
      setData(json);
    } catch (e) {
      setData({ error: String(e) });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Hybrid Research Agent</h1>
      <p className="text-gray-400">
        Multi-agent system: internal RAG (via MCP) + live web search, with runtime routing.
      </p>

      <QueryInput value={query} onChange={setQuery} onSubmit={runSearch} disabled={loading} />

      {data?.trace && <PipelineTrace trace={data.trace} />}

      {data?.routing_decision && (
        <p className="text-sm text-gray-400">
          Routing decision: <span className="font-mono text-emerald-400">{data.routing_decision}</span>
        </p>
      )}

      {data?.report && <ReportView report={data.report} />}

      {data?.internal_chunks?.length > 0 && (
        <div>
          <h3 className="text-sm text-gray-400 uppercase tracking-wide mb-2">Internal sources</h3>
          <div className="space-y-2">
            {data.internal_chunks.map((c: any, i: number) => (
              <SourceCard key={i} source={c.source} page={c.page} content={c.content} kind="internal" />
            ))}
          </div>
        </div>
      )}

      {data?.web_results?.length > 0 && (
        <div>
          <h3 className="text-sm text-gray-400 uppercase tracking-wide mb-2">Web sources</h3>
          <div className="space-y-2">
            {data.web_results.map((r: any, i: number) => (
              <SourceCard key={i} source={r.url} content={r.content} kind="web" />
            ))}
          </div>
        </div>
      )}

      {data?.error && (
        <div className="border border-red-800 bg-red-950 rounded p-4 text-red-300">
          {data.error}
        </div>
      )}
    </div>
  );
}
