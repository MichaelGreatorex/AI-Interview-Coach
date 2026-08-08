export interface InterviewQuestion {
    id: number;
    text: string;
}

export interface ActiveInterview {
    sessionId: string;
    currentQuestion: InterviewQuestion;
}

export type SubmitInterviewResponseResponse = {
    interview_complete: boolean;
    next_question: InterviewQuestion | null;
};