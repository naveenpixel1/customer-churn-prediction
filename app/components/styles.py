import os
import base64
import streamlit as st

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

def inject_particles():
    """Injects a live animated neural-net particle canvas as a fixed background via JS."""
    st.markdown(
        """
<canvas id="particle-canvas" style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:0; pointer-events:none;"></canvas>
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
    var count = 70;
    var colors = ['rgba(108,99,255,', 'rgba(0,212,170,', 'rgba(255,107,107,', 'rgba(59,130,246,'];
    for (var i = 0; i < count; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            r: Math.random() * 2 + 0.5,
            dx: (Math.random() - 0.5) * 0.4,
            dy: (Math.random() - 0.5) * 0.4,
            color: colors[Math.floor(Math.random() * colors.length)],
            alpha: Math.random() * 0.5 + 0.2
        });
    }
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (var i = 0; i < particles.length; i++) {
            for (var j = i + 1; j < particles.length; j++) {
                var dx = particles[i].x - particles[j].x;
                var dy = particles[i].y - particles[j].y;
                var dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < 130) {
                    ctx.beginPath();
                    ctx.strokeStyle = particles[i].color + (0.12 * (1 - dist/130)) + ')';
                    ctx.lineWidth = 0.6;
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
    # Inject Google Font stylesheet link directly into DOM
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">',
        unsafe_allow_html=True
    )

    # Load and encode local background image
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    bg_path = os.path.join(assets_dir, "background.png")
    bg_base64 = get_base64_image(bg_path)

    if bg_base64:
        bg_style = f"background-image: url('data:image/png;base64,{bg_base64}') !important;"
    else:
        bg_style = """
            background-color: #070814 !important;
            background-image:
                radial-gradient(circle at 10% 20%, rgba(108, 99, 255, 0.12) 0%, transparent 45%),
                radial-gradient(circle at 90% 80%, rgba(0, 212, 170, 0.1) 0%, transparent 45%),
                radial-gradient(circle at 50% 50%, rgba(255, 107, 107, 0.04) 0%, transparent 55%) !important;
        """

    # Inject particle canvas
    inject_particles()

    st.markdown(
        f"""
        <style>
        /* Apply fonts globally */
        html, body, .stMarkdown, p, label, li, button, input, select, h1, h2, h3, h4, h5, h6 {{
            font-family: 'Plus Jakarta Sans', 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }}

        /* ===================== BACKGROUND ===================== */
        [data-testid="stAppViewContainer"] {{
            background-color: #070814 !important;
            {bg_style}
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}

        /* Make header solid to hide content scrolling under it */
        [data-testid="stHeader"] {{
            background-color: #070814 !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
        }}

        /* Floating Translucent Glass Sidebar */
        [data-testid="stSidebar"] {{
            background-color: rgba(7, 8, 20, 0.85) !important;
            border-right: 1px solid rgba(108, 99, 255, 0.18) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
        }}

        /* ===================== SCROLLBAR ===================== */
        ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        ::-webkit-scrollbar-track {{ background: rgba(7, 9, 19, 0.5); }}
        ::-webkit-scrollbar-thumb {{ background: rgba(108, 99, 255, 0.3); border-radius: 10px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: rgba(0, 212, 170, 0.5); }}

        /* ===================== RGB ANIMATIONS ===================== */
        @keyframes rgb-shimmer {{
            0%   {{ background-position: 0% 50%; }}
            50%  {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        @keyframes rgb-shadow {{
            0%   {{ text-shadow: 0 0 15px rgba(108,99,255,0.4),  0 0 30px rgba(108,99,255,0.15); }}
            33%  {{ text-shadow: 0 0 18px rgba(0,212,170,0.55),  0 0 35px rgba(0,212,170,0.25); }}
            66%  {{ text-shadow: 0 0 18px rgba(255,107,107,0.5), 0 0 35px rgba(255,107,107,0.2); }}
            100% {{ text-shadow: 0 0 15px rgba(108,99,255,0.4),  0 0 30px rgba(108,99,255,0.15); }}
        }}

        @keyframes rgb-border {{
            0%   {{ border-color: rgba(108,99,255,0.4); box-shadow: 0 0 8px rgba(108,99,255,0.2); }}
            33%  {{ border-color: rgba(0,212,170,0.5);  box-shadow: 0 0 8px rgba(0,212,170,0.25); }}
            66%  {{ border-color: rgba(255,107,107,0.4);box-shadow: 0 0 8px rgba(255,107,107,0.2); }}
            100% {{ border-color: rgba(108,99,255,0.4); box-shadow: 0 0 8px rgba(108,99,255,0.2); }}
        }}

        /* ===================== GRADIENT TEXT (h1) ===================== */
        .gradient-text {{
            background: linear-gradient(120deg, #8B5CF6, #00D4AA, #FF6B6B, #3B82F6, #8B5CF6) !important;
            background-size: 300% 300% !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 800;
            animation: rgb-shimmer 6s ease infinite !important;
            display: inline-block;
        }}

        /* ===================== GLOWING TITLES (.glowing-title) ===================== */
        .glowing-title {{
            font-weight: 800 !important;
            color: #FFFFFF !important;
            animation: rgb-shadow 6s ease-in-out infinite !important;
            margin-bottom: 18px !important;
            letter-spacing: -0.5px !important;
        }}

        /* ===================== NATIVE STREAMLIT SUBHEADERS ===================== */
        /* h2/h3 from st.subheader() — animated neon glow */
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3,
        .stMarkdown h2,
        .stMarkdown h3 {{
            animation: rgb-shadow 6s ease-in-out infinite !important;
            font-weight: 700 !important;
        }}

        /* ===================== CARD CONTAINERS ===================== */
        .glass-card, div[data-testid="stVerticalBlockBorder"] {{
            background: rgba(15, 17, 34, 0.8) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            border: 1px solid rgba(108, 99, 255, 0.22) !important;
            border-radius: 20px !important;
            padding: 28px !important;
            margin-bottom: 22px !important;
            box-shadow:
                0 15px 35px -10px rgba(0, 0, 0, 0.6),
                inset 0 1px 1px 0px rgba(255, 255, 255, 0.08) !important;
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
            animation: rgb-border 8s ease-in-out infinite !important;
        }}

        .glass-card:hover, div[data-testid="stVerticalBlockBorder"]:hover {{
            transform: translateY(-6px) !important;
            border-color: rgba(0, 212, 170, 0.5) !important;
            box-shadow:
                0 25px 45px -12px rgba(108, 99, 255, 0.25),
                0 0 25px 4px rgba(0, 212, 170, 0.15),
                inset 0 1px 1px 0px rgba(255, 255, 255, 0.15) !important;
        }}

        /* ===================== KPI CARDS ===================== */
        .kpi-card {{
            background: rgba(16, 18, 35, 0.85) !important;
            backdrop-filter: blur(6px) !important;
            border: 1px solid rgba(108, 99, 255, 0.18) !important;
            border-left: 6px solid #6C63FF !important;
            border-radius: 16px !important;
            padding: 20px 24px !important;
            margin-bottom: 15px !important;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5) !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        }}
        .kpi-card:hover {{
            transform: translateY(-4px) !important;
            border-left-color: #00D4AA !important;
            border-color: rgba(0, 212, 170, 0.3) !important;
            box-shadow: 0 12px 35px -8px rgba(0, 212, 170, 0.25) !important;
        }}
        .kpi-title {{
            color: #94A3B8 !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin-bottom: 8px !important;
        }}
        .kpi-value {{
            color: #FFFFFF !important;
            font-size: 28px !important;
            font-weight: 700 !important;
            margin: 0 !important;
        }}

        /* ===================== VERDICT / RISK BOX ===================== */
        .verdict-box {{
            border-radius: 16px !important;
            padding: 22px !important;
            margin-bottom: 20px !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-left: 6px solid !important;
            box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5) !important;
            backdrop-filter: blur(8px) !important;
        }}

        /* ===================== REC BOXES ===================== */
        .rec-box {{
            background: rgba(108, 99, 255, 0.03) !important;
            border: 1px solid rgba(108, 99, 255, 0.12) !important;
            border-radius: 10px !important;
            padding: 16px 20px !important;
            margin-bottom: 12px !important;
            transition: all 0.3s ease !important;
        }}
        .rec-box:hover {{
            background: rgba(108, 99, 255, 0.06) !important;
            border-color: rgba(108, 99, 255, 0.25) !important;
        }}

        /* ===================== INSIGHT CARDS ===================== */
        .insight-card {{
            border-left: 5px solid #FFB347 !important;
            background: rgba(255, 179, 71, 0.03) !important;
            padding: 18px !important;
            border-radius: 12px !important;
            margin-bottom: 14px !important;
            border-top: 1px solid rgba(255, 179, 71, 0.08) !important;
            border-right: 1px solid rgba(255, 179, 71, 0.08) !important;
            border-bottom: 1px solid rgba(255, 179, 71, 0.08) !important;
        }}
        .insight-card.danger {{
            border-left-color: #FF6B6B !important;
            background: rgba(255, 107, 107, 0.03) !important;
            border-color: rgba(255, 107, 107, 0.08) !important;
        }}
        .insight-card.success {{
            border-left-color: #00D4AA !important;
            background: rgba(0, 212, 170, 0.03) !important;
            border-color: rgba(0, 212, 170, 0.08) !important;
        }}

        /* ===================== FORM WIDGETS ===================== */
        div[data-baseweb="select"] > div {{
            background-color: rgba(12, 15, 32, 0.85) !important;
            border: 1px solid rgba(108, 99, 255, 0.25) !important;
            border-radius: 10px !important;
            color: #E2E8F0 !important;
            transition: all 0.3s ease;
        }}
        div[data-baseweb="select"] > div:hover {{
            border-color: rgba(0, 212, 170, 0.4) !important;
        }}
        input {{
            background-color: rgba(12, 15, 32, 0.85) !important;
            border: 1px solid rgba(108, 99, 255, 0.25) !important;
            border-radius: 10px !important;
            color: #E2E8F0 !important;
            transition: all 0.3s ease;
        }}
        input:focus {{
            border-color: #00D4AA !important;
            box-shadow: 0 0 10px rgba(0, 212, 170, 0.2) !important;
        }}

        /* ===================== BUTTONS ===================== */
        .stButton>button {{
            background: linear-gradient(135deg, #6C63FF 0%, #00D4AA 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 30px !important;
            padding: 12px 32px !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            letter-spacing: 0.5px !important;
            box-shadow: 0 6px 20px rgba(108, 99, 255, 0.25) !important;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        }}
        .stButton>button:hover {{
            transform: translateY(-3px) scale(1.02) !important;
            box-shadow:
                0 10px 25px rgba(108, 99, 255, 0.45),
                0 0 15px rgba(0, 212, 170, 0.3) !important;
            color: #FFFFFF !important;
        }}
        .stButton>button:active {{
            transform: translateY(-1px) scale(0.99) !important;
        }}

        /* ===================== EXPANDERS ===================== */
        .streamlit-expanderHeader {{
            background-color: rgba(17, 20, 38, 0.3) !important;
            border: 1px solid rgba(108, 99, 255, 0.15) !important;
            border-radius: 10px !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
