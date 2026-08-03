"use client";

import { useState } from "react";

import UploadView from "./UploadView";
import InterviewView from "./InterviewView";
import CompleteView from "./CompleteView";

export type InterviewStage =
  | "upload"
  | "interview"
  | "complete";

export default function InterviewApp() {
  const [stage, setStage] = useState<InterviewStage>("upload");

  switch (stage) {
    case "upload":
      return <UploadView onStartInterview={() => setStage("interview")} />;

    case "interview":
      return <InterviewView />;

    case "complete":
      return <CompleteView />;

    default:
      return null;
  }
}