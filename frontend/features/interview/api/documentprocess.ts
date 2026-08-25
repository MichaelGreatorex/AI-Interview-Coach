import type { ProcessedInterview } from "../models/interview";
import { API_BASE_URL } from "../../../client";

const PROCESS_DOCUMENTS_TIMEOUT_MS = 60_000;

type ProcessDocumentsResponse = {
    session_id: string;
    documents: {
        id: number;
        interview_session_id: number;
        document_type: "cv" | "job_description";
        original_filename: string;
        stored_filename: string;
        mime_type: string;
        file_size: number;
        extracted_text: string;
        created_at: string;
        updated_at: string;
    }[];
};

export async function processDocuments(
    cv: File,
    jobDescription: File,
): Promise<ProcessedInterview> {
    const formData = new FormData();

    formData.append("cv", cv);
    formData.append("job_description", jobDescription);

    const abortController = new AbortController();

    const timeout = setTimeout(
        () => abortController.abort(),
        PROCESS_DOCUMENTS_TIMEOUT_MS,
    );

    let response: Response;

    try {
        response = await fetch(`${API_BASE_URL}/interviews`, {
            method: "POST",
            body: formData,
            signal: abortController.signal,
        });
    } catch (error) {
        if (
            error instanceof DOMException &&
            error.name === "AbortError"
        ) {
            throw new Error(
                "Processing the documents timed out. Please try again.",
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
            `Failed to process documents (HTTP ${response.status})`,
        );
    }

    const data =
        (await response.json()) as ProcessDocumentsResponse;

    return {
        sessionId: data.session_id,
        documents: data.documents,
    };
}