type FileUploadCardProps = {
  title: string;
  description: string;
  file: File | null;
  accept: string;
  onFileSelected: (file: File | null) => void;
  disabled: boolean;
};

export default function FileUploadCard({
  title,
  description,
  file,
  accept,
  onFileSelected,
  disabled,
}: FileUploadCardProps) {
  return (
    <div className="rounded-3xl border border-black/10 bg-background p-6 shadow-sm dark:border-white/10">
      <h2 className="text-xl font-semibold">{title}</h2>

      <p className="mt-2 text-sm text-foreground/70">
        {description}
      </p>
    
    <label
    className="
        mt-6 inline-flex cursor-pointer items-center rounded-xl
        bg-blue-600 px-5 py-3 font-medium text-white
        transition
        hover:bg-blue-700
        focus-within:ring-4
        focus-within:ring-blue-300
        dark:focus-within:ring-blue-800
    "
    >
    Choose File

    <input
        className="hidden"
        type="file"
        accept={accept}
        onChange={(event) =>
            onFileSelected(event.target.files?.[0] ?? null)
        }
        disabled={disabled}
    />
    </label>

    {file ? (
    <span className="font-medium">
        Selected: {file.name}
    </span>
    ) : (
    <span>No file selected yet</span>
    )}
    </div>
  );
}