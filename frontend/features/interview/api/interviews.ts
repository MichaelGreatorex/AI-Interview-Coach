import type { ActiveInterview } from "../models/interview";
import { API_BASE_URL } from "../../../client";

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

    const response = await fetch(`${API_BASE_URL}/interviews`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error("Failed to start interview");
    }

    const data: StartInterviewResponse = await response.json();

    return {
        sessionId: data.session_id,
        currentQuestion: data.question,
    };
}