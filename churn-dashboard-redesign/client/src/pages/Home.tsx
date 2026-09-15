// Coastal Instrument design: editorial analytics, navy casing, sea-glass signals, coral risk accents.
import { useState } from "react";
import { toast } from "sonner";
import {
  Activity,
  ArrowDownRight,
  ArrowUpRight,
  Bell,
  ChevronDown,
  CircleHelp,
  Clock3,
  Download,
  FileText,
  Filter,
  Mail,
  MapPin,
  Phone,
  SlidersHorizontal,
  XCircle,
  Gauge,
  LayoutDashboard,
  Menu,
  MoreHorizontal,
  Search,
  Send,
  Settings2,
  ShieldCheck,
  Sparkles,
  Target,
  Tag,
  Users,
  X,
  Zap,
} from "lucide-react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const trendData = [
  { month: "Jan", retained: 74, risk: 24 },
  { month: "Feb", retained: 78, risk: 22 },
  { month: "Mar", retained: 75, risk: 26 },
  { month: "Apr", retained: 81, risk: 19 },
  { month: "May", retained: 84, risk: 16 },
  { month: "Jun", retained: 86, risk: 14 },
  { month: "Jul", retained: 89, risk: 11 },
];

const segmentData = [
  { name: "Low risk", value: 62, color: "#2BC6B4" },
  { name: "Watch", value: 24, color: "#6D7CF5" },
  { name: "High risk", value: 14, color: "#F17B63" },
];

const customers = [
  { initials: "AC", name: "Atlas Commerce", plan: "Enterprise", score: "87%", scoreValue: 87, signal: "Usage dropped 31%", tone: "coral", owner: "Maya Chen", email: "maya.chen@atlascommerce.com", phone: "+91 98765 20411", location: "Mumbai, India", mrr: "₹2.84L", renewal: "18 days", joined: "Aug 2022", lastSeen: "Today, 09:42", note: "Product usage has fallen sharply across the finance and operations teams. Intervention is recommended before the renewal window.", nextAction: "Schedule executive check-in", aiSummary: "Atlas Commerce is showing a high likelihood of churn because product usage has dropped 31% across two core teams while the renewal window is only 18 days away. The account still represents material recurring revenue, so a senior check-in is the clearest near-term intervention.", aiReasons: ["Usage is down 31% week over week", "Enterprise renewal is inside the next 30 days", "Finance and operations adoption are both softening"] },
  { initials: "NW", name: "Northwind Labs", plan: "Growth", score: "73%", scoreValue: 73, signal: "Renewal in 18 days", tone: "amber", owner: "Arjun Mehta", email: "arjun.mehta@northwindlabs.com", phone: "+91 98111 44820", location: "Bengaluru, India", mrr: "₹1.62L", renewal: "18 days", joined: "Jan 2023", lastSeen: "Yesterday, 16:18", note: "Renewal proximity is the dominant risk factor. Usage remains stable, but engagement with the account team is low.", nextAction: "Send renewal health summary", aiSummary: "Northwind Labs is in a watch state. The account remains active, but the renewal deadline and a quiet account-team relationship reduce the margin for error. A concise value recap should be sent before risk compounds.", aiReasons: ["Renewal is 18 days away", "Account-team engagement is below baseline", "Core usage is stable, creating an intervention window"] },
  { initials: "SP", name: "Solace Partners", plan: "Enterprise", score: "68%", scoreValue: 68, signal: "Support sentiment ↓", tone: "amber", owner: "Priya Nair", email: "priya.nair@solacepartners.com", phone: "+91 99201 18345", location: "Pune, India", mrr: "₹2.17L", renewal: "42 days", joined: "Mar 2022", lastSeen: "Yesterday, 11:05", note: "Recent support interactions contain more negative sentiment than the account baseline.", nextAction: "Review open support threads" },
  { initials: "OR", name: "Orbit Retail", plan: "Scale", score: "61%", scoreValue: 61, signal: "No admin login", tone: "blue", owner: "Devika Rao", email: "devika.rao@orbitretail.com", phone: "+91 98450 70219", location: "Delhi, India", mrr: "₹86K", renewal: "67 days", joined: "Sep 2024", lastSeen: "3 days ago", note: "The account is healthy enough to monitor, but the primary administrator has not logged in recently.", nextAction: "Share new workflow guide" },
];

