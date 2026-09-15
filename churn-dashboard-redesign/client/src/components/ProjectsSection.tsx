import React, { useState } from "react";
import {
  Sparkles,
  Github,
  Play,
} from "lucide-react";
import { ActiveTab } from "../App";

interface ProjectsSectionProps {
  onNavigate: (tab: ActiveTab) => void;
}

export default function ProjectsSection({ onNavigate }: ProjectsSectionProps) {
  const [filter, setFilter] = useState<"all" | "ml" | "data" | "iot">("all");

  const projects = [
    {
      id: "churn-ml",
      category: "ml",
      categoryLabel: "Machine Learning & MLOps",
      categoryAccent: "teal",
      title: "End-to-End Customer Churn Intelligence & Retention System",
      description:
        "Full-lifecycle machine learning system predicting customer attrition in telecommunications. Engineered 24 interaction features, tuned multi-model ensembles with GridSearchCV, and integrated SHAP instance explainability into an operational attention queue.",
      metrics: [
        { label: "ROC-AUC", val: "0.8457" },
        { label: "F1 Score", val: "61.75%" },
        { label: "MRR Safeguarded", val: "₹18.6L" },
        { label: "Dataset Size", val: "7,043 rows" },
      ],
      tags: ["Python", "XGBoost", "Scikit-Learn", "Docker", "Streamlit", "GridSearchCV", "SHAP"],
      liveAction: () => onNavigate("dashboard"),
      liveActionText: "Launch ChurnIQ Dashboard",
      githubUrl: "https://github.com/naveenpixel1/customer-churn-prediction",
    },
    {
      id: "lakehouse-data",
      category: "data",
      categoryLabel: "Data Engineering & Analytics",
      categoryAccent: "violet",
      title: "Automated Lakehouse Retention & Cohort Analytics Pipeline",
      description:
        "High-throughput data analytics architecture with automated ELT staging, cohort retention matrices, billing velocity monitors, and Customer Lifetime Value (CLV) categorization models.",
      metrics: [
        { label: "Ingestion Latency", val: "< 1.2s" },
        { label: "Features Derived", val: "4 Core Interaction" },
        { label: "Query Optimization", val: "38% Faster" },
        { label: "Cohort Tracking", val: "Monthly Retention" },
      ],
      tags: ["SQL", "BigQuery", "dbt", "Pandas", "Plotly", "PostgreSQL", "Dataform"],
      liveAction: () => onNavigate("dashboard"),
      liveActionText: "Inspect Data Cohorts",
      githubUrl: "https://github.com/naveenpixel1/customer-churn-prediction",
    },
    {
      id: "iot-telemetry",
      category: "iot",
      categoryLabel: "IoT & Real-Time Telemetry",
      categoryAccent: "coral",
      title: "Edge IoT Sensor Anomaly Detection & Predictive Maintenance",
      description:
        "Distributed IoT architecture streaming sensor vibration, temperature, and current metrics over MQTT & Kafka. Micro-models on the edge flag anomalies before hardware degradation occurs.",
      metrics: [
        { label: "Sensor Stream Rate", val: "100 Hz" },
        { label: "Detection Latency", val: "< 45ms" },
        { label: "False Positive Rate", val: "< 0.8%" },
        { label: "Uptime Monitored", val: "99.98%" },
      ],
      tags: ["C++", "Python", "MQTT", "Apache Kafka", "ESP32", "InfluxDB", "Grafana"],
      liveAction: () => onNavigate("contact"),
      liveActionText: "Request Architecture Demo",
      githubUrl: "https://github.com/naveenpixel1",
    },
  ];

  const filtered = filter === "all" ? projects : projects.filter((p) => p.category === filter);

  return (
    <div className="space-y-8">
      {/* Section Heading */}
      <section className="section-heading flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <span className="section-index">02 / Engineering Portfolio</span>
          <h2 className="text-2xl font-bold font-['Space_Grotesk'] text-[var(--ink)]">
            Featured Systems & Applications
          </h2>
        </div>

        {/* Filter Pills */}
        <div className="flex gap-1.5 bg-white p-1 rounded-lg border border-[var(--line)] self-start sm:self-auto">
          {(["all", "ml", "data", "iot"] as const).map((key) => (
            <button
              key={key}
              onClick={() => setFilter(key)}
              className={`px-3 py-1 text-xs font-semibold rounded-md transition ${
                filter === key
                  ? "bg-[var(--navy)] text-white shadow-sm"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              {key === "all" ? "All Projects" : key.toUpperCase()}
            </button>
          ))}
        </div>
      </section>

      {/* Projects Grid */}
      <div className="grid grid-cols-1 gap-6">
        {filtered.map((project) => (
          <article
            key={project.id}
            className={`panel p-6 md:p-7 relative overflow-hidden transition-all duration-200 hover:shadow-lg border-t-4 ${
              project.categoryAccent === "teal"
                ? "border-t-[var(--teal)]"
                : project.categoryAccent === "violet"
                ? "border-t-[var(--violet)]"
                : "border-t-[var(--coral)]"
            }`}
          >
            <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
              <div className="space-y-2 max-w-3xl">
                <span className="eyebrow flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider text-[#85949E]">
                  <Sparkles size={13} className="text-[var(--teal)]" />
                  {project.categoryLabel}
                </span>
                <h3 className="text-xl md:text-2xl font-bold font-['Space_Grotesk'] text-[var(--ink)]">
                  {project.title}
                </h3>
                <p className="text-xs md:text-sm text-[#73818A] leading-relaxed">
                  {project.description}
                </p>
              </div>

              {/* Action Buttons */}
              <div className="flex md:flex-col gap-2 shrink-0">
                <button
                  onClick={project.liveAction}
                  className="primary-button flex items-center justify-center gap-1.5 text-xs font-bold px-3.5 py-2 rounded-lg bg-[var(--teal)] text-[#0C2428] hover:bg-[#43D5C3] transition"
                >
                  <Play size={14} /> {project.liveActionText}
                </button>
                <a
                  href={project.githubUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="secondary-button flex items-center justify-center gap-1.5 text-xs font-bold px-3.5 py-2 rounded-lg border border-[var(--line)] bg-white text-gray-700 hover:bg-gray-50 transition"
                >
                  <Github size={14} /> Codebase
                </a>
              </div>
            </div>

            {/* Live Metrics Quad */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 my-6 pt-5 border-t border-[var(--line)]">
              {project.metrics.map((m) => (
                <div key={m.label} className="bg-[var(--mist)]/70 p-3 rounded-lg border border-[var(--line)]">
                  <span className="text-[9px] uppercase tracking-wider font-bold text-gray-500 block">
                    {m.label}
                  </span>
                  <strong className="text-base font-bold font-['Space_Grotesk'] text-[var(--ink)] block mt-1">
                    {m.val}
                  </strong>
                </div>
              ))}
            </div>

            {/* Tech Tags */}
            <div className="flex flex-wrap gap-1.5 pt-2">
              {project.tags.map((t) => (
                <span
                  key={t}
                  className="px-2.5 py-1 rounded-md bg-white border border-[var(--line)] text-gray-700 text-[11px] font-medium"
                >
                  {t}
                </span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
