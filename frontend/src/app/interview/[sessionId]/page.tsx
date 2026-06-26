"use client";

import { useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import FeedbackCard from "@/components/FeedbackCard";
import { startInterview, submitAnswer } from "@/lib/api";
import type { AnswerResponse } from "@/lib/api";

interface Message {
  role: "interviewer" | "user" | "feedback";
  content: string;
  feedback?: AnswerResponse["feedback"];
}

type InterviewStatus = "loading" | "active" | "complete" | "error";

export default function InterviewPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [status, setStatus] = useState<InterviewStatus>("loading");
  const [submitting, setSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    async function init() {
      try {
        const res = await startInterview(sessionId);
        setMessages([{ role: "interviewer", content: res.question }]);
        setStatus("active");
      } catch (err) {
        setErrorMessage(
          err instanceof Error ? err.message : "Failed to start interview.",
        );
        setStatus("error");
      }
    }
    init();
  }, [sessionId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const answer = input.trim();
    if (!answer || submitting) return;

    setInput("");
    setSubmitting(true);
    setMessages((prev) => [...prev, { role: "user", content: answer }]);

    try {
      const res = await submitAnswer(sessionId, answer);

      setMessages((prev) => [
        ...prev,
        { role: "feedback", content: "", feedback: res.feedback },
      ]);

      if (res.interview_complete) {
        setStatus("complete");
      } else if (res.next_question) {
        setMessages((prev) => [
          ...prev,
          { role: "interviewer", content: res.next_question! },
        ]);
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "interviewer",
          content:
            err instanceof Error
              ? `Error: ${err.message}`
              : "Something went wrong. Please try again.",
        },
      ]);
    } finally {
      setSubmitting(false);
    }
  }

  if (status === "loading") {
    return (
      <div className="flex flex-1 items-center justify-center">
        <p className="text-zinc-400 animate-pulse">Loading your interview…</p>
      </div>
    );
  }

  if (status === "error") {
    return (
      <div className="flex flex-1 flex-col items-center justify-center gap-4 px-6 text-center">
        <p className="text-red-500">{errorMessage}</p>
        <Link
          href="/upload"
          className="rounded-full bg-zinc-900 px-6 py-2 text-sm font-medium text-white hover:bg-zinc-700 transition-colors"
        >
          Try again
        </Link>
      </div>
    );
  }

  return (
    <div className="flex flex-col flex-1 h-screen">
      {/* Header */}
      <header className="border-b border-zinc-200 bg-white shrink-0">
        <div className="mx-auto max-w-3xl px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link
              href="/"
              className="text-sm text-zinc-500 hover:text-zinc-800 transition-colors"
            >
              ← Home
            </Link>
            <span className="text-zinc-300">/</span>
            <span className="text-sm font-medium">Interview</span>
          </div>
          {status === "complete" && (
            <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-700">
              Complete
            </span>
          )}
        </div>
      </header>

      {/* Message thread */}
      <div className="flex-1 overflow-y-auto px-6 py-6">
        <div className="mx-auto max-w-3xl space-y-4">
          {messages.map((msg, i) => {
            if (msg.role === "feedback" && msg.feedback) {
              return (
                <div key={i} className="mx-2">
                  <FeedbackCard
                    score={msg.feedback.score}
                    strengths={msg.feedback.strengths}
                    weaknesses={msg.feedback.weaknesses}
                    idealAnswer={msg.feedback.ideal_answer}
                  />
                </div>
              );
            }

            const isUser = msg.role === "user";
            return (
              <div
                key={i}
                className={`flex ${isUser ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-prose rounded-2xl px-4 py-3 text-sm leading-6 ${
                    isUser
                      ? "bg-zinc-900 text-white"
                      : "bg-white border border-zinc-200 text-zinc-800"
                  }`}
                >
                  {!isUser && (
                    <p className="text-xs font-semibold text-zinc-400 mb-1">
                      Interviewer
                    </p>
                  )}
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                </div>
              </div>
            );
          })}

          {submitting && (
            <div className="flex justify-start">
              <div className="rounded-2xl border border-zinc-200 bg-white px-4 py-3 text-sm text-zinc-400 animate-pulse">
                Evaluating your answer…
              </div>
            </div>
          )}

          {status === "complete" && (
            <div className="text-center pt-4">
              <p className="text-zinc-500 text-sm mb-4">
                Interview complete. Well done!
              </p>
              <Link
                href="/upload"
                className="rounded-full bg-zinc-900 px-6 py-2 text-sm font-medium text-white hover:bg-zinc-700 transition-colors"
              >
                Start a new interview
              </Link>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </div>

      {/* Input */}
      {status === "active" && (
        <div className="shrink-0 border-t border-zinc-200 bg-white px-6 py-4">
          <form
            onSubmit={handleSubmit}
            className="mx-auto max-w-3xl flex gap-3"
          >
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e as unknown as React.FormEvent);
                }
              }}
              placeholder="Type your answer… (Enter to send, Shift+Enter for new line)"
              rows={3}
              className="flex-1 resize-none rounded-xl border border-zinc-300 bg-zinc-50 px-4 py-3 text-sm leading-6 placeholder:text-zinc-400 focus:outline-none focus:ring-2 focus:ring-zinc-400"
            />
            <button
              type="submit"
              disabled={!input.trim() || submitting}
              className="self-end rounded-full bg-zinc-900 px-5 py-3 text-sm font-semibold text-white hover:bg-zinc-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Send
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
