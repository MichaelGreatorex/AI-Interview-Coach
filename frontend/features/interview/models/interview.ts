export interface InterviewQuestion {
    id: number;
    text: string;
}

export interface InterviewDocument {
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
}

export interface ProcessedInterview {
    sessionId: string;
    documents: InterviewDocument[];
}

export interface ActiveInterview {
    sessionId: string;
    currentQuestion: InterviewQuestion;
}

export type SubmitInterviewResponseResponse = {
    interview_complete: boolean;
    next_question: InterviewQuestion | null;
};