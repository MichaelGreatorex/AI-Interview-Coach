const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export interface UploadCVResponse {
  session_id: string;
  message: string;
}

export interface StartInterviewResponse {
  session_id: string;
  question: string;
  question_number: number;
  total_questions: number;
}

export interface AnswerResponse {
  feedback: {
    score: number;
    strengths: string[];
    weaknesses: string[];
    ideal_answer: string;
  };
  next_question: string | null;
  interview_complete: boolean;
}

export interface Session {
  session_id: string;
  status: string;
  cv_filename: string;
  job_description: string;
  answers: Array<{
    question: string;
    answer: string;
    score: number;
  }>;
}

async function request<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      ...options.headers,
    },
  });

  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(`API error ${res.status}: ${text}`);
  }

  return res.json() as Promise<T>;
}

export async function uploadCV(
  cvFile: File,
  jobDescription: string,
): Promise<UploadCVResponse> {
  const form = new FormData();
  form.append("cv", cvFile);
  form.append("job_description", jobDescription);
  return request<UploadCVResponse>("/cv/upload", {
    method: "POST",
    body: form,
  });
}

export async function startInterview(
  sessionId: string,
): Promise<StartInterviewResponse> {
  return request<StartInterviewResponse>("/interview/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId }),
  });
}

export async function submitAnswer(
  sessionId: string,
  answer: string,
): Promise<AnswerResponse> {
  return request<AnswerResponse>("/interview/answer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, answer }),
  });
}

export async function getSession(sessionId: string): Promise<Session> {
  return request<Session>(`/sessions/${encodeURIComponent(sessionId)}`);
}
