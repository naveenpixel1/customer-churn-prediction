import os
import base64
import streamlit as st

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

def inject_particles():
    """Injects a subtle light particle canvas background."""
    st.markdown(
        """
<canvas id="particle-canvas" style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:0; pointer-events:none; opacity:0.4;"></canvas>
<script>
(function() {
    var canvas = document.getElementById('particle-canvas');
    if (!canvas || canvas._initialized) return;
    canvas._initialized = true;
    var ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    window.addEventListener('resize', function() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
    var particles = [];
    var count = 40;
    var colors = ['rgba(108,99,255,', 'rgba(0,212,170,', 'rgba(100,116,139,', 'rgba(79,70,229,'];
    for (var i = 0; i < count; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            r: Math.random() * 2 + 1,
            dx: (Math.random() - 0.5) * 0.25,
            dy: (Math.random() - 0.5) * 0.25,
            color: colors[Math.floor(Math.random() * colors.length)],
            alpha: Math.random() * 0.25 + 0.08
        });
    }
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (var i = 0; i < particles.length; i++) {
            for (var j = i + 1; j < particles.length; j++) {
                var dx = particles[i].x - particles[j].x;
                var dy = particles[i].y - particles[j].y;
                var dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < 110) {
                    ctx.beginPath();
                    ctx.strokeStyle = particles[i].color + (0.07 * (1 - dist/110)) + ')';
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
        for (var i = 0; i < particles.length; i++) {
            var p = particles[i];
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = p.color + p.alpha + ')';
            ctx.fill();
            p.x += p.dx;
            p.y += p.dy;
            if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
        }
        requestAnimationFrame(draw);
    }
    draw();
})();
</script>
        """,
        unsafe_allow_html=True
    )

