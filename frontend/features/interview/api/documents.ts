import type { InterviewDocument } from "../models/interview";
import { API_BASE_URL } from "../../../client";

export interface UpdateDocumentTextRequest {
    extracted_text: string;
}

export async function updateDocumentText(
    sessionId: string,
    documentId: number,
    extractedText: string,
): Promise<InterviewDocument> {
    const response = await fetch(
        `${API_BASE_URL}/interviews/${sessionId}/documents/${documentId}`,
        {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                extracted_text: extractedText,
            }),
        },
    );

    if (!response.ok) {
        throw new Error(
            `Failed to update document (HTTP ${response.status})`,
        );
    }

    return response.json() as Promise<InterviewDocument>;
}