interface FeedbackCardProps {
  score: number;
  strengths: string[];
  weaknesses: string[];
  idealAnswer: string;
}

export default function FeedbackCard({
  score,
  strengths,
  weaknesses,
  idealAnswer,
}: FeedbackCardProps) {
  const color =
    score >= 8
      ? "text-emerald-600"
      : score >= 5
        ? "text-amber-500"
        : "text-red-500";

  return (
    <div className="rounded-2xl border border-zinc-200 bg-zinc-50 p-5 space-y-4 text-sm">
      <div className="flex items-center gap-3">
        <span className={`text-2xl font-bold ${color}`}>{score}/10</span>
        <span className="text-zinc-500">AI feedback</span>
      </div>

      {strengths.length > 0 && (
        <div>
          <p className="font-semibold text-emerald-700 mb-1">✅ Strengths</p>
          <ul className="list-disc list-inside space-y-1 text-zinc-700">
            {strengths.map((s, i) => (
              <li key={`strength-${i}`}>{s}</li>
            ))}
          </ul>
        </div>
      )}

      {weaknesses.length > 0 && (
        <div>
          <p className="font-semibold text-amber-600 mb-1">⚠️ Areas to improve</p>
          <ul className="list-disc list-inside space-y-1 text-zinc-700">
            {weaknesses.map((w, i) => (
              <li key={`weakness-${i}`}>{w}</li>
            ))}
          </ul>
        </div>
      )}

      <div>
        <p className="font-semibold text-zinc-700 mb-1">💡 Ideal answer</p>
        <p className="text-zinc-600 leading-6 whitespace-pre-wrap">{idealAnswer}</p>
      </div>
    </div>
  );
}
