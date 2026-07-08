import streamlit as st

def inject_premium_styles():
    st.markdown(
        """
        <style>
        /* Import Outfit or Inter font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
        
        /* Apply fonts globally */
        html, body, [class*="css"], .stMarkdown {
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Set page padding adjustments */
        .reportview-container .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 95%;
        }

        /* Styled Sidebar container */
        [data-testid="stSidebar"] {
            background-color: rgba(14, 17, 28, 0.95) !important;
            border-right: 1px solid rgba(108, 99, 255, 0.1) !important;
            backdrop-filter: blur(10px);
        }

        /* Custom Sleek Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(14, 17, 28, 0.5);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(108, 99, 255, 0.3);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(108, 99, 255, 0.5);
        }

        /* Gradient Text utility */
        .gradient-text {
            background: linear-gradient(135deg, #6C63FF 0%, #FF6B6B 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 800;
        }

        /* Glassmorphism Card Container */
        .glass-card, div[data-testid="stVerticalBlockBorder"] {
            background: rgba(26, 29, 46, 0.65) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(108, 99, 255, 0.15) !important;
            border-radius: 16px !important;
            padding: 24px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        }
        
        .glass-card:hover, div[data-testid="stVerticalBlockBorder"]:hover {
            transform: translateY(-4px) !important;
            border-color: rgba(108, 99, 255, 0.35) !important;
            box-shadow: 0 12px 40px 0 rgba(108, 99, 255, 0.15) !important;
        }

        /* Mini KPI Metric Card */
        .kpi-card {
            background: linear-gradient(135deg, rgba(26, 29, 46, 0.8) 0%, rgba(20, 22, 37, 0.8) 100%);
            border-left: 4px solid #6C63FF;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .kpi-card:hover {
            transform: scale(1.02);
            border-left-color: #00D4AA;
        }

        .kpi-title {
            color: #94A3B8;
            font-size: 13px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.75px;
            margin-bottom: 6px;
        }

        .kpi-value {
            color: #FFFFFF;
            font-size: 26px;
            font-weight: 700;
            margin: 0;
        }

        /* Risk Metric Gauge styling */
        .verdict-box {
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            border-left: 5px solid;
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
            animation: pulse-border 2s infinite alternate;
        }
        
        @keyframes pulse-border {
            0% { box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); }
            100% { box-shadow: 0 8px 25px rgba(108, 99, 255, 0.15); }
        }

        /* Bullet recommendation boxes */
        .rec-box {
            background: rgba(108, 99, 255, 0.05);
            border: 1px solid rgba(108, 99, 255, 0.15);
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 10px;
        }

        /* Glowing titles */
        .glowing-title {
            font-weight: 700;
            color: #FFFFFF;
            text-shadow: 0 0 20px rgba(108, 99, 255, 0.35);
            margin-bottom: 15px;
        }

        /* Wizard progress indicator container */
        .step-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            background: rgba(26, 29, 46, 0.4);
            padding: 12px 20px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .step-node {
            display: flex;
            align-items: center;
            font-size: 14px;
            color: #94A3B8;
            font-weight: 500;
        }

        .step-node.active {
            color: #6C63FF;
            font-weight: 700;
        }

        .step-node.completed {
            color: #00D4AA;
        }

        .step-circle {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            border: 2px solid #94A3B8;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-right: 8px;
            font-size: 12px;
        }

        .step-node.active .step-circle {
            border-color: #6C63FF;
            background: rgba(108, 99, 255, 0.15);
            color: #6C63FF;
        }

        .step-node.completed .step-circle {
            border-color: #00D4AA;
            background: rgba(0, 212, 170, 0.15);
            color: #00D4AA;
        }

        /* Subtle micro-animations on elements */
        .fade-in {
            animation: fadeIn 0.8s ease-in-out forwards;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Custom buttons styling override */
        .stButton>button {
            border-radius: 8px !important;
            padding: 10px 22px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease-in-out !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(108, 99, 255, 0.3) !important;
        }

        /* Styling for warnings and details */
        .insight-card {
            border-left: 4px solid #FFB347;
            background: rgba(255, 179, 71, 0.05);
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 12px;
            border-top: 1px solid rgba(255, 179, 71, 0.1);
            border-right: 1px solid rgba(255, 179, 71, 0.1);
            border-bottom: 1px solid rgba(255, 179, 71, 0.1);
        }

        .insight-card.danger {
            border-left-color: #FF6B6B;
            background: rgba(255, 107, 107, 0.05);
            border-color: rgba(255, 107, 107, 0.1);
        }

        .insight-card.success {
            border-left-color: #00D4AA;
            background: rgba(0, 212, 170, 0.05);
            border-color: rgba(0, 212, 170, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
