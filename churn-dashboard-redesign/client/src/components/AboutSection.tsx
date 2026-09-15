import React from "react";
import { Brain, Cpu, Database, Server, Award } from "lucide-react";

export default function AboutSection() {
  const skillCategories = [
    {
      title: "Machine Learning & AI",
      icon: Brain,
      color: "teal",
      skills: ["Supervised Learning (XGBoost, Random Forest)", "Hyperparameter Optimization (GridSearchCV)", "SHAP & LIME Explainability", "Class Imbalance Handling (SMOTE)", "Model Serialization & Registry"],
    },
    {
      title: "Data Engineering & Lakehouse",
      icon: Database,
      color: "violet",
      skills: ["Feature Engineering & Derivation", "SQL & BigQuery Transformations", "dbt & Dataform Pipelines", "Pandas, NumPy, Polars", "Cohort Analysis & CLV Modeling"],
    },
    {
      title: "IoT & Real-Time Telemetry",
      icon: Cpu,
      color: "coral",
      skills: ["MQTT Protocol & Pub/Sub Brokers", "Apache Kafka Event Streams", "Edge Microcontrollers (ESP32/C++)", "Sensor Anomaly Detection", "Time-Series Databases (InfluxDB)"],
    },
    {
      title: "MLOps & Cloud Infrastructure",
      icon: Server,
      color: "blue",
      skills: ["Docker & Docker Compose", "FastAPI & Streamlit Deployment", "CI/CD & Pytest Automation", "GCP & Vertex AI Services", "Linux Environment Orchestration"],
    },
  ];

  return (
    <div className="space-y-8">
      <section className="section-heading">
        <div>
          <span className="section-index">04 / Background & Capabilities</span>
          <h2 className="text-2xl font-bold font-['Space_Grotesk'] text-[var(--ink)]">
            Engineering Philosophy & Tech Stack
          </h2>
        </div>
      </section>

      {/* Profile Bio Panel */}
      <section className="panel p-6 md:p-8 space-y-4">
        <div className="eyebrow flex items-center gap-2 text-[10px] font-bold tracking-widest text-[#85949E] uppercase">
          <Award size={14} className="text-[var(--teal)]" /> Lead Systems Architect Profile
        </div>
        <h3 className="text-xl md:text-2xl font-bold font-['Space_Grotesk'] text-[var(--ink)]">
          Engineering reliable intelligence from raw data to production decisions.
        </h3>
        <p className="text-xs md:text-sm text-[#73818A] leading-relaxed">
          I specialize in architecting full-lifecycle Machine Learning and IoT systems that solve high-impact enterprise problems. Whether developing predictive models that safeguard recurring revenue or building streaming telemetry feeds on edge microcontrollers, my focus is always on measurable accuracy, resilience, and clean, intuitive interfaces.
        </p>
      </section>

      {/* Skill Matrix */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {skillCategories.map((cat) => {
          const Icon = cat.icon;
          return (
            <div key={cat.title} className="panel p-5 space-y-3">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-[var(--mist)] border border-[var(--line)] grid place-items-center text-gray-700">
                  <Icon size={16} />
                </div>
                <h4 className="font-bold text-sm font-['Space_Grotesk'] text-[var(--ink)]">
                  {cat.title}
                </h4>
              </div>
              <ul className="space-y-1.5 pt-2 border-t border-[var(--line)]">
                {cat.skills.map((s) => (
                  <li key={s} className="text-xs text-gray-600 flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-[var(--teal)]" />
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
      </div>
    </div>
  );
}
