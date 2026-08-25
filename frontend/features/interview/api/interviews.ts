import type { ActiveInterview } from "../models/interview";
import { API_BASE_URL } from "../../../client";

export async function startInterview(
    sessionId: string,
): Promise<ActiveInterview> {
    const response = await fetch(
        `${API_BASE_URL}/interviews/${sessionId}/start`,
        {
            method: "POST",
        },
    );

    if (!response.ok) {
        throw new Error(
            `Failed to start interview (HTTP ${response.status})`,
        );
    }

    const data = await response.json();

    return {
        sessionId: data.session_id,
        currentQuestion: data.question,
    };
}