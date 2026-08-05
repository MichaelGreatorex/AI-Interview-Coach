"use client";

import { useState } from "react";

import UploadView from "./UploadView";
import InterviewView from "./InterviewView";
import CompleteView from "./CompleteView";

import { ActiveInterview } from "../models/interview";

type InterviewStage =
    | "upload"
    | "interview"
    | "complete";

export default function InterviewApp() {
    const [stage, setStage] =
        useState<InterviewStage>("upload");

    const [interview, setInterview] =
        useState<ActiveInterview | null>(null);

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
                />
            );

        case "complete":
            return (
                <CompleteView
                    onEndSession={() => setStage("upload")}
                />
            );

        default:
            return null;
    }
}