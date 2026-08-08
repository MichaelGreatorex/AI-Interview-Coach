"use client";

import { useState } from "react";

import UploadView from "./UploadView";
import InterviewView from "./InterviewView";
import CompleteView from "./CompleteView";

import { ActiveInterview } from "../models/interview";
import { submitResponse } from "../api/responses";
import { deleteSession } from "../api/sessions";

type InterviewStage =
    | "upload"
    | "interview"
    | "complete";

export default function InterviewApp() {
    const [activeInterview, setActiveInterview] =
        useState<ActiveInterview | null>(null);

    const [stage, setStage] =
        useState<InterviewStage>("upload");

    const [isBusy, setIsBusy] = useState(false);

    switch (stage) {
        case "upload":
            return (
                <UploadView
                    onInterviewStarted={(interview) => {
                        setActiveInterview(interview);
                        setStage("interview");
                    }}
                />
            );

        case "interview":
            if (!activeInterview) {
                return null;
            }

            return (
                <InterviewView
                    question={activeInterview.currentQuestion}
                    onSubmitAnswer={async (answer) => {
                        const result = await submitResponse(
                            activeInterview.sessionId,
                            {
                                question_id:
                                    activeInterview.currentQuestion.id,
                                question_text:
                                    activeInterview.currentQuestion.text,
                                answer,
                            },
                        );

                        if (result.interview_complete) {
                            setStage("complete");
                            return;
                        }

                        if (!result.next_question) {
                            throw new Error(
                                "Interview response was accepted but no next question was provided.",
                            );
                        }

                        const nextQuestion = result.next_question;

                        setActiveInterview((previous) => {
                            if (!previous) {
                                return previous;
                            }

                            return {
                                ...previous,
                                currentQuestion:
                                    nextQuestion,
                            };
                        });
                    }}
                />
            );

        case "complete":
            if (!activeInterview) {
                return null;
            }

            return (
                <CompleteView
                    onEndSession={async () => {
                        if (isBusy) {
                            return;
                        }

                        setIsBusy(true);

                        try {
                            await deleteSession(
                                activeInterview.sessionId,
                            );

                            setActiveInterview(null);
                            setStage("upload");
                        } finally {
                            setIsBusy(false);
                        }
                    }}
                />
            );

        default:
            return null;
    }
}