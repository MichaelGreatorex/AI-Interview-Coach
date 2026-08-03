type CompleteViewProps = {
  onEndSession: () => void;
};

export default function CompleteView({
  onEndSession,
}: CompleteViewProps) {
  return (
    <main className="min-h-screen bg-background px-6 py-12">
      <div className="mx-auto flex max-w-3xl flex-col items-center justify-center text-center">
        <div
          className="
            rounded-3xl
            border
            border-black/10
            bg-background
            p-10
            shadow-lg
            dark:border-white/10
          "
        >
          <div className="text-6xl">
            🎉
          </div>

          <h1 className="mt-6 text-4xl font-bold">
            Interview Complete
          </h1>

          <p className="mt-4 text-lg text-foreground/70">
            Great work! You have completed your practice interview.
          </p>

          <button
            className="
              mt-8
              rounded-xl
              bg-blue-600
              px-8
              py-3
              font-semibold
              text-white
              transition
              hover:bg-blue-700
            "
            onClick={onEndSession}
          >
            End Session
          </button>
        </div>
      </div>
    </main>
  );
}