import React, { useState } from "react";
import { Mail, Send, Github, Linkedin, MessageSquare } from "lucide-react";
import { toast } from "sonner";

export default function ContactSection() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [subject, setSubject] = useState("ML & Data Architecture Collaboration");
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email || !message) {
      toast.error("Please fill in all required fields.");
      return;
    }
    toast.success("Message staged for dispatch!", {
      description: "Opening your default mail client...",
    });
    const mailtoUrl = `mailto:naveenpixel1@gmail.com?subject=${encodeURIComponent(
      subject
    )}&body=${encodeURIComponent(`From: ${name} (${email})\n\n${message}`)}`;
    window.location.href = mailtoUrl;
  };

  return (
    <div className="space-y-8">
      <section className="section-heading">
        <div>
          <span className="section-index">05 / Get In Touch</span>
          <h2 className="text-2xl font-bold font-['Space_Grotesk'] text-[var(--ink)]">
            Consultation & Collaboration Hub
          </h2>
        </div>
      </section>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Contact Info Card */}
        <div className="panel p-6 space-y-6">
          <div>
            <span className="eyebrow text-[10px] font-bold text-[#85949E] uppercase tracking-wider block mb-1">
              Direct Access
            </span>
            <h3 className="text-lg font-bold font-['Space_Grotesk'] text-[var(--ink)]">
              Let's Discuss Solutions
            </h3>
            <p className="text-xs text-[#73818A] mt-2 leading-relaxed">
              Available for full-stack Machine Learning architectures, IoT edge system deployments, and enterprise data pipelines.
            </p>
          </div>

          <div className="space-y-3 pt-4 border-t border-[var(--line)]">
            <a
              href="mailto:naveenpixel1@gmail.com"
              className="flex items-center gap-2.5 text-xs text-gray-700 hover:text-[var(--teal)] font-medium"
            >
              <Mail size={15} className="text-[var(--teal)]" /> naveenpixel1@gmail.com
            </a>
            <a
              href="https://github.com/naveenpixel1"
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-2.5 text-xs text-gray-700 hover:text-[var(--teal)] font-medium"
            >
              <Github size={15} className="text-[var(--teal)]" /> github.com/naveenpixel1
            </a>
            <a
              href="https://linkedin.com"
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-2.5 text-xs text-gray-700 hover:text-[var(--teal)] font-medium"
            >
              <Linkedin size={15} className="text-[var(--teal)]" /> LinkedIn Profile
            </a>
          </div>
        </div>

        {/* Message Form */}
        <div className="panel p-6 md:col-span-2 space-y-4">
          <div className="flex items-center justify-between border-b border-[var(--line)] pb-3">
            <span className="font-bold text-sm font-['Space_Grotesk'] text-[var(--ink)] flex items-center gap-2">
              <MessageSquare size={16} className="text-[var(--teal)]" /> Send a Direct Brief
            </span>
            <span className="text-[10px] text-gray-400 font-mono">Response within 24 hours</span>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="text-[10px] font-bold uppercase tracking-wider text-gray-500 block mb-1">
                  Your Name *
                </label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Maya Chen"
                  className="w-full h-9 px-3 text-xs bg-[var(--mist)] border border-[var(--line)] rounded-lg outline-none focus:border-[var(--teal)] transition"
                />
              </div>
              <div>
                <label className="text-[10px] font-bold uppercase tracking-wider text-gray-500 block mb-1">
                  Email Address *
                </label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="e.g. maya@enterprise.com"
                  className="w-full h-9 px-3 text-xs bg-[var(--mist)] border border-[var(--line)] rounded-lg outline-none focus:border-[var(--teal)] transition"
                />
              </div>
            </div>

            <div>
              <label className="text-[10px] font-bold uppercase tracking-wider text-gray-500 block mb-1">
                Project Scope / Subject
              </label>
              <input
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="w-full h-9 px-3 text-xs bg-[var(--mist)] border border-[var(--line)] rounded-lg outline-none focus:border-[var(--teal)] transition"
              />
            </div>

            <div>
              <label className="text-[10px] font-bold uppercase tracking-wider text-gray-500 block mb-1">
                Message Brief *
              </label>
              <textarea
                required
                rows={4}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Describe your Machine Learning, Data Analytics, or IoT project requirements..."
                className="w-full p-3 text-xs bg-[var(--mist)] border border-[var(--line)] rounded-lg outline-none focus:border-[var(--teal)] transition resize-none"
              />
            </div>

            <button
              type="submit"
              className="primary-button flex items-center justify-center gap-2 w-full sm:w-auto px-6 py-2.5 rounded-lg bg-[var(--teal)] text-[#0C2428] font-bold text-xs hover:bg-[#43D5C3] transition shadow-md"
            >
              <Send size={14} /> Send Message Brief
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
