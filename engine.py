# engine.py
import streamlit as st
import pandas as pd
import json
import os
from registry import COLUMNS_STRUCTURE

# Updated cache names to allow for constituency-specific backups
OFFLINE_REGISTRY_CACHE = "constituency_registry_cache.csv"
OFFLINE_METADATA_CACHE = "constituency_metadata_cache.json"


def trigger_background_autosave(selected_constituency):
    """Saves registry data, appending the constituency context to the metadata."""
    try:
        # Save registry
        st.session_state.global_registry.to_csv(OFFLINE_REGISTRY_CACHE, index=False)

        # Save metadata with constituency tag
        meta_payload = {
            "constituency": selected_constituency,
            "submitted_wards": st.session_state.submitted_wards,
            "submitted_pus": st.session_state.submitted_pus,
        }
        with open(OFFLINE_METADATA_CACHE, "w") as f:
            json.dump(meta_payload, f)
    except Exception as e:
        st.caption(f"Autosave sync bypass: {e}")


def initialize_and_recover_system_states():
    # PASTE YOUR initialize_and_recover_system_states CODE HERE
    # Ensure this function checks if OFFLINE_REGISTRY_CACHE exists
    # and loads the data into st.session_state.global_registry
    pass
