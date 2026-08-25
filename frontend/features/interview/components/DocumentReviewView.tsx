"use client";

import { useState } from "react";

import type {
    ActiveInterview,
    InterviewDocument,
    ProcessedInterview,
} from "../models/interview";

import { updateDocumentText } from "../api/documents";
import { startInterview } from "../api/interviews";

type DocumentReviewViewProps = {
    interview: ProcessedInterview;
    onInterviewStarted: (interview: ActiveInterview) => void;
};

export default function DocumentReviewView({
    interview,
    onInterviewStarted,
}: DocumentReviewViewProps) {
    const [documents, setDocuments] =
        useState<InterviewDocument[]>(interview.documents);

    const [isSaving, setIsSaving] = useState(false);
    const [isStarting, setIsStarting] = useState(false);
    const [errorMessage, setErrorMessage] =
        useState<string | null>(null);

    const updateLocalText = (
        documentId: number,
        extractedText: string,
    ) => {
        setDocuments((previous) =>
            previous.map((document) =>
                document.id === documentId
                    ? {
                        ...document,
                        extracted_text: extractedText,
                    }
                    : document,
            ),
        );
    };

    const saveDocuments = async () => {
        setErrorMessage(null);
        setIsSaving(true);

        try {
            const updatedDocuments = await Promise.all(
                documents.map((document) =>
                    updateDocumentText(
                        interview.sessionId,
                        document.id,
                        document.extracted_text,
                    ),
                ),
            );

            setDocuments(updatedDocuments);
        } catch (error) {
            console.error(error);

            setErrorMessage(
                error instanceof Error
                    ? error.message
                    : "Could not save the document changes.",
            );

            throw error;
        } finally {
            setIsSaving(false);
        }
    };

    const handleStartInterview = async () => {
        if (isSaving || isStarting) {
            return;
        }

        setErrorMessage(null);
        setIsStarting(true);

        try {
            await saveDocuments();

            const activeInterview = await startInterview(
                interview.sessionId,
            );

            onInterviewStarted(activeInterview);
        } catch (error) {
            console.error(error);

            setErrorMessage(
                error instanceof Error
                    ? error.message
                    : "Could not start the interview.",
            );
        } finally {
            setIsStarting(false);
        }
    };

    const cv = documents.find(
        (document) => document.document_type === "cv",
    );

    const jobDescription = documents.find(
        (document) =>
            document.document_type === "job_description",
    );

    return (
        <main className="min-h-screen bg-background px-6 py-12">
            <div className="mx-auto max-w-7xl">
                <header className="mb-10 text-center">
                    <h1 className="text-4xl font-bold">
                        Review Your Documents
                    </h1>

                    <p className="mt-4 text-lg text-foreground/70">
                        Review and correct the extracted text before
                        starting your interview.
                    </p>
                </header>

                <div className="grid gap-6 lg:grid-cols-2">
                    {cv ? (
                        <section className="flex flex-col">
                            <div className="mb-3">
                                <h2 className="text-2xl font-semibold">
                                    Curriculum Vitae
                                </h2>

                                <p className="mt-1 text-sm text-foreground/60">
                                    {cv.original_filename}
                                </p>
                            </div>

                            <textarea
                                value={cv.extracted_text}
                                onChange={(event) =>
                                    updateLocalText(
                                        cv.id,
                                        event.target.value,
                                    )
                                }
                                disabled={isSaving || isStarting}
                                className="
                                    min-h-[32rem]
                                    w-full
                                    flex-1
                                    resize-y
                                    rounded-2xl
                                    border
                                    border-black/10
                                    bg-background
                                    p-5
                                    font-mono
                                    text-sm
                                    outline-none
                                    transition
                                    focus:ring-4
                                    focus:ring-blue-300
                                    dark:border-white/10
                                    dark:focus:ring-blue-800
                                "
                            />
                        </section>
                    ) : null}

                    {jobDescription ? (
                        <section className="flex flex-col">
                            <div className="mb-3">
                                <h2 className="text-2xl font-semibold">
                                    Job Description
                                </h2>

                                <p className="mt-1 text-sm text-foreground/60">
                                    {jobDescription.original_filename}
                                </p>
                            </div>

                            <textarea
                                value={jobDescription.extracted_text}
                                onChange={(event) =>
                                    updateLocalText(
                                        jobDescription.id,
                                        event.target.value,
                                    )
                                }
                                disabled={isSaving || isStarting}
                                className="
                                    min-h-[32rem]
                                    w-full
                                    flex-1
                                    resize-y
                                    rounded-2xl
                                    border
                                    border-black/10
                                    bg-background
                                    p-5
                                    font-mono
                                    text-sm
                                    outline-none
                                    transition
                                    focus:ring-4
                                    focus:ring-blue-300
                                    dark:border-white/10
                                    dark:focus:ring-blue-800
                                "
                            />
                        </section>
                    ) : null}
                </div>

                {errorMessage ? (
                    <p className="mt-6 text-center text-sm text-red-600">
                        {errorMessage}
                    </p>
                ) : null}

                <div className="mt-10 flex justify-center">
                    <button
                        onClick={handleStartInterview}
                        disabled={isSaving || isStarting}
                        className="
                            rounded-xl
                            bg-blue-600
                            px-8
                            py-4
                            font-semibold
                            text-white
                            transition
                            hover:bg-blue-700
                            disabled:cursor-not-allowed
                            disabled:bg-slate-400
                        "
                    >
                        {isSaving
                            ? "Saving Documents..."
                            : isStarting
                            ? "Starting Interview..."
                            : "Start Interview"}
                    </button>
                </div>
            </div>
        </main>
    );
}