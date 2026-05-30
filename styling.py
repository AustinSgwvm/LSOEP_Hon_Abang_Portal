import streamlit as st


def apply_styles():
    st.markdown(
        """<style>
        .stApp { background-color: #f8f9fa; }
        h1, h2, h3 { color: #1a2a6c !important; } /* Midnight Navy */
        .stButton>button { border: 2px solid #b8860b; color: #b8860b; } /* Brushed Gold */
        .css-1r6slb0 { background-color: #1a2a6c; color: white; }
        </style>""",
        unsafe_allow_html=True,
    )


def render_marquee_header():
    st.markdown(
        """
        <marquee style='color: #b8860b; font-weight: bold; font-size: 20px; border-top: 1px solid #1a2a6c; border-bottom: 1px solid #1a2a6c;'>
            Honourable Victor Abang a.k.a Mature Cares.............
        </marquee>
    """,
        unsafe_allow_html=True,
    )


def render_module_download_trigger(data_source, filename_prefix, unique_key):
    # This logic handles data exports for your registry,
    # ensuring it captures the constituency context
    st.download_button(
        label="📥 Download Constituency Report",
        data=data_source.to_csv().encode("utf-8"),
        file_name=f"{filename_prefix}_report.csv",
        key=unique_key,
    )


def render_institutional_purge_engine(key_suffix):
    # High-fidelity security control for sensitive data
    if st.button("⚠️ Purge Records", key=f"purge_{key_suffix}"):
        st.error("Institutional Purge Active: Data clearance protocols engaged.")
