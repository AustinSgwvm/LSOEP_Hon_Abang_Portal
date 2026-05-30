# --- CONSOLIDATED GEOGRAPHICAL CONFIGURATION ---
# Consolidating into one source to prevent maintenance errors
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

# The Column structure is optimal and requires no changes
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


def get_wards(lga_name):
    """Helper function to dynamically retrieve wards based on LGA selection."""
    return LGA_WARD_DATA.get(lga_name.upper(), [])
