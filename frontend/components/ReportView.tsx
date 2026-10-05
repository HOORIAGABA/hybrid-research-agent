export default function ReportView({ report }: { report: string }) {
  if (!report) return null;
  return (
    <div className="border border-gray-800 rounded p-4 bg-gray-900">
      <h3 className="text-sm text-gray-400 uppercase tracking-wide mb-3">Report</h3>
      <p className="whitespace-pre-wrap text-gray-200 leading-relaxed">{report}</p>
    </div>
  );
}
