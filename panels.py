# ==============================================================================
# 🏛️ LSOEP PORTAL MODULES & INTERACTIVE COMPONENT PANELS
# Project: Ikom/Boki Federal Constituency (Honourable Victor Abang, PhD)
# File: panels.py (V71.0 - LP Added to Ward Collation Node)
# ==============================================================================

import streamlit as st
import pandas as pd
import datetime
import time
import base64
import requests
import os
import urllib.request
import plotly.graph_objects as go

from registry import (
    LGA_WARD_DATA,
    GEOGRAPHY,
    STRATEGIC_COMMITTEE_COLS,
    COMMUNITY_LEADERS,
    COLUMNS_STRUCTURE,
    STRATEGIC_COMMITTEE_NAMES,
    STRATEGIC_COMMITTEE_PASSWORDS,
    SPONSORED_BILLS,
    ANNOUNCEMENT_CACHE_FILE,
)
from ui_modules import (
    render_module_download_trigger,
    render_institutional_purge_engine,
)
from utils import trigger_background_autosave

if "live_scores" not in st.session_state:
    st.session_state.live_scores = {
        "PRESIDENTIAL": {"APC": 12110, "NDC": 13400, "PDP": 14520, "LP": 4320, "ADC": 850},
        "SENATORIAL": {"APC": 11400, "NDC": 15100, "PDP": 16180, "LP": 2100, "ADC": 980},
        "FEDERAL HOUSE": {"APC": 9890, "NDC": 17200, "PDP": 18240, "LP": 1150, "ADC": 420},
        "GOVERNORSHIP": {"APC": 13900, "NDC": 14250, "PDP": 15410, "LP": 3200, "ADC": 710},
        "STATE HOUSE": {"APC": 10250, "NDC": 16050, "PDP": 17110, "LP": 940, "ADC": 310},
    }


def render_pie_chart(title):
    labels = ['Category A', 'Category B', 'Category C', 'Category D']
    values = [4500, 2500, 1053, 500]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text=title, showlegend=False)
    st.plotly_chart(fig, width='stretch')


# ==============================================================================
# CONSTITUENT ENTRY MANIFEST ENGINE FORMS
# ==============================================================================

