# ==============================================================================
# 🏛️ LSOEP PORTAL PLATFORM ENGINE - INTEGRATED MASTER ROUTER
# Project: Ikom/Boki Federal Constituency (Honourable Victor Abang, PhD)
# File: main.py (V57.0 - Professional Layout Restoration)
# ==============================================================================

import sys
import asyncio
import warnings
import streamlit as st

# --- 1. SUPER-EARLY STATE INITIALIZATION ---
if "current_route" not in st.session_state:
    st.session_state.current_route = "HOME"
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if sys.platform == "win32":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from styling import inject_custom_css
from ui_modules import render_hero_banner, render_marquee_header
from registry import initialize_system_states, HON_TITLE
import panels

# --- 2. PAGE CONFIG & STYLING ---
st.set_page_config(
    page_title="LSOEP - Honourable Victor Abang, PhD Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_custom_css()

# --- 3. STANDARD INITIALIZATIONS ---
initialize_system_states()

# --- 4. NAVIGATION SETUP ---
NAVIGATION_OPTIONS = [
    "🏛️ LEGISLATIVE FOOTPRINTS",
    "🚀 LEGISLATIVE PROGRESS TRACKER",
    "🛠️ SKILL VOCATION POOL",
    "🎓 STUDENT SCHOLARSHIP/GRANT",
    "📦 PALLIATIVE ENROLLMENT",
    "💡 CV & ARTISAN VAULT",
    "🚨 COMMUNITY URGENT NEED",
    "🏛️ BEYOND RHETORICS PROJECT EXECUTION",
    "🗣️ SPEAK TO ME DIRECTLY",
    "🛡️ LOCAL LEADERSHIP VOUCHING",
]
ADMIN_OPTIONS = {
    "CONTROL_ROOM": "🔑 EXECUTIVE CONTROL ROOM",
    "STRATEGIC_COMMITTEES": "🛡️ STRATEGIC COMMITTEES (MODULE 13)",
    "AGENT_HUB": "🗳️ POLLING UNIT AGENT HUB",
    "COLLATION_HUB": "🛡️ WARD COLLATION OFFICER HUB",
}

# --- 5. SIDEBAR RENDERING ---
st.sidebar.markdown(
    f"""<a href="https://www.facebook.com/profile.php?id=100076989890731" target="_blank" class="inst-link-box">🌐 {HON_TITLE} Official Facebook</a>""",
    unsafe_allow_html=True,
)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<h3 class='admin-header'>Admin Portals</h3>", unsafe_allow_html=True
)

# Admin buttons
if st.sidebar.button(ADMIN_OPTIONS["CONTROL_ROOM"], use_container_width=True, key="nav_btn_admin"):
    st.session_state.current_route = ADMIN_OPTIONS["CONTROL_ROOM"]
    st.rerun()
if st.sidebar.button(ADMIN_OPTIONS["STRATEGIC_COMMITTEES"], use_container_width=True, key="nav_btn_committee"):
    st.session_state.current_route = ADMIN_OPTIONS["STRATEGIC_COMMITTEES"]
    st.rerun()
if st.sidebar.button(ADMIN_OPTIONS["AGENT_HUB"], use_container_width=True, key="nav_btn_agent"):
    st.session_state.current_route = ADMIN_OPTIONS["AGENT_HUB"]
    st.rerun()
if st.sidebar.button(ADMIN_OPTIONS["COLLATION_HUB"], use_container_width=True, key="nav_btn_collation"):
    st.session_state.current_route = ADMIN_OPTIONS["COLLATION_HUB"]
    st.rerun()

st.sidebar.caption("Engine Architecture: v57.0 | Professional Layout")

# --- 6. GLOBAL ROUTER & LAYOUT ENGINE ---
selected_route = st.session_state.current_route

if selected_route == "HOME":
    render_hero_banner()
    render_marquee_header()
    st.markdown("<h2 class='nav-title' style='margin-top: 25px !important;'>CONSTITUENCY ENGAGEMENT CHANNELS</h2>", unsafe_allow_html=True)
    
    cols = st.columns(5)
    for i, option in enumerate(NAVIGATION_OPTIONS):
        if cols[i % len(cols)].button(option, key=f"nav_card_{i}", use_container_width=True):
            st.session_state.current_route = option
            st.rerun()
else:
    # On other pages, show the marquee at the top
    render_marquee_header()
    
    if st.button("↩️ Return to Main Gateway", use_container_width=True, key="nav_btn_return"):
        st.session_state.current_route = "HOME"
        st.session_state.admin_authenticated = False # Always reset admin auth on return
        st.rerun()
    st.markdown("<hr class='nav-divider'>", unsafe_allow_html=True)

    # --- Panel Rendering Logic ---
    if selected_route in panels.__dict__:
        panel_func = panels.__dict__[selected_route]
        panel_func()
    # Simplified Panel Router
    elif selected_route == "🏛️ LEGISLATIVE FOOTPRINTS":
        panels.render_sponsored_bills_panel()
    elif selected_route == "🚀 LEGISLATIVE PROGRESS TRACKER":
        panels.render_legislative_progress_panel()
    elif selected_route == "🛠️ SKILL VOCATION POOL":
        panels.render_skill_form()
    elif selected_route == "🎓 STUDENT SCHOLARSHIP/GRANT":
        panels.render_scholarship_form()
    elif selected_route == "📦 PALLIATIVE ENROLLMENT":
        panels.render_palliative_form()
    elif selected_route == "💡 CV & ARTISAN VAULT":
        panels.render_cv_vault()
    elif selected_route == "🚨 COMMUNITY URGENT NEED":
        panels.render_cun_trigger()
    elif selected_route == "🏛️ BEYOND RHETORICS PROJECT EXECUTION":
        panels.render_project_verifications()
    elif selected_route == "🗣️ SPEAK TO ME DIRECTLY":
        panels.render_speak_directly_panel()
    elif selected_route == "🛡️ LOCAL LEADERSHIP VOUCHING":
        panels.render_vouching_form()

    # --- Admin Panel Rendering ---
    elif selected_route == ADMIN_OPTIONS["CONTROL_ROOM"]:
        if st.session_state.admin_authenticated:
            panels.main_dashboard(conn=None)
        else:
            st.markdown("### 🔑 Executive Command System Authorization")
            admin_key = st.text_input("Enter Command Hub Key:", type="password", key="admin_key_input")
            if st.button("Authorize Access", key="admin_auth_button"):
                if admin_key == "victor2027":
                    st.session_state.admin_authenticated = True
                    st.rerun()
                elif admin_key:
                    st.error("🛑 SYSTEM ACCESS REJECTED")
    elif selected_route == ADMIN_OPTIONS["STRATEGIC_COMMITTEES"]:
        panels.strategic_committees_panel()
    elif selected_route == ADMIN_OPTIONS["AGENT_HUB"]:
        st.markdown("### 🗳️ Polling Unit Agent Security Checkpoint")
        agent_key = st.text_input("Enter Agent Authorization Key:", type="password", key="gate_agent_key")
        if agent_key == "victor2027":
            panels.agent_panel()
        elif agent_key:
            st.error("🛑 ACCESS REJECTED: Invalid Agent Authorization Signature.")
    elif selected_route == ADMIN_OPTIONS["COLLATION_HUB"]:
        st.markdown("### 🛡️ Ward Collation Command Security Checkpoint")
        collation_key = st.text_input("Enter Collation Officer Key:", type="password", key="gate_collation_key")
        if collation_key == "victor2027":
            panels.ward_collation_officer_panel()
        elif collation_key:
            st.error("🛑 ACCESS REJECTED: Invalid Collation Authority Signature.")
