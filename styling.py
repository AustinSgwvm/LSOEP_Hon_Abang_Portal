# ==============================================================================
# 🎨 LSOEP PLATFORM UI CUSTOM STYLING SHEET OVERLAYS
# Project: Ikom/Boki Federal Constituency (Honourable Victor Abang, PhD)
# File: styling.py (V88.5 - Compact Flag Wave Banner with Enlarged Portrait)
# ==============================================================================

import streamlit as st

def inject_custom_css():
    st.markdown(
        '''
        <style>
            /* --- GLOBAL BACKGROUND OVERHAUL & EXECUTIVE TYPOGRAPHY --- */
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

            .stApp {
                background: radial-gradient(circle at 50% 0%, #041421 0%, #01080e 60%, #000306 100%) !important;
                background-attachment: fixed !important;
            }

            .stApp::before {
                content: "";
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                background-image: 
                    linear-gradient(rgba(255, 255, 255, 0.012) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255, 255, 255, 0.012) 1px, transparent 1px);
                background-size: 50px 50px;
                background-position: center top;
                pointer-events: none;
                z-index: 0;
                opacity: 0.6;
            }

            body, html, [data-testid="stAppViewContainer"] {
                color: #F8FAFC !important;
                font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
            }

            h1, h2, h3, h4, h5, h6 {
                font-family: 'Space Grotesk', system-ui, sans-serif !important;
                color: #FFFFFF !important;
            }

            /* --- 🌐 SIDEBAR COLOR SEPARATION MATRIX --- */
            [data-testid="stSidebar"] {
                background-color: #01080f !important;
                border-right: 1px solid rgba(15, 54, 87, 0.5) !important;
            }

            /* Admin Checkpoints Elements / Selectors Styling */
            .sidebar-admin-checkpoint {
                background: linear-gradient(135deg, #1e1602 0%, #0f0b01 100%) !important;
                border: 1px solid #D4AF37 !important;
                border-radius: 6px;
                padding: 10px;
                margin-bottom: 10px;
                color: #E2BB3C !important;
                font-family: 'Space Grotesk', sans-serif;
            }

            /* Command Hub Active Streams / Analytics Styling */
            .sidebar-command-hub {
                background: linear-gradient(135deg, #020f1c 0%, #01060d 100%) !important;
                border: 1px solid #00E5FF !important;
                border-radius: 6px;
                padding: 10px;
                margin-bottom: 10px;
                color: #00E5FF !important;
                font-family: 'Space Grotesk', sans-serif;
            }

            /* --- 🇳🇬 NIGERIAN PATRIOTIC SILK WAVE ANIMATION KEYFRAMES --- */
            @keyframes flag-silk-wave {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /* --- 🏛️ ELITE INTERACTIVE PROFILE BANNER HERO CARD (COMPACT FRAME) --- */
            .honourable-profile-hero {
                position: relative;
                display: flex;
                justify-content: space-between;
                align-items: center;
                
                /* Dynamic waving gradient combining rich Nigerian green, clean silk white highlights, and deep administrative navy */
                background: linear-gradient(270deg, 
                    rgba(3, 31, 19, 0.95), 
                    rgba(5, 22, 43, 0.98), 
                    rgba(255, 255, 255, 0.08), 
                    rgba(3, 31, 19, 0.95)
                ) !important;
                background-size: 400% 400% !important;
                animation: flag-silk-wave 12s ease infinite !important;
                
                backdrop-filter: blur(12px) saturate(160%) !important;
                border: 1px solid rgba(0, 135, 81, 0.4) !important; 
                border-radius: 8px !important;
                
                /* Reduced vertical container height frame from 18px 25px to a sleeker 12px 20px */
                padding: 12px 20px !important;
                margin-bottom: 15px;
                box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.55);
                overflow: hidden;
                
                /* Slightly reduced container height constraint */
                min-height: 120px;
            }

            /* Premium segmented Green-White-Green Top Accent Bar Display */
            .honourable-profile-hero::before {
                content: "";
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 4px;
                background: linear-gradient(90deg, 
                    #008751 0%, #008751 35%, 
                    #FFFFFF 35%, #FFFFFF 65%, 
                    #008751 65%, #008751 100%
                ) !important;
                z-index: 3;
            }

            .hero-left-content {
                flex: 1;
                /* Expanded right padding slightly to accommodate the larger portrait */
                padding-right: 185px;
                z-index: 2;
            }

            .hero-badge-strip {
                display: flex;
                gap: 6px;
                margin-bottom: 4px;
            }

            /* Styled Mace Overlay Symbol with boosted size rules */
            .hero-mace-icon {
                font-size: 1.45rem !important; /* Bumped size of the mace slightly */
                color: #D4AF37 !important;
                filter: drop-shadow(0px 2px 4px rgba(0, 0, 0, 0.5));
                margin-right: 8px;
            }

            .hero-title-main {
                color: #FFFFFF !important;
                font-size: 1.35rem !important;
                font-weight: 700 !important;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin: 0 !important;
                line-height: 1.2;
            }

            .hero-subtitle-sub {
                color: #D4AF37 !important;
                font-size: 0.9rem !important;
                font-weight: 600 !important;
                margin-top: 2px !important;
            }

            /* --- 📸 ENLARGED PORTRAIT FRAME --- */
            .hero-right-portrait {
                position: absolute !important;
                top: 4px !important; 
                bottom: 0 !important;
                right: 0 !important;
                
                /* Increased width size of portrait from 150px to 180px */
                width: 180px !important;
                height: calc(100% - 4px) !important;
                background-size: cover !important;
                background-position: center top !important;
                background-repeat: no-repeat !important;
                border-radius: 0 0 7px 0 !important;
                z-index: 1;
            }

            .honourable-profile-hero::after {
                content: "";
                position: absolute;
                top: 4px; bottom: 0; right: 140px; left: 0; /* Shifted gradient edge to cover the new wide picture bounds */
                background: linear-gradient(90deg, rgba(3, 31, 19, 0.95) 0%, rgba(5, 22, 43, 0.8) 60%, transparent 100%);
                z-index: 1;
                pointer-events: none;
            }

            /* --- ⚡ PREMIUM HIGH-APPEAL NAVIGATION CHANNELS --- */
            .premium-nav-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 8px;
                margin-top: 6px;
                margin-bottom: 14px;
            }

            .premium-nav-card {
                background: linear-gradient(145deg, rgba(7, 28, 51, 0.85) 0%, rgba(3, 15, 28, 0.95) 100%) !important;
                backdrop-filter: blur(8px) !important;
                border: 1px solid rgba(15, 54, 87, 0.8) !important;
                border-radius: 6px !important;
                padding: 10px 8px !important;
                text-align: center;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.35);
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .premium-nav-card:hover {
                border-color: #D4AF37 !important;
                background: linear-gradient(145deg, rgba(12, 45, 82, 0.9) 0%, rgba(7, 28, 51, 0.95) 100%) !important;
                box-shadow: 0 6px 18px rgba(0, 229, 255, 0.15);
                transform: translateY(-2px);
            }

            .premium-card-text {
                font-family: 'Space Grotesk', system-ui, sans-serif !important;
                color: #FFFFFF !important;
                font-weight: 600 !important;
                font-size: 0.82rem !important;
                letter-spacing: 0.3px;
                text-transform: uppercase;
                margin-top: 4px !important;
                line-height: 1.2;
            }

            .premium-card-badge {
                display: inline-block;
                padding: 1px 5px;
                background: rgba(214, 175, 55, 0.1) !important;
                border: 1px solid rgba(214, 175, 55, 0.3) !important;
                color: #E2BB3C !important;
                font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
                font-size: 0.6rem;
                font-weight: 700;
                border-radius: 3px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 2px;
            }

            /* --- 🛡️ COLOR SEPARATION BOXES --- */
            .admin-checkpoint-box {
                background: linear-gradient(135deg, #1e1602 0%, #0f0b01 100%) !important;
                border: 1px solid #D4AF37 !important;
                box-shadow: 0 8px 24px rgba(214, 175, 55, 0.15) !important;
                border-radius: 8px;
                padding: 18px;
                margin-bottom: 15px;
            }
            
            .command-hub-pane {
                background: linear-gradient(135deg, #020f1c 0%, #01060d 100%) !important;
                border: 1px solid #00E5FF !important;
                box-shadow: 0 8px 30px rgba(0, 229, 255, 0.1) !important;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
            }

            /* --- NATIVE DIRECT INTERACTION PRINT ENGINE INJECTION --- */
            .lsoep-print-engine-btn {
                display: block;
                width: 100%;
                text-align: center;
                background-color: rgba(5, 22, 43, 0.8) !important;
                color: #00E5FF !important;
                border: 1px solid rgba(0, 229, 255, 0.4) !important;
                border-radius: 4px;
                padding: 10px;
                font-weight: bold;
                font-size: 0.75rem;
                text-transform: uppercase;
                text-decoration: none !important;
                transition: all 0.2s ease;
            }
            .lsoep-print-engine-btn:hover {
                background-color: #00E5FF !important;
                color: #020b12 !important;
                border-color: #FFFFFF !important;
            }

            div[data-testid="stForm"], .stButton>button {
                background: rgba(5, 22, 43, 0.5) !important;
                backdrop-filter: blur(10px) saturate(140%) !important;
                border: 1px solid #0B3C5D !important;
                border-radius: 4px !important;
            }

            .stButton>button {
                color: #FFFFFF !important;
                font-weight: 600 !important;
                text-transform: uppercase;
                font-size: 0.8rem;
                padding: 4px 12px !important;
                transition: all 0.2s ease;
            }
            .stButton>button:hover {
                background-color: #D4AF37 !important;
                border-color: #FFFFFF !important;
                color: #031424 !important;
                transform: scale(1.01);
            }

            /* --- 🔍 GLOBAL FORM FIELD TYPOGRAPHY & SIZE ENHANCEMENT --- */
            div[data-testid="stWidgetLabel"] p {
                font-size: 18px !important;
                font-weight: 700 !important;
                color: #F8FAFC !important;
                letter-spacing: 0.3px !important;
                margin-bottom: 6px !important;
            }

            div[data-testid="stTextInput"] input, 
            div[data-testid="stTextArea"] textarea {
                font-size: 17px !important;
                font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
                padding: 12px 15px !important;
                color: #FFFFFF !important;
                background-color: #051625 !important;
                border: 1px solid rgba(214, 175, 55, 0.3) !important;
                border-radius: 6px !important;
            }

            div[data-testid="stTextInput"] input:focus, 
            div[data-testid="stTextArea"] textarea:focus {
                border-color: #D4AF37 !important;
                box-shadow: 0 0 10px rgba(214, 175, 55, 0.3) !important;
            }

            div[data-testid="stSelectbox"] div[role="combobox"] {
                font-size: 17px !important;
                font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
                padding: 6px 12px !important;
                color: #FFFFFF !important;
                background-color: #051625 !important;
                border: 1px solid rgba(214, 175, 55, 0.3) !important;
            }

            div[data-testid="stFileUploader"] section {
                padding: 20px !important;
                border: 2px dashed rgba(214, 175, 55, 0.3) !important;
                background-color: #020b12 !important;
                border-radius: 8px !important;
            }
            div[data-testid="stFileUploader"] section span {
                font-size: 16px !important;
                color: #E2E8F0 !important;
            }

            div[data-testid="stMarkdownContainer"] p {
                font-size: 17px !important;
            }
            div[data-testid="stRadio"] label p {
                font-size: 16px !important;
                color: #F1F5F9 !important;
            }

            /* --- PRINT LAYOUT OVERRIDES --- */
            @media print {
                body, .stApp {
                    background: #FFFFFF !important;
                    color: #000000 !important;
                }
                div[data-testid="stForm"], .stApp::before, header, [data-testid="stSidebar"], button, .honourable-profile-hero::after {
                    display: none !important;
                }
                .stDataFrame div, table, tr, td, th {
                    color: #000000 !important;
                    background-color: #FFFFFF !important;
                }
            }
        </style>
        ''',
        unsafe_allow_html=True
    )