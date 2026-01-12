import { Mic, Users, FileText, Receipt } from "lucide-react";

export function Process() {
  const steps = [
    {
      icon: Mic,
      title: "Audio Capture",
      description: "Secure, ambient recording",
    },
    {
      icon: Users,
      title: "Smart Transcription",
      description: "Speaker diarization",
    },
    {
      icon: FileText,
      title: "SOAP Generation",
      description: "Structured clinical notes",
    },
    {
      icon: Receipt,
      title: "Automated Billing",
      description: "ICD-10 & CPT Mapping",
    },
  ];

  return (
    <section className="py-16 px-6 dark:bg-background-dark">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <p className="text-sm font-semibold text-primary uppercase tracking-wider mb-2">
            THE PROCESS
          </p>
          <h2 className="text-3xl md:text-4xl font-bold text-text-main dark:text-white">
            Streamlined Clinical Documentation
          </h2>
        </div>

        {/* Steps Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <div
              key={index}
              className="flex flex-col items-center text-center group"
            >
              {/* Icon Circle */}
              <div className="w-16 h-16 rounded-full bg-gray-50 dark:bg-surface-dark border border-gray-200 dark:border-gray-700 flex items-center justify-center mb-4 group-hover:bg-primary-light dark:group-hover:bg-primary/10 group-hover:border-primary transition-all duration-300">
                <step.icon className="w-6 h-6 text-gray-600 dark:text-gray-400 group-hover:text-primary transition-colors" />
              </div>

              {/* Title */}
              <h3 className="text-lg font-semibold text-text-main dark:text-white mb-2">
                {step.title}
              </h3>

              {/* Description */}
              <p className="text-sm text-text-sub dark:text-gray-400">
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
