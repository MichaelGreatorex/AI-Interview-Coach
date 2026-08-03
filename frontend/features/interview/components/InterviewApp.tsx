"use client";

import { useInterview } from "../hooks/useInterview";

import UploadView from "./UploadView";
import InterviewView from "./InterviewView";
import CompleteView from "./CompleteView";

export default function InterviewApp() {

    const interview = useInterview(); 

    switch (interview.stage) {
        case "upload":
            return <UploadView onStartInterview={interview.startInterview} />;

        case "interview":
            return (
                <InterviewView
                    questionNumber={interview.questionNumber}
                    totalQuestions={interview.totalQuestions}
                    question={interview.currentQuestion}
                    onSubmitAnswer={interview.submitAnswer}
                />
                );

        case "complete":
            return (
                <CompleteView
                onEndSession={interview.endSession}
                />
            );

    default:
        return null;
    }
}