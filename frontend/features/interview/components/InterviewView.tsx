"use client";

import { useState } from "react";
import { InterviewQuestion } from "../models/interview";

type InterviewViewProps = {
    question: InterviewQuestion;
};

export default function InterviewView({
    question,
}: InterviewViewProps) {

    const [answer, setAnswer] = useState("");

    return (
        <main className="min-h-screen bg-background px-6 py-12">
        <div className="mx-auto max-w-3xl">
            <header className="mb-10">

            <h1 className="mt-4 text-4xl font-bold">
                {question.text}
            </h1>
            </header>

            <section>
            <textarea
                value={answer}
                onChange={(event) => setAnswer(event.target.value)}
                placeholder="Type your answer here..."
                className="
                min-h-48
                w-full
                rounded-2xl
                border
                border-black/10
                bg-background
                p-5
                text-base
                outline-none
                transition
                focus:ring-4
                focus:ring-blue-300
                dark:border-white/10
                dark:focus:ring-blue-800
                "
            />

            <div className="mt-6 flex justify-end">
                <button
                onClick={() => {
                    // Handle answer submission
                }}
                disabled={!answer.trim()}
                className="
                    rounded-xl
                    bg-blue-600
                    px-6
                    py-3
                    font-semibold
                    text-white
                    transition
                    hover:bg-blue-700
                    disabled:cursor-not-allowed
                    disabled:bg-slate-400
                "
                >
                Submit Answer
                </button>
            </div>
            </section>
        </div>
        </main>
    );
}