export default function QueryInput({
  value, onChange, onSubmit, disabled,
}: { value: string; onChange: (v: string) => void; onSubmit: () => void; disabled?: boolean }) {
  return (
    <div className="flex gap-2">
      <input
        className="flex-1 bg-gray-900 border border-gray-700 rounded px-3 py-2"
        placeholder="Ask a question that might need internal + web sources..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && onSubmit()}
      />
      <button
        className="bg-emerald-600 hover:bg-emerald-500 disabled:bg-gray-700 px-4 py-2 rounded font-medium"
        onClick={onSubmit}
        disabled={disabled}
      >
        {disabled ? "Running..." : "Research"}
      </button>
    </div>
  );
}
