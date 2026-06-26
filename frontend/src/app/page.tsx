import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col flex-1">
      {/* Nav */}
      <header className="border-b border-zinc-200 bg-white">
        <div className="mx-auto max-w-5xl px-6 py-4 flex items-center justify-between">
          <span className="text-lg font-semibold tracking-tight">
            🧠 AI Interview Coach
          </span>
          <Link
            href="/upload"
            className="rounded-full bg-zinc-900 px-5 py-2 text-sm font-medium text-white hover:bg-zinc-700 transition-colors"
          >
            Get started
          </Link>
        </div>
      </header>

      {/* Hero */}
      <main className="flex flex-col flex-1">
        <section className="bg-white border-b border-zinc-200">
          <div className="mx-auto max-w-3xl px-6 py-24 text-center">
            <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
              Ace your next interview
            </h1>
            <p className="mt-6 text-lg leading-8 text-zinc-600">
              Upload your CV and a job description. Our AI generates tailored
              interview questions, runs a mock interview, and gives you scored,
              structured feedback — so you walk in confident.
            </p>
            <div className="mt-10 flex justify-center gap-4">
              <Link
                href="/upload"
                className="rounded-full bg-zinc-900 px-7 py-3 text-sm font-semibold text-white shadow hover:bg-zinc-700 transition-colors"
              >
                Start practicing →
              </Link>
            </div>
          </div>
        </section>

        {/* Features */}
        <section className="mx-auto max-w-5xl px-6 py-20">
          <h2 className="text-center text-2xl font-semibold mb-12">
            How it works
          </h2>
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {steps.map((step) => (
              <div
                key={step.title}
                className="flex flex-col gap-3 rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm"
              >
                <span className="flex h-10 w-10 items-center justify-center rounded-full bg-zinc-100 text-xl font-bold">
                  {step.number}
                </span>
                <h3 className="font-semibold">{step.title}</h3>
                <p className="text-sm text-zinc-500 leading-6">
                  {step.description}
                </p>
              </div>
            ))}
          </div>
        </section>
      </main>

      <footer className="border-t border-zinc-200 bg-white py-6 text-center text-sm text-zinc-400">
        AI Interview Coach — portfolio project
      </footer>
    </div>
  );
}

const steps = [
  {
    number: "1",
    title: "Upload your CV",
    description:
      "Upload your CV as a PDF. We extract your experience, skills, and background automatically.",
  },
  {
    number: "2",
    title: "Add a job description",
    description:
      "Paste the job description for the role you are applying for. We identify skill gaps and key requirements.",
  },
  {
    number: "3",
    title: "Mock interview",
    description:
      "Answer AI-generated technical, behavioural, and CV-specific questions in a realistic chat interface.",
  },
  {
    number: "4",
    title: "Get feedback",
    description:
      "Receive a score, strengths, weaknesses, and an ideal answer for every response.",
  },
];
