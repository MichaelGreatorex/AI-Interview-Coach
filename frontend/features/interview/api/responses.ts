import { API_BASE_URL } from "../../../client";
import { SubmitInterviewResponseResponse } from "../models/interview";

const SUBMIT_RESPONSE_TIMEOUT_MS = 10_000;

export interface SubmitInterviewResponseRequest {
    question_id: number;
    question_text: string;
    answer: string;
}

// Submit an interview response and return the backend's
// decision about the next stage of the interview.
export async function submitResponse(
    sessionId: string,
    request: SubmitInterviewResponseRequest,
): Promise<SubmitInterviewResponseResponse> {
    const abortController = new AbortController();

    const timeout = setTimeout(
        () => abortController.abort(),
        SUBMIT_RESPONSE_TIMEOUT_MS,
    );

    let response: Response;

    try {
        response = await fetch(
            `${API_BASE_URL}/sessions/${sessionId}/responses`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(request),
                signal: abortController.signal,
            },
        );
    } catch (error) {
        if (
            error instanceof DOMException &&
            error.name === "AbortError"
        ) {
            throw new Error(
                "Submitting response timed out. Please try again.",
            );
        }

        throw new Error(
            "Could not reach the backend. Check that the API is running.",
        );
    } finally {
        clearTimeout(timeout);
    }

    if (!response.ok) {
        throw new Error(
            `Failed to submit interview response (HTTP ${response.status})`,
        );
    }

    return response.json() as Promise<SubmitInterviewResponseResponse>;
}