def inject_premium_styles():
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">',
        unsafe_allow_html=True
    )

    inject_particles()

    st.markdown(
        """
        <style>
        /* Plus Jakarta Sans globally */
        html, body, .stMarkdown, p, label, li, button, input, select,
        h1, h2, h3, h4, h5, h6, [data-testid="stHeader"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        /* ===== MAIN CONTAINER PADDING & LAYOUT ===== */
        .block-container, [data-testid="stMainBlockContainer"] {
            padding-top: 3.5rem !important;
            padding-bottom: 3rem !important;
            max-width: 1300px !important;
        }

        /* ===== LIGHT MODE BACKGROUND ===== */
        [data-testid="stAppViewContainer"] {
            background-color: #F8FAFC !important;
            background-image:
                radial-gradient(circle at 10% 10%, rgba(108,99,255,0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 90%, rgba(0,212,170,0.04) 0%, transparent 40%) !important;
            background-attachment: fixed !important;
            color: #1E293B !important;
        }

        [data-testid="stHeader"] {
            background-color: #F8FAFC !important;
            border-bottom: 1px solid #E2E8F0 !important;
        }

        /* Light Sidebar */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
            box-shadow: 2px 0 10px rgba(0,0,0,0.02) !important;
        }
        [data-testid="stSidebar"] * {
            color: #334155 !important;
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #F1F5F9; }
        ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #6C63FF; }

        /* Gradient text */
        .gradient-text {
            background: linear-gradient(120deg, #4F46E5, #6C63FF, #00D4AA) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 800;
            display: inline-block;
        }
        .glowing-title {
            font-weight: 800 !important;
            color: #0F172A !important;
            margin-bottom: 12px !important;
            letter-spacing: -0.5px !important;
        }

        /* Subheaders */
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3,
        div[data-testid="stMarkdownContainer"] h4,
        .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
            color: #0F172A !important;
            font-weight: 700 !important;
        }
        div[data-testid="stMarkdownContainer"] p,
        .stMarkdown p {
            color: #334155 !important;
            line-height: 1.6 !important;
        }

        /* ===== CLEAN LIGHT CARDS ===== */
        .glass-card, div[data-testid="stVerticalBlockBorder"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 16px !important;
            padding: 24px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 4px 12px -2px rgba(15,23,42,0.05),
                        0 2px 4px -1px rgba(15,23,42,0.03) !important;
            transition: all 0.25s ease !important;
            color: #1E293B !important;
        }
        .glass-card h1, .glass-card h2, .glass-card h3, .glass-card h4 {
            color: #0F172A !important;
            font-weight: 700 !important;
        }
        .glass-card p, .glass-card span {
            color: #334155 !important;
            line-height: 1.5 !important;
        }
        .glass-card:hover, div[data-testid="stVerticalBlockBorder"]:hover {
            border-color: #CBD5E1 !important;
            box-shadow: 0 10px 20px -3px rgba(108,99,255,0.08),
                        0 4px 6px -2px rgba(15,23,42,0.04) !important;
        }

        /* KPI Cards */
        .kpi-card {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-left: 4px solid #6C63FF !important;
            border-radius: 12px !important;
            padding: 16px 18px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        .kpi-card:hover {
            transform: translateY(-2px) !important;
            border-left-color: #00D4AA !important;
            box-shadow: 0 6px 16px rgba(108,99,255,0.1) !important;
        }
        .kpi-title {
            color: #64748B !important;
            font-size: 12px !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            margin-bottom: 4px !important;
        }
        .kpi-value {
            color: #0F172A !important;
            font-size: 26px !important;
            font-weight: 800 !important;
            margin: 0 !important;
        }

        /* Verdict / Risk Box */
        .verdict-box {
            border-radius: 14px !important;
            padding: 20px !important;
            margin-bottom: 18px !important;
            border: 1px solid #E2E8F0 !important;
            border-left: 6px solid !important;
            background: #FFFFFF !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.04) !important;
        }

        /* Retention Driver Cards */
        .driver-card {
            background: #F8FAFC !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px !important;
            padding: 16px !important;
            margin-bottom: 10px !important;
        }
        .driver-card.accelerator {
            border-left: 4px solid #EF4444 !important;
            background: #FEF2F2 !important;
        }
        .driver-card.protective {
            border-left: 4px solid #0D9488 !important;
            background: #F0FDF4 !important;
        }

        /* Insight Cards */
        .insight-card {
            border-left: 5px solid #D97706 !important;
            background: #FFFBEB !important;
            padding: 18px !important;
            border-radius: 12px !important;
            margin-bottom: 14px !important;
            border: 1px solid #FDE68A !important;
        }
        .insight-card.danger {
            border-left-color: #EF4444 !important;
            background: #FEF2F2 !important;
            border-color: #FCA5A5 !important;
        }
        .insight-card.success {
            border-left-color: #0D9488 !important;
            background: #F0FDF4 !important;
            border-color: #A7F3D0 !important;
        }

        /* Form Widgets */
        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 10px !important;
            color: #0F172A !important;
            transition: all 0.2s ease;
        }
        div[data-baseweb="select"] > div:hover {
            border-color: #6C63FF !important;
        }
        input {
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 10px !important;
            color: #0F172A !important;
        }
        input:focus {
            border-color: #6C63FF !important;
            box-shadow: 0 0 0 3px rgba(108,99,255,0.15) !important;
        }

        /* Prominent Indigo Button */
        .stButton>button {
            background: #6C63FF !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 14px 28px !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            letter-spacing: 0.3px !important;
            box-shadow: 0 4px 14px rgba(108,99,255,0.3) !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
        }
        .stButton>button:hover {
            background: #4F46E5 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(79,70,229,0.4) !important;
            color: #FFFFFF !important;
        }
        .stButton>button:active {
            transform: translateY(0) !important;
        }

        /* Expanders */
        .streamlit-expanderHeader {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 10px !important;
            color: #0F172A !important;
            font-weight: 600 !important;
        }

        /* Honeypot bot-trap field: visually hidden from real users (Item #12) */
        [data-testid="stTextInput"][aria-label="Leave this field empty"],
        div[data-testid="stTextInput"]:has(input[aria-label="Leave this field empty"]) {
            position: absolute !important;
            left: -9999px !important;
            height: 0 !important;
            overflow: hidden !important;
            opacity: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
