export interface InterviewQuestion {
    id: number;
    text: string;
}

export interface ActiveInterview {
    sessionId: string;
    currentQuestion: InterviewQuestion;
}