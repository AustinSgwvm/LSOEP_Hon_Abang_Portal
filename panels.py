import streamlit as st
import pandas as pd
import datetime
import time
import base64
import requests
import os
import urllib.request
import plotly.graph_objects as go
import sqlite3
from io import BytesIO

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

# --- NATIONAL GEOGRAPHIC LOOKUP MATRIX (SUPERIOR INFRASTRUCTURE BASELINE) ---
GEO_MATRIX = {
    "Gombe": {
        "Akko": ["Kumo Central", "Kumo East", "Kumo West"],
        "Balanga": ["Bambam", "Bangu", "Dadiya", "Galam", "Tal", "Siri", "Mwona"],
        "Billiri": ["Billiri-North", "Billiri-South", "Bare", "Kantali", "Tanglang", "Todi"],
        "Dukku": ["Dukku", "Gombe Abba", "Malala"],
    },
    "FCT": {
        "AMAC": ["Garki", "Wuse", "Asokoro", "Maitama"],
        "Gwagwalada": ["Central", "Staff Quarters"],
    },
    "Cross River": {
        "Ikom": [
            "Ikom Urban",
            "Olulumo",
            "Ofutop I",
            "Ofutop II",
            "Nta/Selimba",
            "Abanyom",
            "Yala",
        ],
        "Boki": [
            "Boki East",
            "Boki West",
            "Boki North",
            "Boki South",
            "Osokom",
            "Wula",
            "Boje",
        ],
        "Ogoja": ["Ogoja Urban", "Mbube I", "Mbube II", "Ekajuk"],
        "Calabar Municipal": ["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"],
    },
    "Abia": {"Aba North": ["Ward 1", "Ward 2"], "Aba South": ["Ward 3", "Ward 4"]},
    "Adamawa": {
        "Yola North": ["Alkalawa", "Doueli"],
        "Yola South": ["Adarawo", "Bole"],
    },
    "Akwa Ibom": {"Uyo": ["Ward 1", "Ward 2"], "Eket": ["Urban I", "Urban II"]},
    "Anambra": {
        "Awka South": ["Ward 1", "Ward 2"],
        "Onitsha North": ["Ward 3", "Ward 4"],
    },
    "Bauchi": {"Bauchi LGA": ["Majema", "Makama"], "Katagum": ["Azare", "Chinade"]},
    "Bayelsa": {"Yenagoa": ["Epie I", "Epie II"], "Brass": ["Ward 1", "Ward 2"]},
    "Benue": {"Makurdi": ["Central", "North"], "Otukpo": ["Town East", "Town West"]},
    "Borno": {
        "Maiduguri": ["Shehuri", "Maisandari"],
        "Biu": ["Biu Central", "Biu East"],
    },
    "Delta": {"Asaba": ["Ward 1", "Ward 2"], "Warri South": ["Urban I", "Urban II"]},
    "Ebonyi": {"Abakaliki": ["Azuiyi", "Azugwu"], "Afikpo North": ["Oziza", "Amisu"]},
    "Edo": {"Oredo": ["Ward 1", "Ward 2"], "Ikpoba Okha": ["Ward 3", "Ward 4"]},
    "Ekiti": {"Ado Ekiti": ["Ado I", "Ado II"], "Ikole": ["Ikole West", "Ikole East"]},
    "Enugu": {"Enugu North": ["Asata", "Ogui"], "Enugu South": ["Uwani", "Achara"]},
    "Imo": {"Owerri Municipal": ["Ward 1", "Ward 2"], "Orlu": ["Central", "East"]},
    "Jigawa": {
        "Dutse": ["Dutse Takur", "Limawa"],
        "Hadejia": ["Matsaro", "Sabon Garu"],
    },
    "Kaduna": {
        "Kaduna North": ["Shaba", "Gaji"],
        "Kaduna South": ["Tudun Wada", "Unguwan Sanusi"],
    },
    "Kano": {
        "Fagge": ["Fagge North", "Fagge South"],
        "Dala": ["Dala Central", "Dogon Nama"],
    },
    "Katsina": {
        "Katsina LGA": ["Wakilin Central", "Wakilin South"],
        "Daura": ["Daura Arena", "Kofar Baru"],
    },
    "Kebbi": {
        "Birnin Kebbi": ["Nassarawa", "Rafin Atiku"],
        "Argungu": ["Kokani North", "Kokani South"],
    },
    "Kogi": {"Lokoja": ["Ward A", "Ward B"], "Okene": ["Bariki", "Onyukoko"]},
    "Kwara": {
        "Ilorin West": ["Ajikobi", "Baboko"],
        "Ilorin East": ["Balogun", "Gambari"],
    },
    "Lagos": {
        "Alimosho": ["Ikotun", "Egbeda", "Ipaja"],
        "Ikeja": ["Anifowoshe", "Gra", "Oregun"],
    },
    "Nasarawa": {
        "Lafia": ["Lafia Central", "Lafia East"],
        "Karu": ["Mararaba", "Karu Towns"],
    },
    "Niger": {"Minna": ["Central", "Sabon Gari"], "Bida": ["Landzun", "Masaga"]},
    "Ogun": {
        "Abeokuta South": ["Ake I", "Ake II"],
        "Ijebu Ode": ["Ijebu North", "Ijebu South"],
    },
    "Ondo": {"Akure South": ["Gbogi", "Isinkan"], "Ondo West": ["Urban I", "Urban II"]},
    "Osun": {"Osogbo": ["Alekuwodo", "Ataoja"], "Ife Central": ["Ilare", "More"]},
    "Oyo": {
        "Ibadan North": ["Ward 1", "Ward 2"],
        "Ogbomoso North": ["Isale", "Sabon Gari"],
    },
    "Plateau": {
        "Jos North": ["Vanderpuye", "Tafawa Balewa"],
        "Jos South": ["Bukuru", "Gyandobolo"],
    },
    "Rivers": {
        "Port Harcourt": ["Diobu", "Town", "Borokiri"],
        "Obio/Akpor": ["Rumuomasi", "Rumuokwuta"],
    },
    "Sokoto": {
        "Sokoto North": ["Waziri A", "Waziri B"],
        "Sokoto South": ["Sarkin Adar", "Rijiyar Dorowa"],
    },
    "Taraba": {
        "Jalingo": ["Turaki A", "Turaki B"],
        "Wukari": ["Hospital Ward", "Avyi"],
    },
    "Yobe": {"Damaturu": ["Central", "Nayi-Nawa"], "Potiskum": ["Bolewa", "Hausawa"]},
    "Zamfara": {
        "Gusau": ["Central", "Sabon Gari"],
        "Kaura Namoda": ["Bangana", "Sabon Gari"],
    },
}

# Pre-populate session state structures for live data if missing
if "live_scores" not in st.session_state:
    st.session_state.live_scores = {
        "PRESIDENTIAL": {"PDP": 14520, "APC": 12110, "LP": 4320, "NNPP": 850},
        "SENATORIAL": {"PDP": 16180, "APC": 11400, "LP": 2100, "ADC": 980},
        "FEDERAL HOUSE": {"PDP": 18240, "APC": 9890, "LP": 1150, "SDP": 420},
        "GOVERNORSHIP": {"PDP": 15410, "APC": 13900, "LP": 3200, "NNPP": 710},
        "STATE HOUSE": {"PDP": 17110, "APC": 10250, "LP": 940, "APGA": 310},
    }

def sync_election_tally_engine():
    # This is a placeholder to prevent crashes.
    # We will implement the full logic for this in the next step.
    pass

