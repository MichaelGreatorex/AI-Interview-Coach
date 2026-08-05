import { useState } from "react";

import FileUploadCard from "./FileUploadCard";
import { ActiveInterview } from "../models/interview";
import { startInterview } from "../api/interviews";

type UploadViewProps = {
    onInterviewStarted: (interview: ActiveInterview) => void;
};

export default function UploadView({
    onInterviewStarted,
}: UploadViewProps) {
    const [cv, setCv] = useState<File | null>(null);
    const [jobDescription, setJobDescription] = useState<File | null>(null);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    
    const canStart = cv !== null && jobDescription !== null;
    const [isBusy, setIsBusy] = useState(false);

    const handleStartInterview = async () => {
        if (!cv || !jobDescription || isBusy) {
            return;
        }

        setErrorMessage(null);
        setIsBusy(true);
        
        try {
            const interview = await startInterview(cv, jobDescription);
            onInterviewStarted(interview);
        } catch (error) {
            console.error(error);
            setErrorMessage(
                error instanceof Error
                    ? error.message
                    : "Could not start interview. Please try again.",
            );
        } finally {
            setIsBusy(false);
        }
    };

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
                disabled={isBusy}
            />

            <FileUploadCard
                title="Job Description"
                description="Choose the job description you're applying for."
                file={jobDescription}
                accept=".pdf,.doc,.docx"
                onFileSelected={setJobDescription}
                disabled={isBusy}
            />
            </div>

            <div className="mt-10 text-center">
            <button
                disabled={!canStart || isBusy}
                onClick={handleStartInterview}
                className="rounded-xl bg-blue-600 px-8 py-4 font-semibold text-white disabled:cursor-not-allowed disabled:bg-foreground/10 disabled:text-foreground/50"
            >
                Start Interview
            </button>
            {isBusy ? (
                <p className="mt-4 text-sm text-foreground/70">
                {isBusy ? "Preparing your interview, please wait..." : "Start Interview"}
                </p>
            ) : null}
            {errorMessage ? (
                <p className="mt-4 text-sm text-red-600">{errorMessage}</p>
            ) : null}
            </div>
        </div>
        </main>
    );
}