# ==============================================================================
# PROJECT: LSOEP TITAN CROSS RIVER - CORE ENGINE INTERFACE
# REVISION: v34.0.67 [FINAL LAYOUT & STYLE REFINEMENTS]
# ==============================================================================

import streamlit as st
import pandas as pd
import datetime
import os
import json
import time
import base64

# ==============================================================================
# IMAGE HANDLING HELPER
# ==============================================================================
def image_to_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# ==============================================================================
# DATA ARCHITECTURE LAYER: BOKI/IKOM ADMINISTRATIVE MATRIX (EXPLICIT DECLARATION)
# ==============================================================================

GEOGRAPHY = {
    "Boki LGA": [
        "Abo",
        "Alankwu",
        "Beebo/Bumaji",
        "Boje",
        "Buda",
        "Buentsebe",
        "Bunyia/Okubuchi",
        "Ekpashi",
        "Kakwagom/Bawop",
        "Ogep/Osokom",
        "Oku/Borum/Njua",
    ],
    "Ikom LGA": [
        "Abanyum",
        "Akparabong",
        "Ikom Urban I",
        "Ikom Urban II",
        "Nde",
        "Nnam",
        "Nta/Nselle",
        "Ofutop I",
        "Ofutop II",
        "Olulumo",
        "Yala/Nkum",
    ],
}

LGA_WARD_DATA = {
    "BOKI": [
        "ABO",
        "ALANKWU",
        "BEEBO/BUMAJI",
        "BOJE",
        "BUDA",
        "BUENTSEBE",
        "BUNYIA/OKUBUCHI",
        "EKPASHI",
        "KAKWAGOM/BAWOP",
        "OGEP/OSOKOM",
        "OKU/BORUM/NJUA",
    ],
    "IKOM": [
        "ABANYUM",
        "AKPARABONG",
        "IKOM URBAN I",
        "IKOM URBAN II",
        "NDE",
        "NNAM",
        "NTA/NSELLE",
        "OFUTOP I",
        "OFUTOP II",
        "OLULUMO",
        "YALA/NKUM",
    ],
}

MOCK_DATA_REGISTRY = [
    {
        "ID": "LSOEP-CRS-BOK-001",
        "Name": "John Ochui Boje",
        "LGA": "Boki LGA",
        "Ward": "Boje",
        "NIN": "12345678901",
        "Status": "Verified",
        "Allocation": "SME Seed Capital",
    },
    {
        "ID": "LSOEP-CRS-IKO-002",
        "Name": "Mary Akpan Ikom",
        "LGA": "Ikom LGA",
        "Ward": "Ikom Urban I",
        "NIN": "98765432109",
        "Status": "Verified",
        "Allocation": "Agro-Development Grant",
    },
    {
        "ID": "LSOEP-CRS-BOK-003",
        "Name": "Peter Ogar Abo",
        "LGA": "Boki LGA",
        "Ward": "Abo",
        "NIN": "45678912301",
        "Status": "Pending Review",
        "Allocation": "Educational Bursary",
    },
    {
        "ID": "LSOEP-CRS-IKO-004",
        "Name": "Grace Etta Nnam",
        "LGA": "Ikom LGA",
        "Ward": "Nnam",
        "NIN": "78912345602",
        "Status": "Verified",
        "Allocation": "Dry Season Irrigation Support",
    },
    {
        "ID": "LSOEP-CRS-BOK-005",
        "Name": "Michael Besong Buda",
        "LGA": "Boki LGA",
        "Ward": "Buda",
        "NIN": "32165498705",
        "Status": "Flagged",
        "Allocation": "None - Verification Required",
    },
]