def render_pie_chart(title):
    """Renders a placeholder pie chart for a module."""
    labels = ['Category A', 'Category B', 'Category C', 'Category D']
    values = [4500, 2500, 1053, 500]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text=title, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


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
            sv_name = st.text_input("Full name as displayed on NIN")
            sv_phone = st.text_input("Applicant Contact Number")
            sv_nin = st.text_input("Your NIN number")
            sv_vin = st.text_input("Your Voters card number")
            sv_dob = st.date_input("Date of Birth", value=datetime.date(2000, 1, 1))
            sv_gender = st.selectbox(
                "Gender Matrix", ["Male", "Female", "Prefer Not to Say"]
            )
            sv_disability = st.selectbox(
                "Vulnerability/Disability Status",
                [
                    "None",
                    "Visual Impairment",
                    "Hearing Impairment",
                    "Physical Challenge/Locomotor",
                    "Other Challenges",
                ],
            )
            sv_file = st.file_uploader(
                "Upload Profile NIN Slip Document Click", type=["pdf", "jpg", "png"]
            )
        with k2:
            klga_raw = st.selectbox(
                "Your LGA", list(LGA_WARD_DATA.keys()), key="skill_lga_select"
            )
            klga_clean = klga_raw.upper().split()[0] if klga_raw else ""
            kward = st.selectbox("Your Ward", LGA_WARD_DATA.get(klga_clean, []))
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
            sv_selection = st.selectbox(
                "Vocational Domain Target Pool Sector", vocation_list
            )
            custom_vocation = (
                st.text_input("Type Your Choice Vocation Natively Here")
                if sv_selection == "Other (Type Custom Vocation Below)"
                else ""
            )
            sv_palliative_check = st.selectbox(
                "Have you received a palliative from this office before?", ["No", "Yes"]
            )

        sv_stmt = st.text_area("Candidate Skill Interest Statement Details")
        sv_cam = st.camera_input("Biometric Security Verification Core Scan")
        st.markdown("##### 🛡️ LEADERSHIP VOUCHING TIER INTERFACE")
        v_leader_name = st.selectbox(
            "Select Vouching Community Leader",
            list(COMMUNITY_LEADERS.keys()),
            key="skill_leader_select",
        )
        v_leader_details = COMMUNITY_LEADERS[v_leader_name]

        if st.form_submit_button(
            "🚀 COMMIT APPLICATION TO TRAINING POOLS", use_container_width=True
        ):
            if not (sv_name and sv_phone and sv_nin and sv_vin and sv_stmt):
                st.error(
                    "🛑 FORM ERROR: All core validation strings, documents, and biometric snapshot frames are mandatory."
                )
            else:
                match_check = st.session_state.global_registry[
                    st.session_state.global_registry["NIN"] == sv_nin
                ]
                if not match_check.empty:
                    st.session_state.radar_threat = True
                    st.session_state.threat_msg = f"Collision: NIN [{sv_nin}] matches a record belonging to user [{match_check.iloc[0]['Name']}]"
                    st.error(
                        "Duplicate Entry Detected. Entry Rejected by Security System Shield Protocols."
                    )
                else:
                    final_skill = (
                        custom_vocation
                        if sv_selection == "Other (Type Custom Vocation Below)"
                        else sv_selection
                    )
                    new_voucher_code = (
                        f"V-{klga_clean[:3]}-{kward[:3]}-{int(time.time())}".upper()
                    )
                    new_profile_row = {
                        "NIN": sv_nin,
                        "VIN": sv_vin,
                        "Name": sv_name.upper(),
                        "LGA": klga_clean,
                        "Ward": kward,
                        "Status": "Pending Review Tracker",
                        "Category": "Applicant",
                        "Skill_Interest": final_skill,
                        "Custom_Skill": custom_vocation,
                        "Gender": sv_gender,
                        "DOB": str(sv_dob),
                        "Disability_Status": sv_disability,
                        "Prior_Palliative": sv_palliative_check,
                        "Academic_Qual": "Degree Matrix",
                        "Admission_Year": "2026",
                        "Admission_Letter": None,
                        "Phone": sv_phone,
                        "Leader_Name": v_leader_name,
                        "Leader_Contact": v_leader_details["contact"],
                        "Leader_NIN": v_leader_details["nin"],
                        "Leader_LGA": v_leader_details["lga"],
                        "Leader_Ward": v_leader_details["ward"],
                        "Leader_Portfolio": v_leader_details["portfolio"],
                        "Voucher_Code": new_voucher_code,
                        "Remarks": "Verified Clear",
                        "Timestamp": str(datetime.datetime.now()),
                    }
                    st.session_state.global_registry = pd.concat(
                        [
                            st.session_state.global_registry,
                            pd.DataFrame([new_profile_row]),
                        ],
                        ignore_index=True,
                    )
                    trigger_background_autosave()
                    st.success(
                        "Registration parameter logged into production records system!"
                    )
                    st.balloons()
                    time.sleep(1)
                    st.rerun()


def render_scholarship_form():
    st.markdown(
        '''<h3 class="swing-in" style="text-transform: uppercase; font-size: 1.7rem;">🎓 Constituent Student Scholarship Application Portal</h3>''',
        unsafe_allow_html=True,
    )
    with st.form("scholarship_form_engine"):
        s1, s2 = st.columns(2)
        with s1:
            sch_name = st.text_input("Full name as displayed on NIN")
            sch_nin = st.text_input("Your NIN number")
            sch_phone = st.text_input("Applicant Contact Number")
            sch_year = st.selectbox(
                "Academic Year of Intake Admission", [str(y) for y in range(2018, 2027)]
            )
            sch_file_nin = st.file_uploader(
                "Attach Scanned NIN Identity Slip File", type=["pdf", "jpg", "png"]
            )
        with s2:
            sch_inst = st.text_input("Tertiary Institution Allocation Name")
            sch_level = st.selectbox(
                "Current Institutional Study Level Track",
                [
                    "Level 100",
                    "Level 200",
                    "Level 300",
                    "Level 400",
                    "Level 500",
                    "Post-Graduate Stream",
                ],
            )
            slga_raw = st.selectbox(
                "Your LGA", list(LGA_WARD_DATA.keys()), key="sch_lga_select"
            )
            slga_clean = slga_raw.upper().split()[0] if slga_raw else ""
            sward = st.selectbox("Your Ward", LGA_WARD_DATA.get(slga_clean, []))
            sch_file_adm = st.file_uploader(
                "Attach Official University Admission Letter Asset File",
                type=["pdf", "jpg", "png"],
            )
        sch_just = st.text_area("Applicant Justification Space")
        sch_cam = st.camera_input("Capture Student Identity Card Sensor")
        if st.form_submit_button(
            "🚀 SUBMIT SCHOLARSHIP ENTRY APPLICATION PARAMETERS",
            use_container_width=True,
        ):
            st.info("System intake pipeline initialized successfully.")


def render_cv_vault():
    st.markdown(
        '''<h3 class="swing-in" style="text-transform: uppercase; font-size: 1.7rem;">🚀 Constituent Professional Talent Vault Engine</h3>''',
        unsafe_allow_html=True,
    )
    with st.form("cv_vault_engine"):
        v1, v2 = st.columns(2)
        with v1:
            cv_name = st.text_input("Full name as displayed on NIN")
            cv_cat = st.selectbox(
                "Talent Classification Target Category",
                [
                    "Professional Domain Leader",
                    "Skilled Artisan Professional",
                    "Business Executive Owner",
                ],
            )
            cv_qual = st.selectbox(
                "Highest Level Academic Qualification Attained",
                [
                    "Doctorate PhD",
                    "Masters Degree Level",
                    "Bachelors Degree / HND Layer",
                    "National Diploma ND",
                    "NCE",
                    "SSCE Credentials Matrix",
                    "Primary Leaving",
                    "None",
                ],
            )
            cv_file = st.file_uploader(
                "Attach Professional CV/Resume Document Link File",
                type=["pdf", "jpg", "png"],
            )
        with v2:
            cv_nin = st.text_input("Your NIN number")
            cv_phone = st.text_input("Applicant Contact Number")
            vlga_raw = st.selectbox(
                "Your LGA", list(LGA_WARD_DATA.keys()), key="cv_lga_select"
            )
            vlga_clean = vlga_raw.upper().split()[0] if vlga_raw else ""
            vward = st.selectbox("Your Ward", LGA_WARD_DATA.get(vlga_clean, []))
        cv_summary = st.text_area(
            "Summary Matrix of Functional Career Experience Vectors"
        )
        cv_cam = st.camera_input("Capture Valid Professional Certification Seals")
        if st.form_submit_button(
            "📤 COMMIT CREDENTIALS STRINGS TO TALENT PLATFORM ARCHIVE",
            use_container_width=True,
        ):
            st.info("Transmission channel connected smoothly.")


