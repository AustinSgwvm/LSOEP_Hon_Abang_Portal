# ==============================================================================
# 🏛️ LSOEP FEDERAL MASTER REGISTRY & GEOGRAPHIC DATA LAYER
# Project: Ikom/Boki Federal Constituency (Honourable Victor Abang, PhD)
# File: registry.py (Aggregated Master Data & Session Memory State Core)
# ==============================================================================

import streamlit as st
import pandas as pd
import os
import json

# Institutional Software Display Branding Variables
HON_TITLE = "Honourable Victor Abang, PhD"
CONSTITUENCY_DESC = "Ikom/Boki Federal Constituency (Cross River State)"

GEOGRAPHY = {
    "Ikom LGA": [
        'Abanyum', 'Akam', 'Ikom Urban', 'Nde', 'Nta Nselle', 'Ofutop I', 
        'Ofutop II', 'Olulumo', 'Yala', 'Nnam', 'Nkum'
    ],
    "Boki LGA": [
        'Abo', 'Boje', 'Beebo/Bumaji', 'Budi', 'Bunyia', 'Ekpashi', 'Iku', 
        'Kakwagom/Bawop', 'Katchuan', 'Oku/Borum/Njua', 'Okundi', 'Osokom I', 
        'Osokom II', 'Wula'
    ],
}

LGA_WARD_DATA = {
    "IKOM": GEOGRAPHY["Ikom LGA"],
    "BOKI": GEOGRAPHY["Boki LGA"],
}

# 🏛️ EXPLICIT COMMUNITY STAKEHOLDER DIRECTORY
COMMUNITY_LEADERS = {
    "Honourable Victor Abang, PhD": {
        "contact": "08000000000",
        "nin": "00000000000",
        "lga": "IKOM",
        "ward": "Ikom Urban",
        "portfolio": "Federal Representative, Ikom/Boki",
    },
}

# ==============================================================================
# LEGISLATIVE DATA (As per user update)
# ==============================================================================
SPONSORED_BILLS = [
    {
        "title": "A Bill for an Act to Establish the Federal College of Agriculture, Ikom, Cross River State",
        "description": "This bill seeks to establish a dedicated federal institution for agricultural education and research in Ikom, aiming to boost the local agrarian economy, provide specialized training, and promote modern farming techniques in the region.",
        "status": "First Reading",
        "date": "2023-11-15",
        "progress": 20,
    },
    {
        "title": "A Bill for an Act to Amend the National Health Act for Improved Rural Healthcare Access",
        "description": "This proposed amendment aims to allocate specific funding and resources for the upgrade of primary healthcare centers in rural constituencies, including Ikom and Boki, ensuring better access to quality medical services for all citizens.",
        "status": "In Committee",
        "date": "2024-02-05",
        "progress": 40,
    },
    {
        "title": "A Bill for an Act to Provide for the Rehabilitation of the Calabar-Ikom-Ogoja Federal Highway",
        "description": "This bill calls for the urgent reconstruction and dualization of the critical Calabar-Ikom-Ogoja highway to improve transportation, reduce travel time, and enhance economic activities across Cross River State.",
        "status": "Second Reading",
        "date": "2023-12-10",
        "progress": 60,
    },
    {
        "title": "A Bill for an Act to Promote Youth Entrepreneurship and Skill Development in Ikom/Boki",
        "description": "This bill proposes the creation of a dedicated fund and support framework to provide grants, training, and mentorship for young entrepreneurs and artisans within the Ikom/Boki federal constituency.",
        "status": "Passed",
        "date": "2023-09-20",
        "progress": 100,
    }
]

# ==============================================================================
# STRATEGIC COMMITTEE CREDENTIALS
# ==============================================================================
STRATEGIC_COMMITTEE_NAMES = [
    "Committee 1: Finance & Appropriations",
    "Committee 2: Healthcare & Social Welfare",
    "Committee 3: Education & Human Capital",
    "Committee 4: Infrastructure & Public Works",
    "Committee 5: Agriculture & Rural Development",
    "Committee 6: Security & Community Affairs",
    "Committee 7: Youth & Sports Development",
    "Committee 8: Women Affairs & Inclusion",
    "Committee 9: Legislative Liaison & Compliance",
    "Committee 10: Constituency Outreach & Engagement",
]

