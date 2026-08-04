"use client";

import { useState } from "react";

import { interviewQuestions, type InterviewStage } from "../types/interview";

export function useInterview() {
    const [stage, setStage] = useState<InterviewStage>("upload");
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [answers, setAnswers] = useState<string[]>([]);

    function startInterview() {
        setStage("interview");
    }

    function submitAnswer(answer: string) {
        setAnswers((previous) => [...previous, answer]);

        if (currentQuestionIndex === interviewQuestions.length - 1) {
        setStage("complete");
        return;
        }

        setCurrentQuestionIndex((previous) => previous + 1);
    }

    function endSession() {
        setStage("upload");
        setCurrentQuestionIndex(0);
        setAnswers([]);
    }

    const currentQuestion = interviewQuestions[currentQuestionIndex];

    const questionNumber = currentQuestionIndex + 1;

    const totalQuestions = interviewQuestions.length;

    const isLastQuestion = currentQuestionIndex === interviewQuestions.length - 1;
    return {
        stage,
        currentQuestionIndex,
        currentQuestion,
        questionNumber,
        totalQuestions,
        isLastQuestion,
        answers,
        startInterview,
        submitAnswer,
        endSession,
    };
}