const reportRows = [
  ["Jan", 74, 24], ["Feb", 78, 22], ["Mar", 75, 26], ["Apr", 81, 19], ["May", 84, 16], ["Jun", 86, 14], ["Jul", 89, 11],
];

function downloadFile(filename: string, content: BlobPart, type: string) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}

function makePdfReport() {
  const lines = ["CHURNIQ / RETENTION & RISK REPORT", "Generated 14 July 2025", "", "Month       Retained %       At risk %", ...reportRows.map(([month, retained, risk]) => `${String(month).padEnd(12)}${String(retained).padEnd(17)}${risk}`), "", "Portfolio risk distribution", "Low risk  62%", "Watch     24%", "High risk 14%", "", "At-risk revenue: ₹18.6L", "Model F1 score: 61.75%"];
  const escapePdf = (value: string) => value;
  const stream = ["BT", "/F1 11 Tf", "50 760 Td", ...lines.map((line, index) => `(${escapePdf(line)}) Tj 0 -16 Td`), "ET"].join("\\n");
  const objects = ["<< /Type /Catalog /Pages 2 0 R >>", "<< /Type /Pages /Kids [3 0 R] /Count 1 >>", "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>", "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>", `<< /Length ${stream.length} >>\\nstream\\n${stream}\\nendstream`];
  let pdf = "%PDF-1.4\\n";
  const offsets = [0];
  objects.forEach((object, index) => { offsets[index + 1] = pdf.length; pdf += `${index + 1} 0 obj\\n${object}\\nendobj\\n`; });
  const xref = pdf.length;
  pdf += `xref\\n0 ${objects.length + 1}\\n0000000000 65535 f \\n`;
  offsets.slice(1).forEach((offset) => { pdf += `${String(offset).padStart(10, "0")} 00000 n \\n`; });
  pdf += `trailer\\n<< /Size ${objects.length + 1} /Root 1 0 R >>\\nstartxref\\n${xref}\\n%%EOF`;
  return pdf;
}

const nav = [
  { label: "Overview", icon: LayoutDashboard },
  { label: "Churn signals", icon: Activity },
  { label: "Customers", icon: Users },
  { label: "Model health", icon: Gauge },
];

function ChartTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  return <div className="chart-tooltip"><span className="tooltip-label">{label}</span>{payload.map((item: any) => <div className="tooltip-row" key={item.dataKey}><i style={{ background: item.color }} /><span>{item.name === "retained" ? "Retained" : "At risk"}</span><strong>{item.value}%</strong><em>{item.dataKey === "retained" ? "+" : "−"}{item.dataKey === "retained" ? Math.abs(item.payload.retained - 74).toFixed(1) : Math.abs(item.payload.risk - 24).toFixed(1)} pts vs Jan</em></div>)}</div>;
}

function MetricCard({ label, value, change, detail, icon: Icon, accent = "teal" }: any) {
  return (
    <article className={`metric-card metric-${accent}`}>
      <div className="metric-top"><span>{label}</span><Icon size={17} strokeWidth={1.8} /></div>
      <div className="metric-value">{value}</div>
      <div className="metric-foot"><span className={change.startsWith("+") ? "positive" : "negative"}>{change}</span><span>{detail}</span></div>
      <div className="mini-spark" aria-hidden="true"><span /><span /><span /><span /><span /><span /><span /></div>
    </article>
  );
}