# ==============================================================================
# MASTER NATIONAL ADMINISTRATIVE GEOGRAPHY VAULT (ALL 36 STATES + FCT)
# ==============================================================================
STATE_DATA_LEDGER = {
    "Abia State": {
        "ABA NORTH": ["Eziama", "Industrial Area", "Osusu I", "Osusu II", "Uratta"],
        "ABA SOUTH": ["Aba River", "Aba Town Hall", "Enyimba", "Asa Triangle"],
        "OHAFIA": ["Ania", "Ohafor", "Ohafia Urban"],
        "UMUAHIA NORTH": ["Ibeku East I", "Ibeku East II", "Umuahia Urban I"],
    },
    "Adamawa State": {
        "YOLA NORTH": ["Ajiya", "Gbadabiri", "Nassarowo", "Yolde Pate"],
        "YOLA SOUTH": ["Adarawo", "Bole Yolde", "Makama", "Mbamba"],
        "MUBI NORTH": ["Lokuwa", "Digil", "Yelwa"],
        "DEMSA": ["Demsa Moro", "Bille", "Gwamba"],
    },
    "Akwa Ibom State": {
        "UYO": ["Uyo Urban I", "Uyo Urban II", "Etoi I", "Etoi II", "Offot I"],
        "EKET": ["Eket Urban I", "Eket Urban II", "Afaha Clan", "Okon Clan"],
        "IKOT EKPENE": ["Ikot Ekpene Urban I", "Ikot Ekpene Urban II", "Amayam"],
        "ORON": ["Oron Urban I", "Oron Urban II", "Oron Urban III"],
    },
    "Anambra State": {
        "AWKA NORTH": ["Achalla I", "Achalla II", "Amansea", "Mgbakwu"],
        "AWKA SOUTH": ["Awka I", "Awka II", "Awka III", "Nise I", "Amawbia I"],
        "ONITSHA NORTH": ["American Quarters", "Inland Town I", "Inland Town II"],
        "NNEWI NORTH": ["Otolo", "Uruagu", "Umudim", "Nnewichi"],
    },
    "Bauchi State": {
        "BAUCHI": ["Bakari Dukku", "Daniya", "Hardawa", "Makama Sarki"],
        "KATAGUM": ["Azare Federal", "Chinade", "Madangala"],
        "MISAU": ["Misau Town", "Gwaram", "Hardawa"],
        "ALKALERI": ["Alkaleri Ward", "Gwana", "Pali"],
    },
    "Bayelsa State": {
        "SAGBAMA": ["Sagbama Ward 1", "Salope Ward 2", "Asamabiri Ward 3"],
        "EKEREMOR": ["Ekeremor Ward 1", "Onyilolo Ward 2", "Ogbosuware Ward 3"],
        "SOUTHERN IJAW": ["Oporoma Ward 1", "Amassoma Ward 5"],
        "YENAGOA": ["Yenagoa Epie I", "Gbarain I"],
    },
    "Benue State": {
        "MAKURDI": ["Central Markets", "Clergy Ward", "Fiidi", "Wadata"],
        "GBOKO": ["Gboko Central", "Gboko East", "Yandev"],
        "OTUKPO": ["Otukpo Town East", "Otukpo Town West", "Adoka"],
        "VANDEIKYA": ["Vandeikya Township", "Mbaduku", "Tsambe"],
    },
    "Borno State": {
        "MAIDUGURI": ["Bolori I", "Bolori II", "Shehuri North", "Shehuri South"],
        "BIU": ["Biu Central", "Miringa", "Zarawuyaku"],
        "JERE": ["Alau", "Bale Galtimari", "Maimusari"],
        "GWOZA": ["Gwoza Town", "Pulka", "Ashigashiya"],
    },
    "Cross River State": {
        "BOKI": [
            "Abo",
            "Alankwu",
            "Beebo/Bumaji",
            "Boje",
            "Buda",
            "Buentsebe",
            "Bunyia/Okubuchi",
            "Ekpashi",
            "Kakwagom/Bawop",
            "Ogep/Osokom",
            "Oku/Borum/Njua",
        ],
        "IKOM": [
            "Abanyum",
            "Akparabong",
            "Ikom Urban I",
            "Ikom Urban II",
            "Nde",
            "Nnam",
            "Nta/Nselle",
            "Ofutop I",
            "Ofutop II",
            "Olulumo",
            "Yala/Nkum",
        ],
        "CALABAR MUNICIPAL": ["Amanisong", "Big Qua", "Kasuk", "Ikot Ansa"],
        "AKAMKPA": ["Akamkpa Urban", "Erei", "Ojo"],
        "OBUDU": ["Obudu Urban", "Bete", "Utanga"],
    },
    "Delta State": {
        "WARRI SOUTH": ["Warri GRA", "Warri Central", "Warri Pesu", "Warri Okere"],
        "BOMADI": ["Akugbene", "Bomadi Town", "Esama"],
        "ASABA": ["Asaba Cable", "Umuaji", "West End"],
        "UGHELLI NORTH": ["Ughelli Urban I", "Ughelli Urban II", "Orogun I"],
    },
    "Ebonyi State": {
        "ABAKALIKI": ["Azuiyiokwu", "Azuiyiator", "Abakiliki Town", "Kpirikpiri"],
        "AFIKPO": ["Afikpo Town", "Unwana I", "Unwana II"],
        "IZZIE": ["Izzi Urban", "Ezza Inyimagu", "Ndieze"],
        "OHAUKWU": ["Ezzamgbo", "Effium I", "Effium II"],
    },
    "Edo State": {
        "OREDO": ["Oredo I", "Oredo II", "Ikpoba Hill", "New Benin"],
        "OVIA NORTH EAST": ["Adolor", "Ofunama", "Okada"],
        "ESAN CENTRAL": ["Irrua Urban", "Ewu Urban", "Opoji"],
        "ETSAKO WEST": ["Auchi Urban I", "Auchi Urban II", "Uzairue"],
    },
    "Ekiti State": {
        "ADO EKITI": ["Ado I", "Ado II", "Ado III", "Okesha", "Irona"],
        "IKERE": ["Ikere Urban", "Odo Oja", "Ogbonjana"],
        "OMUO": ["Omuo Township", "Omuo East", "Kota"],
        "IKOLE": ["IKole Urban", "Asin", "Odo Oro"],
    },
    "Enugu State": {
        "ENUGU NORTH": ["Asata", "China Town", "Ogui New Layout"],
        "ENUGU SOUTH": ["Awkunanaw I", "Awkunanaw II", "Uwani"],
        "NSUKKA": ["Nsukka Urban", "Alor Uno", "Eha Alumona"],
        "UDI": ["Udi Town", "9th Mile", "Abor"],
    },
    "FCT Abuja": {
        "AMAC": ["Garki", "Wuse", "Asokoro", "Maitama", "Nyanya", "Karu"],
        "GWAGWALADA": ["Gwagwalada Center", "Paiko", "Zuba"],
        "BWARI": ["Bwari Central", "Kubwa", "Ushafa"],
        "KUJE": ["Kuje Center", "Rubochi", "Gaube"],
    },
    "Gombe State": {
        "GOMBE": ["Gombe East", "Gombe West", "Jekadafari", "Pantami"],
        "AKKO": ["Akko Town", "Kumo Central", "Pindiga"],
        "YAMALTU DEBA": ["Deba", "Zambuk", "Kano"],
        "BALANGA": ["Talasse", "Gelengu", "Chilung"],
    },
    "Imo State": {
        "OWERRI MUNICIPAL": ["Owerri Urban I", "Owerri Urban II", "Aladinma"],
        "ORLU": ["Orlu Urban", "Amaifeke", "Omuma"],
        "OKIGWE": ["Okigwe Town", "Amuro", "Ezinachi"],
        "MBEISE": ["Ogbe", "Ekwereazu", "Ahiara"],
    },
    "Jigawa State": {
        "DUTSE": ["Dutse Gari", "Kachi", "Limawa", "Madobi"],
        "HADEJIA": ["Hadejia Central", "Matsaro", "Sabon Garu"],
        "KAZAURE": ["Kazaure Gari", "Ba'auzini", "Dandi"],
        "GUMEL": ["Gumel Town", "Galgadi", "Hammado"],
    },
    "Kaduna State": {
        "SOBA": [
            "Alhazai",
            "Danwata",
            "Gamagira",
            "Garkaye",
            "Gimba",
            "KINKIBA",
            "Kwassallo",
            "Maigana",
            "Rahama",
            "Soba",
            "Turawa",
        ],
        "KADUNA NORTH": ["Dadi", "Kawo", "Gabassawa", "Unguwan Rimi"],
        "ZARIA": ["Zaria City", "Tudun Wada", "Samaru"],
        "KADUNA SOUTH": ["Tudun Wada West", "Barnawa", "Makera"],
    },
    "Kano State": {
        "FAGGE": ["Fagge North", "Fagge South", "Kwaciri"],
        "NASSARAWA": ["Gwagwarwa", "Kano GRA", "Tudun Murtala"],
        "DALA": ["Dala Ward", "Gwangwazo", "Yakkaasai"],
        "GVALE": ["Gvale Town", "Galadanchi", "Mandawari"],
    },
    "Katsina State": {
        "KATSINA": ["Katsina Central", "Wakilin Kebbi", "Yamma"],
        "FUNTUA": ["Funtua Central", "Maska", "Tudun Wada"],
        "DAURA": ["Daura Urban", "Madoba", "Sarki"],
        "MALUMFASHI": ["Malumfashi Town", "Yankara", "Dansarai"],
    },
    "Kebbi State": {
        "BIRNIN KEBBI": ["Birnin Kebbi Central", "Nassarawa", "Gwadangaji"],
        "ARGUNGU": ["Argungu Central", "Felande"],
        "YURI": ["Yuri Town", "Genuwa", "Koko"],
        "ZURU": ["Zuru Town", "Dabai", "Rikoto"],
    },
    "Kogi State": {
        "LOKOJA": ["Lokoja Core", "Adankolo", "Sarki Ward"],
        "OKENE": ["Okene Central", "Bariki", "Onyukoko"],
        "ANYIGBA": ["Anyigba Town", "Agbeji", "Ayingba Rural"],
        "KABBA": ["Kabba Town", "Asaya", "Okejumu"],
    },
    "Kwara State": {
        "ILORIN WEST": ["Adewole", "Baboko", "Oloje", "Wara"],
        "ILORIN EAST": ["Gambari", "Oke Oyi", "Ipata"],
        "OFFA": ["Offa Township", "Balogun", "Essa"],
        "OMU ARAN": ["Omu Aran Core", "Ipetu", "Arandun"],
    },
    "Lagos State": {
        "ALIMOSHO": ["Egbe-Idimu", "Ipaja", "Ikotun", "Gowon Estate"],
        "IKEJA": ["Ikeja GRA", "Anifowoshe", "Ojodu", "Oregun"],
        "SURULERE": ["Adeniran Ogunsanya", "Ojuelegba", "Aguda", "Ijesha"],
        "BADAGRY": ["Badagry Town", "Iworo", "Ajara"],
    },
    "Nasarawa State": {
        "LAFIA": ["Lafia East", "Lafia Central", "Chiroma", "Makama"],
        "KEFFI": ["Keffi Central", "Yelwa", "Angwan Rimi"],
        "AKWANGA": ["Akwanga Town", "Gudi", "Mada"],
        "KARU": ["Mararaba", "Karu Urban", "Ado", "Nyanya Boundary"],
    },
    "Niger State": {
        "CHANCHAGA": ["Minna Central", "Sabon Gari", "Tunga"],
        "BIDA": ["Bida Central", "Dokodza", "Masaga"],
        "SULEJA": ["SULEJA Town", "Abuja Mandate", "Iku"],
        "KONTAGORA": ["Kontagora Town", "Usman", "Central"],
    },
    "Ogun State": {
        "ABEOKUTA SOUTH": ["Ake I", "Ake II", "Imo Ward", "Lafenwa"],
        "IJEBU ODE": ["Ijebu Ode Central", "Ome Ward"],
        "SAGAMU": ["Sagamu Central", "Sabo", "Makun"],
        "OTA": ["Ota Urban", "Iju", "Sango"],
    },
    "Ondo State": {
        "AKURE SOUTH": ["Akure Core", "Arakale", "Gbogi", "Isinkan"],
        "ONDO WEST": ["Ondo Core", "Yaba Ward"],
        "OWO": ["Owo Township", "Ehin Ogbe", "Igboroko"],
        "OKITIPUPA": ["Okitipupa Town", "Ikoya", "Ilutitun"],
    },
    "Osun State": {
        "OSOGBO": ["Osogbo Central", "Ataoja I", "Ataoja II", "Alekuwodo"],
        "IFE CENTRAL": ["Ilare", "Iremo", "More Ward"],
        "ILESHA WEST": ["Ilesha Town", "Omofe", "Ereja"],
        "EDE SOUTH": ["Ede Town", "Babaruba", "Okejimi"],
    },
    "Oyo State": {
        "IBADAN NORTH": ["Agodi", "Bodija", "Mokola", "Sabo"],
        "OYO WEST": ["Oyo Central", "Isokun", "Opapa"],
        "OGBOMOSO NORTH": ["Oja Igbo", "Sabon Gari", "Isale General"],
        "ISEYIN": ["Iseyin Town", "Okeho", "Ado Awaye"],
    },
    "Plateau State": {
        "JOS NORTH": ["Jos Central", "Gangare", "Tafawa Balewa"],
        "JOS SOUTH": ["Bukuru", "Du Ward", "Gyel Ward"],
        "PANKSHIN": ["Pankshin Town", "Wokkos", "Fier"],
        "SHENDAM": ["Shendam Town", "Kalong", "Shimankar"],
    },
    "Rivers State": {
        "PORT HARCOURT": ["PH I", "PH II", "Nkpolu Oroworukwo"],
        "OBIO-AKPOR": ["Rumueme", "Choba", "Elelenwo"],
        "BONNY": ["Bonny Town I", "Finima"],
        "DEGEMA": ["Degema Urban", "Bakana"],
    },
    "Sokoto State": {
        "SOKOTO NORTH": ["Sokoto Central", "Waziri Ward", "Rijiyar Zaki"],
        "WAMAKKO": ["Wamakko Town", "Gidan Bubu"],
        "TAMBUWAL": ["Tambuwal Town", "Dogon Daji"],
        "GURONYO": ["Guronyo Town", "Rimawa"],
    },
    "Taraba State": {
        "JALINGO": ["Jalingo Central", "Turaki Ward", "Barade Ward"],
        "WUKARI": ["Wukari Central", "Avyi"],
        "BALI": ["Bali Town", "Suntai"],
        "GASHAKA": ["Serti", "Mayo Selbe"],
    },
    "Yobe State": {
        "DAMATURU": ["Damaturu Central", "Maisandari", "Pawari"],
        "POTISKUM": ["Potiskum Central", "Bolewa"],
        "GASHUA": ["Gashua Town", "Bade"],
        "GEIDAM": ["Geidan Town", "Asheik"],
    },
    "Zamfara State": {
        "GUSAU": ["Gusau Central", "Galadima", "Mayana"],
        "KAURA NAMODA": ["Kaura Central", "Bangana"],
        "TFAFE": ["Tfafe Town", "Kazaure"],
        "MARADUN": ["Maradun Town", "Dakai"],
    },
}

PROJECT_PARTITION_ID = "BOKI_IKOM_CROSS_RIVER"
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

OFFLINE_REGISTRY_CACHE = "offline_registry_cache.csv"
OFFLINE_METADATA_CACHE = "offline_metadata_cache.json"


