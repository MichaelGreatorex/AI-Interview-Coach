import { useState } from "react";

import FileUploadCard from "./FileUploadCard";

export default function UploadView() {
  const [cv, setCv] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState<File | null>(null);

  const canStart = cv !== null && jobDescription !== null;

  return (
    <main className="min-h-screen bg-background px-6 py-12">
      <div className="mx-auto max-w-3xl">
        <header className="mb-10 text-center">
          <h1 className="text-5xl font-bold">
            AI Interview Coach
          </h1>

          <p className="mt-4 text-lg text-foreground/70">
            Upload your CV and job description to begin your mock interview.
          </p>
        </header>

        <div className="space-y-6">
          <FileUploadCard
            title="Curriculum Vitae"
            description="Choose the CV you'd like to interview from."
            file={cv}
            accept=".pdf,.doc,.docx"
            onFileSelected={setCv}
          />

          <FileUploadCard
            title="Job Description"
            description="Choose the job description you're applying for."
            file={jobDescription}
            accept=".pdf,.doc,.docx"
            onFileSelected={setJobDescription}
          />
        </div>

        <div className="mt-10 text-center">
          <button
            disabled={!canStart}
            className="rounded-xl bg-blue-600 px-8 py-4 font-semibold text-white disabled:cursor-not-allowed disabled:bg-foreground/10 disabled:text-foreground/50"
          >
            Start Interview
          </button>
        </div>
      </div>
    </main>
  );
}