import streamlit as st

def inject_custom_css():
    st.markdown(
        '''
        <style>
            /* --- GLOBAL FONT & BACKGROUND --- */
            body {
                color: #F0F0F0; /* Softer off-white for all text */
            }

            /* --- GENERAL STYLING & ANIMATIONS --- */
            @keyframes swing-in {
                0% { transform: translateY(-30px) scale(0.9); opacity: 0; }
                100% { transform: translateY(0) scale(1); opacity: 1; }
            }
            .swing-in {
                animation: swing-in 0.6s ease-out;
            }

            /* --- SIDEBAR --- */
            .st-emotion-cache-16txtl3 {
                padding: 1rem 1rem;
            }
            .admin-header {
                font-size: 1.5rem !important;
                color: #D4AF37;
                text-align: center;
                margin-bottom: 1rem;
            }
            
            /* --- NAVIGATION BUTTONS / TABS (MAIN PAGE) --- */
            .nav-title {
                text-align: center;
                color: #00E5FF; /* UPDATED: Changed to vibrant cyan */
                font-weight: 700;
                text-transform: uppercase;
                margin-bottom: 1.5rem;
                text-shadow: 0 0 10px rgba(0, 229, 255, 0.7);
            }
            
            .stButton>button {
                border-radius: 10px !important;
                border: 2px solid #D4AF37 !important; /* UPDATED: Gold border by default */
                background-color: #0B3C5D; /* UPDATED: Distinct medium blue background */
                color: #FFFFFF !important; /* UPDATED: Ensure text is bright white */
                transition: background-color 0.3s, color 0.3s, border-color 0.3s, transform 0.2s;
            }
            .stButton>button:hover {
                background-color: #D4AF37 !important; /* UPDATED: Gold background on hover */
                border-color: #FFFFFF !important; /* UPDATED: White border on hover */
                color: #061A33 !important; /* UPDATED: Dark blue text on hover */
                transform: scale(1.05);
            }

            /* --- SIDEBAR LINK --- */
            .inst-link-box {
                display: block;
                background-color: #D4AF37;
                color: #061A33 !important;
                padding: 10px;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                text-decoration: none !important;
                transition: background-color 0.3s, transform 0.2s;
            }
            .inst-link-box:hover {
                background-color: #b89b31;
                transform: scale(1.03);
            }

            /* --- FORM & INPUT STYLING --- */
            .stTextInput, .stSelectbox, .stDateInput, .stTextArea, .stFileUploader, .stCameraInput {
                background-color: rgba(6, 26, 51, 0.7);
                border: 1px solid #0B3C5D;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 10px;
            }

            /* --- SPECIFIC MODULE HEADERS --- */
            .supervisor-header, .agent-header {
                background-color: #0B3C5D;
                color: #D4AF37;
                padding: 1rem;
                border-radius: 8px;
                text-align: center;
                margin-bottom: 1.5rem;
            }
            
            /* --- Printable Slip for Verification --- */
            .printable-slip-box {
                 background-color: #f9f9f9;
                 color: #333;
                 border: 2px solid #D4AF37;
                 border-radius: 10px;
                 padding: 20px;
                 font-family: 'Courier New', Courier, monospace;
                 margin-top: 20px;
            }
            .slip-header {
                 font-size: 1.2rem;
                 font-weight: bold;
                 text-align: center;
                 border-bottom: 1px solid #ccc;
                 margin-bottom: 15px;
                 padding-bottom: 10px;
            }
            .slip-row {
                 display: flex;
                 justify-content: space-between;
                 margin-bottom: 8px;
                 font-size: 1rem;
            }
            .slip-row span:first-child {
                 font-weight: bold;
            }
             
        </style>
        ''',
        unsafe_allow_html=True
    )
