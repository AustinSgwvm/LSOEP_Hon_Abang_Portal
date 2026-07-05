import os
import base64
import streamlit as st
import pandas as pd
import json

OFFLINE_REGISTRY_CACHE = "offline_registry_cache.csv"
OFFLINE_METADATA_CACHE = "offline_metadata_cache.json"
COLUMNS_STRUCTURE = [
    "NIN",
    "VIN",
    "Name",
    "LGA",
    "Ward",
    "Status",
    "Category",
    "Skill_Interest",
    "Custom_Skill",
    "Gender",
    "DOB",
    "Disability_Status",
    "Prior_Palliative",
    "Academic_Qual",
    "Admission_Year",
    "Admission_Letter",
    "Phone",
    "Leader_Name",
    "Leader_Contact",
    "Leader_NIN",
    "Leader_LGA",
    "Leader_Ward",
    "Leader_Portfolio",
    "Voucher_Code",
    "Remarks",
    "Timestamp",
]


def image_to_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def trigger_background_autosave():
    try:
        st.session_state.global_registry.to_csv(OFFLINE_REGISTRY_CACHE, index=False)
        meta_payload = {
            "submitted_wards": st.session_state.submitted_wards,
            "submitted_pus": st.session_state.submitted_pus,
        }
        with open(OFFLINE_METADATA_CACHE, "w") as f:
            json.dump(meta_payload, f)
    except Exception as e:
        st.caption(f"Autosave sync bypass: {e}")


def initialize_and_recover_system_states():
    if "global_registry" not in st.session_state:
        if os.path.exists(OFFLINE_REGISTRY_CACHE):
            try:
                st.session_state.global_registry = pd.read_csv(OFFLINE_REGISTRY_CACHE)
            except Exception:
                os.remove(OFFLINE_REGISTRY_CACHE)

        if "global_registry" not in st.session_state:
            st.session_state.global_registry = pd.DataFrame(
                [
                    {
                        "NIN": "23456789012",
                        "VIN": "90FVA2345678901",
                        "Name": "Besong Abang",
                        "LGA": "BILLIRI",
                        "Ward": "TURE",
                        "Status": "Verified",
                        "Category": "Professional",
                        "Skill_Interest": "ICT & AI Core Programming",
                        "Custom_Skill": "",
                        "Gender": "Male",
                        "DOB": "1994-04-12",
                        "Disability_Status": "None",
                        "Prior_Palliative": "No",
                        "Academic_Qual": "Degree/HND",
                        "Admission_Year": "2024",
                        "Admission_Letter": None,
                        "Phone": "08039999999",
                        "Leader_Name": "Hon. Ali Isa JC",
                        "Leader_Contact": "08038888888",
                        "Leader_NIN": "33333333333",
                        "Leader_LGA": "BILLIRI",
                        "Leader_Ward": "TURE",
                        "Leader_Portfolio": "Community Leader",
                        "Voucher_Code": "BL01V",
                        "Remarks": "Authentic",
                        "Timestamp": "2026-05-15 10:00:00",
                    },
                    {
                        "NIN": "87654321098",
                        "VIN": "90FVA8765432109",
                        "Name": "Agnes Etta",
                        "LGA": "BALANGA",
                        "Ward": "DADIYA",
                        "Status": "Flagged",
                        "Category": "Skilled Artisan",
                        "Skill_Interest": "Solar Renewable Energy Engineering",
                        "Custom_Skill": "",
                        "Gender": "Female",
                        "DOB": "1998-09-21",
                        "Disability_Status": "None",
                        "Prior_Palliative": "Yes",
                        "Academic_Qual": "SSCE",
                        "Admission_Year": "2025",
                        "Admission_Letter": None,
                        "Phone": "08037777777",
                        "Leader_Name": "Chief Ogar",
                        "Leader_Contact": "08036666666",
                        "Leader_NIN": "44444444444",
                        "Leader_LGA": "BALANGA",
                        "Leader_Ward": "DADIYA",
                        "Leader_Portfolio": "Clergy",
                        "Voucher_Code": "BA02V",
                        "Remarks": "Verify Biometrics",
                        "Timestamp": "2026-05-15 11:15:22",
                    },
                ],
                columns=COLUMNS_STRUCTURE,
            )

    if (
        "submitted_wards" not in st.session_state
        or "submitted_pus" not in st.session_state
    ):
        recovered_meta = False
        if os.path.exists(OFFLINE_METADATA_CACHE):
            try:
                with open(OFFLINE_METADATA_CACHE, "r") as f:
                    meta_payload = json.load(f)
                st.session_state.submitted_wards = meta_payload.get(
                    "submitted_wards", {}
                )
                st.session_state.submitted_pus = meta_payload.get("submitted_pus", {})
                recovered_meta = True
            except Exception:
                os.remove(OFFLINE_METADATA_CACHE)

        if not recovered_meta:
            st.session_state.submitted_wards = {
                "BILLIRI_TURE": "2026-05-15 08:12:04",
                "BALANGA_DADIYA": "2026-05-15 09:45:10",
            }
            st.session_state.submitted_pus = {
                "BILLIRI_TURE_PU001": '{"Presidential": 120, "Senatorial": 245, "Governorship": 190, "State_House": 210, "Timestamp": "2026-05-15 08:10:00", "Agent": "Ojong Ogar", "EC8A_Status": "Verified_PNG"}',
                "BALANGA_DADIYA_PU003": '{"Presidential": 95, "Senatorial": 310, "Governorship": 220, "State_House": 185, "Timestamp": "2026-05-15 09:30:15", "Agent": "Eno Takim", "EC8A_Status": "Verified_JPG"}',
            }

    if "current_page" not in st.session_state:
        st.session_state.current_page = "skill_form"
    if "radar_threat" not in st.session_state:
        st.session_state.radar_threat = False
    if "threat_msg" not in st.session_state:
        st.session_state.threat_msg = ""
    if "recycle_bin_registry" not in st.session_state:
        st.session_state.recycle_bin_registry = None
    if "recycle_bin_wards" not in st.session_state:
        st.session_state.recycle_bin_wards = {}
    if "recycle_bin_pus" not in st.session_state:
        st.session_state.recycle_bin_pus = {}