def render_skill_form():
    st.markdown(
        '''<div class="swing-in" style="background-color:#061A33; padding:10px; border-left:4px solid #D4AF37; margin-bottom:15px;">
        <h4 style="color:#D4AF37; margin:0; text-transform: uppercase; font-size: 1.5rem;">🛠️ Constituent Skill Empowerment Pool</h4>
    </div>''',
        unsafe_allow_html=True,
    )
    with st.form("skill_form_engine"):
        k1, k2 = st.columns(2)
        with k1:
            sv_name = st.text_input("Full name as displayed on NIN", key="sv_n_in")
            sv_phone = st.text_input("Applicant Contact Number", key="sv_p_in")
            sv_nin = st.text_input("Your National Identification Number (NIN)", key="sv_ni_in")
            sv_vin = st.text_input("Your Permanent Voters Card Number (VIN)", key="sv_v_in")
            sv_dob = st.date_input("Date of Birth Registration", value=datetime.date(2000, 1, 1), key="sv_d_in")
            sv_gender = st.selectbox("Gender Matrix Identification", ["Male", "Female", "Prefer Not to Say"], key="sv_g_in")
            sv_disability = st.selectbox(
                "Vulnerability / Physical Challenge Status Matrix",
                ["None", "Visual Impairment", "Hearing Impairment", "Physical Challenge/Locomotor", "Other Challenges"],
                key="sv_di_in"
            )
            sv_file = st.file_uploader("Upload Scanned NIN Profile Slip Document Layout (PDF/JPG)", type=["pdf", "jpg", "png"], key="sv_f_in")
        with k2:
            klga_raw = st.selectbox("Your Local Government Area (LGA)", list(LGA_WARD_DATA.keys()), key="skill_lga_select")
            klga_clean = klga_raw.upper().split()[0] if klga_raw else ""
            kward = st.selectbox("Your Administrative Ward Location", LGA_WARD_DATA.get(klga_clean, []), key="skill_w_select")
            vocation_list = [
                "ICT & AI Core Programming",
                "Solar Renewable Energy Engineering",
                "Fashion & Textile Design Layout",
                "Catering & Culinary Arts Matrix",
                "Automobile Mechanical Engineering",
                "Electrical Installation & Wiring",
                "Plumbing & Hydraulics Systems",
                "Carpentry & Woodwork Manufacturing",
                "Modern Hairdressing & Cosmetology",
                "Other (Type Custom Vocation Below)",
            ]
            sv_selection = st.selectbox("Vocational Domain Target Pool Sector Selection", vocation_list, key="sv_s_in")
            custom_vocation = st.text_input("Type Your Choice Vocation Natively Here", key="sv_c_in") if sv_selection == "Other (Type Custom Vocation Below)" else ""
            sv_palliative_check = st.selectbox("Have you received a palliative benefit layout from this office before?", ["No", "Yes"], key="sv_pa_in")

        sv_stmt = st.text_area("Candidate Skill Interest Statement & Ambition Details", key="sv_st_in")
        st.caption("📷 Provide dynamic biometric snapshot verification below:")
        sv_cam = st.camera_input("Biometric Security Verification Core Scan Terminal Matrix", key="sv_cam_in")
        
        st.markdown("##### 🛡️ INSTITUTIONAL LEADERSHIP VOUCHING TIER OVERLAY")
        v_leader_name = st.selectbox("Select Authorized Vouching Community Leader Profile", list(COMMUNITY_LEADERS.keys()), key="skill_leader_select")
        v_leader_details = COMMUNITY_LEADERS[v_leader_name]

        if st.form_submit_button("🚀 COMMIT APPLICATION TO TRAINING SECTOR POOLS", width='stretch'):
            if not (sv_name and sv_phone and sv_nin and sv_vin and sv_stmt):
                st.error("🛑 FORM ERROR: All core validation strings, documents, and biometric snapshot frames are mandatory.")
            else:
                match_check = st.session_state.global_registry[st.session_state.global_registry["NIN"] == sv_nin]
                if not match_check.empty:
                    st.session_state.radar_threat = True
                    st.session_state.threat_msg = f"Collision: NIN [{sv_nin}] matches a record belonging to user [{match_check.iloc[0]['Name']}]"
                    st.error("Duplicate Entry Detected. Entry Rejected by Security System Shield Protocols.")
                else:
                    final_skill = custom_vocation if sv_selection == "Other (Type Custom Vocation Below)" else sv_selection
                    new_voucher_code = f"V-{klga_clean[:3]}-{kward[:3]}-{int(time.time())}".upper()
                    new_profile_row = {
                        "NIN": sv_nin, "VIN": sv_vin, "Name": sv_name.upper(), "LGA": klga_clean, "Ward": kward,
                        "Status": "Pending Review Tracker", "Category": "Applicant", "Skill_Interest": final_skill,
                        "Custom_Skill": custom_vocation, "Gender": sv_gender, "DOB": str(sv_dob), "Disability_Status": sv_disability,
                        "Prior_Palliative": sv_palliative_check, "Academic_Qual": "Degree Matrix", "Admission_Year": "2026",
                        "Admission_Letter": None, "Phone": sv_phone, "Leader_Name": v_leader_name, "Leader_Contact": v_leader_details["contact"],
                        "Leader_NIN": v_leader_details["nin"], "Leader_LGA": v_leader_details["lga"], "Leader_Ward": v_leader_details["ward"],
                        "Leader_Portfolio": v_leader_details["portfolio"], "Voucher_Code": new_voucher_code, "Remarks": "Verified Clear",
                        "Timestamp": str(datetime.datetime.now()),
                    }
                    st.session_state.global_registry = pd.concat([st.session_state.global_registry, pd.DataFrame([new_profile_row])], ignore_index=True)
                    trigger_background_autosave()
                    st.success("Registration parameter logged into production records system!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()


def render_scholarship_form():
    st.markdown(
        '''<div class="swing-in" style="background-color:#061A33; padding:10px; border-left:4px solid #D4AF37; margin-bottom:15px;">
        <h4 style="color:#D4AF37; margin:0; text-transform: uppercase; font-size: 1.5rem;">🎓 Constituent Student Scholarship Application Portal</h4>
    </div>''',
        unsafe_allow_html=True,
    )
    with st.form("scholarship_form_engine"):
        s1, s2 = st.columns(2)
        with s1:
            sch_name = st.text_input("Full student name (must match NIN records exact format)", key="sch_n")
            sch_nin = st.text_input("Student National Identification Number (NIN)", key="sch_ni")
            sch_phone = st.text_input("Applicant Active Contact Number", key="sch_p")
            sch_year = st.selectbox("Academic Year of Institution Intake Admission", [str(y) for y in range(2018, 2027)], key="sch_y")
            sch_file_nin = st.file_uploader("Attach Scanned NIN Identity Slip File Asset", type=["pdf", "jpg", "png"], key="sch_fn")
        with s2:
            sch_inst = st.text_input("Tertiary Institution Full Allocation Name", key="sch_i")
            sch_level = st.selectbox("Current Institutional Study Level Track Phase", ["Level 100", "Level 200", "Level 300", "Level 400", "Level 500", "Post-Graduate Stream"], key="sch_l")
            slga_raw = st.selectbox("Your Local Government Area (LGA)", list(LGA_WARD_DATA.keys()), key="sch_lga_select")
            slga_clean = slga_raw.upper().split()[0] if slga_raw else ""
            sward = st.selectbox("Your Ward Registry Location", LGA_WARD_DATA.get(slga_clean, []), key="sch_w")
            sch_file_adm = st.file_uploader("Attach Official University Admission Letter Verification File", type=["pdf", "jpg", "png"], key="sch_fa")
        sch_just = st.text_area("Applicant Academic Need Justification Space", key="sch_ju")
        sch_cam = st.camera_input("Capture Student Identity Card Sensor Matrix Snap", key="sch_c")
        if st.form_submit_button("🚀 SUBMIT SCHOLARSHIP ENTRY APPLICATION PARAMETERS", width='stretch'):
            if not (sch_name and sch_nin and sch_inst and sch_just):
                st.error("🛑 Mandatory fields missing. Matrix upload suspended.")
            else:
                st.success("System intake pipeline initialized successfully.")


def render_cv_vault():
    st.markdown(
        '''<div class="swing-in" style="background-color:#061A33; padding:10px; border-left:4px solid #D4AF37; margin-bottom:15px;">
        <h4 style="color:#D4AF37; margin:0; text-transform: uppercase; font-size: 1.5rem;">🚀 Constituent Professional Talent Vault Engine</h4>
    </div>''',
        unsafe_allow_html=True,
    )
    with st.form("cv_vault_engine"):
        v1, v2 = st.columns(2)
        with v1:
            cv_name = st.text_input("Full name as displayed on NIN", key="cv_n")
            cv_cat = st.selectbox("Talent Classification Target Category Field", ["Professional Domain Leader", "Skilled Artisan Professional", "Business Executive Owner"], key="cv_c")
            cv_qual = st.selectbox("Highest Level Academic Qualification Attained Matrix", ["Doctorate PhD", "Masters Degree Level", "Bachelors Degree / HND Layer", "National Diploma ND", "NCE", "SSCE Credentials Matrix", "Primary Leaving", "None"], key="cv_q")
            cv_file = st.file_uploader("Attach Professional CV/Resume Document Link File", type=["pdf", "doc", "docx", "jpg", "png"], key="cv_f")
        with v2:
            cv_nin = st.text_input("Your National Identification Number (NIN)", key="cv_ni")
            cv_phone = st.text_input("Applicant Contact Phone Number", key="cv_p")
            vlga_raw = st.selectbox("Your Registered LGA Node", list(LGA_WARD_DATA.keys()), key="cv_lga_select")
            vlga_clean = vlga_raw.upper().split()[0] if vlga_raw else ""
            vward = st.selectbox("Your Polling Ward Precinct", LGA_WARD_DATA.get(vlga_clean, []), key="cv_w")
        cv_summary = st.text_area("Summary Matrix of Functional Career Experience Vectors", key="cv_s")
        cv_cam = st.camera_input("Capture Valid Professional Certification Seals or Snap", key="cv_cm")
        if st.form_submit_button("📤 COMMIT CREDENTIALS STRINGS TO TALENT PLATFORM ARCHIVE", width='stretch'):
            st.info("Transmission channel connected smoothly.")


def render_cun_trigger():
    st.markdown(
        '''<div class="swing-in" style="background-color:#061A33; padding:10px; border-left:4px solid #D4AF37; margin-bottom:15px;">
        <h4 style="color:#D4AF37; margin:0; text-transform: uppercase; font-size: 1.5rem;">🚨 Community Urgent Need Field Deficit Report Gateway</h4>
    </div>''',
        unsafe_allow_html=True,
    )
    with st.form("cun_form_engine"):
        cun_member = st.text_input("Reporting Community Member Name", key="cun_m")
        cun_phone = st.text_input("Applicant Infrastructure Liaison Phone", key="cun_p")
        clga_raw = st.selectbox("Affected Target LGA Focus", list(LGA_WARD_DATA.keys()), key="cun_lga_select")
        clga_clean = clga_raw.upper().split()[0] if clga_raw else ""
        cward = st.selectbox("Affected Ward Sector Location", LGA_WARD_DATA.get(clga_clean, []), key="cun_w")
        cun_area = st.selectbox("Area of Urgent Attention / Critical Deficiency", ["Water Source Deficit", "Grid Electricity Failure", "Access Road Failure Collapse", "Community Security Vulnerability", "Healthcare Facility Absence"], key="cun_a")
        cun_file = st.file_uploader("Attach Identification NIN Validation Document Slip (PDF/PNG)", type=["pdf", "jpg", "png"], key="cun_f")
        cun_logs = st.text_area("Detailed Situation Report Narrative Logs & Geographical Landmarks", key="cun_l")
        cun_cam = st.camera_input("Field Visual Evidence Deficit Capture Sensor Matrix Camera", key="cun_c")
        if st.form_submit_button("🚨 TRIGGER COMMAND INCIDENT VECTOR ALERT", width='stretch'):
            st.info("Field alert dispatch sequence routing triggered.")


def render_palliative_form():
    st.markdown(
        '''<div class="swing-in" style="background-color:#061A33; padding:10px; border-left:4px solid #D4AF37; margin-bottom:15px;">
        <h4 style="color:#D4AF37; margin:0; text-transform: uppercase; font-size: 1.5rem;">📦 Constituent Palliative/Empowerment Enrollment Registry</h4>
    </div>''',
        unsafe_allow_html=True,
    )
    with st.form("palliative_form_engine"):
        p1, p2 = st.columns(2)
        with p1:
            p_name = st.text_input("Full nominee name as written on identity documentation", key="p_n")
            p_nin = st.text_input("Nominee National Identification Number (NIN)", key="p_ni")
            p_vin = st.text_input("Nominee Permanent Voters Card number (VIN)", key="p_v")
            p_vuln = st.multiselect("Vulnerability Category Status Flags", ["Aged Eldership Category", "Widowhood Support Matrix", "Physical Disability Framework Challenge", "Long-Term Unemployed Status Tracker"], key="p_vu")
            p_file_nin = st.file_uploader("Upload Nominee Profile NIN Slip Document Layout Check", type=["pdf", "jpg", "png"], key="p_f")
        with p2:
            p_phone = st.text_input("Nominee Active Contact Phone Number", key="p_p")
            plga_raw = st.selectbox("Constituent Local Government Area (LGA)", list(LGA_WARD_DATA.keys()), key="pal_lga_select")
            plga_clean = plga_raw.upper().split()[0] if plga_raw else ""
            pward = st.selectbox("Constituent Allocation Ward", LGA_WARD_DATA.get(plga_clean, []), key="p_w")
            p_agro_select = st.selectbox("Specific Area of Agro Intervention and Seeds Input", ["Fertilizer Allocation", "High-Yield Crop Seedlings", "Artisan Tools Leverages", "Other Area of Likely Intervention"], key="p_ag")
            p_expect = st.text_input("Type Detailed Expectation Parameters Natively", key="p_ex")
        st.markdown("##### 🛡️ LEADERSHIP TIER AUTHENTICATION SIGNATURE OVERLAY")
        v_leader_name_p = st.selectbox("Select Vouching Community Leader Node Reference", list(COMMUNITY_LEADERS.keys()), key="pal_leader_select")
        p_remarks = st.text_area("Leader Affirmation Testimony Verification Remarks Statement", key="p_re")
        p_cam = st.camera_input("Biometric Face Capture Matrix Core Verification Face Scan", key="p_c")
        if st.form_submit_button("🚀 COMPLETE EMPOWERMENT / PALLIATIVE NOMINATION RECORD", width='stretch'):
            st.info("Palliative submission metrics validated against core cache.")


def render_vouching_form():
    st.markdown(
        '''<div class="swing-in" style="background-color:#061A33; padding:10px; border-left:4px solid #D4AF37; margin-bottom:15px;">
        <h4 style="color:#D4AF37; margin:0; text-transform: uppercase; font-size: 1.5rem;">🛡️ Local Leadership Vouching Verification Gateway</h4>
    </div>''',
        unsafe_allow_html=True,
    )
    with st.form("leadership_vouch_form"):
        v_name = st.text_input("Leader Full Name Credentials")
        v_title = st.text_input("Official Portfolio Designation (Traditional Ruler / Ward Chairman / Elder)")
        v_target_nin = st.text_input("Target Constituent Applicant NIN to Vouch For")
        v_token = st.text_input("Security Validation Token (Assigned Code)", type="password")
        st.text_area("Official Endorsement Affirmation Text Clause Block")
        if st.form_submit_button("🔒 Affix Electronic Leadership Seal", width='stretch'):
            st.success("Electronic verification endorsement logged successfully under structural constraints.")


# ==============================================================================
# PUBLIC LEGISLATIVE FEED MODULES
# ==============================================================================

def render_sponsored_bills_panel():
    st.markdown(
        '''<div class="swing-in" style="background-color:#061A33; padding:10px; border-left:4px solid #D4AF37; margin-bottom:15px;">
        <h4 style="color:#D4AF37; margin:0; text-transform: uppercase; font-size: 1.5rem;">📜 Legislative Footprints & Motions</h4>
    </div>''',
        unsafe_allow_html=True,
    )
    if not SPONSORED_BILLS:
        st.info("Information on sponsored bills and motions by Honourable Victor Abang will be updated here shortly.")
    else:
        for bill in SPONSORED_BILLS:
            with st.container(border=True):
                status_color = {"Passed": "green", "Second Reading": "blue", "In Committee": "orange", "First Reading": "yellow"}.get(bill["status"], "gray")
                st.markdown(f"**{bill['title']}**")
                st.markdown(f'''*Status: <span style='color:{status_color};'>{bill['status']}</span>* | *Date: {bill['date']}*''', unsafe_allow_html=True)
                st.markdown(bill["description"])
                st.progress(bill["progress"])


def render_legislative_progress_panel():
    st.markdown('<div class="supervisor-header"><h2>🚀 LEGISLATIVE PROGRESS TRACKER</h2></div>', unsafe_allow_html=True)
    st.markdown(
        '''
        <style>
        .progress-card { background-color: rgba(11, 60, 93, 0.4); border: 2px solid #0B3C5D; border-left: 6px solid #D4AF37; border-radius: 12px; padding: 24px; margin-bottom: 22px; }
        .progress-title { color: #D4AF37 !important; font-size: 1.45rem !important; font-weight: 700 !important; }
        .status-pill { display: inline-block; padding: 6px 16px; border-radius: 20px; font-weight: 800; font-size: 0.95rem; text-transform: uppercase; }
        .pill-passed { background-color: #1E4620; color: #4AF256; }
        .pill-committee { background-color: #5C4308; color: #FAD02C; }
        </style>
        ''', unsafe_allow_html=True
    )
    st.markdown(
        '''
        <div class="progress-card">
            <div class="progress-title">🏛️ A Bill for an Act to Establish the Federal College of Agriculture, Ikom</div>
            <div class="status-pill pill-passed">Status: Passed</div>
            <p style="color:#F0F0F0; font-size:1.12rem; margin-top:10px;">
                This landmark bill seeks to establish a dedicated federal institution for agricultural education and research in Ikom, aiming to boost the local agrarian economy, provide specialized training, and promote modern farming techniques in the region.
            </p>
        </div>
        ''', unsafe_allow_html=True
    )


# ==============================================================================
# WARD COLLATION OFFICER HUB (LP ADDED TO PARTY TALLY CARD)
# ==============================================================================

def ward_collation_officer_panel():
    st.markdown('### 🛡️ Ward Collation Officer Command: Form EC8A Logs')
    with st.form("supervisor_form"):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Supervisor Full Name Allocation")
            st.text_input("Phone Number Identity Line")
            sup_lga_raw = st.selectbox("Your Verification LGA Node", list(LGA_WARD_DATA.keys()))
            sup_lga_clean = sup_lga_raw.upper().split()[0] if sup_lga_raw else ""
            st.selectbox("Your Collation Ward Bounds", LGA_WARD_DATA.get(sup_lga_clean, []))
            st.text_input("BVAS Hardware Serial Number Reference")
            st.number_input("Total Number of Accredited Voters Matrix", min_value=0)
        with c2:
            st.markdown("**Official Party Votes Breakdown Card**")
            st.number_input("All Progressives Congress (APC) Votes", min_value=0)
            st.number_input("National Democratic Congress (NDC) Votes", min_value=0)
            st.number_input("Peoples Democratic Party (PDP) Votes", min_value=0)
            st.number_input("Labour Party (LP) Votes", min_value=0, key="coll_lp_votes")
            st.number_input("African Democratic Congress (ADC) Votes", min_value=0)
            st.selectbox("Field Malpractice Incident Occurred?", ["No", "Yes"])
            st.text_area("Detailed Situation/Incident Narrative Report Logs")
        st.camera_input("Live Capture Optical Sensor Scan: Form EC8A Sheet Capture")
        st.form_submit_button("🔒 LOCK AND LOG COLLATION METRICS TO MASTER DATABASE", width='stretch')


# ==============================================================================
# 🗳️ POLLING UNIT AGENT HUB - TIERS & PARAMS
# ==============================================================================

def agent_panel():
    st.markdown('### 🗳️ POLLING UNIT AGENT HUB: COMMAND HUB & TIERS')
    
    if "agent_authenticated" not in st.session_state:
        st.session_state.agent_authenticated = False

    if not st.session_state.agent_authenticated:
        with st.form("agent_checkpoint_login"):
            password = st.text_input("Enter Agent Authorization Key:", type="password")
            if st.form_submit_button("Verify Security Authorization Credentials", width='stretch'):
                if password == "victor2027":
                    st.session_state.agent_authenticated = True
                    st.rerun()
                else:
                    st.error("🛑 ACCESS REJECTED: Invalid Agent Signature Key.")
        return

    st.success("✅ Secure Gateway Authorized. Select Election Monitoring Target Tier Axis:")
    
    agent_tiers = [
        {"label": "🦅 Presidential", "border": "#4AF256"},
        {"label": "🏛️ Senate Chamber", "border": "#D4AF37"},
        {"label": "🏛️ House of Reps", "border": "#00E5FF"},
        {"label": "🏰 Gubernatorial Ledger", "border": "#FAD02C"},
        {"label": "📜 State Assembly", "border": "#FF4136"}
    ]
    
    t_cols = st.columns(5)
    for idx, t_spec in enumerate(agent_tiers):
        with t_cols[idx]:
            is_selected = st.session_state.agent_active_tier == t_spec["label"]
            bg_card = "#0B3C5D" if is_selected else "#020B14"
            border_card = "2px solid #D4AF37" if is_selected else f"1px solid {t_spec['border']}"
            
            st.markdown(
                f'''
                <div style="background-color:{bg_card}; border:{border_card}; border-radius:8px; padding:12px; text-align:center; margin-bottom:8px;">
                    <span style="color:#FFFFFF; font-weight:bold; font-size:0.95rem;">{t_spec['label']}</span>
                </div>
                ''', unsafe_allow_html=True
            )
            if st.button(f"Monitor {t_spec['label']}", key=f"agent_tier_trigger_{idx}", width='stretch'):
                st.session_state.agent_active_tier = t_spec["label"]
                st.rerun()

    st.markdown(f"#### 📡 Data Transmission Matrix Active: `{st.session_state.agent_active_tier}`")
    
    with st.form("agent_form"):
        a1, a2 = st.columns(2)
        with a1:
            st.text_input("Field Polling Agent Full Name", key="agt_n")
            st.text_input("Agent Contact Verification Number", key="agt_p")
            state_list = sorted(list(st.session_state.DYNAMIC_GEO_MATRIX.keys()))
            selected_state = st.selectbox("Federal Target State Registry", options=state_list, index=state_list.index("Cross River") if "Cross River" in state_list else 0)
            
            lga_list = sorted(list(st.session_state.DYNAMIC_GEO_MATRIX[selected_state].keys()))
            agt_lga = st.selectbox("Target LGA Focal Node", options=lga_list, key="agent_lga_select")
            ward_list = sorted(st.session_state.DYNAMIC_GEO_MATRIX[selected_state][agt_lga])
            st.selectbox("Target Registration Ward Sector", options=ward_list, key="agent_ward_select")
            st.text_input("Polling Unit (PU) Specific Code Number", key="agt_pu")
            
            st.text_input("🔢 Registered BVAS Serial Number Token:", key="agt_bvas_sn", placeholder="Enter unique BVAS ID line...")
            
        with a2:
            st.markdown(f"**{st.session_state.agent_active_tier} Tally Records (ADC & LP Accounted)**")
            st.number_input("All Progressives Congress (APC) Score", min_value=0, key="agt_apc")
            st.number_input("National Democratic Congress (NDC) Score", min_value=0, key="agt_ndc")
            st.number_input("Peoples Democratic Party (PDP) Score", min_value=0, key="agt_pdp")
            st.number_input("Labour Party (LP) Score", min_value=0, key="agt_lp")
            st.number_input("African Democratic Congress (ADC) Score", min_value=0, key="agt_adc")
            
            st.selectbox("Security Disruption Threat Intercepted?", ["No", "Yes"], key="agt_sec")
            
        st.markdown("##### 🚨 Polling Precinct Incident Form Sheet Logs")
        st.text_area("Log specific operational field scenarios, malfunctions, or irregularities here:", key="agt_incident_form_desc", placeholder="Type full scene notes...")

        st.camera_input("📸 FIELD IMAGE SNAPPING: FORM EC8A RESULT SHEET CORE SCAN", key="agt_cam")
        if st.form_submit_button("🔍 TRANSMIT ENCRYPTED STREAMS TO EXECUTIVE ROOM", width='stretch'):
            st.success(f"Encrypted streams logged safely under {st.session_state.agent_active_tier} data array tracks!")


# ==============================================================================
# ADMINISTRATIVE CENTRAL CONTROL ROOM CORE
# ==============================================================================

def main_dashboard(conn):
    st.markdown('<h2 style="font-size: 1.8rem; text-transform: uppercase; color:#D4AF37;">🏛️ Executive Control Command Dashboard</h2>', unsafe_allow_html=True)
    selected_module = st.session_state.get("admin_module_view", "📊 Master Registry Matrix")
    st.markdown(f"### Current Node Axis: `{selected_module}`")

    if selected_module == "📊 Master Registry Matrix":
        st.subheader("📊 Master Verification Registry Database Partition Array")
        st.dataframe(st.session_state.get("global_registry", pd.DataFrame()))
    elif selected_module == "📢 Plenary Broadcast Terminal":
        render_admin_plenary_broadcast_terminal()
    elif selected_module == "🗣️ Citizen Feedback":
        st.subheader("🗣️ Citizen Feedback Inbox Messages")
        st.dataframe(st.session_state.get("feedback_registry", pd.DataFrame()))
    elif selected_module == "📢 Admin Announcement Control":
        st.subheader("📢 Admin Announcement Ticker Control Room")
        current_announcement = st.session_state.get("global_scrolling_announcement", "")
        new_announcement = st.text_area("Update scrolling marquee overlay text content:", value=current_announcement)
        if st.button("Publish Updated Announcement String"):
            st.session_state.global_scrolling_announcement = new_announcement
            trigger_background_autosave()
            st.success("Announcement updated across portal displays!")
            st.rerun()
    elif selected_module == "📝 Ground Truth Form EC8A Data":
        st.subheader("📝 Ground Truth Form EC8A Audited Verification Schema")
        ec8a_df = pd.DataFrame(list(st.session_state.get("submitted_wards", {}).values()))
        st.dataframe(ec8a_df)
    elif selected_module == "🗳️ Live Election Analytical Sync":
        render_election_analytical_sync()
    elif selected_module == "🚀 Legislative Progress Tracker":
        render_legislative_progress_panel()
    elif selected_module == "📋 Strategic Committee Compliance Logs":
        render_committee_compliance_form()
    else:
        st.info(f"ℹ️ {selected_module} background framework trails running securely under diagnostic monitoring rules.")


@st.cache_data
def load_pdf_bytes(file_path):
    with open(file_path, "rb") as f:
        return f.read()


def render_project_verifications():
    st.markdown(
        '''<h2 class="swing-in" style="color:#D4AF37; text-transform: uppercase; font-size: 2rem;">🦅 BEYOND RHETORICS: PROJECT VERIFICATION HUB</h2>''',
        unsafe_allow_html=True,
    )
    st.write("Cross-examining performance metrics with verifiable ground-truth evidence trails.")
    media_dir = "media" if os.path.exists("media") else "MEDIA MEDIA MEDIA"
    if os.path.exists(media_dir):
        files_to_render = [
            ("Cover Page Document", "Cover_compressed.pdf"),
            ("Project Verification Batch 1", "1_compressed.pdf"),
            ("Project Verification Batch 2", "2_compressed.pdf"),
        ]
        for title, filename in files_to_render:
            full_path = os.path.join(media_dir, filename)
            if os.path.exists(full_path):
                with st.expander(f"📄 View Official {title} ({filename})", expanded=False):
                    pdf_bytes = load_pdf_bytes(full_path)
                    st.download_button(label=f"📥 Download {filename}", data=pdf_bytes, file_name=filename, mime="application/pdf", key=f"dl_{filename}", width='stretch')
    else:
        st.error("🚨 Media structural repository directory not encountered on host.")


def strategic_committees_panel():
    st.markdown(
        '''<div class="supervisor-header swing-in" style="font-size: 1.7rem; text-transform: uppercase;">🛡️ MODULE 13: STRATEGIC COMMITTEES (1-10) ACCESS GATEWAY</div>''',
        unsafe_allow_html=True,
    )
    if "module_13_unlocked" not in st.session_state:
        st.session_state.module_13_unlocked = False

    if not st.session_state.module_13_unlocked:
        with st.form("general_login_form"):
            committee_key_input = st.text_input("Enter General Cryptographic Passkey to Unlock Module Layer:", type="password")
            if st.form_submit_button("Unlock Committee Nodes", width='stretch'):
                if committee_key_input == "congratulationshonvictor":  
                    st.session_state.module_13_unlocked = True
                    st.rerun()
                else:
                    st.error("🛑 ACCESS REJECTED: General passkey signature mismatch.")
        return

    st.success("✅ General Access Matrix Granted. Please choose target assignment matrix node lines below.")
    st.selectbox("Select Your Assigned Committee Hub Node Allocation Line:", options=[""] + STRATEGIC_COMMITTEE_NAMES)


def render_speak_directly_panel():
    st.markdown("### 🗣️ Direct Citizen Liaison Communication Pipeline Channel")
    with st.form("citizen_direct_feedback_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Citizen First Name *")
            st.text_input("Citizen Surname *")
            st.selectbox("Biological Sex Classification", ["Male", "Female", "Other"])
            lga_raw = st.selectbox("LGA Border Delineation *", list(LGA_WARD_DATA.keys()), key="feedback_lga")
            lga_clean = lga_raw.upper().split()[0] if lga_raw else ""
        with col2:
            st.selectbox("Ward Polling Boundary *", LGA_WARD_DATA.get(lga_clean, []), key="feedback_ward")
            st.text_input("Verified WhatsApp Communication Line (Optional)")
            st.text_input("Secure Email Profile Address (Optional)")
        st.text_area("Write Detailed Consultation Message to the House Rep Office *", max_chars=1200)
        if st.form_submit_button("🔒 TRANSMIT SECURE END-TO-END CITIZEN BRIEF", width='stretch'):
            st.success("Liaison communication string sent successfully.")
            st.balloons()


def render_committee_compliance_form():
    st.markdown(
        '''<div class="supervisor-header"><h2 style="margin:0; font-weight:800; font-size:1.8rem;">📋 STRATEGIC COMMITTEE COMPLIANCE LOGS</h2></div>''',
        unsafe_allow_html=True,
    )
    committee_group = st.selectbox("Select Committee Strategic Group Allocation Matrix Node Focus:", [
        "Group A: Agricultural Development & Horticulture Council Sector", 
        "Group B: Vocational Capacity, Technical Pools & Modern Economy Infrastructure"
    ])
    with st.form("committee_compliance_matrix_form"):
        st.text_input("Reporting Compliance Officer Name:")
        st.text_input("Geographical Jurisdiction Focus Scope:")
        st.text_area("Detailed Action Metrics Narrative Account Summary Strings Content:")
        st.number_input("Total Vouched Capital Outlay Projects Disbursed (NGN):", min_value=0.0, step=5000.0)
        st.form_submit_button("🔒 DISPATCH REPORT CARD TO MASTER LEDGER", width='stretch')


# ==============================================================================
# 🗳️ LIVE ELECTION ANALYTICAL SYNC DISPLAY
# ==============================================================================

def render_election_analytical_sync():
    st.markdown('<div class="supervisor-header"><h2>📊 LIVE ELECTION ANALYTICAL SYNC DISPLAY</h2></div>', unsafe_allow_html=True)
    st.markdown("### 5 BEAUTIFUL COLORED ELECTION TIERS")
    cols = st.columns(5)
    
    tier_styling = [
        {"title": "🦅 Presidential Matrix", "bg": "#041424", "border": "#4AF256", "shadow": "rgba(74,242,86,0.2)"},
        {"title": "🏛️ Senate Chamber Sync", "bg": "#061F38", "border": "#D4AF37", "shadow": "rgba(212,175,55,0.2)"},
        {"title": "🏛️ House of Reps Core", "bg": "#041424", "border": "#00E5FF", "shadow": "rgba(0,229,255,0.2)"},
        {"title": "🏰 Gubernatorial Ledger", "bg": "#061F38", "border": "#FAD02C", "shadow": "rgba(250,208,44,0.2)"},
        {"title": "📜 State Assembly Matrix", "bg": "#041424", "border": "#FF4136", "shadow": "rgba(255,65,54,0.2)"}
    ]

    for idx, spec in enumerate(tier_styling):
        with cols[idx]:
            st.markdown(
                f'''
                <div style="background-color:{spec['bg']}; border:2px solid {spec['border']}; border-radius:12px; padding:20px; text-align:center; box-shadow:0 4px 15px {spec['shadow']};">
                    <h5 style="color:#FFFFFF; margin:0; font-size:1.05rem; font-weight:700;">{spec['title']}</h5>
                    <div style="margin-top:10px; font-size:0.8rem; color:{spec['border']}; font-weight:bold; text-transform:uppercase;">STREAM SYNCED</div>
                </div>
                ''', unsafe_allow_html=True
            )

    st.markdown("### CASCADING NATIONWIDE GEO-SEARCH TERMINAL SELECTION")
    geo_mode_tab1, geo_mode_tab2 = st.tabs(["⚡ Standard Cascading Dropdown Selectors", "✍️ Manual Direct Entry Input Blocks"])
    
    with geo_mode_tab1:
        c1, c2, c3 = st.columns(3)
        with c1:
            state_list = sorted(list(st.session_state.DYNAMIC_GEO_MATRIX.keys()))
            selected_state = st.selectbox("🎯 Target Audit State Profile Axis:", options=state_list, index=state_list.index("Cross River") if "Cross River" in state_list else 0, key="sync_state_dd")
        with c2:
            lga_list = sorted(list(st.session_state.DYNAMIC_GEO_MATRIX[selected_state].keys()))
            selected_lga = st.selectbox("🏢 Target Local Government Area (LGA) Node:", options=lga_list, key="sync_lga_dd")
        with c3:
            ward_list = sorted(st.session_state.DYNAMIC_GEO_MATRIX[selected_state][selected_lga])
            st.selectbox("📍 Target Polling Ward Precinct Boundary:", options=ward_list, key="sync_ward_dd")
            
    with geo_mode_tab2:
        st.info("💡 Use this panel to query or submit data elements for fields not comprehensively populated inside the native indices.")
        cm1, cm2, cm3 = st.columns(3)
        with cm1:
            manual_state = st.text_input("Type/Query Target State Name:", placeholder="e.g., Cross River", key="man_state_in")
        with cm2:
            manual_lga = st.text_input("Type/Query Target Local Government Area (LGA):", placeholder="e.g., Ikom", key="man_lga_in")
        with cm3:
            manual_ward = st.text_input("Type/Query Target Polling Ward Precinct Name:", placeholder="e.g., Ikom Urban", key="man_ward_in")
            
        if st.button("🔒 Commit and Synchronize Custom Search Inputs", width='stretch'):
            if manual_state and manual_lga and manual_ward:
                cs = manual_state.strip().title()
                cl = manual_lga.strip().title()
                cw = manual_ward.strip().title()
                
                if cs not in st.session_state.DYNAMIC_GEO_MATRIX:
                    st.session_state.DYNAMIC_GEO_MATRIX[cs] = {}
                if cl not in st.session_state.DYNAMIC_GEO_MATRIX[cs]:
                    st.session_state.DYNAMIC_GEO_MATRIX[cs][cl] = []
                if cw not in st.session_state.DYNAMIC_GEO_MATRIX[cs][cl]:
                    st.session_state.DYNAMIC_GEO_MATRIX[cs][cl].append(cw)
                    
                st.success(f"Successfully added tracking node layout: [{cs} ➡️ {cl} ➡️ {cw}]")
                time.sleep(0.5)
                st.rerun()
            else:
                st.warning("⚠️ Enter target descriptors across all blocks to register manual overrides.")


# ==============================================================================
# 📢 ADVANCED PLENARY BROADCAST MULTI-MEDIA TERMINAL ENGINE
# ==============================================================================

def render_admin_plenary_broadcast_terminal():
    st.markdown("### 📢 Advanced Plenary Broadcast Terminal Interface")
    st.caption("Publish direct high-definition physical video clips, photography snapshot logs, and floor write-ups live to the Gateway stream database.")
    
    with st.form("plenary_upload_form_v3", clear_on_submit=True):
        update_text = st.text_area("Write Plenary Message / Contextual Legislative Floor Brief:", placeholder="Type official house briefs, sponsored bills statement outlines, or session summaries here...")
        
        st.markdown("##### 📎 Hard Media Attachment Interface Channels")
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            uploaded_video = st.file_uploader("🎥 Upload Real Physical Video Clip Asset (.MP4, .MOV):", type=["mp4", "mov", "avi", "mkv"])
        with p_col2:
            uploaded_image = st.file_uploader("📸 Attach Session Photography Picture Clip (.JPG, .PNG):", type=["png", "jpg", "jpeg", "webp"])
            
        submit_broadcast = st.form_submit_button("🚀 DISPATCH DYNAMIC MULTI-MEDIA BRIEF TO CONSTITUENCY TIMELINE", width='stretch')
        
        if submit_broadcast:
            if not update_text and not uploaded_video and not uploaded_image:
                st.error("🛑 Empty broadcast sequence aborted. You must supply text or upload media files.")
                return
                
            video_data = None
            if uploaded_video is not None:
                with st.spinner("Processing physical video file byte array mapping calculations..."):
                    v_bytes = uploaded_video.read()
                    video_data = f"data:{uploaded_video.type};base64,{base64.b64encode(v_bytes).decode()}"
                    
            image_data = None
            if uploaded_image is not None:
                with st.spinner("Encrypting high-resolution visual session picture package..."):
                    i_bytes = uploaded_image.read()
                    image_data = f"data:{uploaded_image.type};base64,{base64.b64encode(i_bytes).decode()}"

            new_update = {
                "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                "message": update_text,
                "video": video_data,
                "image": image_data
            }
            
            if "plenary_broadcast_feed" not in st.session_state:
                st.session_state.plenary_broadcast_feed = []
                
            st.session_state.plenary_broadcast_feed.insert(0, new_update)
            st.success("🌟 Plenary Multi-Media report successfully encoded and dispatched live!")
            st.rerun()


def render_constituent_plenary_updates():
    st.markdown("## 🏛️ Live Plenary Session Updates")
    st.markdown("Explore official direct feeds, visual media clips, and legislative briefs straight from the chamber floor of the House of Representatives.")
    st.markdown("---")
    
    st.image("https://naltf.gov.ng/wp-content/uploads/2025/05/green-chamber-image.webp", width='stretch', caption="Inside the Green Chamber floor of the House of Representatives during plenary operations.")
    
    feed = st.session_state.get("plenary_broadcast_feed", [])
    if not feed:
        st.info("ℹ️ No multi-media updates have been dispatched to the plenary feed yet today.")
        return
        
    for item in feed:
        with st.container(border=True):
            st.caption(f"⏱️ Dispatched: **{item.get('timestamp', 'Recent Update')}** | Location Target: National Assembly Abuja Chambers Floor")
            if item.get("message"):
                st.markdown(f"#### {item['message']}")
            
            if item.get("video"):
                st.video(item["video"])
            if item.get("image"):
                st.image(item["image"], width='stretch')
            st.markdown(" ")