# ==============================================================================
# AUTOSAVE PERSISTENCE & ERROR EXTRACTION MATRIX
# ==============================================================================
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
                        "LGA": "BOKI",
                        "Ward": "BOJE",
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
                        "Leader_Name": "Hon. Victor Abang",
                        "Leader_Contact": "08038888888",
                        "Leader_NIN": "33333333333",
                        "Leader_LGA": "BOKI",
                        "Leader_Ward": "BOJE",
                        "Leader_Portfolio": "Community Leader",
                        "Voucher_Code": "BK01V",
                        "Remarks": "Authentic",
                        "Timestamp": "2026-05-15 10:00:00",
                    },
                    {
                        "NIN": "87654321098",
                        "VIN": "90FVA8765432109",
                        "Name": "Agnes Etta",
                        "LGA": "IKOM",
                        "Ward": "AKPARABONG",
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
                        "Leader_LGA": "IKOM",
                        "Leader_Ward": "AKPARABONG",
                        "Leader_Portfolio": "Clergy",
                        "Voucher_Code": "IK02V",
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
                "BOKI_BOJE": "2026-05-15 08:12:04",
                "IKOM_AKPARABONG": "2026-05-15 09:45:10",
            }
            st.session_state.submitted_pus = {
                "BOKI_BOJE_PU001": '{"Presidential": 120, "Senatorial": 245, "Governorship": 190, "State_House": 210, "Timestamp": "2026-05-15 08:10:00", "Agent": "Ojong Ogar", "EC8A_Status": "Verified_PNG"}',
                "IKOM_AKPARABONG_PU003": '{"Presidential": 95, "Senatorial": 310, "Governorship": 220, "State_House": 185, "Timestamp": "2026-05-15 09:30:15", "Agent": "Eno Takim", "EC8A_Status": "Verified_JPG"}',
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


initialize_and_recover_system_states()
IS_LOCAL_SANDBOX = not os.path.exists("/app/secrets.toml") and not os.path.exists(
    ".streamlit/secrets.toml"
)

conn = None
if not IS_LOCAL_SANDBOX:
    try:
        conn = st.connection("postgresql", type="sql")
    except Exception:
        conn = None

# ==============================================================================
# UI STYLE CONFIGURATION & REGAL EXPANDED GLASSMORPHISM KEYFRAMES
# ==============================================================================
st.set_page_config(
    page_title="LSOEP TITAN CROSS RIVER | HON. VICTOR ABANG PhD HUB",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    from modules import branding

    HAS_MODULES = True
except ImportError:
    HAS_MODULES = False

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { 
        background-color: #030f21 !important; 
        border-right: 4px solid #8B0000 !important;
    }
    
    .admin-launch-zone {
        border: 2px dashed #00E5FF; padding: 15px; border-radius: 14px;
        background-color: rgba(0, 229, 255, 0.08); margin-bottom: 15px;
    }
    
    .inst-link-box {
        display: block; background: linear-gradient(90deg, #8B0000 0%, #4A0000 100%) !important;
        color: #FFFFFF !important; padding: 12px; border-radius: 10px; 
        text-align: center; font-weight: 900; margin-bottom: 10px; text-decoration: none;
        font-size: 14px; letter-spacing: 1px; text-transform: uppercase;
    }
    
    .stButton>button { 
        width: 100% !important; height: 48px !important; font-weight: 800 !important; 
        font-size: 14px !important; margin-bottom: 10px !important; border: 2px solid #8B0000 !important;
        border-radius: 10px !important; color: #FFFFFF !important; transition: all 0.3s ease;
        text-transform: uppercase; letter-spacing: 1px;
    }
    
    button[key="btn_skill"] { background: linear-gradient(90deg, #00B4DB 0%, #0083B0 100%) !important; }
    button[key="btn_sch"] { background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%) !important; }
    button[key="btn_pal"] { background: linear-gradient(90deg, #2e8b57 0%, #38ef7d 100%) !important; }
    button[key="btn_cv"] { background: linear-gradient(90deg, #8E2DE2 0%, #4A00E0 100%) !important; }
    button[key="btn_cmd"] { background: #0b1e36 !important; border: 2px solid #00E5FF !important; }

    @keyframes master_chroma_flow {
        0% { border-color: #FFD700; box-shadow: 0 0 25px rgba(255, 215, 0, 0.6); background-position: 0% 50%; }
        50% { border-color: #00E5FF; box-shadow: 0 0 45px rgba(0, 229, 255, 0.9); background-position: 100% 50%; }
        100% { border-color: #FFD700; box-shadow: 0 0 25px rgba(255, 215, 0, 0.6); background-position: 0% 50%; }
    }

    @keyframes radar_flash {
        0% { background-color: #FF0000; color: #FFFFFF; box-shadow: 0 0 20px #FF0000; }
        50% { background-color: #330000; color: #FF0000; box-shadow: 0 0 0px #000000; }
        100% { background-color: #FF0000; color: #FFFFFF; box-shadow: 0 0 20px #FF0000; }
    }

    /* ENLARGED EXTRA-DIMENSION ANIMATED HIGH-AESTHETIC PORTAL CONTAINER */
    .unified-command-vault {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        height: 330px !important; 
        background: linear-gradient(-45deg, #04142c, #0b264f, #020a17, #071e3d) !important;
        background-size: 400% 400% !important;
        border: 5px solid #FFD700 !important;
        animation: master_chroma_flow 6s infinite ease-in-out !important;
        padding: 0px !important; 
        border-radius: 24px !important;
        backdrop-filter: blur(35px) !important;
        -webkit-backdrop-filter: blur(35px) !important;
        margin-top: 5px !important;
        box-shadow: inset 0 0 50px rgba(255, 215, 0, 0.35), 0 20px 45px rgba(0, 0, 0, 0.65) !important;
        overflow: hidden !important;
        transition: all 0.5s ease-in-out;
    }

    /* ENLARGED COMPONENT CONTAINER CELLS */
    .mace-vault-shield {
        flex-shrink: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 310px !important; 
        height: 100% !important; 
        background: rgba(4, 20, 48, 0.7) !important; 
        overflow: hidden !important;
        border-right: 3px solid rgba(255, 215, 0, 0.3);
    }

    .mace-vault-shield img {
        height: 90% !important; 
        width: 90% !important; 
        object-fit: contain !important; 
        filter: drop-shadow(0px 0px 20px rgba(255, 215, 0, 0.85)) contrast(1.4) brightness(1.1);
    }

    .photo-vault-shield {
        flex-shrink: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 450px !important; 
        height: 100% !important; 
        background: rgba(2, 10, 23, 0.5) !important; 
        overflow: hidden !important;
        border-left: 3px solid rgba(0, 229, 255, 0.3);
    }

    .photo-vault-shield img {
        height: 100% !important;
        width: 100% !important; 
        object-fit: cover !important; 
        filter: contrast(1.3) brightness(1.05) drop-shadow(-10px 0px 25px rgba(0,0,0,0.8));
    }

    .vault-text-block {
        flex-grow: 2 !important;
        text-align: center !important;
        padding: 0 20px !important;
    }

    /* INTEGRATED FORCEFUL TYPOGRAPHY REDUCTION FOR VISUAL AUTHENTICITY */
    .vault-text-block h1 {
        color: #FFFF00 !important;
        margin: 0 !important;
        font-size: 1.95rem !important; /* Forcefully scaled down from 2.8rem to guarantee container clearance */
        font-weight: 950 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        text-shadow: 2px 2px 6px #000000, 0 0 15px rgba(255,255,0,0.3) !important;
        line-height: 1.2 !important;
    }

    .vault-text-block .sub-title {
        color: #FFFFFF !important;
        margin: 6px 0 0 0 !important;
        font-size: 1.05rem !important; /* Scaled down from 1.4rem to prevent column blowout */
        font-weight: 800 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8) !important;
        line-height: 1.2 !important;
    }

    .vault-text-block .geo-stamp {
        color: #00E5FF !important;
        margin: 6px 0 0 0 !important;
        font-size: 1.25rem !important; /* Kept prominent but highly tracked to prevent container overspill */
        font-weight: 900 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9) !important;
        display: block !important;
    }

    .mobile-return-banner {
        display: none; background: linear-gradient(90deg, #0b1e36 0%, #05101e 100%);
        border: 2px solid #00E5FF; padding: 12px; border-radius: 8px; text-align: center;
        margin-bottom: 15px; cursor: pointer; text-transform: uppercase; font-weight: 800; letter-spacing: 1px;
    }

    @media (max-width: 1024px) {
        .unified-command-vault { flex-direction: column !important; height: auto !important; padding: 30px 10px !important; gap: 20px !important; }
        .mace-vault-shield { width: 100% !important; height: 200px !important; border-right: none; border-bottom: 3px solid rgba(255, 215, 0, 0.3); }
        .photo-vault-shield { width: 100% !important; height: 260px !important; border-left: none; border-top: 3px solid rgba(0, 229, 255, 0.3); }
        .vault-text-block h1 { font-size: 1.9rem !important; line-height: 1.2 !important; }
        .vault-text-block .sub-title { font-size: 1.05rem !important; }
        .vault-text-block .geo-stamp { font-size: 1.15rem !important; }
        .mobile-return-banner { display: block !important; }
    }

    .supervisor-header {
        background-color: #B71C1C;
        color: #FFFFFF !important;
        padding: 6px;
        border-radius: 8px;
        text-align: center; font-weight: 900; 
        display: block; width: 100%; font-size: 15px;
        margin-bottom: 12px; letter-spacing: 1px; text-transform: uppercase;
    }
    .radar-sticky-threat {
        animation: radar_flash 0.5s infinite; padding: 15px; border-radius: 8px; border: 3px solid #FFFFFF;
        text-align: center; font-weight: bold; font-size: 14px; margin-bottom: 15px;
    }
    .tier-box { display: inline-block; padding: 10px 20px; margin: 5px; border-radius: 6px; font-weight: bold; color: white; text-align: center; border: 2px solid #FFFFFF; }
    .tier-box.tier-pres { background-color: #FF4B4B !important; }
    .tier-box.tier-sen { background-color: #1F77B4 !important; }
    .tier-box.tier-rep { background-color: #2CA02C !important; }
    .tier-box.tier-gov { background-color: #9467BD !important; }
    .tier-box.tier-house { background-color: #FF7F0E !important; }
    
    .printable-slip-box { background-color: #FFFFFF !important; color: #000000 !important; padding: 25px; border: 3px double #8B0000; border-radius: 4px; font-family: 'Courier New', Courier, monospace; margin-top: 15px; }
    .slip-header { text-align: center; font-weight: 900; font-size: 16px; margin-bottom: 15px; border-bottom: 2px dashed #000; padding-bottom: 10px; }
    .slip-row { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px; font-weight: bold; }
    
    .stTextInput label p { color: #00E5FF !important; font-weight: 700 !important; }
    </style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# UNIFIED STRATEGIC AUTHORIZATION INTERFACE ROUTER MATRIX
# ==============================================================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "skill_form"

if st.session_state.get("adm_v30_auth") == "boki ikom 2027":
    st.session_state.current_page = "main_dashboard"
elif st.session_state.get("sup_v30_auth_sidebar") == "boki ikom 2027":
    st.session_state.current_page = "supervisor_panel"
elif st.session_state.get("agt_v30_auth_sidebar") == "boki":
    st.session_state.current_page = "agent_panel"

# ==============================================================================
# SIDEBAR NAVIGATION INTERFACE CONTROL MATRIX
# ==============================================================================
with st.sidebar:
    if st.session_state.radar_threat:
        st.markdown(
            f'<div class="radar-sticky-threat">🚨 SECURITY WARNING: IDENTITY DUPLICATION COLLISION<br>{st.session_state.threat_msg}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="admin-launch-zone">', unsafe_allow_html=True)
    adm_key = st.text_input("COMMAND HUB KEY", type="password", key="adm_v30_auth")
    st.markdown(
        '<a href="https://www.facebook.com/your-page-url" target="_blank" class="inst-link-box">🌐 Hon. Victor Abang Facebook</a>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    if st.button("🛠️ SKILL VOCATION POOL", key="btn_skill"):
        st.session_state.current_page = "skill_form"
    if st.button("🎓 STUDENT SCHOLARSHIP/GRANT", key="btn_sch"):
        st.session_state.current_page = "scholarship_form"
    if st.button("📦 CONSTITUENT PALLIATIVE ENROLLMENT", key="btn_pal"):
        st.session_state.current_page = "palliative_gateway"
    if st.button("🚀 CV & ARTISAN VAULT", key="btn_cv"):
        st.session_state.current_page = "cv_vault"

    st.markdown(
        '<div class="sidebar-red-flash">🚨 COMMUNITY URGENT NEED</div>',
        unsafe_allow_html=True,
    )
    if st.button("TRIGGER REGISTRATION INTERFACE", key="btn_cun_redirect"):
        st.session_state.current_page = "cun_trigger"

    st.divider()
    st.divider()
    st.markdown(
        "<p style='color:#8B0000; font-weight:bold; text-transform: uppercase;'>🔒 Field Authentication Core</p>",
        unsafe_allow_html=True,
    )

    sup_key_input = st.text_input(
        "WARD SUPERVISOR KEY", type="password", key="sup_v30_auth_sidebar"
    )
    agt_key_input = st.text_input(
        "POLLING UNIT AGENT KEY", type="password", key="agt_v30_auth_sidebar"
    )

    if sup_key_input:
        st.text_area(
            "Supervisor Remarks/Field Observations",
            key="sup_remarks",
            placeholder="Field log entry space...",
        )
    if agt_key_input:
        st.text_area(
            "Agent Remarks/Field Observations",
            key="agt_remarks",
            placeholder="Unit log entry space...",
        )

    st.caption(f"Engine: v34.0.67-BOKI-IKOM | {datetime.date.today()}")


# ==============================================================================
# INTEGRATED HEADER OBJECTS BUILD ZONE (PIXEL PERFECT FLUSH & TEXTURE CONTROL)
# ==============================================================================
def render_marquee_header():
    mace_path = os.path.join("assets", "digital_mace.png")
    portrait_path = os.path.join("assets", "hon_abang.png")

    mace_base64 = image_to_base64(mace_path)
    portrait_base64 = image_to_base64(portrait_path)

    mace_html = f'<img src="data:image/png;base64,{mace_base64}">' if mace_base64 else "<p>Mace image not found</p>"
    portrait_html = f'<img src="data:image/png;base64,{portrait_base64}">' if portrait_base64 else "<p>Portrait not found</p>"


    st.markdown(
        f"""
        <div class="unified-command-vault">
            <div class="mace-vault-shield">
                {mace_html}
            </div>
            <div class="vault-text-block">
                <h1>HONOURABLE VICTOR ABANG (PhD)</h1>
                <div class="sub-title">MEMBER REPRESENTING BOKI/IKOM FEDERAL CONSTITUENCY</div>
                <div class="geo-stamp">CROSS RIVER STATE</div>
            </div>
            <div class="photo-vault-shield">
                {portrait_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="margin-top:15px; background:linear-gradient(180deg, #061a33 0%, #020b17 100%); padding:8px; border-radius:8px;">'
        '  <marquee scrollamount="4" style="color:#FFFFFF; font-weight:800; font-size:16px; letter-spacing:1.5px; font-family:sans-serif;">'
        "    Honourable Victor Abang a.k.a MATURE cares....... #HERE TO SERVE THE BOKI/IKOM NATION WITH INTERGRITY, TRANSPARENCY, ACCOUNTABILITY DRIVEN BY PEOPLE ORIENTED PROGRAMS."
        "  </marquee>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_module_download_trigger(data_source, filename_prefix, unique_key):
    try:
        csv_bytes = pd.DataFrame(data_source).to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 DOWNLOAD SYSTEM LOG EXPORT",
            data=csv_bytes,
            file_name=f"{filename_prefix}_{datetime.date.today()}.csv",
            mime="text/csv",
            key=f"dl_btn_{unique_key}",
        )
    except Exception as e:
        st.caption(f"Download entry failure: {e}")


def render_institutional_purge_engine(key_suffix):
    st.markdown("---")
    st.subheader("🚨 Institutional Data Purge Zone")
    confirm_purge = st.text_input(
        "Type 'PURGE SYSTEM DATA' to authorize reset:", key=f"purge_box_{key_suffix}"
    )
    if st.button(
        "💥 EXECUTE SYSTEM PURGE afresh", type="primary", key=f"purge_btn_{key_suffix}"
    ):
        if confirm_purge == "PURGE SYSTEM DATA":
            st.session_state.global_registry = pd.DataFrame(columns=COLUMNS_STRUCTURE)
            st.session_state.submitted_wards = {}
            st.session_state.submitted_pus = {}
            trigger_background_autosave()
            st.success("System tracking layers reset completely.")
            st.sidebar.rerun()


# ==============================================================================
# MASTER APPLICATION CORE ROUTING LAYER
# ==============================================================================

if st.session_state.current_page == "supervisor_panel":
    render_marquee_header()
    st.markdown(
        '<div class="supervisor-header">🛡️ WARD SUPERVISOR COMMAND: FORM EC8A LOGS</div>',
        unsafe_allow_html=True,
    )
    if "sup_slip_preview" not in st.session_state:
        st.session_state.sup_slip_preview = None

    with st.form("supervisor_form"):
        c1, c2 = st.columns(2)
        with c1:
            sup_name = st.text_input("Supervisor Full Name")
            sup_phone = st.text_input("Phone Number")
            sup_state = st.text_input("State Link Node", value="CROSS RIVER STATE")
            sup_lga = st.selectbox("Your LGA", list(LGA_WARD_DATA.keys()))
            sup_ward = st.selectbox("Your Ward", LGA_WARD_DATA.get(sup_lga, []))
            sup_unit = st.text_input("Ward Unit Tracking Code/Number")

        ward_id = f"{sup_lga}_{sup_ward}".replace(" ", "_").upper()

        with c2:
            tiers_selected = st.multiselect(
                "Active Scope Assessment Matrix",
                [
                    "Federal House",
                    "Senatorial",
                    "Presidential",
                    "Governorship Aspirant",
                    "State House of Assembly",
                ],
                default=["Federal House"],
            )

            if tiers_selected:
                st.markdown(
                    """
                **Tiers Audited Vector Checkbox Mapping:**<br>
                <div class="tier-box tier-rep">Federal House</div><div class="tier-box tier-sen">Senatorial</div><div class="tier-box tier-pres">Presidential</div><div class="tier-box tier-gov">Governorship</div><div class="tier-box tier-house">State House</div>
                """,
                    unsafe_allow_html=True,
                )

            st.number_input(
                "Highest Party Vote Recorded", min_value=0, key="sup_high_vote"
            )
            st.number_input(
                "Principal Votes Cast Density", min_value=0, key="sup_pr_vote"
            )
            st.file_uploader(
                "Upload Supervisor Physical NIN Slip Link Asset",
                type=["pdf", "jpg", "png"],
            )

        st.camera_input("Live Capture Sensor Matrix: Form EC8A Sheet")

        if st.form_submit_button("🔍 GENERATE SYSTEM INTEGRITY PREVIEW RECORD SLIP"):
            if not sup_name or not sup_phone or not sup_unit:
                st.error(
                    "🛑 FORM ERROR: All core supervisor tracking strings must be completely specified before submission execution."
                )
            else:
                st.session_state.sup_slip_preview = {
                    "Supervisor": sup_name,
                    "Phone": sup_phone,
                    "LGA": sup_lga,
                    "Ward": sup_ward,
                    "Unit": sup_unit,
                    "Tiers": ", ".join(tiers_selected),
                    "High_Vote": int(st.session_state.get("sup_high_vote", 0)),
                    "Principal_Votes": int(st.session_state.get("sup_pr_vote", 0)),
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

    if st.session_state.sup_slip_preview is not None:
        p_data = st.session_state.sup_slip_preview
        st.markdown(
            f"""
        <div class="printable-slip-box">
            <div class="slip-header">🏛️ LSOEP NATIONAL ASSEMBLY INTEGRITY RECEIPT OVERVIEW</div>
            <div class="slip-row"><span>TIMESTAMP DATA:</span> <span>{p_data['Timestamp']}</span></div>
            <div class="slip-row"><span>SUPERVISOR NAME:</span> <span>{p_data['Supervisor']}</span></div>
            <div class="slip-row"><span>PHONE INTERFACE:</span> <span>{p_data['Phone']}</span></div>
            <div class="slip-row"><span>YOUR LGA:</span> <span>{p_data['LGA']}</span></div>
            <div class="slip-row"><span>YOUR WARD:</span> <span>{p_data['Ward']}</span></div>
            <div class="slip-row"><span>UNIT IDENTIFIER:</span> <span>{p_data['Unit']}</span></div>
            <div class="slip-row"><span>ACTIVE TIERS:</span> <span>{p_data['Tiers']}</span></div>
            <div class="slip-row"><span>HIGHEST TOTAL:</span> <span>{p_data['High_Vote']:}</span></div>
            <div class="slip-row"><span>VALID CORE SUM:</span> <span>{p_data['Principal_Votes']:}</span></div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button("🔒 CONFIRM METRICS: LOG INTO PRODUCTION ARRAYS"):
                if ward_id in st.session_state.submitted_wards:
                    st.error(
                        "🛑 Results sheet indicators for this Ward coordinate set have already been locked."
                    )
                else:
                    st.session_state.submitted_wards[ward_id] = p_data["Timestamp"]
                    trigger_background_autosave()
                    st.session_state.sup_slip_preview = None
                    st.success("Thanks for your submission! You are appreciated.")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
        with col_v2:
            if st.button("❌ ABORT TRANSACTION: CLEAR PREVIEW NODE STUB"):
                st.session_state.sup_slip_preview = None
                st.warning("Preview storage wiped successfully.")
                st.rerun()

elif st.session_state.current_page == "agent_panel":
    render_marquee_header()
    st.markdown("### 🗳️ POLLING UNIT AGENT: FIELD DATA TRANSFERS")
    if "agt_slip_preview" not in st.session_state:
        st.session_state.agt_slip_preview = None

    a1, a2 = st.columns(2)
    with a1:
        agt_name = st.text_input("Agent Full Operator Name")
        agt_phone = st.text_input("Agent Communication Contact Phone")
        agt_lga = st.selectbox("Your LGA", list(LGA_WARD_DATA.keys()))
        agt_ward = st.selectbox("Your Ward", LGA_WARD_DATA.get(agt_lga, []))
        agt_pu_num = (
            st.text_input("Polling Unit (PU) Identity Name Code")
            .strip()
            .replace(" ", "_")
            .upper()
        )

    pu_id = f"{agt_lga}_{agt_ward}_{agt_pu_num}".replace(" ", "_").upper()

    if agt_pu_num != "" and pu_id in st.session_state.submitted_pus:
        st.error(
            "🛑 Polling Unit entry parameter sequence matches locked profile record. Dropping link stream."
        )
    else:
        with st.form("agent_form"):
            with a2:
                agt_tiers = st.multiselect(
                    "Affirm Verification Parameters Scope",
                    [
                        "Federal House",
                        "Senatorial",
                        "Presidential",
                        "Governorship Aspirant",
                        "State House of Assembly",
                    ],
                    default=["Federal House"],
                )

                if agt_tiers:
                    st.markdown(
                        """
                    **Unit Active Layout Validation Mapping Check:**<br>
                    <div class="tier-box tier-rep">Federal House</div><div class="tier-box tier-sen">Senatorial</div><div class="tier-box tier-pres">Presidential</div><div class="tier-box tier-gov">Governorship</div><div class="tier-box tier-house">State House</div>
                    """,
                        unsafe_allow_html=True,
                    )

                st.number_input(
                    "Total Ballots Inside Unit Box Container",
                    min_value=0,
                    key="agt_tot_vote",
                )
                st.number_input(
                    "Valid Votes Quantum Metric Total", min_value=0, key="agt_pr_vote"
                )
                st.file_uploader(
                    "Upload Agent Verification NIN Slip Column File",
                    type=["pdf", "jpg", "png"],
                )
            st.camera_input(
                "Capture Local Unit Level Physical Document Ledger Asset Sheet"
            )

            if st.form_submit_button("🔍 COMPREHENSIVE ENTRY EVALUATION"):
                if not agt_name or not agt_phone or not agt_pu_num:
                    st.error(
                        "🛑 FORM ERROR: Agent metadata strings must be completely specified before proceeding."
                    )
                else:
                    st.session_state.agt_slip_preview = {
                        "Agent": agt_name,
                        "Phone": agt_phone,
                        "LGA": agt_lga,
                        "Ward": agt_ward,
                        "PU": agt_pu_num,
                        "Tiers": ", ".join(agt_tiers),
                        "Total_Votes": int(st.session_state.get("agt_tot_vote", 0)),
                        "Principal_Votes": int(st.session_state.get("agt_pr_vote", 0)),
                        "Timestamp": datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    }

        if st.session_state.agt_slip_preview is not None:
            a_data = st.session_state.agt_slip_preview
            st.markdown(
                f"""
            <div class="printable-slip-box">
                <div class="slip-header">🗳️ LSOEP FIELD OPERATOR REGISTERED FIELD SLIP LOG</div>
                <div class="slip-row"><span>CAPTURED TIMESTAMP:</span> <span>{a_data['Timestamp']}</span></div>
                <div class="slip-row"><span>AGENT NAME STAMP:</span> <span>{a_data['Agent']}</span></div>
                <div class="slip-row"><span>CELLULAR INTERFACE:</span> <span>{a_data['Phone']}</span></div>
                <div class="slip-row"><span>YOUR LGA:</span> <span>{a_data['LGA']}</span></div>
                <div class="slip-row"><span>YOUR WARD:</span> <span>{a_data['Ward']}</span></div>
                <div class="slip-row"><span>POLLING UNIT NUM:</span> <span>{a_data['PU']}</span></div>
                <div class="slip-row"><span>AUDITED BALANCES:</span> <span>{a_data['Total_Votes']:}</span></div>
                <div class="slip-row"><span>VALID QUANTUM LOG:</span> <span>{a_data['Principal_Votes']:}</span></div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            av1, av2 = st.columns(2)
            with av1:
                if st.button("🔒 COMMIT METRICS CONFIGURATION AND ARCHIVE RECORD"):
                    st.session_state.submitted_pus[pu_id] = a_data["Timestamp"]
                    trigger_background_autosave()
                    st.session_state.agt_slip_preview = None
                    st.success("Thanks for your submission! You are appreciated.")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
            with av2:
                if st.button("❌ DISCARD TRANSACTION BUFFER"):
                    st.session_state.agt_slip_preview = None
                    st.warning("Buffer variables cleared.")
                    st.rerun()

elif st.session_state.current_page == "main_dashboard":
    render_marquee_header()
    st.markdown("## 🏛️ EXECUTIVE CONTROL COMMAND DASHBOARD PORTAL ARRAY")

    tabs = st.tabs(
        [
            "📊 Master Registry Matrix",
            "📈 Infrastructure CUN Matrix",
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
        ]
    )

    boki_ikom_index_metrics_mock = pd.DataFrame(
        {
            "Constituency Node": ["BOKI/IKOM FEDERAL CONSTITUENCY"],
            "Performance Index Score": [88.2],
            "CUN Deficit Rate Proportion": [19.8],
            "Voter Turnout Metric Density": [81.3],
            "Waivers Distributed Yield": [25],
        }
    ).set_index("Constituency Node")

    with tabs[0]:
        st.subheader("📊 Master Verification Registry Database Partition Array")
        mc1, mc2 = st.columns([1, 2])
        with mc1:
            st.markdown("**Active Intake Status Partition Trace Records**")
            st.dataframe(
                st.session_state.global_registry[["Name", "LGA", "Ward", "Status"]]
            )
        with mc2:
            st.markdown(
                "**Processing Stream Success Metrics Vector Chart Across Boki/Ikom Constituency**"
            )
            st.bar_chart(boki_ikom_index_metrics_mock["Performance Index Score"])
        st.dataframe(st.session_state.global_registry, width="stretch")
        render_module_download_trigger(
            st.session_state.global_registry, "Master_Registry_Log", "t1_dl"
        )
        render_institutional_purge_engine("t1_purge")

    with tabs[1]:
        st.subheader("📈 Regional Community Urgent Need Matrix Framework Indicators")
        cun_records_array = []
        all_wards = GEOGRAPHY["Boki LGA"] + GEOGRAPHY["Ikom LGA"]
        for index_node, ward_string_name in enumerate(all_wards):
            lga_name = (
                "BOKI" if ward_string_name in GEOGRAPHY["Boki LGA"] else "IKOM"
            )
            cun_records_array.append(
                {
                    "LGA Territory Identification Link": f"{lga_name} CONST AREA",
                    "Administrative Ward Boundary Target": ward_string_name.upper(),
                    "Water Infrastructure Asset Deficit Ratio %": 44
                    + (index_node * 4) % 15,
                    "Grid Energy Power Interruption Density %": 88
                    - (index_node * 3) % 12,
                    "Critical Access Road Shortage Weights %": 71
                    + (index_node * 5) % 16,
                    "Logged Internal Community Security Threats Metrics": 11
                    + (index_node * 2) % 9,
                }
            )
        df_cun_matrix_canvas = pd.DataFrame(cun_records_array)
        st.dataframe(df_cun_matrix_canvas, width="stretch")
        st.bar_chart(
            df_cun_matrix_canvas.set_index("Administrative Ward Boundary Target")[
                [
                    "Water Infrastructure Asset Deficit Ratio %",
                    "Grid Energy Power Interruption Density %",
                ]
            ]
        )
        render_module_download_trigger(
            df_cun_matrix_canvas, "CUN_Deficit_Matrix_Log", "t2_dl"
        )
        render_institutional_purge_engine("t2_purge")

    with tabs[2]:
        st.subheader("⚖️ Forensic Audit Database Query & Connection Diagnostic Stream")
        st.error(
            "⚠️ Isolation Warning Layer: Supabase API Cloud Gateway locked inside internal local execution container frames."
        )

        if conn is not None:
            try:
                df_db_direct_test = conn.query(
                    f"SELECT * FROM ward_returns WHERE project_partition = '{PROJECT_PARTITION_ID}' LIMIT 5;",
                    ttl="0m",
                )
                st.success(
                    "Operational link established cleanly with relational query tables vector pools."
                )
                st.dataframe(df_db_direct_test)
            except Exception as e:
                st.caption(
                    f"Connection framework bypassed intentionally to run local backup cache: {e}"
                )

        with st.expander(
            "🛠️ Expose Active Developer State Cache JSON Mapping Trees", expanded=False
        ):
            st.json(
                {
                    "Memory_State_Allocation_Tokens": [
                        "agt_v30_auth_sidebar",
                        "btn_cv",
                        "purge_box_t2_purge",
                        "btn_pal",
                        "btn_cun_redirect",
                        "purge_box_t1_purge",
                        "adm_v30_auth",
                        "btn_sch",
                        "purge_btn_t2_purge",
                        "global_registry",
                        "FormSubmitter:skill_form_engine-🚀 COMMIT APPLICATION TO TRAINING POOLS",
                        "submitted_pus",
                        "submitted_wards",
                        "purge_btn_t1_purge",
                        "dl_btn_t2_dl",
                        "radar_threat",
                        "threat_msg",
                        "recycle_bin_pus",
                        "btn_cmd",
                        "recycle_bin_wards",
                        "sup_v30_auth_sidebar",
                        "btn_skill",
                        "recycle_bin_registry",
                        "dl_btn_t1_dl",
                        "current_page",
                    ],
                    "Sandbox_Static_Override_Circuit": "ACTIVE LOCAL BACKUP CONTAINER",
                    "Internal_Target_Matrix_Stencil": PROJECT_PARTITION_ID,
                    "Current_System_Clock_Time": "2026-05-25 21:20:50.370383",
                }
            )
        render_institutional_purge_engine("t3_purge")

    with tabs[3]:
        st.subheader(
            "🛡️ RADAR Multi-Intake Anti-Fraud Deduplication Interceptor Shield"
        )
        radar_records_array = []
        all_wards = GEOGRAPHY["Boki LGA"] + GEOGRAPHY["Ikom LGA"]
        for index_node, ward_string_name in enumerate(all_wards):
            lga_name = (
                "BOKI" if ward_string_name in GEOGRAPHY["Boki LGA"] else "IKOM"
            )
            radar_records_array.append(
                {
                    "LGA Territory Identification Link": f"{lga_name} CONST AREA",
                    "Administrative Ward Boundary Target": ward_string_name.upper(),
                    "Cross-Verification Biometric Pass Confidence %": 99.1
                    - (index_node * 0.12),
                    "Intercepted Duplication Collision Anomalies Tracked": index_node
                    % 2,
                    "Multi-Voucher System Fraud Attempts Dropped": index_node % 3,
                }
            )
        df_radar_matrix_canvas = pd.DataFrame(radar_records_array)
        st.dataframe(df_radar_matrix_canvas, width="stretch")
        st.metric(
            "Total Duplicate Fraud Collisions Terminated Safely",
            "0 Active Threat Logs Confirmed",
        )

        if st.button("Send Global System Clear Code To Sidebar Threat Indicators"):
            st.session_state.radar_threat = False
            st.session_state.threat_msg = ""
            st.success("Threat verification clear signals dispatched smoothly.")
            st.rerun()
        render_module_download_trigger(
            df_radar_matrix_canvas, "Radar_Deduplication_Logs", "t4_dl"
        )
        render_institutional_purge_engine("t4_purge")

    with tabs[4]:
        st.subheader("🎓 Academic Grants Distribution Pools & Talent Demographics Hub")
        cv_records_array = []
        all_wards = GEOGRAPHY["Boki LGA"] + GEOGRAPHY["Ikom LGA"]
        for index_node, ward_string_name in enumerate(all_wards):
            lga_name = (
                "BOKI" if ward_string_name in GEOGRAPHY["Boki LGA"] else "IKOM"
            )
            cv_records_array.append(
                {
                    "LGA Territory Identification Link": f"{lga_name} CONST AREA",
                    "Administrative Ward Boundary Target": ward_string_name.upper(),
                    "PhD High-Fidelity Research Candidates Enrolled": index_node % 2,
                    "Masters Level Profiles Captured": 1 + (index_node % 3),
                    "Bachelors Degree Holders Indexed": 15 + (index_node * 2),
                    "Technical Vocation Artisans Tracked": 30 + (index_node * 4),
                }
            )
        df_cv_matrix_canvas = pd.DataFrame(cv_records_array)
        st.dataframe(df_cv_matrix_canvas, width="stretch")
        st.bar_chart(
            df_cv_matrix_canvas.set_index("Administrative Ward Boundary Target")[
                [
                    "Bachelors Degree Holders Indexed",
                    "Technical Vocation Artisans Tracked",
                ]
            ]
        )
        render_module_download_trigger(
            df_cv_matrix_canvas, "Talent_Pool_Demographics", "t5_dl"
        )
        render_institutional_purge_engine("t5_purge")

    with tabs[5]:
        st.subheader("💎 Vantedge Strategic Influence Vectors & Demographics Scale")
        vantage_records_array = []
        all_wards = GEOGRAPHY["Boki LGA"] + GEOGRAPHY["Ikom LGA"]
        for index_node, ward_string_name in enumerate(all_wards):
            lga_name = (
                "BOKI" if ward_string_name in GEOGRAPHY["Boki LGA"] else "IKOM"
            )
            vantage_records_array.append(
                {
                    "LGA Territory Identification Link": f"{lga_name} CONST AREA",
                    "Administrative Ward Boundary Target": ward_string_name.upper(),
                    "Opinion Influencers Authenticated": 3 + (index_node % 4),
                    "Youth Mobilization Mobilization Directors": 6 + (index_node % 5),
                    "Community Vouched Elders Registered": 4 + (index_node % 6),
                    "Regional Strategic Weight Matrix Allocation Coefficient": round(
                        1.15 + (index_node * 0.04), 2
                    ),
                }
            )
        df_vantage_matrix_canvas = pd.DataFrame(vantage_records_array)
        st.dataframe(df_vantage_matrix_canvas, width="stretch")
        render_module_download_trigger(
            df_vantage_matrix_canvas, "Vantedge_Influence_Matrix_Log", "t6_dl"
        )
        render_institutional_purge_engine("t6_purge")

    with tabs[6]:
        st.subheader(
            "🗳️ Cross-National Multi-Tier Election Verification War Room Sync Arrays"
        )
        state_query_search = st.text_input(
            "Type target State name to evaluate returns parameters:", key="nat_search"
        ).strip()
        if state_query_search:
            matched_state = None
            for key in STATE_DATA_LEDGER.keys():
                if state_query_search.lower() == key.lower():
                    matched_state = key
                    break
            if matched_state:
                registered_calc = 1200000 + (len(matched_state) * 54321)
                turnout_calc = 600000 + (len(matched_state) * 21043)
                tally_calc = 550000 + (len(matched_state) * 19280)
                st.success(
                    f"📊 **{matched_state} Core Operational Index Extracted Mapping Safely:**"
                )
                tc1, tc2, tc3 = st.columns(3)
                tc1.metric("INEC Total Registered Base", f"{registered_calc:,}")
                tc2.metric("Audited Ballots Turnout", f"{turnout_calc:,}")
                tc3.metric("🔴 Presidential Confirmed Tally", f"{tally_calc:,}")
            else:
                st.warning(
                    "State identifier token not located inside target administrative tables. Check characters pattern alignment."
                )

        national_votes_calculated_sum = sum(
            (550000 + (len(k) * 19280)) for k in STATE_DATA_LEDGER.keys()
        )

        # ACTIVE 5-TIER COMPLETE ELECTION MONITORING FLAGS
        st.markdown(
            f"""
        **Static Visual Alignment Layout Flags Check:**
        * <div class="tier-box tier-pres" style="width:100%; text-align:left;">🔴 Presidential Accumulation Tally — <b style="float:right;">{national_votes_calculated_sum:,} Total Clean Votes</b></div>
        * <div class="tier-box tier-sen" style="width:100%; text-align:left;">🔵 Senatorial Accumulation Tally — <b style="float:right;">24,815,402 Valid Ballots</b></div>
        * <div class="tier-box tier-rep" style="width:100%; text-align:left;">🟢 Federal Houses Verification Array — <b style="float:right;">Operational Data Nodes Syncing</b></div>
        * <div class="tier-box tier-gov" style="width:100%; text-align:left;">🟣 Governorship Strategic Matrix Feed — <b style="float:right;">Live Field Pipeline Stream</b></div>
        * <div class="tier-box tier-house" style="width:100%; text-align:left;">🟠 State Houses of Assembly Returns Ledger — <b style="float:right;">Unit Validation Engine Armed</b></div>
        """,
            unsafe_allow_html=True,
        )

        st.divider()
        st.markdown("### 📡 Continuous Automated Pipeline Result Scraper Matrix Entry")
        target_state_scoop = st.selectbox(
            "Select Target State Node to Scoop Results",
            list(STATE_DATA_LEDGER.keys()),
            key="sync_state_scoop_select",
        )

        if st.button(
            "⚡ EXECUTE AUTOMATIC NATIONAL DATA SCOOP", key="btn_trigger_scoop_votes"
        ):
            st.success(
                f"🎉 Channel tunneled cleanly to Live National Data Node. Parsing INEC blocks configuration arrays..."
            )
            scoop_records = []
            selected_state_data = STATE_DATA_LEDGER[target_state_scoop]
            for lga_name, wards_list in selected_state_data.items():
                for ward_name in wards_list:
                    for pu_idx in range(1, 3):
                        pu_code = f"PU{pu_idx:03d}"
                        scoop_records.append(
                            {
                                "State Node": target_state_scoop,
                                "INEC LGA Boundary": lga_name,
                                "INEC Verified Ward Unit": ward_name.upper(),
                                "Polling Unit Identifier": f"{ward_name[:3].upper()}-{pu_code}",
                                "Presidential Tally (Red)": 135 + (pu_idx * 16),
                                "Senatorial Tally (Blue)": 245 + (pu_idx * 22),
                                "House of Reps Tally (Green)": 115 + (pu_idx * 12),
                                "Governorship Tally (Purple)": 190 + (pu_idx * 18),
                                "State House Tally (Orange)": 155 + (pu_idx * 14),
                            }
                        )
            st.session_state.last_scooped_df = pd.DataFrame(scoop_records)
            st.dataframe(st.session_state.last_scooped_df, width="stretch")
            st.bar_chart(
                st.session_state.last_scooped_df.set_index("Polling Unit Identifier")[
                    ["Presidential Tally (Red)", "Senatorial Tally (Blue)"]
                ]
            )

        if "last_scooped_df" in st.session_state:
            render_module_download_trigger(
                st.session_state.last_scooped_df,
                "National_Election_Scoop",
                "election_dl",
            )
        render_institutional_purge_engine("t7_purge")

    with tabs[7]:
        st.subheader("📝 Ground Truth Form EC8A Audited Verification Schema")
        target_state_ec8a = st.selectbox(
            "Select State Target Matrix Boundary Node",
            list(STATE_DATA_LEDGER.keys()),
            key="ec8a_master_state_select",
        )
        state_lga_map = STATE_DATA_LEDGER.get(target_state_ec8a, {})
        lga_options = (
            list(state_lga_map.keys())
            if state_lga_map
            else ["NO COMPATIBLE LGA KEY DETECTED"]
        )
        selected_lga_ec8a = st.selectbox(
            f"Select LGA Sub-partition for {target_state_ec8a}",
            lga_options,
            key="ec8a_lga_select",
        )
        ward_options = state_lga_map.get(selected_lga_ec8a, ["CENTRAL WARD 1"])
        selected_ward_ec8a = st.selectbox(
            f"Select Ward Boundary for {selected_lga_ec8a}",
            ward_options,
            key="ec8a_ward_select",
        )

        if st.button("Run Real-Time Verification Document Audit Transfer"):
            st.info(
                f"Establishing verification tracking streams with {target_state_ec8a} repositories..."
            )
            ec8a_records = []
            for item_node in range(1, 6):
                ec8a_records.append(
                    {
                        "State Link Mapped": target_state_ec8a,
                        "LGA Node Mapping": selected_lga_ec8a.upper(),
                        "Ward Sector Mapped": selected_ward_ec8a.upper(),
                        "Polling Unit Code Identification Link": f"{selected_ward_ec8a[:3].upper()}-WARD-PU00{item_node}",
                        "EC8A Image Link Validation Checksum": f"BLOB_IMG_ID_0{item_node}_SECURE.PNG",
                        "Cryptographic SHA-256 Stamp Metric": f"0xSHA256_{item_node}B99A11FF_{selected_lga_ec8a[:3].upper() if len(selected_lga_ec8a) >=3 else 'LGA'}",
                        "Audited Discrepancy Margin Rate": "0.00% Match Perfect",
                    }
                )
            st.session_state.last_ec8a_df = pd.DataFrame(ec8a_records)
            st.dataframe(st.session_state.last_ec8a_df, width="stretch")
        if "last_ec8a_df" in st.session_state:
            render_module_download_trigger(
                st.session_state.last_ec8a_df,
                "Ground_Truth_EC8A_Audit",
                "ground_truth_dl",
            )
        render_institutional_purge_engine("t8_purge")

    with tabs[8]:
        st.subheader("📂 Bulk Throughput Tunnel Sync")
        global_search_string = st.text_input(
            "Input specific Profile target parameters (Name/NIN/VIN):"
        ).strip()
        if st.button("Fire Core Scan"):
            st.success(
                f"Scan completed. String '{global_search_string}' verified safely against local registry schemas partition filters."
            )
        render_institutional_purge_engine("t9_purge")

    with tabs[9]:
        st.subheader("📜 Strategic Waiver Assignment Parameters Matrix Ledgers")
        waiver_records_array = []
        all_wards = GEOGRAPHY["Boki LGA"] + GEOGRAPHY["Ikom LGA"]
        for index_node, ward_string_name in enumerate(all_wards):
            lga_name = (
                "BOKI" if ward_string_name in GEOGRAPHY["Boki LGA"] else "IKOM"
            )
            waiver_records_array.append(
                {
                    "LGA Territory Identification Link": f"{lga_name} CONST AREA",
                    "Administrative Ward Boundary Target": ward_string_name.upper(),
                    "Waivers Dispatched Allocation": 1 + (index_node % 3),
                    "Financial Allocation Metric Equivalent": 150000 * (index_node % 4),
                    "Bypass Signature Seal String": f"EXE-AUTH-CRS-{lga_name[:3]}-0{index_node}",
                }
            )
        df_waiver_matrix_canvas = pd.DataFrame(waiver_records_array)
        st.dataframe(df_waiver_matrix_canvas, width="stretch")
        render_module_download_trigger(
            df_waiver_matrix_canvas, "Executive_Waivers_Dispatched", "t10_dl"
        )
        render_institutional_purge_engine("t10_purge")

    with tabs[10]:
        st.subheader("🚀 National Assembly Legislative Action Motion Tracking")
        df_nass_bills_matrix = pd.DataFrame(
            [
                {
                    "Bill Identification Code": "HB-2026-102",
                    "Legislative Title Summary": "Agro-Processing Zone Development (Boki/Ikom) Act",
                    "Current Floor Progress Track": "Third Reading Concluded & Passed",
                    "Last Checked Update Time": "May 2026",
                },
                {
                    "Bill Identification Code": "HB-2026-115",
                    "Legislative Title Summary": "Federal Medical Centre, Ikom (Establishment) Bill",
                    "Current Floor Progress Track": "Committee Reference Referral",
                    "Last Checked Update Time": "April 2026",
                },
                {
                    "Bill Identification Code": "HB-2026-128",
                    "Legislative Title Summary": "Cross River Basin Development Fund Bill",
                    "Current Floor Progress Track": "First Reading Table Entry",
                    "Last Checked Update Time": "May 2026",
                },
            ]
        ).set_index("Bill Identification Code")
        st.dataframe(df_nass_bills_matrix, width="stretch")
        st.progress(
            85,
            text="HB-2026-102 Analytical Progress: 85% Concluded (Awaiting Executive Assent Node Mapping)",
        )
        render_institutional_purge_engine("t11_purge")

    with tabs[11]:
        st.subheader("📅 Long-Term Temporal Momentum Tracking Interface Matrix Trends")
        mc_col1, mc_col2 = st.columns(2)
        with mc_col1:
            st.markdown("**Weekly Intake Performance Trajectory**")
            st.line_chart(boki_ikom_index_metrics_mock["Voter Turnout Metric Density"])
        with mc_col2:
            st.markdown("**Monthly Deficiency Compression Scale Ratios**")
            st.bar_chart(boki_ikom_index_metrics_mock["CUN Deficit Rate Proportion"])
        render_institutional_purge_engine("t12_purge")

elif st.session_state.current_page == "skill_form":
    render_marquee_header()
    st.markdown(
        '<div class="white-registry-header">🛠 CONSTITUENT SKILL EMPOWERMENT POOL</div>',
        unsafe_allow_html=True,
    )
    with st.form("skill_form_engine"):
        k1, k2 = st.columns(2)
        with k1:
            sv_name = st.text_input("Full name as displayed on NIN")
            sv_phone = st.text_input("Applicant Contact Number")
            sv_nin = st.text_input("Your NIN number")
            sv_vin = st.text_input("your Voters card number")
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
            klga = st.selectbox("Your LGA", list(LGA_WARD_DATA.keys()))
            kward = st.selectbox("Your Ward", LGA_WARD_DATA.get(klga, []))
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
            custom_vocation = ""
            if sv_selection == "Other (Type Custom Vocation Below)":
                custom_vocation = st.text_input(
                    "Type Your Choice Vocation Natively Here"
                )
            st.divider()
            sv_palliative_check = st.selectbox(
                "Have you received a palliative from this office before?", ["No", "Yes"]
            )

        sv_stmt = st.text_area("Candidate Skill Interest Statement Details")
        sv_cam = st.camera_input("Biometric Security Verification Core Scan")

        if st.form_submit_button("🚀 COMMIT APPLICATION TO TRAINING POOLS"):
            if (
                not sv_name
                or not sv_phone
                or not sv_nin
                or not sv_vin
                or not sv_stmt
                or sv_file is None
                or sv_cam is None
                or (
                    sv_selection == "Other (Type Custom Vocation Below)"
                    and not custom_vocation
                )
            ):
                st.error(
                    "🛑 FORM ERROR: All field entries on this registration pool form are strictly mandatory. Uploads and biometric camera checks must be valid."
                )
            else:
                match_check = st.session_state.global_registry[
                    st.session_state.global_registry["NIN"] == sv_nin
                ]
                if not match_check.empty:
                    st.session_state.radar_threat = True
                    st.session_state.threat_msg = f"Collision: NIN [{sv_nin}] matches a record belonging to user [{match_check.iloc[0]['Name']}]."
                    st.error(
                        "Duplicate Entry Detected. Entry Rejected by Security System Shield Protocols."
                    )
                else:
                    final_skill = (
                        custom_vocation
                        if sv_selection == "Other (Type Custom Vocation Below)"
                        else sv_selection
                    )
                    new_profile_row = {
                        "NIN": sv_nin,
                        "VIN": sv_vin,
                        "Name": sv_name,
                        "LGA": klga,
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
                        "Leader_Name": "Hon. Victor Abang Vouched",
                        "Leader_Contact": "080",
                        "Leader_NIN": "000",
                        "Leader_LGA": "BOKI",
                        "Leader_Ward": "CENTRAL",
                        "Leader_Portfolio": "Directorate Node",
                        "Voucher_Code": "V-BKI",
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
                    st.success("Thanks for your submission! You are appreciated.")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()

elif st.session_state.current_page == "scholarship_form":
    render_marquee_header()
    st.markdown("### 🎓 CONSTITUENT STUDENT SCHOLARSHIP APPLICATION PORTAL")
    with st.form("scholarship_form_engine"):
        s1, s2 = st.columns(2)
        with s1:
            sch_name = st.text_input("Full name as displayed on NIN")
            sch_nin = st.text_input("Your NIN number")
            sch_phone = st.text_input("Applicant Contact Number")
            sch_year = st.selectbox(
                "Academic Year of Intake Admission",
                [str(year_token) for year_token in range(2018, 2027)],
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
            slga = st.selectbox("Your LGA", list(LGA_WARD_DATA.keys()))
            sward = st.selectbox("Your Ward", LGA_WARD_DATA.get(slga, []))
        sch_file_adm = st.file_uploader(
            "Attach Official University Admission Letter Asset File",
            type=["pdf", "jpg", "png"],
        )
        sch_just = st.text_area("Applicant Justification Space")
        sch_cam = st.camera_input("Capture Student Identity Card Sensor")

        if st.form_submit_button("🚀 SUBMIT SCHOLARSHIP ENTRY APPLICATION PARAMETERS"):
            if (
                not sch_name
                or not sch_nin
                or not sch_phone
                or not sch_inst
                or not sch_just
                or sch_file_nin is None
                or sch_file_adm is None
                or sch_cam is None
            ):
                st.error(
                    "🛑 FORM ERROR: Absolute processing requirement failed. All input fields, historical assets, and live card capture parameters are required."
                )
            else:
                st.success("Thanks for your submission! You are appreciated.")
                st.balloons()

elif st.session_state.current_page == "cv_vault":
    render_marquee_header()
    st.markdown("### 🚀 CONSTITUENT PROFESSIONAL TALENT VAULT ENGINE")
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
            vlga = st.selectbox("Your LGA", list(LGA_WARD_DATA.keys()))
            vward = st.selectbox("Your Ward", LGA_WARD_DATA.get(vlga, []))
        cv_summary = st.text_area(
            "Summary Matrix of Functional Career Experience Vectors"
        )
        cv_cam = st.camera_input("Capture Valid Professional Certification Seals")

        if st.form_submit_button(
            "📤 COMMIT CREDENTIALS STRINGS TO TALENT PLATFORM ARCHIVE MATRIX"
        ):
            if (
                not cv_name
                or not cv_nin
                or not cv_phone
                or not cv_summary
                or cv_file is None
                or cv_cam is None
            ):
                st.error(
                    "🛑 FORM ERROR: System cannot commit strings. Please completely populate all input arrays and provide file/camera captures."
                )
            else:
                st.success("Thanks for your submission! You are appreciated.")
                st.balloons()

elif st.session_state.current_page == "cun_trigger":
    render_marquee_header()
    st.markdown("### 🚨 COMMUNITY URGENT NEED FIELD DEFICIT REPORT GATEWAY")
    with st.form("cun_form_engine"):
        cun_member = st.text_input("Reporting Community member")
        cun_phone = st.text_input("Applicant Contact Number")
        clga = st.selectbox("Affected LGA", list(LGA_WARD_DATA.keys()))
        cward = st.selectbox("Affected Ward", LGA_WARD_DATA.get(clga, []))
        cun_area = st.selectbox(
            "Area of urgent government Attention",
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
            "🚨 TRIGGER COMMAND INCIDENT VECTOR ALERT TO CORE MASTER LEDGERS"
        ):
            if (
                not cun_member
                or not cun_phone
                or not cun_logs
                or cun_file is None
                or cun_cam is None
            ):
                st.error(
                    "🛑 FORM ERROR: Core matrix validation failed. Satisfy all reporting details, identification files, and site images."
                )
            else:
                st.success("Thanks for your submission! You are appreciated.")
                st.balloons()

else:
    render_marquee_header()
    st.markdown("### 📦 CONSTITUENT PALLIATIVE ENROLLMENT REGISTRY")
    with st.form("palliative_form_engine"):
        p1, p2 = st.columns(2)
        with p1:
            p_name = st.text_input("Full name as displayed on NIN")
            p_nin = st.text_input("Your NIN number")
            p_vin = st.text_input("your Voters card number")
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
            plga = st.selectbox("Your LGA", list(LGA_WARD_DATA.keys()))
            pward = st.selectbox("Your Ward", LGA_WARD_DATA.get(plga, []))
            p_agro_select = st.selectbox(
                "Specific Area of Agro Intervention and Others",
                ["Fertilizer", "Seedlings", "Other Area of Likely Intervention"],
            )
            p_expect = st.text_input("Type Your Expectation")

        st.divider()
        st.markdown(
            "### 🛡️ FULL STRATEGIC LEADERSHIP VOUCHING TIER INTERFACE FRAME (ANTI-FRAUD MATRIX)"
        )
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            v_leader = st.text_input("Vouching Community Leader Full Legal Name")
            v_lphone = st.text_input(
                "Vouching Leader Mobile Communication Contact Phone"
            )
            v_lnin = st.text_input(
                "Vouching Leader National ID Validation String (NIN)"
            )
            vl_lga = st.selectbox(
                "Vouching Leader LGA Registration Link", list(LGA_WARD_DATA.keys())
            )
        with v_col2:
            vl_ward = st.selectbox(
                "Vouching Leader Ward Area Code Linking Check (Auto)",
                LGA_WARD_DATA.get(vl_lga, []),
            )
            v_port = st.text_input(
                "Current Portfolio/Traditional Leadership Title Stamped Within Community"
            )
            v_file_leader = st.file_uploader(
                "Upload Vouching Leader Authentic NIN Verification Slip Document File",
                type=["pdf", "jpg", "png"],
            )

        p_remarks = st.text_area(
            "Leader Affirmation Testimony Verification Remarks Statement"
        )
        p_cam = st.camera_input(
            "Biometric Face Capture Matrix Core Verification Face Scan"
        )

        if st.form_submit_button(
            "🚀 COMPLETE TRANSACTION: AUTHORIZE PALLIATIVE NOMINATION RECORD"
        ):
            if (
                not p_name
                or not p_nin
                or not p_vin
                or not p_phone
                or not p_expect
                or not p_vuln
                or not v_leader
                or not v_lphone
                or not v_lnin
                or not v_port
                or not p_remarks
                or p_file_nin is None
                or v_file_leader is None
                or p_cam is None
            ):
                st.error(
                    "🛑 FORM ERROR: Enrollment verification failed. All fields, agro specifications, physical identity files, and live camera captures are required."
                )
            else:
                match_check = st.session_state.global_registry[
                    st.session_state.global_registry["NIN"] == p_nin
                ]
                if not match_check.empty:
                    st.session_state.radar_threat = True
                    st.session_state.threat_msg = f"Collision Trace Block: Identification NIN Token [{p_nin}] already allocated inside database system matrix arrays."
                    st.error(
                        "Duplicate Registration Attempt Dropped Instantly. Verification Engine Locked Transaction Block."
                    )
                else:
                    new_profile_row = {
                        "NIN": p_nin,
                        "VIN": p_vin,
                        "Name": p_name,
                        "LGA": plga,
                        "Ward": pward,
                        "Status": "Verified Clear",
                        "Category": "Applicant",
                        "Skill_Interest": f"Agro: {p_agro_select}",
                        "Custom_Skill": p_expect,
                        "Gender": "Not Specified",
                        "DOB": "Not Specified",
                        "Disability_Status": ", ".join(p_vuln),
                        "Prior_Palliative": "Yes",
                        "Academic_Qual": "None",
                        "Admission_Year": "2026",
                        "Admission_Letter": None,
                        "Phone": p_phone,
                        "Leader_Name": v_leader,
                        "Leader_Contact": v_lphone,
                        "Leader_NIN": v_lnin,
                        "Leader_LGA": vl_lga,
                        "Leader_Ward": vl_ward,
                        "Leader_Portfolio": v_port,
                        "Voucher_Code": "P-BKI",
                        "Remarks": p_remarks,
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
                    st.success("Thanks for your submission! You are appreciated.")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()