export default function Home() {
  const [activeNav, setActiveNav] = useState("Overview");
  const [mobileOpen, setMobileOpen] = useState(false);
  const [period, setPeriod] = useState("Last 30 days");
  const [selectedCustomer, setSelectedCustomer] = useState<any>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [riskFilter, setRiskFilter] = useState("All risk");
  const [sortBy, setSortBy] = useState("risk-desc");
  const [selectedCustomers, setSelectedCustomers] = useState<string[]>([]);
  const [bulkAssignee, setBulkAssignee] = useState("Maya Chen");
  const [bulkTag, setBulkTag] = useState("");
  const [emailDraftOpen, setEmailDraftOpen] = useState(false);
  const [appliedTags, setAppliedTags] = useState<Record<string, string[]>>({});

  const visibleCustomers = customers.filter((customer) => {
    const matchesSearch = `${customer.name} ${customer.plan} ${customer.signal}`.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRisk = riskFilter === "All risk" || (riskFilter === "High risk" && customer.scoreValue >= 75) || (riskFilter === "Watch" && customer.scoreValue >= 60 && customer.scoreValue < 75) || (riskFilter === "Monitor" && customer.scoreValue < 60);
    return matchesSearch && matchesRisk;
  }).sort((a, b) => sortBy === "risk-desc" ? b.scoreValue - a.scoreValue : sortBy === "risk-asc" ? a.scoreValue - b.scoreValue : a.name.localeCompare(b.name));

  const allVisibleSelected = visibleCustomers.length > 0 && visibleCustomers.every((customer) => selectedCustomers.includes(customer.name));

  const toggleCustomer = (name: string) => setSelectedCustomers((current) => current.includes(name) ? current.filter((item) => item !== name) : [...current, name]);
  const toggleAllVisible = () => setSelectedCustomers((current) => allVisibleSelected ? current.filter((name) => !visibleCustomers.some((customer) => customer.name === name)) : Array.from(new Set([...current, ...visibleCustomers.map((customer) => customer.name)])));
  const assignSelected = () => {
    if (!selectedCustomers.length) return;
    toast.success(`${selectedCustomers.length} account${selectedCustomers.length === 1 ? "" : "s"} assigned`, { description: `The selected attention queue accounts are now assigned to ${bulkAssignee}.` });
    setSelectedCustomers([]);
  };
  const applyBulkTag = () => {
    const normalizedTag = bulkTag.trim().replace(/^#/, "");
    if (!selectedCustomers.length || !normalizedTag) return;
    setAppliedTags((current) => selectedCustomers.reduce((next, name) => ({ ...next, [name]: Array.from(new Set([...(next[name] || []), normalizedTag])) }), current));
    toast.success(`Tag #${normalizedTag} applied`, { description: `${selectedCustomers.length} selected account${selectedCustomers.length === 1 ? "" : "s"} updated.` });
    setBulkTag("");
  };
  const activityFor = (customer: any) => [
    { type: "interaction", title: "Customer success check-in logged", detail: `Reviewed ${customer.signal.toLowerCase()} with ${customer.owner}.`, time: "Today · 09:42", icon: Phone },
    { type: "status", title: "Risk status changed to attention", detail: `Model score moved to ${customer.score} after the latest signal refresh.`, time: "Yesterday · 16:18", icon: Activity },
    { type: "assignee", title: `Assigned to ${customer.owner}`, detail: "Ownership updated from the retention operations queue.", time: "12 Jul · 11:05", icon: Users },
    { type: "interaction", title: "Account activity synced", detail: `Latest customer activity received from ${customer.location}.`, time: "08 Jul · 14:26", icon: Clock3 },
  ];
  const generateEmailDraft = (customer: any) => `Subject: A quick check-in on ${customer.name}\\n\\nHi ${customer.owner.split(" ")[0]},\\n\\nI wanted to reach out because we noticed a few changes in your recent account activity. ${customer.aiSummary || customer.note}\\n\\nWould you be open to a 20-minute conversation this week? We can review what is working, answer any open questions, and make sure your team is getting the most value from the platform.\\n\\nBest,\\nRiya\\nCustomer Success`;

  const exportCsv = () => {
    const csv = [["Month", "Retained %", "At risk %"], ...reportRows].map((row) => row.join(",")).join("\\n");
    downloadFile("churniq-retention-risk-report.csv", csv, "text/csv;charset=utf-8");
    toast.success("CSV report downloaded", { description: "Retention and risk trend data is ready to share." });
  };

  const exportPdf = () => {
    downloadFile("churniq-retention-risk-report.pdf", makePdfReport(), "application/pdf");
    toast.success("PDF report downloaded", { description: "Your retention and risk summary is ready." });
  };

  const comingSoon = (message: string) => toast(message, { description: "This interaction is staged for the next product release." });

  return (
    <div className="app-shell">
      <aside className={`sidebar ${mobileOpen ? "open" : ""}`}>
        <div className="brand-lockup">
          <div className="brand-mark"><img src="/manus-storage/churniq-logo_31201a36.png" alt="" /></div>
          <div><div className="brand-name">churn<span>IQ</span></div><div className="brand-caption">Retention intelligence</div></div>
          <button className="mobile-close" onClick={() => setMobileOpen(false)} aria-label="Close navigation"><X size={18} /></button>
        </div>
        <div className="workspace-switcher"><div className="workspace-avatar">AC</div><div><span>Workspace</span><strong>Acme Cloud</strong></div><ChevronDown size={15} /></div>
        <div className="nav-label">Workspace</div>
        <nav>{nav.map(({ label, icon: Icon }) => <button key={label} className={activeNav === label ? "nav-item active" : "nav-item"} onClick={() => { setActiveNav(label); setMobileOpen(false); }}><Icon size={18} /><span>{label}</span>{label === "Churn signals" && <span className="nav-count">14</span>}</button>)}</nav>
        <div className="nav-label lower">Manage</div>
        <nav><button className="nav-item" onClick={() => comingSoon("Customer segments are coming soon")}><Target size={18} /><span>Segments</span></button><button className="nav-item" onClick={() => comingSoon("Settings are coming soon")}><Settings2 size={18} /><span>Settings</span></button></nav>
        <div className="sidebar-bottom"><div className="model-status"><span className="status-dot" /><div><span>Model status</span><strong>Ready to predict</strong></div><ShieldCheck size={17} /></div><div className="user-row"><div className="user-avatar">RS</div><div><strong>Riya Shah</strong><span>Admin</span></div><MoreHorizontal size={18} /></div></div>
      </aside>
      {mobileOpen && <button className="scrim" onClick={() => setMobileOpen(false)} aria-label="Close navigation" />}
      <main className="main-content">
        <header className="topbar"><button className="mobile-menu" onClick={() => setMobileOpen(true)} aria-label="Open navigation"><Menu size={20} /></button><div className="breadcrumb"><span>Workspace</span><span>/</span><strong>{activeNav}</strong></div><div className="top-actions"><button className="icon-button" onClick={() => comingSoon("Search is coming soon")} aria-label="Search"><Search size={18} /></button><button className="icon-button has-dot" onClick={() => comingSoon("You have 3 new signal alerts")} aria-label="Notifications"><Bell size={18} /></button><button className="help-button" onClick={() => comingSoon("Help center is coming soon")}><CircleHelp size={17} /> Help center</button></div></header>
        <div className="content-wrap">
          <section className="hero-row"><div><div className="eyebrow"><span className="eyebrow-line" /> Monday, 14 July 2025</div><h1>Good morning, Riya.</h1><p className="hero-copy">Here’s where retention pressure is building across your customer base.</p></div><div className="hero-actions"><div className="export-actions"><button className="secondary-button" onClick={exportCsv}><Download size={15} /> CSV</button><button className="secondary-button" onClick={exportPdf}><FileText size={15} /> PDF</button></div><button className="primary-button" onClick={() => comingSoon("New prediction run is coming soon")}><Zap size={16} /> Run prediction</button></div></section>
          <section className="signal-banner"><div className="signal-icon"><Sparkles size={18} /></div><div><span className="signal-kicker">Signal of the day</span><strong>High-value accounts showing early friction</strong><p>14 enterprise customers have a rising risk score this week. A focused intervention could protect <b>₹8.4L</b> in recurring revenue.</p></div><button onClick={() => comingSoon("Signal details are coming soon")}>Open signal <ArrowUpRight size={16} /></button></section>
          <section className="section-heading"><div><span className="section-index">01 / Snapshot</span><h2>Model & business pulse</h2></div><div className="period-select"><span>Viewing</span><select value={period} onChange={(e) => setPeriod(e.target.value)}><option>Last 30 days</option><option>Last 90 days</option><option>This year</option></select><ChevronDown size={14} /></div></section>
          <section className="metric-grid"><MetricCard label="Customers monitored" value="2,480" change="+8.2%" detail="vs. previous period" icon={Users} accent="blue" /><MetricCard label="At-risk revenue" value="₹18.6L" change="−4.1%" detail="vs. previous period" icon={ArrowUpRight} accent="coral" /><MetricCard label="Model F1 score" value="61.75%" change="+2.4 pts" detail="vs. last validation" icon={Gauge} accent="violet" /><MetricCard label="Prediction coverage" value="94.2%" change="+1.8%" detail="of active accounts" icon={ShieldCheck} accent="teal" /></section>
          <section className="dashboard-grid"><article className="panel trend-panel"><div className="panel-heading"><div><span className="panel-kicker">Retention signal</span><h3>Churn risk is cooling</h3><p>High-risk accounts as a share of all active customers.</p></div><button className="panel-menu" onClick={() => comingSoon("Chart options are coming soon")}><MoreHorizontal size={19} /></button></div><div className="chart-legend"><span><i className="legend-dot teal" /> Retained</span><span><i className="legend-dot coral" /> At risk</span></div><div className="trend-chart"><ResponsiveContainer width="100%" height="100%"><AreaChart data={trendData} margin={{ top: 12, right: 8, left: -22, bottom: 0 }}><defs><linearGradient id="retainedFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#2BC6B4" stopOpacity={0.22} /><stop offset="100%" stopColor="#2BC6B4" stopOpacity={0} /></linearGradient><linearGradient id="riskFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#F17B63" stopOpacity={0.16} /><stop offset="100%" stopColor="#F17B63" stopOpacity={0} /></linearGradient></defs><CartesianGrid stroke="#E8EDF1" vertical={false} /><XAxis dataKey="month" tick={{ fill: "#86929D", fontSize: 11 }} axisLine={false} tickLine={false} /><YAxis tick={{ fill: "#86929D", fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={(v) => `${v}%`} /><Tooltip content={<ChartTooltip />} cursor={{ stroke: "#9AA9B3", strokeDasharray: "3 3" }} /><Area type="monotone" dataKey="retained" stroke="#2BC6B4" strokeWidth={3} fill="url(#retainedFill)" /><Area type="monotone" dataKey="risk" stroke="#F17B63" strokeWidth={2.5} fill="url(#riskFill)" /></AreaChart></ResponsiveContainer></div><div className="chart-foot"><span><b>−12.4%</b> high-risk share since January</span><span className="good-pill">Healthy trend <ArrowUpRight size={13} /></span></div></article>
            <article className="panel mix-panel"><div className="panel-heading"><div><span className="panel-kicker">Portfolio mix</span><h3>Risk distribution</h3><p>Current customer classification.</p></div></div><div className="donut-wrap"><ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={segmentData} dataKey="value" innerRadius={62} outerRadius={84} paddingAngle={4} stroke="none"><Cell fill="#2BC6B4" /><Cell fill="#6D7CF5" /><Cell fill="#F17B63" /></Pie></PieChart></ResponsiveContainer><div className="donut-center"><strong>2,480</strong><span>accounts</span></div></div><div className="mix-legend">{segmentData.map((item) => <div key={item.name}><span><i style={{ background: item.color }} />{item.name}</span><strong>{item.value}%</strong></div>)}</div></article>
            <article className="panel segment-panel"><div className="panel-heading"><div><span className="panel-kicker">Revenue exposure</span><h3>Risk by segment</h3></div><button className="panel-menu" onClick={() => comingSoon("Segment filters are coming soon")}><Filter size={17} /></button></div><div className="segment-chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={[{ name: "Enterprise", value: 82 }, { name: "Growth", value: 54 }, { name: "Scale", value: 38 }, { name: "Starter", value: 21 }]} layout="vertical" margin={{ left: 16, right: 16, top: 4, bottom: 4 }}><XAxis type="number" hide /><YAxis type="category" dataKey="name" axisLine={false} tickLine={false} tick={{ fill: "#62707C", fontSize: 11 }} width={72} /><Bar dataKey="value" radius={[0, 5, 5, 0]} barSize={12} fill="#6D7CF5"><Cell fill="#F17B63" /><Cell fill="#6D7CF5" /><Cell fill="#8B98F9" /><Cell fill="#B7C0FD" /></Bar></BarChart></ResponsiveContainer></div><p className="panel-note"><span className="risk-dot" /> Enterprise accounts carry <b>₹8.4L</b> of open exposure.</p></article>
          </section>
          <section className="section-heading compact"><div><span className="section-index">02 / Attention queue</span><h2>Accounts worth a closer look</h2></div><span className="queue-count">{visibleCustomers.length} of {customers.length} accounts</span></section>
          <section className="queue-controls"><div className="queue-search"><Search size={15} /><input value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} placeholder="Search customers or signals" aria-label="Search customers or signals" /></div><div className="queue-select"><SlidersHorizontal size={14} /><select value={riskFilter} onChange={(e) => setRiskFilter(e.target.value)} aria-label="Filter by risk"><option>All risk</option><option>High risk</option><option>Watch</option><option>Monitor</option></select><ChevronDown size={13} /></div><div className="queue-select"><select value={sortBy} onChange={(e) => setSortBy(e.target.value)} aria-label="Sort customers"><option value="risk-desc">Highest risk</option><option value="risk-asc">Lowest risk</option><option value="name">Customer name</option></select><ChevronDown size={13} /></div>{(searchTerm || riskFilter !== "All risk") && <button className="clear-filter" onClick={() => { setSearchTerm(""); setRiskFilter("All risk"); }}><XCircle size={14} /> Clear</button>}{selectedCustomers.length > 0 && <div className="bulk-actions"><span>{selectedCustomers.length} selected</span><select value={bulkAssignee} onChange={(e) => setBulkAssignee(e.target.value)} aria-label="Assign selected customers"><option>Maya Chen</option><option>Arjun Mehta</option><option>Priya Nair</option><option>Devika Rao</option></select><button className="assign-button" onClick={assignSelected}>Assign selected</button><div className="bulk-tag-input"><Tag size={13} /><input value={bulkTag} onChange={(e) => setBulkTag(e.target.value)} placeholder="custom tag" aria-label="Custom tag" onKeyDown={(event) => { if (event.key === "Enter") applyBulkTag(); }} /></div><button className="tag-button" onClick={applyBulkTag} disabled={!bulkTag.trim()}><Tag size={13} /> Apply tag</button></div>}</section>
          <section className="panel customer-panel"><div className="customer-table-head"><label className="select-cell"><input type="checkbox" checked={allVisibleSelected} onChange={toggleAllVisible} aria-label="Select all visible customers" /></label><span>Customer</span><span>Plan</span><span>Risk score</span><span>Latest signal</span><span /></div>{visibleCustomers.map((customer) => <button className={`customer-row ${selectedCustomers.includes(customer.name) ? "selected" : ""}`} key={customer.name} onClick={() => setSelectedCustomer(customer)}><label className="select-cell" onClick={(event) => event.stopPropagation()}><input type="checkbox" checked={selectedCustomers.includes(customer.name)} onChange={() => toggleCustomer(customer.name)} aria-label={`Select ${customer.name}`} /></label><div className="customer-name"><div className={`customer-avatar ${customer.tone}`}>{customer.initials}</div><div><strong>{customer.name}</strong><span>Updated {customer.lastSeen}</span></div></div><span className="plan-tag">{customer.plan}</span><div className="score-cell"><strong className={customer.tone === "coral" ? "score-coral" : "score-amber"}>{customer.score}</strong><div className="score-bar"><span style={{ width: customer.score }} /></div></div><span className="signal-cell"><i className={`signal-marker ${customer.tone}`} />{customer.signal}{appliedTags[customer.name]?.map((tag) => <small className="row-tag" key={tag}>#{tag}</small>)}</span><ArrowUpRight size={17} className="row-arrow" /></button>)}{visibleCustomers.length === 0 && <div className="empty-queue">No accounts match these queue controls. Try widening the risk filter.</div>}</section>
          <footer><span>ChurnIQ <b>·</b> Retention intelligence for teams who act early.</span><span>Model v2.4 <b>·</b> Updated 14 Jul 2025</span></footer>
        </div>
      </main>
      {selectedCustomer && <div className="modal-backdrop" role="presentation" onClick={() => setSelectedCustomer(null)}><section className="profile-modal" role="dialog" aria-modal="true" aria-labelledby="profile-title" onClick={(event) => event.stopPropagation()}><div className="modal-head"><div><span className="panel-kicker">Customer profile / Attention queue</span><h2 id="profile-title">{selectedCustomer.name}</h2></div><button className="modal-close" onClick={() => setSelectedCustomer(null)} aria-label="Close customer profile"><X size={19} /></button></div><div className="profile-summary"><div className={`profile-avatar ${selectedCustomer.tone}`}>{selectedCustomer.initials}</div><div><strong>{selectedCustomer.owner}</strong><span>{selectedCustomer.plan} account owner</span></div><div className={`profile-score ${selectedCustomer.tone}`}><span>Risk score</span><strong>{selectedCustomer.score}</strong></div></div><div className="profile-grid"><div><span>Monthly recurring revenue</span><strong>{selectedCustomer.mrr}</strong></div><div><span>Renewal window</span><strong>{selectedCustomer.renewal}</strong></div><div><span>Customer since</span><strong>{selectedCustomer.joined}</strong></div><div><span>Last active</span><strong>{selectedCustomer.lastSeen}</strong></div></div><div className="profile-note"><span className="section-index">Latest signal</span><h3>{selectedCustomer.signal}</h3><p>{selectedCustomer.note}</p></div><div className="ai-summary"><div className="ai-summary-head"><span className="ai-spark">✦</span><div><span className="section-index">AI risk summary</span><strong>Why this account needs attention</strong></div><span className="ai-badge">Generated from account signals</span></div><p>{selectedCustomer.aiSummary || `${selectedCustomer.name} is currently flagged because ${selectedCustomer.signal.toLowerCase()}. The model recommends reviewing the latest account activity and taking the next action before the risk score increases.`}</p><div className="ai-reasons">{(selectedCustomer.aiReasons || [selectedCustomer.signal, `${selectedCustomer.plan} account requiring active monitoring`, `Current risk score is ${selectedCustomer.score}`]).map((reason: string) => <span key={reason}><i />{reason}</span>)}</div></div><div className="timeline-section"><div className="timeline-heading"><div><span className="section-index">Activity timeline</span><h3>Recent account history</h3></div><span>{activityFor(selectedCustomer).length} events</span></div><div className="activity-timeline">{activityFor(selectedCustomer).map((event: any) => { const EventIcon = event.icon; return <div className="timeline-event" key={`${event.title}-${event.time}`}><div className={`timeline-icon ${event.type}`}><EventIcon size={14} /></div><div className="timeline-copy"><strong>{event.title}</strong><p>{event.detail}</p><span>{event.time}</span></div></div>; })}</div></div><div className="profile-contact"><a href={`mailto:${selectedCustomer.email}`}><Mail size={15} /> {selectedCustomer.email}</a><a href={`tel:${selectedCustomer.phone}`}><Phone size={15} /> {selectedCustomer.phone}</a><span><MapPin size={15} /> {selectedCustomer.location}</span></div>{emailDraftOpen && <div className="email-draft"><div className="email-draft-head"><div><span className="section-index">Re-engagement draft</span><strong>Personalized outreach</strong></div><button onClick={() => setEmailDraftOpen(false)} aria-label="Close email draft"><X size={15} /></button></div><pre>{generateEmailDraft(selectedCustomer)}</pre><div className="email-draft-actions"><button className="secondary-button" onClick={() => { navigator.clipboard?.writeText(generateEmailDraft(selectedCustomer)); toast.success("Email draft copied"); }}><FileText size={14} /> Copy draft</button><a className="primary-button" href={`mailto:${selectedCustomer.email}?subject=${encodeURIComponent(`A quick check-in on ${selectedCustomer.name}`)}&body=${encodeURIComponent(generateEmailDraft(selectedCustomer).split("\\n\\n").slice(1).join("\\n\\n"))}`}><Send size={14} /> Open in email</a></div></div>}<div className="modal-actions"><button className="secondary-button" onClick={() => setEmailDraftOpen(true)}><Mail size={15} /> Generate email draft</button><button className="primary-button" onClick={() => comingSoon(selectedCustomer.nextAction)}><Zap size={15} /> {selectedCustomer.nextAction}</button></div></section></div>}
    </div>
  );
}