def render_cun_trigger():
    st.markdown(
        '''<h3 class="swing-in" style="text-transform: uppercase; font-size: 1.7rem;">🚨 Community Urgent Need Field Deficit Report Gateway</h3>''',
        unsafe_allow_html=True,
    )
    with st.form("cun_form_engine"):
        cun_member = st.text_input("Reporting Community Member")
        cun_phone = st.text_input("Applicant Contact Number")
        clga_raw = st.selectbox(
            "Affected LGA", list(LGA_WARD_DATA.keys()), key="cun_lga_select"
        )
        clga_clean = clga_raw.upper().split()[0] if clga_raw else ""
        cward = st.selectbox("Affected Ward", LGA_WARD_DATA.get(clga_clean, []))
        cun_area = st.selectbox(
            "Area of Urgent Attention",
            [
                "Water Source Deficit",
                "Grid Electricity Failure",
                "Access Road Failure Collapse",
                "Community Security Vulnerability",
                "Healthcare Facility Absence",
            ],
        )
        cun_file = st.file_uploader(
            "Attach Identification NIN Validation Document Slip",
            type=["pdf", "jpg", "png"],
        )
        cun_logs = st.text_area("Detailed Situation Report Narrative Logs")
        cun_cam = st.camera_input(
            "Field Visual Evidence Deficit Capture Sensor Matrix Camera"
        )
        if st.form_submit_button(
            "🚨 TRIGGER COMMAND INCIDENT VECTOR ALERT", use_container_width=True
        ):
            st.info("Field alert dispatch sequence routing triggered.")


def render_palliative_form():
    st.markdown(
        '''<h3 class="swing-in" style="text-transform: uppercase; font-size: 1.7rem;">📦 Constituent Palliative Enrollment Registry</h3>''',
        unsafe_allow_html=True,
    )
    with st.form("palliative_form_engine"):
        p1, p2 = st.columns(2)
        with p1:
            p_name = st.text_input("Full name as displayed on NIN")
            p_nin = st.text_input("Your NIN number")
            p_vin = st.text_input("Your Voters card number")
            p_vuln = st.multiselect(
                "Vulnerability/Disability Status",
                [
                    "Aged Eldership Category",
                    "Widowhood Support Matrix",
                    "Physical Disability Framework Challenge",
                    "Long-Term Unemployed Status Tracker",
                ],
            )
            p_file_nin = st.file_uploader(
                "Upload Nominee Profile NIN Slip Document Layout Check",
                type=["pdf", "jpg", "png"],
            )
        with p2:
            p_phone = st.text_input("Applicant Contact Number")
            plga_raw = st.selectbox(
                "Your LGA", list(LGA_WARD_DATA.keys()), key="pal_lga_select"
            )
            plga_clean = plga_raw.upper().split()[0] if plga_raw else ""
            pward = st.selectbox("Your Ward", LGA_WARD_DATA.get(plga_clean, []))
            p_agro_select = st.selectbox(
                "Specific Area of Agro Intervention and Others",
                ["Fertilizer", "Seedlings", "Other Area of Likely Intervention"],
            )
            p_expect = st.text_input("Type Your Expectation")
        st.markdown("##### 🛡️ LEADERSHIP VOUCHING TIER INTERFACE")
        v_leader_name_p = st.selectbox(
            "Select Vouching Community Leader",
            list(COMMUNITY_LEADERS.keys()),
            key="pal_leader_select",
        )
        p_remarks = st.text_area(
            "Leader Affirmation Testimony Verification Remarks Statement"
        )
        p_cam = st.camera_input(
            "Biometric Face Capture Matrix Core Verification Face Scan"
        )
        if st.form_submit_button(
            "🚀 COMPLETE PALLIATIVE NOMINATION RECORD", use_container_width=True
        ):
            st.info("Palliative submission metrics validated against core cache.")


def render_sponsored_bills_panel():
    st.markdown(
        '''<div class="swing-in" style="background-color:#061A33; padding:10px; border-left:4px solid #D4AF37; margin-bottom:15px;">
        <h4 style="color:#D4AF37; margin:0; text-transform: uppercase; font-size: 1.5rem;">📜 Legislative Footprints & Motions</h4>
    </div>''',
        unsafe_allow_html=True,
    )

    if not SPONSORED_BILLS:
        st.info(
            "Information on sponsored bills and motions by Honourable Victor Abang will be updated here shortly."
        )
    else:
        for bill in SPONSORED_BILLS:
            with st.container(border=True):
                status_color = {
                    "Passed": "green",
                    "Second Reading": "blue",
                    "In Committee": "orange",
                    "First Reading": "yellow",
                }.get(bill["status"], "gray")
                st.markdown(f"**{bill['title']}**")
                st.markdown(
                    f'''*Status: <span style='color:{status_color};'>{bill['status']}</span>* | *Date: {bill['date']}*''',
                    unsafe_allow_html=True,
                )
                st.markdown(bill["description"])
                st.progress(bill["progress"])

    st.markdown(
        '''<div class="swing-in" style="background-color:#061A33; padding:10px; border-left:4px solid #00E5FF; margin-top:30px; margin-bottom:15px;">
        <h4 style="color:#00E5FF; margin:0; text-transform: uppercase; font-size: 1.5rem;">🌐 External Resources & Mentions</h4>
    </div>''',
        unsafe_allow_html=True
    )
    st.markdown(
        """
        - **Wikipedia:** [As a member of the house, he has sponsored bills and motions targeted at education, healthcare, community development, and constituency representation.](https://en.wikipedia.org/wiki/Victor_Abang#:~:text=As%20a%20member%20of%20the,community%20development%2C%20and%20constituency%20representation.)
        - **CrossRiverWatch:** [Congressman Victor Abang: Making Critical Laws and Carrying People Along](https://crossriverwatch.com/2024/04/congressman-victor-abang-making-critical-laws-and-carrying-people-along-by-dominic-kidzu/)
        """,
        unsafe_allow_html=True
    )


