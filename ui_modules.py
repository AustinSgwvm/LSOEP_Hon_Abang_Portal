# ==============================================================================
# 🏛️ LSOEP UI MODULES & COMPONENTS
# Project: Ikom/Boki Federal Constituency (Honourable Victor Abang)
# File: ui_modules.py (V60.0 - Aesthetic & Responsive Polish)
# ==============================================================================

import streamlit as st
import pandas as pd
import base64
import os
from registry import HON_TITLE, initialize_system_states

@st.cache_data
def get_image_as_base64(path):
    """Reads a local image file and returns it as a base64 encoded string."""
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_hero_banner():
    """Renders the final, responsive, and aesthetically enhanced hero banner."""
    mace_path = "assets/digital_mace.png"
    hon_path = "assets/hon_abang.png"

    mace_base64 = get_image_as_base64(mace_path)
    hon_base64 = get_image_as_base64(hon_path)

    if not (mace_base64 and hon_base64):
        st.error("Critical Error: Hero banner image assets not found in the 'assets' directory.")
        return

    mace_image_src = f"data:image/png;base64,{mace_base64}"
    hon_image_src = f"data:image/png;base64,{hon_base64}"

    st.markdown(
        f'''
        <style>
        @keyframes gradientLineBG {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        @keyframes swipe-right-left {{
            0% {{ transform: translateX(-20px) rotate(-5deg); }}
            100% {{ transform: translateX(20px) rotate(5deg); }}
        }}

        .hero-card-container {{
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 2rem;
            border-radius: 18px;
            /* Updated professional background with multiple color lines */
            background: linear-gradient(-45deg, #021024, #0B3C5D, #021024, #D4AF37, #061A33);
            background-size: 600% 600%;
            animation: gradientLineBG 20s ease infinite;
            border-left: 5px solid #D4AF37;
            border-right: 5px solid #0B3C5D;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
            margin-bottom: 1.5rem;
            flex-wrap: wrap; /* Allows wrapping for responsiveness */
        }}

        .mace-left img {{
            height: 180px; /* Increased size */
            filter: drop-shadow(0 0 20px rgba(255, 223, 100, 0.5));
            animation: swipe-right-left 3.5s ease-in-out infinite alternate;
        }}

        .hero-text-content {{
            text-align: center;
            color: #F0F0F0; /* Soft off-white */
            padding: 0 1rem;
        }}
        
        .hero-text-content .title {{
            color: #D4AF37;
            font-size: 2.8rem;
            font-weight: 800;
        }}

        .hon-right img {{
            height: 180px; /* Increased size */
            width: 180px;  /* Increased size */
            border-radius: 50%;
            border: 6px solid #D4AF37;
            object-fit: cover;
            box-shadow: 0 0 30px rgba(212, 175, 55, 0.6);
        }}

        /* --- Mobile Responsiveness --- */
        @media (max-width: 768px) {{
            .hero-card-container {{
                flex-direction: column; /* Stack elements vertically on mobile */
                padding: 1.5rem;
            }}
            .mace-left {{
                order: 2; /* Change order for mobile layout */
                margin: 1rem 0;
            }}
            .hero-text-content {{
                order: 1; /* Title appears first */
                margin-bottom: 1.5rem;
            }}
            .hon-right {{
                order: 3; /* Picture appears last */
                 margin-top: 1rem;
            }}
            .hero-text-content .title {{
                font-size: 2.2rem;
            }}
            .mace-left img, .hon-right img {{
                height: 150px; /* Slightly smaller for mobile */
                width: 150px;
            }}
        }}
        </style>

        <div class="hero-card-container">
            <div class="mace-left">
                <img src="{mace_image_src}" alt="Mace">
            </div>
            <div class="hero-text-content">
                <h1 class="title">{HON_TITLE}</h1>
                <h2 class="subtitle">MEMBER, HOUSE OF REPRESENTATIVES</h2>
                <p class="constituency">IKOM/BOKI FEDERAL CONSTITUENCY</p>
                <p class="state">CROSS RIVER STATE</p>
            </div>
            <div class="hon-right">
                <img src="{hon_image_src}" alt="Honourable Victor Abang">
            </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

def render_marquee_header():
    """Renders a refined, slower, and recolored marquee."""
    announcement = st.session_state.get(
        "global_scrolling_announcement",
        "Welcome to the official constituency outreach portal of Honourable Victor Abang, PhD. This platform is designed for transparency, accountability, and direct engagement.",
    )
    long_announcement = (announcement + " • ") * 3 

    st.markdown(
        f"""
        <style>
        .marquee-container {{
            background-color: #041d3d;
            padding: 12px 0;
            overflow: hidden;
            white-space: nowrap;
            border-top: 2px solid #D4AF37;
            border-bottom: 2px solid #D4AF37;
            margin-bottom: 10px;
        }}

        .marquee-content {{
            display: inline-block;
            padding-left: 100%;
            animation: marquee 90s linear infinite; /* Increased duration to slow down */
            font-size: 1.1rem;
            font-weight: 600;
            letter-spacing: 1.5px;
            color: #EAEAEA; /* Changed text color to a soft off-white */
        }}
        
        @keyframes marquee {{
            0%   {{ transform: translateX(0); }}
            100% {{ transform: translateX(-100%); }}
        }}
        </style>

        <div class="marquee-container">
            <div class="marquee-content">{long_announcement}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_module_download_trigger(df, filename_prefix, key):
    """Renders a download button for a given DataFrame."""
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Download {filename_prefix}.csv",
            data=csv,
            file_name=f"{filename_prefix}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key=key,
            use_container_width=True,
        )

def render_institutional_purge_engine(key_prefix):
    """Renders a button to purge all registry data from the session state."""
    st.markdown("---")
    st.warning("🔴 **DANGER ZONE**: The functions below can lead to irreversible data loss.")
    
    if st.button("🔥 PURGE ENTIRE REGISTRY", key=f"{key_prefix}_purge_all", use_container_width=True):
        keys_to_purge = [
            "global_registry", "strategic_committee_registry", "feedback_registry",
            "committee_double_dipping_ledger", "submitted_wards", "submitted_pus",
            "agent_field_registry",
        ]
        for k in keys_to_purge:
            if k in st.session_state:
                del st.session_state[k]
        
        initialize_system_states()
        st.success("✅ All registry data has been purged and system state re-initialized.")
        st.rerun()
