import React from "react";
import { Calendar, MapPin, CheckCircle2 } from "lucide-react";

export default function ExperienceSection() {
  const experiences = [
    {
      role: "Lead Machine Learning & IoT Engineer",
      organization: "Autonomous Intelligent Systems Lab",
      period: "2024 — Present",
      location: "Bengaluru, India",
      summary:
        "Architecting predictive maintenance pipelines and real-time retention telemetry engines for cloud and edge environments.",
      highlights: [
        "Built end-to-end customer churn classification pipelines achieving 80.62% accuracy and 0.8457 ROC-AUC with tree ensembles.",
        "Engineered streaming IoT anomaly detection telemetry processing sensor telemetry at 100Hz with sub-50ms latency.",
        "Containerized production pipelines with Docker Compose, automating testing and zero-downtime rollouts.",
      ],
      skills: ["Python", "XGBoost", "Docker", "FastAPI", "BigQuery", "MQTT", "Linux"],
    },
    {
      role: "Data Systems & Software Engineer",
      organization: "Enterprise Intelligence & Analytics",
      period: "2023 — 2024",
      location: "India",
      summary:
        "Spearheaded database modeling, automated ELT workflows, and dynamic business intelligence dashboards for enterprise SaaS.",
      highlights: [
        "Constructed automated data pipelines extracting customer engagement signals across 7,000+ subscriber accounts.",
        "Implemented Customer Lifetime Value (CLV) scoring modules reducing customer attrition risk by 12.4%.",
        "Optimized analytical SQL queries and database schemas, slashing report execution latency by 38%.",
      ],
      skills: ["SQL", "Scikit-Learn", "PostgreSQL", "dbt", "Streamlit", "Plotly"],
    },
  ];

  return (
    <div className="space-y-8">
      <section className="section-heading">
        <div>
          <span className="section-index">03 / Career Milestones</span>
          <h2 className="text-2xl font-bold font-['Space_Grotesk'] text-[var(--ink)]">
            Professional Experience & Leadership
          </h2>
        </div>
      </section>

      <div className="space-y-6">
        {experiences.map((exp, idx) => (
          <article key={idx} className="panel p-6 md:p-7 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[var(--line)] pb-4">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-[var(--teal)]">
                  {exp.organization}
                </span>
                <h3 className="text-xl font-bold font-['Space_Grotesk'] text-[var(--ink)]">
                  {exp.role}
                </h3>
              </div>
              <div className="flex items-center gap-3 text-xs text-gray-500">
                <span className="flex items-center gap-1">
                  <Calendar size={13} /> {exp.period}
                </span>
                <span className="flex items-center gap-1">
                  <MapPin size={13} /> {exp.location}
                </span>
              </div>
            </div>

            <p className="text-xs md:text-sm text-[#73818A] leading-relaxed">
              {exp.summary}
            </p>

            <div className="space-y-2">
              <span className="text-[10px] font-bold uppercase tracking-wider text-gray-500">
                Key Accomplishments
              </span>
              <ul className="space-y-1.5">
                {exp.highlights.map((h, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-gray-700 leading-normal">
                    <CheckCircle2 size={14} className="text-[var(--teal)] mt-0.5 shrink-0" />
                    <span>{h}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="flex flex-wrap gap-1.5 pt-2">
              {exp.skills.map((s) => (
                <span
                  key={s}
                  className="px-2 py-0.5 rounded bg-[var(--mist)] border border-[var(--line)] text-gray-600 text-[11px] font-medium"
                >
                  {s}
                </span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