STRATEGIC_COMMITTEE_PASSWORDS = {
    "Committee 1: Finance & Appropriations": "ten",
    "Committee 2: Healthcare & Social Welfare": "nine",
    "Committee 3: Education & Human Capital": "eight",
    "Committee 4: Infrastructure & Public Works": "seven",
    "Committee 5: Agriculture & Rural Development": "six",
    "Committee 6: Security & Community Affairs": "five",
    "Committee 7: Youth & Sports Development": "four",
    "Committee 8: Women Affairs & Inclusion": "three",
    "Committee 9: Legislative Liaison & Compliance": "two",
    "Committee 10: Constituency Outreach & Engagement": "one",
}

PROJECT_PARTITION_ID = "Ikom/Boki_CROSS_RIVER"
COLUMNS_STRUCTURE = [
    "NIN", "VIN", "Name", "LGA", "Ward", "Status", "Category", "Skill_Interest",
    "Custom_Skill", "Gender", "DOB", "Disability_Status", "Prior_Palliative",
    "Academic_Qual", "Admission_Year", "Admission_Letter", "Phone",
    "Leader_Name", "Leader_Contact", "Leader_NIN", "Leader_LGA",
    "Leader_Ward", "Leader_Portfolio", "Voucher_Code", "Remarks", "Timestamp",
]
STRATEGIC_COMMITTEE_COLS = [
    "Committee_Node", "First_Name", "Surname", "Contact_Number", "Gender",
    "Account_Number", "Account_Name", "Bank", "LGA", "Ward", "NIN_Number",
    "Voters_Card_Number", "Timestamp",
]
LITIGATION_AGENT_COLS = [
    "Polling_Unit_Name", "Ward_Collation_Officer_Key", "Accredited_Voters",
    "APC_Votes", "NDC_Votes", "PDP_Votes", "ADC_Votes", "BVAS_Serial_Number",
    "Incident_Occurred", "Incident_Form_Scenario", "Timestamp",
]

OFFLINE_REGISTRY_CACHE = "offline_registry_cache.csv"
OFFLINE_METADATA_CACHE = "offline_metadata_cache.json"
ANNOUNCEMENT_CACHE_FILE = "announcement_cache.txt"


def initialize_system_states():
    if "global_scrolling_announcement" not in st.session_state:
        try:
            with open(ANNOUNCEMENT_CACHE_FILE, "r") as f:
                st.session_state.global_scrolling_announcement = f.read()
        except FileNotFoundError:
            st.session_state.global_scrolling_announcement = "NOTICE: OFFICIAL DIGITAL LEDGER GATEWAY DEPLOYED FOR TRANSPARENT ACCOUNTABILITY."
    if "global_registry" not in st.session_state:
        st.session_state.global_registry = pd.DataFrame(columns=COLUMNS_STRUCTURE)
    if "strategic_committee_registry" not in st.session_state:
        st.session_state.strategic_committee_registry = pd.DataFrame(columns=STRATEGIC_COMMITTEE_COLS)
    if "committee_double_dipping_ledger" not in st.session_state:
        st.session_state.committee_double_dipping_ledger = {}
    if "submitted_wards" not in st.session_state:
        st.session_state.submitted_wards = {}
    if "submitted_pus" not in st.session_state:
        st.session_state.submitted_pus = {}
    if "agent_field_registry" not in st.session_state:
        st.session_state.agent_field_registry = pd.DataFrame(columns=LITIGATION_AGENT_COLS)
    if "radar_threat" not in st.session_state:
        st.session_state.radar_threat = False
    if "threat_msg" not in st.session_state:
        st.session_state.threat_msg = ""
    if "authenticated_committee" not in st.session_state:
        st.session_state.authenticated_committee = None
        
    if "plenary_broadcast_feed" not in st.session_state:
        st.session_state.plenary_broadcast_feed = [
            {
                "timestamp": "2024-07-15 12:00:00",
                "type": "Text Only",
                "message": "Welcome to the Live Plenary Update Feed for Honourable Victor Abang, PhD. Official legislative broadcasts from the chamber floor will appear below.",
                "media": None
            }
        ]
