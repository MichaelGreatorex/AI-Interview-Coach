import type { ActiveInterview } from "../models/interview";
import { API_BASE_URL } from "../../../client";

const START_INTERVIEW_TIMEOUT_MS = 15_000;

type StartInterviewResponse = {
    session_id: string;
    question: {
        id: number;
        text: string;
    };
};

export async function startInterview(
    cv: File,
    jobDescription: File,
): Promise<ActiveInterview> {
    const formData = new FormData();

    formData.append("cv", cv);
    formData.append("job_description", jobDescription);

    const abortController = new AbortController();
    const timeout = setTimeout(
        () => abortController.abort(),
        START_INTERVIEW_TIMEOUT_MS,
    );

    let response: Response;

    try {
        response = await fetch(`${API_BASE_URL}/interviews`, {
            method: "POST",
            body: formData,
            signal: abortController.signal,
        });
    } catch (error) {
        if (error instanceof DOMException && error.name === "AbortError") {
            throw new Error("Starting the interview timed out. Please try again.");
        }

        throw new Error("Could not reach the backend. Check that the API is running.");
    } finally {
        clearTimeout(timeout);
    }

    if (!response.ok) {
        throw new Error(`Failed to start interview (HTTP ${response.status})`);
    }

    const data: StartInterviewResponse = await response.json();

    return {
        sessionId: data.session_id,
        currentQuestion: data.question,
    };
}