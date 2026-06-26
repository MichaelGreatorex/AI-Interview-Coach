"use client";

import { useRef, useState } from "react";

interface CVUploadProps {
  onFileSelected: (file: File) => void;
  selectedFile: File | null;
}

export default function CVUpload({ onFileSelected, selectedFile }: CVUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [fileError, setFileError] = useState<string | null>(null);

  function handleFiles(files: FileList | null) {
    setFileError(null);
    if (!files || files.length === 0) return;
    const file = files[0];
    if (file.type !== "application/pdf") {
      setFileError("Only PDF files are supported. Please choose a PDF.");
      return;
    }
    onFileSelected(file);
  }

  return (
    <div className="space-y-2">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          handleFiles(e.dataTransfer.files);
        }}
        onClick={() => inputRef.current?.click()}
        className={`flex cursor-pointer flex-col items-center justify-center gap-3 rounded-2xl border-2 border-dashed px-6 py-10 text-center transition-colors ${
          dragging
            ? "border-zinc-500 bg-zinc-100"
            : "border-zinc-300 bg-white hover:border-zinc-400 hover:bg-zinc-50"
        }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          className="hidden"
          onChange={(e) => handleFiles(e.target.files)}
        />
        {selectedFile ? (
          <>
            <span className="text-3xl">📄</span>
            <p className="font-medium text-zinc-800">{selectedFile.name}</p>
            <p className="text-sm text-zinc-400">
              {(selectedFile.size / 1024).toFixed(1)} KB — click to change
            </p>
          </>
        ) : (
          <>
            <span className="text-3xl">⬆️</span>
            <p className="font-medium text-zinc-700">
              Drag &amp; drop your CV here
            </p>
            <p className="text-sm text-zinc-400">PDF only — click to browse</p>
          </>
        )}
      </div>
      {fileError && (
        <p className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-600">
          {fileError}
        </p>
      )}
    </div>
  );
}
