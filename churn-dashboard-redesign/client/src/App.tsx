import React, { useState } from "react";
import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import {
  LayoutDashboard,
  BrainCircuit,
  FolderGit2,
  Briefcase,
  User,
  Mail,
  ShieldCheck,
  Search,
  Bell,
  ChevronDown,
  Menu,
  X,
  ExternalLink,
  Github,
  Linkedin,
} from "lucide-react";
import { toast } from "sonner";

// View Components
import Home from "./pages/Home";
import HeroSection from "./components/HeroSection";
import ProjectsSection from "./components/ProjectsSection";
import ExperienceSection from "./components/ExperienceSection";
import AboutSection from "./components/AboutSection";
import ContactSection from "./components/ContactSection";

export type ActiveTab = "dashboard" | "overview" | "projects" | "experience" | "about" | "contact";

export default function App() {
  const [activeTab, setActiveTab] = useState<ActiveTab>("overview");
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { id: "overview", label: "Overview & Hero", icon: LayoutDashboard },
    { id: "dashboard", label: "ChurnIQ Live Engine", icon: BrainCircuit, badge: "Live ML" },
    { id: "projects", label: "Featured Projects", icon: FolderGit2, count: "3" },
    { id: "experience", label: "Experience & Roles", icon: Briefcase },
    { id: "about", label: "Engineering & Skills", icon: User },
    { id: "contact", label: "Contact & Connect", icon: Mail },
  ];

  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="light">
        <TooltipProvider>
          <Toaster richColors position="top-right" />
          
          <div className="app-shell min-h-screen bg-[var(--mist)] flex text-[var(--ink)]">
            {/* Sticky Command Rail / Sidebar */}
            <aside className={`sidebar ${mobileMenuOpen ? "open" : ""}`}>
              {/* Brand Header */}
              <div className="brand-lockup">
                <div className="brand-mark bg-[#20353E] w-8 h-8 rounded-lg grid place-items-center">
                  <span className="text-[var(--teal)] font-bold text-sm font-['Space_Grotesk']">NK</span>
                </div>
                <div>
                  <div className="brand-name">
                    Naveen<span>.dev</span>
                  </div>
                  <div className="brand-caption">ML & Data Systems Architect</div>
                </div>
                <button
                  className="mobile-close md:hidden ml-auto text-gray-400 hover:text-white"
                  onClick={() => setMobileMenuOpen(false)}
                  aria-label="Close menu"
                >
                  <X size={18} />
                </button>
              </div>

              {/* Workspace / Profile Pill */}
              <div className="workspace-switcher">
                <div className="workspace-avatar">ML</div>
                <div>
                  <span>Production System</span>
                  <strong>Telco Churn v2.4</strong>
                </div>
                <ChevronDown size={14} className="text-gray-400" />
              </div>

              {/* Navigation Rail */}
              <div className="nav-label">Navigation Hub</div>
              <nav className="space-y-1">
                {navItems.map(({ id, label, icon: Icon, badge, count }) => (
                  <button
                    key={id}
                    className={`nav-item ${activeTab === id ? "active" : ""}`}
                    onClick={() => {
                      setActiveTab(id as ActiveTab);
                      setMobileMenuOpen(false);
                      window.scrollTo({ top: 0, behavior: "smooth" });
                    }}
                  >
                    <Icon size={17} strokeWidth={2} />
                    <span>{label}</span>
                    {badge && (
                      <span className="ml-auto bg-[var(--teal)]/20 text-[var(--teal)] border border-[var(--teal)]/40 px-1.5 py-0.5 rounded text-[9px] font-bold">
                        {badge}
                      </span>
                    )}
                    {count && (
                      <span className="nav-count ml-auto">{count}</span>
                    )}
                  </button>
                ))}
              </nav>

              {/* Quick Links */}
              <div className="nav-label lower">Connect</div>
              <nav className="space-y-1">
                <a
                  href="https://github.com/naveenpixel1"
                  target="_blank"
                  rel="noreferrer"
                  className="nav-item"
                >
                  <Github size={16} />
                  <span>GitHub Repository</span>
                  <ExternalLink size={12} className="ml-auto opacity-60" />
                </a>
                <a
                  href="https://linkedin.com"
                  target="_blank"
                  rel="noreferrer"
                  className="nav-item"
                >
                  <Linkedin size={16} />
                  <span>LinkedIn Profile</span>
                  <ExternalLink size={12} className="ml-auto opacity-60" />
                </a>
              </nav>

              {/* Sidebar Bottom Telemetry */}
              <div className="sidebar-bottom">
                <div className="model-status">
                  <span className="status-dot animate-pulse" />
                  <div>
                    <span>Pipeline Status</span>
                    <strong>Models Online (F1: 61.75%)</strong>
                  </div>
                  <ShieldCheck size={16} className="text-[var(--teal)]" />
                </div>
                <div className="user-row">
                  <div className="user-avatar bg-[#26515A] text-[#C6F4EE]">NK</div>
                  <div>
                    <strong>Naveen Kumar .D</strong>
                    <span>ML & IoT Engineer</span>
                  </div>
                </div>
              </div>
            </aside>

            {/* Mobile Scrim */}
            {mobileMenuOpen && (
              <div
                className="scrim fixed inset-0 bg-black/50 z-20 md:hidden"
                onClick={() => setMobileMenuOpen(false)}
              />
            )}

            {/* Main Application Content */}
            <main className="main-content flex-1 min-w-0">
              {/* Header Topbar */}
              <header className="topbar">
                <button
                  className="mobile-menu md:hidden mr-3 p-1.5 rounded-lg border border-[var(--line)] bg-white text-gray-600"
                  onClick={() => setMobileMenuOpen(true)}
                  aria-label="Open menu"
                >
                  <Menu size={18} />
                </button>

                <div className="breadcrumb">
                  <span>Portfolio</span>
                  <span>/</span>
                  <strong className="capitalize text-[var(--ink)]">
                    {navItems.find((n) => n.id === activeTab)?.label}
                  </strong>
                </div>

                <div className="top-actions flex items-center gap-2">
                  <button
                    className="icon-button"
                    onClick={() => toast.info("Global Search", { description: "Filter across ML models, IoT streams & datasets." })}
                    aria-label="Search"
                  >
                    <Search size={16} />
                  </button>
                  <button
                    className="icon-button has-dot"
                    onClick={() => toast.success("Live Signals Active", { description: "14 high-risk accounts flagged by XGBoost." })}
                    aria-label="Alerts"
                  >
                    <Bell size={16} />
                  </button>
                  <button
                    className="help-button flex items-center gap-1.5 px-3 h-[34px] rounded-lg border border-[var(--line)] bg-white text-xs font-semibold text-gray-700 hover:bg-gray-50"
                    onClick={() => setActiveTab("contact")}
                  >
                    <Mail size={15} /> Let's Talk
                  </button>
                </div>
              </header>

              {/* Dynamic View Router */}
              <div className="content-wrap transition-opacity duration-200">
                {activeTab === "overview" && <HeroSection onNavigate={setActiveTab} />}
                {activeTab === "dashboard" && <Home />}
                {activeTab === "projects" && <ProjectsSection onNavigate={setActiveTab} />}
                {activeTab === "experience" && <ExperienceSection />}
                {activeTab === "about" && <AboutSection />}
                {activeTab === "contact" && <ContactSection />}
              </div>
            </main>
          </div>
        </TooltipProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}
