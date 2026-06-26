"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import CVUpload from "@/components/CVUpload";
import { uploadCV } from "@/lib/api";

export default function UploadPage() {
  const router = useRouter();
  const [cvFile, setCvFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = cvFile !== null && jobDescription.trim().length > 0;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!cvFile) return;
    setLoading(true);
    setError(null);
    try {
      const { session_id } = await uploadCV(cvFile, jobDescription.trim());
      router.push(`/interview/${session_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col flex-1">
      <header className="border-b border-zinc-200 bg-white">
        <div className="mx-auto max-w-5xl px-6 py-4 flex items-center gap-3">
          <Link
            href="/"
            className="text-sm text-zinc-500 hover:text-zinc-800 transition-colors"
          >
            ← Home
          </Link>
          <span className="text-zinc-300">/</span>
          <span className="text-sm font-medium">Upload</span>
        </div>
      </header>

      <main className="flex flex-1 items-start justify-center px-6 py-16">
        <div className="w-full max-w-xl space-y-8">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              Start your interview practice
            </h1>
            <p className="mt-2 text-zinc-500">
              Upload your CV and paste the job description to generate a
              personalised mock interview.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">
                Your CV <span className="text-zinc-400">(PDF)</span>
              </label>
              <CVUpload
                onFileSelected={setCvFile}
                selectedFile={cvFile}
              />
            </div>

            <div>
              <label
                htmlFor="jd"
                className="block text-sm font-medium mb-2"
              >
                Job description
              </label>
              <textarea
                id="jd"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the full job description here…"
                rows={8}
                className="w-full rounded-xl border border-zinc-300 bg-white px-4 py-3 text-sm leading-6 placeholder:text-zinc-400 focus:outline-none focus:ring-2 focus:ring-zinc-400 resize-none"
              />
            </div>

            {error && (
              <p className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={!canSubmit || loading}
              className="w-full rounded-full bg-zinc-900 py-3 text-sm font-semibold text-white hover:bg-zinc-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Uploading…" : "Start interview →"}
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
