"use client";

import { useState } from "react";
import { interviewQuestions } from "../types/interview";

import UploadView from "./UploadView";
import InterviewView from "./InterviewView";
import CompleteView from "./CompleteView";

export type InterviewStage =
  | "upload"
  | "interview"
  | "complete";

export default function InterviewApp() {
  const [stage, setStage] = useState<InterviewStage>("upload");

  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  const [answers, setAnswers] = useState<string[]>([]);

    function handleAnswerSubmitted(answer: string) {
    setAnswers((previous) => [...previous, answer]);

    if (currentQuestionIndex === interviewQuestions.length - 1) {
        setStage("complete");
        return;
    }

    setCurrentQuestionIndex((previous) => previous + 1);
    }

    function handleEndSession() {
  setStage("upload");
  setCurrentQuestionIndex(0);
  setAnswers([]);
}

  switch (stage) {
    case "upload":
      return <UploadView onStartInterview={() => setStage("interview")} />;

    case "interview":
      return (
        <InterviewView
            questionNumber={currentQuestionIndex + 1}
            totalQuestions={interviewQuestions.length}
            question={interviewQuestions[currentQuestionIndex]}
            onSubmitAnswer={handleAnswerSubmitted}
        />
        );

    case "complete":
        return (
            <CompleteView
            onEndSession={handleEndSession}
            />
        );

    default:
      return null;
  }
}