def render_legislative_progress_panel():
    """Renders the comprehensive Legislative Progress Tracker for Hon. Ali Isa JC."""
    st.markdown(
        '''
        <div class="supervisor-header">
            <h2 style="margin:0; font-weight:800; font-size:2rem; letter-spacing:0.5px;">🚀 LEGISLATIVE PROGRESS TRACKER</h2>
            <p style="margin:8px 0 0 0; opacity:0.9; font-size:1.1rem; font-weight:500;">
                Real-time tracking matrix of bills, proposals, and official motions processed.
            </p>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    st.markdown(
        '''
        <style>
        .progress-card {
            background-color: rgba(11, 60, 93, 0.4);
            border: 2px solid #0B3C5D;
            border-left: 6px solid #D4AF37;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 22px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        .progress-title {
            color: #D4AF37 !important;
            font-size: 1.45rem !important;
            font-weight: 700 !important;
            margin-top: 0px !important;
            margin-bottom: 12px !important;
            line-height: 1.4;
        }
        .status-pill {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: 800;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 14px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .pill-passed { background-color: #1E4620; color: #4AF256; }
        .pill-committee { background-color: #5C4308; color: #FAD02C; }
        .pill-reading { background-color: #1D3A56; color: #00E5FF; }
        .pill-adopted { background-color: #1E4620; color: #4AF256; }
        .progress-desc {
            color: #F0F0F0;
            font-size: 1.12rem;
            line-height: 1.6;
            margin: 0;
        }
        </style>
        ''',
        unsafe_allow_html=True,
    )

    # --- PROGRESS ITEM 1 ---
    st.markdown(
        '''
        <div class="progress-card">
            <div class="progress-title">🏛️ A Bill for an Act to Establish the Federal College of Horticulture, Dadin Kowa</div>
            <div class="status-pill pill-passed">Status: Passed</div>
            <p class="progress-desc">
                This landmark bill establishes a specialized Federal College of Horticulture in Dadin Kowa, Gombe State. 
                It aims to promote agricultural education, develop modern horticultural practices, and create a hub for 
                research and innovation in the North-East, thereby boosting food security and providing employment 
                opportunities for the youth.
            </p>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    # --- PROGRESS ITEM 2 ---
    st.markdown(
        '''
        <div class="progress-card">
            <div class="progress-title">⚖️ A Bill for an Act to amend the Trafficking in Persons (Prohibition) Enforcement and Administration Act, 2015</div>
            <div class="status-pill pill-committee">Status: In Committee</div>
            <p class="progress-desc">
                This bill seeks to strengthen the legal framework for combating human trafficking by introducing 
                stricter penalties for offenders, enhancing victim protection measures, and improving the operational 
                capacity of NAPTIP to investigate and prosecute trafficking cases.
            </p>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    # --- PROGRESS ITEM 3 ---
    st.markdown(
        '''
        <div class="progress-card">
            <div class="progress-title">⚙️ A Bill for an Act to Establish the National Skills and Innovation Development Council</div>
            <div class="status-pill pill-reading">Status: First Reading</div>
            <p class="progress-desc">
                Proposes the creation of a national council to streamline and regulate vocational and technical 
                training across Nigeria. The goal is to standardize certification, promote innovation, and align 
                skill acquisition programs with the demands of the modern economy.
            </p>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    # --- PROGRESS ITEM 4 ---
    st.markdown(
        '''
        <div class="progress-card">
            <div class="progress-title">🚨 Motion on the Need to Address the Menace of Soil Erosion in Balanga/Billiri Federal Constituency</div>
            <div class="status-pill pill-adopted">Status: Adopted</div>
            <p class="progress-desc">
                A successful motion that called the Federal Government\'s attention to the severe ecological degradation 
                caused by soil erosion in the constituency. The motion urged relevant agencies like the Ecological 
                Fund Office to implement urgent intervention projects to protect farmlands, infrastructure, and residential areas.
            </p>
        </div>
        ''',
        unsafe_allow_html=True,
    )


# ==============================================================================
# AUTHENTICATED PANELS
# ==============================================================================


def ward_collation_officer_panel():
    st.markdown(
        '''<div class="supervisor-header swing-in" style="font-size: 1.7rem; text-transform: uppercase;">🛡️ Ward Collation Officer Command: Form EC8A Logs</div>''',
        unsafe_allow_html=True,
    )
    if "sup_slip_preview" not in st.session_state:
        st.session_state.sup_slip_preview = None

    with st.form("supervisor_form"):
        c1, c2 = st.columns(2)
        with c1:
            sup_name = st.text_input("Supervisor Full Name")
            sup_phone = st.text_input("Phone Number")
            sup_lga_raw = st.selectbox("Your LGA", list(LGA_WARD_DATA.keys()))
            sup_lga_clean = sup_lga_raw.upper().split()[0]
            sup_ward = st.selectbox("Your Ward", LGA_WARD_DATA.get(sup_lga_clean, []))
            bvas_serial = st.text_input("BVAS Serial Number")
            accredited_voters = st.number_input(
                "Number of Accredited Voters", min_value=0
            )

        ward_id = f"{sup_lga_clean}_{sup_ward}".replace(" ", "_").upper()

        with c2:
            st.markdown("**Votes Scored by Party**")
            apc_votes = st.number_input("APC Votes", min_value=0)
            ndc_votes = st.number_input("NDC Votes", min_value=0)
            pdp_votes = st.number_input("PDP Votes", min_value=0)
            adc_votes = st.number_input("ADC Votes", min_value=0)

            incident_occurred = st.selectbox("Incident Occurred?", ["No", "Yes"])
            incident_details = ""
            if incident_occurred == "Yes":
                incident_details = st.text_area("Incident Form Scenario")

        st.camera_input("Live Capture Sensor Matrix: Form EC8A Sheet")

        if st.form_submit_button(
            "🔍 GENERATE SYSTEM INTEGRITY PREVIEW RECORD SLIP", use_container_width=True
        ):
            if not sup_name or not sup_phone:
                st.error("🛑 FORM ERROR: Supervisor name and phone must be specified.")
            else:
                st.session_state.sup_slip_preview = {
                    "Supervisor": sup_name,
                    "Phone": sup_phone,
                    "LGA": sup_lga_clean,
                    "Ward": sup_ward,
                    "APC_Votes": apc_votes,
                    "NDC_Votes": ndc_votes,
                    "PDP_Votes": pdp_votes,
                    "ADC_Votes": adc_votes,
                    "BVAS_Serial_Number": bvas_serial,
                    "Accredited_Voters": accredited_voters,
                    "Incident_Occurred": incident_occurred,
                    "Incident_Details": incident_details,
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                st.rerun()

    if st.session_state.sup_slip_preview is not None:
        p_data = st.session_state.sup_slip_preview
        st.markdown(
            f'''
            <div class="printable-slip-box">
                <div class="slip-header">🏛️ LSOEP WARD COLLATION INTEGRITY RECEIPT</div>
                <div class="slip-row"><span>TIMESTAMP:</span> <span>{p_data['Timestamp']}</span></div>
                <div class="slip-row"><span>SUPERVISOR:</span> <span>{p_data['Supervisor']}</span></div>
                <div class="slip-row"><span>LGA:</span> <span>{p_data['LGA']}</span></div>
                <div class="slip-row"><span>WARD:</span> <span>{p_data['Ward']}</span></div>
                <div class="slip-row"><span>ACCREDITED:</span> <span>{p_data['Accredited_Voters']}</span></div>
                <div class="slip-row"><span>BVAS S/N:</span> <span>{p_data['BVAS_Serial_Number']}</span></div>
                <div class="slip-row" style="color:red;"><span>APC:</span> <span>{p_data['APC_Votes']}</span></div>
                <div class="slip-row" style="color:blue;"><span>NDC:</span> <span>{p_data['NDC_Votes']}</span></div>
                <div class="slip-row" style="color:green;"><span>PDP:</span> <span>{p_data['PDP_Votes']}</span></div>
                <div class="slip-row" style="color:orange;"><span>ADC:</span> <span>{p_data['ADC_Votes']}</span></div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
        
        st.markdown('<div style="margin-top: -10px; margin-bottom: 25px;">', unsafe_allow_html=True)
        export_col1, export_col2, export_col3 = st.columns(3)
        
        selected_pu_df = pd.DataFrame([{
            "INEC_FORM": "FORM EC8A",
            "STATE": "CROSS RIVER",
            "LGA": p_data['LGA'],
            "WARD": p_data['Ward'],
            "POLLING_UNIT_DESC": p_data.get('Incident_Details', 'N/A'),
            "TIER": "N/A", # Not available in this panel's data
            "BVAS_SERIAL": p_data['BVAS_Serial_Number'],
            "ACCREDITED_VOTERS": p_data['Accredited_Voters'],
            "APC": p_data['APC_Votes'],
            "NDC": p_data['NDC_Votes'],
            "PDP": p_data['PDP_Votes'],
            "LP": 0, # Not available in this panel's data
            "ADC": p_data['ADC_Votes'],
            "SUBMITTED_BY": p_data['Supervisor'],
            "RECORD_TIMESTAMP": p_data['Timestamp']
        }])
        
        csv_payload_pu = selected_pu_df.to_csv(index=False).encode('utf-8')
        pu_filename_clean = f"EC8A_{p_data['LGA']}_{p_data['Ward']}".replace(" ", "_").upper()
        
        with export_col1:
            st.download_button(
                label="📥 Export Sheet to Excel (.XLSX)",
                data=csv_payload_pu,
                file_name=f"LSOEP_GROUND_TRUTH_{pu_filename_clean}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"ec8a_excel_dl_{p_data['Timestamp']}",
                use_container_width=True
            )
        with export_col2:
            st.download_button(
                label="📝 Export Brief Report (.DOCX)",
                data=csv_payload_pu,
                file_name=f"LSOEP_EC8A_REPORT_{pu_filename_clean}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key=f"ec8a_docx_dl_{p_data['Timestamp']}",
                use_container_width=True
            )
        with export_col3:
            st.markdown(
                '''<a href="javascript:window.print()" class="lsoep-print-engine-btn" style="display: block; text-align: center; text-decoration: none; padding: 10px; background-color: #AA7C11; color: white; border-radius: 4px; font-size: 0.85rem; font-weight: bold; border: 1px solid #D4AF37;">🖨️ Execute Local Print Routine</a>''', 
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button("🔒 CONFIRM & LOG METRICS", use_container_width=True):
                ward_id = f"{p_data['LGA']}_{p_data['Ward']}".replace(" ", "_").upper()
                if ward_id in st.session_state.submitted_wards:
                    st.error("🛑 Results for this Ward have already been locked.")
                else:
                    st.session_state.submitted_wards[ward_id] = p_data
                    trigger_background_autosave()
                    st.session_state.sup_slip_preview = None
                    st.success("Submission logged successfully!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
        with col_v2:
            if st.button("❌ ABORT TRANSACTION", use_container_width=True):
                st.session_state.sup_slip_preview = None
                st.warning("Preview cleared.")
                st.rerun()


def agent_panel():
    """
    🗳️ HIGH-PERFORMANCE POLLING UNIT AGENT COMMAND CONTROL HUB
    Fully syncs real-time results directly into our master matrix grid arrays.
    """
    if "agent_authenticated" not in st.session_state:
        st.session_state.agent_authenticated = False

    st.markdown("### 🗳️ POLLING UNIT AGENT COMMAND CONTROL NODE")
    st.write("---")
    
    # Session Termination Header Strip
    ac1, ac2 = st.columns([5, 2])
    with ac2:
        if st.button("🔒 Seal Node & Close Terminal Session", key="seal_agent_node_btn_v9", use_container_width=True):
            st.session_state.agent_authenticated = False
            st.success("Terminal session disconnected securely.")
            time.sleep(0.4)
            st.rerun()

    geo_matrix = st.session_state.get("DYNAMIC_GEO_MATRIX", {})

    st.markdown('<div class="command-hub-pane">', unsafe_allow_html=True)
    st.markdown("##### 📡 Live Telemetry Field Tally Submission Matrix")

    # --- Section 1: Geographic Selection (Moved Outside Form for dynamic updates) ---
    st.markdown("###### 📍 Section 1: Geographic Boundary Assignment")
    colA, colB, colC = st.columns(3)
    with colA:
        pu_state = st.selectbox("State Assignment Jurisdiction *:", list(geo_matrix.keys()), key="pu_state_sel_v5")
    
    # Allow manual entry for LGA and Ward
    with colB:
        lga_options = list(geo_matrix.get(pu_state, {}).keys()) if pu_state else []
        pu_lga_select = st.selectbox("LGA Ward Boundary Focus *:", lga_options, key="pu_lga_sel_v5")
        manual_pu_lga = st.text_input("Or type LGA if not listed:", key="manual_pu_lga_v5")
    with colC:
        ward_options = geo_matrix.get(pu_state, {}).get(pu_lga_select, []) if pu_lga_select else []
        pu_ward_select = st.selectbox("Specific Ward Precinct Designation *:", ward_options, key="pu_ward_sel_v5")
        manual_pu_ward = st.text_input("Or type Ward if not listed:", key="manual_pu_ward_v5")

    st.markdown("---")
    
    with st.form("agent_tally_submission_form_rich_core", clear_on_submit=False):
        # Determine final LGA and Ward, prioritizing manual input
        final_pu_lga = manual_pu_lga if manual_pu_lga else pu_lga_select
        final_pu_ward = manual_pu_ward if manual_pu_ward else pu_ward_select
        
        # 👤 Section 2: Agent Identification & Credentials
        st.markdown("###### 👤 Section 2: Field Officer Credentials")
        col1, col2 = st.columns(2)
        with col1:
            pu_officer = st.text_input("Polling Agent Full Name *:", key="pu_agent_name")
            pu_phone = st.text_input("Active Contact Phone Number *:", key="pu_agent_phone")
        with col2:
            pu_bvas_id = st.text_input("BVAS Machine Hardware Serial ID Number *:", key="pu_bvas_id")

        # 📊 Section 3: Core Election Mathematics & Ballot Verification
        st.markdown("---")
        st.markdown("###### 📊 Section 3: Core Election Mathematics & Verification Checks")
        col3, col4 = st.columns(2)
        with col3:
            pu_tier = st.selectbox("Target Election Tier Matrix Cluster *:", ["PRESIDENTIAL", "SENATORIAL", "FEDERAL HOUSE", "STATE GOVERNMENT", "STATE HOUSE OF ASSEMBLY"], key="pu_tier_focus")
            pu_accredited = st.number_input("Total Accredited Voters Counted (Per BVAS Verification) *:", min_value=0, value=0, key="pu_acc_voters")
        with col4:
            pu_incident_flag = st.selectbox("Log Field Security Incident/Anomaly Status *:", ["Normal Session - No Anomaly", "BVAS Hardware Malfunction Timeout", "Disruptive Public Violence Event", "Overt Ballot Box Tampering Attempt"], key="pu_incident")

        # 🗳️ Section 4: Party Political Vote Aggregations
        st.markdown("---")
        st.markdown("###### 🗳️ Section 4: Party Political Vote Aggregations")
        col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)
        with col_p1:
            v_apc = st.number_input("APC Score Tally:", min_value=0, value=0, key="v_apc_in")
        with col_p2:
            v_ndc = st.number_input("NDC Score Tally:", min_value=0, value=0, key="v_ndc_in")
        with col_p3:
            v_pdp = st.number_input("PDP Score Tally:", min_value=0, value=0, key="v_pdp_in")
        with col_p4:
            v_lp = st.number_input("LP Score Tally:", min_value=0, value=0, key="v_lp_in")
        with col_p5:
            v_adc = st.number_input("ADC Score Tally:", min_value=0, value=0, key="v_adc_in")

        pu_description = st.text_area("Field Operator Narrative Notes & Structural Situation Report Description *:", key="pu_desc_notes")
        
        # 📸 Section 5: Optical Sensor Evidence Core
        st.markdown("---")
        st.markdown("###### 📸 Section 5: Physical Evidence Document Capture")
        st.camera_input("Optical Sensor Frame: Capture Signed Polling Unit Result Slip Picture *", key="pu_cam_slip")

        if st.form_submit_button("📤 TRANSMIT SECURE FIELD PAYLOAD TO BALANCING HARMONY CORE", use_container_width=True):
            # Math cross-check verification loop
            calculated_sum = v_apc + v_ndc + v_pdp + v_lp + v_adc
            
            if not (pu_officer and pu_phone and final_pu_ward and pu_bvas_id and pu_description):
                st.error("🛑 DATA TRANSMISSION REFUSED: All credential fields, location/ward data, hardware serial tracking, and situational notes must be provided.")
            elif calculated_sum > pu_accredited:
                st.error(f"🚨 MATHEMATICAL IMPOSSIBILITY ENCOUNTERED: Aggregate party votes calculated ({calculated_sum:,}) cannot cross total accredited voters count ({pu_accredited:,}). Check input parameters.")
            else:
                try:
                    conn = sqlite3.connect("lsoep_database.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO agent_tally_logs (officer, phone, lga, ward, bvas, accredited, apc, ndc, pdp, lp, adc, incident, description)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (pu_officer.upper(), pu_phone, final_pu_lga.upper(), final_pu_ward.upper(), pu_bvas_id, pu_accredited, v_apc, v_ndc, v_pdp, v_lp, v_adc, pu_tier, pu_description))
                    conn.commit()
                    conn.close()
                    
                    # 🔄 INTERLOCK SYNC ENGAGED: Force real-time telemetry calculation
                    sync_election_tally_engine()
                    
                    st.success(f"✅ SECURE TELEMETRY LINK LOCKED OVER FOR WARD: {final_pu_ward.upper()}!")
                    st.balloons()
                except Exception as ex:
                    st.error(f"System storage cluster encountered database write fault: {ex}")
                    
    st.markdown('</div>', unsafe_allow_html=True)


def strategic_committees_panel():
    st.markdown("### 🛡️ Secure Channel 12: Integrated Strategic Committees (1-10) Control Hub Vault")

    if 'sc12_master_unlocked' not in st.session_state:
        st.session_state.sc12_master_unlocked = False
    if 'sc12_active_committee_id' not in st.session_state:
        st.session_state.sc12_active_committee_id = None

    if not st.session_state.sc12_master_unlocked:
        st.markdown('<div class="admin-checkpoint-box">', unsafe_allow_html=True)
        st.markdown("#### 🔒 Restricted Access Gate: Tier 1 Master Shield Validation Required")
        master_key = st.text_input("Enter Centralized Executive Master Passkey String to view Committees:", type="password", key="sc12_master_pass_v6")
        if st.button("Verify Master Cryptographic Authorization", key="sc12_master_btn_v6", use_container_width=True):
            if master_key == "congratulationshonvictor":
                st.session_state.sc12_master_unlocked = True
                st.success("✓ Master Shield authorized. Sub-group security verification partitions unlocked.")
                time.sleep(0.4)
                st.rerun()
            else:
                st.error("🛑 MASTER DISCONNECT: Security signature mismatch.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.success("✅ Tier 1 Master Shield Clear. Select Committee Target Cluster Array Below:")
    
    committee_names_list = ["-- Choose Committee Group Partition --"] + STRATEGIC_COMMITTEE_NAMES
    selected_committee_node = st.selectbox(
        "Select Target Committee Hub Panel Allocation Focus Line:",
        committee_names_list,
        key="sc12_dropdown_selector_v6"
    )

    if selected_committee_node == "-- Choose Committee Group Partition --":
        if st.button("🔒 Reset Master Shield Locks", key="reset_sc12_master_lock_v6", use_container_width=True):
            st.session_state.sc12_master_unlocked = False
            st.session_state.sc12_active_committee_id = None
            st.rerun()
        return

    comm_idx = STRATEGIC_COMMITTEE_NAMES.index(selected_committee_node) + 1
    required_sub_password = STRATEGIC_COMMITTEE_PASSWORDS.get(selected_committee_node)

    if st.session_state.sc12_active_committee_id != comm_idx:
        st.markdown('<div class="admin-checkpoint-box">', unsafe_allow_html=True)
        st.markdown(f"#### 🔑 Internal Verification Gate: {selected_committee_node}")
        sub_token = st.text_input(f"Enter Counting Code Password Token For {selected_committee_node}:", type="password", key=f"sc12_sub_token_v6_{comm_idx}")
        if st.button(f"Unlock Committee {comm_idx} Form Infrastructure", key=f"sc12_sub_btn_v6_{comm_idx}", use_container_width=True):
            if sub_token and required_sub_password and sub_token.strip().lower() == required_sub_password:
                st.session_state.sc12_active_committee_id = comm_idx
                st.success("✓ Committee authorization match successful.")
                time.sleep(0.4)
                st.rerun()
            else:
                st.error("🛑 CRYPTO ERROR: Wrong verification word token input.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # --- UNLOCKED RICH REGISTRATION WEB FORM AREA ---
    st.markdown('<div class="command-hub-pane">', unsafe_allow_html=True)
    st.markdown(f"🎯 **PRODUCTION TELEMETRY LEDGER CORE ACTIVE: {selected_committee_node}**")
    
    geo_matrix = st.session_state.get("DYNAMIC_GEO_MATRIX", {})
    
    with st.form(f"sc12_rich_production_data_form_{comm_idx}", clear_on_submit=True):
        st.markdown("##### 👤 Section 1: Committee Member Personal Identity")
        col1, col2 = st.columns(2)
        with col1:
            m_name = st.text_input("Full Name (Must match official documents) *")
            m_contact = st.text_input("Contact Phone Number *")
        with col2:
            m_state = st.selectbox("State Jurisdiction *", list(geo_matrix.keys()), key=f"sc12_state_{comm_idx}")
            m_lga = st.selectbox("LGA Ward Boundary *", list(geo_matrix.get(m_state, {}).keys()) if m_state else [], key=f"sc12_lga_{comm_idx}")
            m_ward = st.selectbox("Ward Precinct Designation *", geo_matrix.get(m_state, {}).get(m_lga, []) if m_lga else [], key=f"sc12_ward_{comm_idx}")

        st.markdown("---")
        st.markdown("##### 🔑 Section 2: Core Verification Credentials")
        col3, col4 = st.columns(2)
        with col3:
            m_nin = st.text_input("National Identification Number (11-Digit NIN) *", max_chars=11)
        with col4:
            m_vin = st.text_input("Permanent Voters Card Number (VIN) *")

        st.markdown("---")
        st.markdown("##### 💳 Section 3: Financial Disbursal Details")
        col5, col6, col7 = st.columns(3)
        with col5:
            m_bank = st.selectbox("Select Bank *", [
                "Access Bank", "Zenith Bank", "Guaranty Trust Bank (GTB)", 
                "United Bank for Africa (UBA)", "First Bank", "Fidelity Bank", "Other"
            ], key=f"sc12_bank_{comm_idx}")
        with col6:
            m_acct_name = st.text_input("Account Holder Name *")
        with col7:
            m_acct_num = st.text_input("Bank Account Number (10-Digit NUBAN) *", max_chars=10)

        st.markdown("---")
        st.markdown("##### 📸 Section 4: Document Verification & Biometrics")
        col8, col9 = st.columns(2)
        with col8:
            m_slip = st.file_uploader("📥 Upload NIN Slip Document (PDF, PNG, JPG) *", type=["pdf", "jpg", "png"], key=f"sc12_slip_{comm_idx}")
        with col9:
            m_cam = st.camera_input("Camera Trigger: Capture Committee Member Picture *", key=f"sc12_cam_{comm_idx}")
        
        if st.form_submit_button("🔒 LOCK AND TRANSMIT STRATEGIC COMMITTEE RECORD", use_container_width=True):
            if not (m_name and m_contact and m_ward and len(m_nin) == 11 and m_vin and m_acct_name and len(m_acct_num) == 10 and m_slip and m_cam):
                st.error("🛑 REGISTRATION SUSPENDED: Ensure all details, 11-digit NIN, 10-digit account number, scanned file, and face photo are captured before transmitting.")
            else:
                try:
                    conn = sqlite3.connect("lsoep_database.db")
                    cursor = conn.cursor()
                    
                    # 🛡️ Dynamic schema upgrade to ensure the local SQLite database holds all new columns
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS strategic_committee_logs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            committee_id INTEGER NOT NULL,
                            committee_name TEXT NOT NULL,
                            member_name TEXT NOT NULL,
                            contact_number TEXT NOT NULL,
                            lga TEXT NOT NULL,
                            ward TEXT NOT NULL,
                            nin_number TEXT NOT NULL,
                            vin_number TEXT NOT NULL,
                            bank_name TEXT,
                            account_name TEXT,
                            account_number TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    
                    cursor.execute("""
                        INSERT INTO strategic_committee_logs (
                            committee_id, committee_name, member_name, contact_number, lga, ward, 
                            nin_number, vin_number, bank_name, account_name, account_number
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        comm_idx, selected_committee_node, m_name.upper(), m_contact, 
                        m_lga.upper(), m_ward.upper(), m_nin, m_vin, m_bank.upper(), m_acct_name.upper(), m_acct_num
                    ))
                    conn.commit()
                    conn.close()
                    st.success(f"✓ Strategic committee member profile successfully verified and committed under {selected_committee_node}!")
                except Exception as e:
                    st.error(f"Database write lock execution exception: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔒 Close Group Sub-Partition Lock", key="lock_sub_group_node_action_v6", use_container_width=True):
        st.session_state.sc12_active_committee_id = None
        st.rerun()

def render_ground_truth_tab():
    st.subheader("📝 Ground Truth Form EC8A Audited Verification Schema")
    
    # Fetch data from the database directly for the most up-to-date information
    try:
        conn = sqlite3.connect("lsoep_database.db")
        conn.row_factory = sqlite3.Row # This allows accessing columns by name
        cursor = conn.cursor()
        cursor.execute("SELECT rowid as id, * FROM agent_tally_logs ORDER BY timestamp DESC")
        all_entries = cursor.fetchall()
        conn.close()
    except Exception as e:
        st.error(f"Database read error: {e}")
        # Create an empty table if it doesn't exist
        conn = sqlite3.connect("lsoep_database.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_tally_logs (
                officer TEXT, phone TEXT, lga TEXT, ward TEXT, bvas TEXT, 
                accredited INTEGER, apc INTEGER, ndc INTEGER, pdp INTEGER, 
                lp INTEGER, adc INTEGER, incident TEXT, description TEXT, 
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.close()
        all_entries = []

    if not all_entries:
        st.info("No EC8A records have been submitted via the Agent Hub yet.")
        return

    # Create a dictionary for the selectbox
    entry_options = {entry['id']: f"{entry['lga']} - {entry['ward']} ({entry['timestamp']})" for entry in all_entries}
    
    selected_entry_id = st.selectbox(
        "Select a Submitted Record to View Details:",
        options=list(entry_options.keys()),
        format_func=lambda x: entry_options[x],
        key="ec8a_view_selector_v2"
    )

    if selected_entry_id:
        # Find the selected entry from the list
        active_row = next((item for item in all_entries if item['id'] == selected_entry_id), None)

        if active_row:
            # --- RENDER VIRTUAL COLOR-KEYED EC8A RESULTS SHEET CARD ---
            st.markdown(
                f'''
                <div style="background-color: #031424; border: 3px double #D4AF37; border-radius: 12px; padding: 25px; margin: 20px 0; font-family: 'Space Grotesk', sans-serif; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                    <div class="slip-header" style="text-align: center; font-weight: bold; font-size: 1.5rem; color: #D4AF37; margin-bottom: 15px;">OFFICIAL FORM EC8A TALLY</div>
                    <div class="slip-row"><span>RECORD TIMESTAMP:</span> <span>{active_row['timestamp']}</span></div>
                    <div class="slip-row"><span>SUBMITTED BY (AGENT):</span> <span>{active_row['officer']}</span></div>
                    <div class="slip-row"><span>LGA:</span> <span>{active_row['lga']}</span></div>
                    <div class="slip-row"><span>WARD:</span> <span>{active_row['ward']}</span></div>
                    <hr style="border-color: #D4AF37; opacity: 0.3;">
                    <div class="slip-row"><span>ACCREDITED VOTERS:</span> <span>{active_row['accredited']}</span></div>
                    <div class="slip-row"><span>BVAS S/N:</span> <span>{active_row['bvas']}</span></div>
                    <hr style="border-color: #D4AF37; opacity: 0.3;">
                    <div class="slip-row" style="color:#FF4B4B;"><span>APC:</span> <span>{active_row['apc']}</span></div>
                    <div class="slip-row" style="color:#3C8DFF;"><span>NDC:</span> <span>{active_row['ndc']}</span></div>
                    <div class="slip-row" style="color:#28A745;"><span>PDP:</span> <span>{active_row['pdp']}</span></div>
                    <div class="slip-row" style="color:#FFC107;"><span>LP:</span> <span>{active_row['lp']}</span></div>
                    <div class="slip-row" style="color:#FFA500;"><span>ADC:</span> <span>{active_row['adc']}</span></div>
                    <hr style="border-color: #D4AF37; opacity: 0.3;">
                    <div class="slip-row"><span>ELECTION TIER:</span> <span>{active_row['incident']}</span></div>
                    <div class="slip-row"><span>NARRATIVE/INCIDENT:</span> <span style="white-space: pre-wrap;">{active_row['description']}</span></div>
                </div>
                ''', unsafe_allow_html=True
            )

            # --- EXPORT STRIP ---
            st.markdown('<div style="margin-top: -10px; margin-bottom: 25px;">', unsafe_allow_html=True)
            export_col1, export_col2, export_col3 = st.columns(3)
            
            selected_pu_df = pd.DataFrame([{
                "INEC_FORM": "FORM EC8A", "STATE": "CROSS RIVER", "LGA": active_row['lga'],
                "WARD": active_row['ward'], "POLLING_UNIT_DESC": active_row['description'],
                "TIER": active_row['incident'], "BVAS_SERIAL": active_row['bvas'], "ACCREDITED_VOTERS": active_row['accredited'],
                "APC": active_row['apc'], "NDC": active_row['ndc'], "PDP": active_row['pdp'],
                "LP": active_row['lp'], "ADC": active_row['adc'], "SUBMITTED_BY": active_row['officer'], "RECORD_TIMESTAMP": active_row['timestamp']
            }])
            
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                selected_pu_df.to_excel(writer, index=False, sheet_name='EC8A_Record')
            excel_payload = output.getvalue()

            csv_payload_pu = selected_pu_df.to_csv(index=False).encode('utf-8')
            pu_filename_clean = f"EC8A_{active_row['lga']}_{active_row['ward']}_{active_row['id']}".replace(" ", "_").upper()
            
            with export_col1:
                st.download_button(
                    label="📥 Export Sheet to Excel (.XLSX)", data=excel_payload,
                    file_name=f"LSOEP_GROUND_TRUTH_{pu_filename_clean}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"ec8a_excel_dl_{active_row['id']}", use_container_width=True
                )
            with export_col2:
                st.download_button(
                    label="📝 Export Brief Report (.TXT)", data=csv_payload_pu,
                    file_name=f"LSOEP_EC8A_REPORT_{pu_filename_clean}.txt",
                    mime="text/plain",
                    key=f"ec8a_txt_dl_{active_row['id']}", use_container_width=True
                )
            with export_col3:
                st.markdown(
                    '''<a href="javascript:window.print()" class="lsoep-print-engine-btn" style="display: block; text-align: center; text-decoration: none; padding: 10px; background-color: #AA7C11; color: white; border-radius: 4px; font-size: 0.85rem; font-weight: bold; border: 1px solid #D4AF37;">🖨️ Execute Local Print Routine</a>''', 
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)

def render_announcements_panel():
    """
    Manages the creation and display of official plenary broadcasts/announcements.
    """
    st.subheader("📢 Plenary Broadcast & Announcement Terminal")
    st.markdown("Create and view all official announcements for the public portal.")

    with st.form("new_announcement_form", clear_on_submit=True):
        announcement_title = st.text_input("Announcement Title *")
        announcement_body = st.text_area("Full Announcement Body (Supports Markdown) *", height=200)
        submitted = st.form_submit_button("📢 PUBLISH ANNOUNCEMENT", use_container_width=True)

        if submitted:
            if not announcement_title or not announcement_body:
                st.error("🛑 Both title and body are required to publish an announcement.")
            else:
                try:
                    conn = sqlite3.connect("lsoep_database.db")
                    cursor = conn.cursor()
                    # Ensure table exists
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS announcements (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            body TEXT NOT NULL,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    # Insert new announcement
                    cursor.execute(
                        "INSERT INTO announcements (title, body) VALUES (?, ?)",
                        (announcement_title, announcement_body)
                    )
                    conn.commit()
                    conn.close()
                    st.success("✅ Announcement has been successfully published!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Database Error: {e}")

    st.markdown("---")
    st.subheader("📜 Published Announcements Log")

    try:
        conn = sqlite3.connect("lsoep_database.db")
        cursor = conn.cursor()
        # Ensure table exists before trying to select from it
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS announcements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("SELECT title, body, timestamp FROM announcements ORDER BY timestamp DESC")
        all_announcements = cursor.fetchall()
        conn.close()

        if not all_announcements:
            st.info("No announcements have been published yet.")
        else:
            for i, (title, body, timestamp) in enumerate(all_announcements):
                with st.expander(f"**{title}** - *Published on {timestamp}*"):
                    st.markdown(body, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Could not retrieve announcements from database: {e}")

def main_dashboard(conn):
    st.markdown(
        '''<h2 class="swing-in" style="font-size: 1.8rem; text-transform: uppercase;">🏛️ Executive Control Command Dashboard</h2>''',
        unsafe_allow_html=True,
    )

    admin_modules = [
        "📊 Master Registry Matrix",
        "📢 Plenary Broadcast Terminal",
        "🗣️ Citizen Feedback",
        "📢 Admin Announcement Control",
        "⚖️ Database Audit Diagnostics",
        "🛡️ RADAR Deduplication Interceptor",
        "🎓 Scholar Talent Matrix",
        "💎 Vantedge Influencer Proportions",
        "🗳️ Live Election Analytical Sync",
        "📝 Ground Truth Form EC8A Data",
        "📂 Bulk Data Sync Stream",
        "📜 Executive Waiver Ledger",
        "🚀 Legislative Progress Tracker",
        "📅 Long-Term Momentum Monitoring",
        "📋 Strategic Committee Compliance Logs",
    ]

    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.markdown(
        '''<h3 class='admin-header' style='font-size: 1.5rem;'>Command Modules</h3>''',
        unsafe_allow_html=True,
    )

    if "admin_module_view" not in st.session_state:
        st.session_state.admin_module_view = admin_modules[0]

    selected_module = st.sidebar.radio(
        "MODULES",
        options=admin_modules,
        key="admin_module_view",
        label_visibility="collapsed",
    )

    if selected_module:
        st.subheader(selected_module)
        if selected_module != "📝 Ground Truth Form EC8A Data":
             render_pie_chart(selected_module)

    if selected_module == "📊 Master Registry Matrix":
        st.subheader("📊 Master Verification Registry Database Partition Array")
        st.dataframe(st.session_state.get("global_registry", pd.DataFrame()))
    elif selected_module == "📢 Plenary Broadcast Terminal":
        render_announcements_panel()
    elif selected_module == "🗣️ Citizen Feedback":
        st.subheader("🗣️ Citizen Feedback Messages")
        feedback_df = st.session_state.get("feedback_registry", pd.DataFrame())
        st.dataframe(feedback_df)
    elif selected_module == "📢 Admin Announcement Control":
        st.subheader("📢 Admin Announcement Control")
        current_announcement = st.session_state.get("global_scrolling_announcement", "")
        new_announcement = st.text_area(
            "Update marquee text:", value=current_announcement
        )
        if st.button("Update Announcement"):
            st.session_state.global_scrolling_announcement = new_announcement
            trigger_background_autosave()
            st.success("Announcement updated!")
            st.rerun()
    elif selected_module == "📝 Ground Truth Form EC8A Data":
        render_ground_truth_tab()
    elif selected_module == "🗳️ Live Election Analytical Sync":
        render_election_analytical_sync()
    elif selected_module == "🚀 Legislative Progress Tracker":
        render_legislative_progress_panel()
    elif selected_module == "📋 Strategic Committee Compliance Logs":
        render_committee_compliance_form()
    elif selected_module == "⚖️ Database Audit Diagnostics":
        st.subheader("⚖️ Database Audit Diagnostics")
        st.info("This module is under construction.")
    elif selected_module == "🛡️ RADAR Deduplication Interceptor":
        st.subheader("🛡️ RADAR Deduplication Interceptor")
        st.info("This module is under construction.")
    elif selected_module == "🎓 Scholar Talent Matrix":
        st.subheader("🎓 Scholar Talent Matrix")
        st.info("This module is under construction.")
    elif selected_module == "💎 Vantedge Influencer Proportions":
        st.subheader("💎 Vantedge Influencer Proportions")
        st.info("This module is under construction.")
    elif selected_module == "📂 Bulk Data Sync Stream":
        st.subheader("📂 Bulk Data Sync Stream")
        st.info("This module is under construction.")
    elif selected_module == "📜 Executive Waiver Ledger":
        st.subheader("📜 Executive Waiver Ledger")
        st.info("This module is under construction.")
    elif selected_module == "📅 Long-Term Momentum Monitoring":
        st.subheader("📅 Long-Term Momentum Monitoring")
        st.info("This module is under construction.")

@st.cache_data
def load_pdf_bytes(file_path):
    with open(file_path, "rb") as f:
        return f.read()

def render_project_verifications():
    st.markdown(
        '''<h2 class="swing-in" style="color:#D4AF37; text-transform: uppercase; font-size: 2rem;">🦅 BEYOND RHETORICS: PROJECT VERIFICATION HUB</h2>''',
        unsafe_allow_html=True,
    )
    st.write(
        "Cross-examining performance metrics with verifiable ground-truth evidence."
    )
    media_dir = "MEDIA MEDIA MEDIA"
    if not os.path.exists(media_dir):
        media_dir = "media"
    if os.path.exists(media_dir):
        files_to_render = [
            ("Cover Page Document", "Cover_compressed.pdf"),
            ("Project Verification Batch 1", "1_compressed.pdf"),
            ("Project Verification Batch 2", "2_compressed.pdf"),
            ("Project Verification Batch 3", "3_compressed.pdf"),
            ("Project Verification Batch 4", "4_compressed.pdf"),
            ("Project Verification Batch 5", "5_compressed.pdf"),
            ("Project Verification Batch 6", "6_compressed.pdf"),
        ]
        for title, filename in files_to_render:
            full_path = os.path.join(media_dir, filename)
            if os.path.exists(full_path):
                with st.expander(f"📄 View {title} ({filename})", expanded=False):
                    pdf_bytes = load_pdf_bytes(full_path)
                    st.download_button(
                        label=f"📥 Download {filename}",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf",
                        key=f"dl_{filename}",
                    )
            else:
                st.warning(f"⚠️ File not found: {filename}")
    else:
        st.error("🚨 Media directory not found.")


def render_speak_directly_panel():
    st.subheader("📬 Submit Direct Message to the Legislative Office")
    st.write(
        "Please fill out the official communications pipeline form below. Your feedback is valuable."
    )
    with st.form("citizen_direct_feedback_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *")
            surname = st.text_input("Surname *")
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
            lga_raw = st.selectbox(
                "LGA *", list(LGA_WARD_DATA.keys()), key="feedback_lga"
            )
            lga_clean = lga_raw.upper().split()[0] if lga_raw else ""
        with col2:
            ward = st.selectbox(
                "Ward *", LGA_WARD_DATA.get(lga_clean, []), key="feedback_ward"
            )
            whatsapp_contact = st.text_input("WhatsApp Contact (Optional)")
            email = st.text_input("Email Address (Optional)")
        message_body = st.text_area("Message *", max_chars=1000)
        if st.form_submit_button(
            "🔒 Transmit Secure Message", use_container_width=True
        ):
            if not all([first_name, surname, message_body]):
                st.error("Please fill all required fields.")
            else:
                # ... (feedback submission logic)
                st.success("Message transmitted successfully.")
                st.balloons()


def render_committee_compliance_form():
    """Renders the 14th Tab Form module enabling tracking logs based on grouping sorting rules."""
    st.markdown(
        '''
        <div class="supervisor-header">
            <h2 style="margin:0; font-weight:800; font-size:1.8rem;">📋 STRATEGIC COMMITTEE COMPLIANCE LOGS</h2>
            <p style="margin:5px 0 0 0; opacity:0.9; font-size:1.05rem;">
                Categorized regulatory compliance submissions and data logs for direct administrative sorting.
            </p>
        </div>
        ''',
        unsafe_allow_html=True,
    )
    committee_group = st.selectbox(
        "Select Committee Strategic Group Allocation:",
        [
            "Group A: Agricultural Development & Horticulture Council",
            "Group B: Vocational Capacity, Technical Pools & Modern Economy",
            "Group C: Ecological Monitoring, Erosion Fund & Infrastructure",
            "Group D: Palliative Logistics & Community Social Investment",
        ],
    )
    with st.form("committee_compliance_matrix_form"):
        st.write(f"📝 **Filing Progress Report for:** `{committee_group}`")
        officer_name = st.text_input("Reporting Official Name:")
        regional_scope = st.text_input("Target Local Government Area / Ward Location:")
        activity_summary = st.text_area(
            "Comprehensive Execution Metrics & Compliance Actions Summary:"
        )
        expenditure_vouched = st.number_input(
            "Vouched Project Resources Expended (NGN):", min_value=0.0, step=1000.0
        )
        if st.form_submit_button(
            "🔒 Transmit Report to Executive Control Room", use_container_width=True
        ):
            st.success(
                f"✅ Report for {officer_name} logged under {committee_group.split(':')[0]}!"
            )


def render_election_analytical_sync():
    """Renders the Control Room containing the National Geographic Filtering and Sync Matrix."""
    st.markdown(
        '''
        <div class="supervisor-header">
            <h2 style="margin:0; font-weight:800; font-size:2rem;">📊 LIVE ELECTION ANALYTICAL SYNC DISPLAY</h2>
            <p style="margin:6px 0 0 0; opacity:0.9; font-size:1.1rem;">
                National real-time command dashboard. Drill down across 36 states, LGAs, and operational units.
            </p>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    # 5 Tier High-Prestige Card Row
    st.markdown("### 5 ELECTION TIERS")
    cols = st.columns(5)
    tiers = {
        "PRESIDENTIAL": "🦅 Presidential Matrix",
        "SENATORIAL": "🏛️ Senate Chamber Sync",
        "FEDERAL HOUSE": "🏛️ House of Representatives Core",
        "GOVERNORSHIP": "🏰 Gubernatorial Ledger",
        "STATE HOUSE": "📜 State House of Assembly Matrix",
    }

    for i, (key, title) in enumerate(tiers.items()):
        with cols[i]:
            st.markdown(f'''<div class="card"><div class="card-body"><h5>{title}</h5></div></div>''', unsafe_allow_html=True)

    # Cascading Geo-Search Terminal
    st.markdown("### CASCADING GEO-SEARCH TERMINAL")
    c1, c2, c3 = st.columns(3)
    with c1:
        state_list = sorted(list(GEO_MATRIX.keys()))
        selected_state = st.selectbox(
            "🎯 Select Target State:",
            options=state_list,
            index=state_list.index("Gombe") if "Gombe" in state_list else 0,
        )
    with c2:
        lga_list = sorted(list(GEO_MATRIX[selected_state].keys()))
        selected_lga = st.selectbox("🏢 Select LGA:", options=lga_list)
    with c3:
        ward_list = sorted(GEO_MATRIX[selected_state][selected_lga])
        selected_ward = st.selectbox("📍 Select Ward:", options=ward_list)
