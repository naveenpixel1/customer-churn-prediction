import React from "react";
import {
  Zap,
  ArrowUpRight,
  Sparkles,
  Users,
  Gauge,
  ShieldCheck,
  BrainCircuit,
  Database,
  Cpu,
  ArrowRight,
} from "lucide-react";
import { ActiveTab } from "../App";

interface HeroSectionProps {
  onNavigate: (tab: ActiveTab) => void;
}

export default function HeroSection({ onNavigate }: HeroSectionProps) {
  return (
    <div className="space-y-8">
      {/* Hero Header */}
      <section className="hero-row flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-[var(--line)]">
        <div>
          <div className="eyebrow flex items-center gap-2 text-[10px] font-bold tracking-widest text-[#85949E] uppercase mb-2">
            <span className="w-5 h-0.5 bg-[var(--teal)] rounded" />
            Machine Learning & IoT Systems Engineer
          </div>
          <h1 className="text-3xl md:text-5xl font-bold tracking-tight text-[var(--ink)] font-['Space_Grotesk'] leading-tight">
            Building Predictive ML, Real-Time Data Pipelines & Edge IoT.
          </h1>
          <p className="hero-copy text-sm md:text-base text-[#73818A] mt-3 max-w-2xl">
            Designing production-grade intelligence systems—from tree ensemble churn prediction to distributed IoT sensor telemetry and automated data warehouse pipelines.
          </p>
        </div>

        <div className="hero-actions flex flex-wrap gap-2.5">
          <button
            className="primary-button flex items-center gap-2 px-4 py-2.5 rounded-lg bg-[var(--teal)] text-[#0C2428] font-bold text-xs shadow-md hover:bg-[#43D5C3] transition"
            onClick={() => onNavigate("dashboard")}
          >
            <Zap size={15} /> Launch Live ChurnIQ
          </button>
          <button
            className="secondary-button flex items-center gap-2 px-4 py-2.5 rounded-lg border border-[var(--line)] bg-white text-[#53626B] font-bold text-xs hover:bg-gray-50 transition"
            onClick={() => onNavigate("projects")}
          >
            Explore Projects <ArrowRight size={14} />
          </button>
        </div>
      </section>

      {/* Live System Signal Banner */}
      <section className="signal-banner">
        <div className="signal-icon">
          <Sparkles size={18} />
        </div>
        <div>
          <span className="signal-kicker">Core Specialization</span>
          <strong>End-to-End MLOps & Production Retention Intelligence</strong>
          <p>
            Trained with <b>GridSearchCV</b>, serialized with scikit-learn & XGBoost, and deployed inside containerized Docker microservices with SHAP explainability.
          </p>
        </div>
        <button onClick={() => onNavigate("dashboard")}>
          View Active Model <ArrowUpRight size={16} />
        </button>
      </section>

      {/* KPI Telemetry Cards */}
      <section>
        <div className="section-heading mb-4">
          <div>
            <span className="section-index">01 / Telemetry</span>
            <h2 className="text-xl font-bold font-['Space_Grotesk']">System Performance & Impact</h2>
          </div>
        </div>

        <div className="metric-grid grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          <article className="metric-card metric-violet">
            <div className="metric-top">
              <span>Model F1 Score</span>
              <Gauge size={17} strokeWidth={1.8} />
            </div>
            <div className="metric-value">61.75%</div>
            <div className="metric-foot">
              <span className="positive">+2.4 pts</span>
              <span>vs baseline classifier</span>
            </div>
            <div className="mini-spark" aria-hidden="true">
              <span /><span /><span /><span /><span /><span /><span />
            </div>
          </article>

          <article className="metric-card metric-coral">
            <div className="metric-top">
              <span>At-Risk Revenue Protected</span>
              <ArrowUpRight size={17} strokeWidth={1.8} />
            </div>
            <div className="metric-value">₹18.6L</div>
            <div className="metric-foot">
              <span className="positive">−12.4%</span>
              <span>high-risk cohort drop</span>
            </div>
            <div className="mini-spark" aria-hidden="true">
              <span /><span /><span /><span /><span /><span /><span />
            </div>
          </article>

          <article className="metric-card metric-blue">
            <div className="metric-top">
              <span>ROC-AUC Discriminator</span>
              <ShieldCheck size={17} strokeWidth={1.8} />
            </div>
            <div className="metric-value">0.8457</div>
            <div className="metric-foot">
              <span className="positive">80.62%</span>
              <span>test accuracy</span>
            </div>
            <div className="mini-spark" aria-hidden="true">
              <span /><span /><span /><span /><span /><span /><span />
            </div>
          </article>

          <article className="metric-card metric-teal">
            <div className="metric-top">
              <span>Accounts Monitored</span>
              <Users size={17} strokeWidth={1.8} />
            </div>
            <div className="metric-value">7,043</div>
            <div className="metric-foot">
              <span className="positive">24 features</span>
              <span>engineered per batch</span>
            </div>
            <div className="mini-spark" aria-hidden="true">
              <span /><span /><span /><span /><span /><span /><span />
            </div>
          </article>
        </div>
      </section>

      {/* Architectural Pillars */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="panel p-5 space-y-3 hover:shadow-md transition">
          <div className="w-9 h-9 rounded-lg bg-[#E4F5F2] text-[#168C7E] grid place-items-center">
            <BrainCircuit size={19} />
          </div>
          <h3 className="font-bold text-base font-['Space_Grotesk'] text-[var(--ink)]">
            Machine Learning & MLOps
          </h3>
          <p className="text-xs text-[#73818A] leading-relaxed">
            Class imbalance handling, hyperparameter tuning via GridSearchCV, model artifact serialization, and Docker deployment.
          </p>
          <button
            onClick={() => onNavigate("projects")}
            className="text-button text-xs font-bold text-[#168C7E] flex items-center gap-1 hover:underline"
          >
            Explore ML Stack <ArrowUpRight size={13} />
          </button>
        </div>

        <div className="panel p-5 space-y-3 hover:shadow-md transition">
          <div className="w-9 h-9 rounded-lg bg-[#E8EBFF] text-[#5667DE] grid place-items-center">
            <Database size={19} />
          </div>
          <h3 className="font-bold text-base font-['Space_Grotesk'] text-[var(--ink)]">
            Data Analytics & Lakehouse
          </h3>
          <p className="text-xs text-[#73818A] leading-relaxed">
            Automated feature engineering (`Tenure_To_Monthly_Ratio`, `Service_Count`), BigQuery ELT transformations, and cohort tracking.
          </p>
          <button
            onClick={() => onNavigate("projects")}
            className="text-button text-xs font-bold text-[#5667DE] flex items-center gap-1 hover:underline"
          >
            Explore Analytics <ArrowUpRight size={13} />
          </button>
        </div>

        <div className="panel p-5 space-y-3 hover:shadow-md transition">
          <div className="w-9 h-9 rounded-lg bg-[#FCE9E4] text-[#CC614D] grid place-items-center">
            <Cpu size={19} />
          </div>
          <h3 className="font-bold text-base font-['Space_Grotesk'] text-[var(--ink)]">
            IoT & Edge Telemetry
          </h3>
          <p className="text-xs text-[#73818A] leading-relaxed">
            Real-time sensor event streaming over MQTT/Kafka, anomaly detection on edge devices, and preventative maintenance alerting.
          </p>
          <button
            onClick={() => onNavigate("projects")}
            className="text-button text-xs font-bold text-[#CC614D] flex items-center gap-1 hover:underline"
          >
            Explore IoT Architecture <ArrowUpRight size={13} />
          </button>
        </div>
      </section>
    </div>
  );
}
