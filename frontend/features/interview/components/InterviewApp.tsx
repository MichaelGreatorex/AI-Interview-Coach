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
    const [stage, setStage] =
        useState<InterviewStage>("upload");

    const [interview, setInterview] =
        useState<ActiveInterview | null>(null);

    const [isBusy, setIsBusy] = useState(false);

    switch (stage) {
        case "upload":
            return (
                <UploadView
                    onInterviewStarted={(interview) => {
                        setInterview(interview);
                        setStage("interview");
                    }}
                />
            );

        case "interview":
            if (!interview) {
                return null;
            }

            return (
                <InterviewView
                    question={interview.currentQuestion}
                    onSubmitAnswer={async (answer) => {
                        if (!interview) return;
                        await submitResponse(interview.sessionId, {
                            question_id: interview.currentQuestion.id,
                            question_text: interview.currentQuestion.text,
                            answer,
                        });
                        setStage("complete");
                    }}
                />
            );

        case "complete":
            if (!interview) {
                return null;
            }

            return (
                <CompleteView
                    onEndSession={async () => {
                        if (isBusy) return;

                        setIsBusy(true);

                        try {
                            await deleteSession(interview.sessionId);

                            setInterview(null);
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