import streamlit as st
import pandas as pd
from datetime import datetime


class ElectionSyncEngine:
    def __init__(self):
        # Force initialization here immediately upon class creation
        self._ensure_initialized()

    def _ensure_initialized(self):
        """Creates the session state variable if it doesn't exist."""
        if "war_room_sync" not in st.session_state:
            st.session_state.war_room_sync = pd.DataFrame(
                columns=[
                    "pu_id",
                    "bvas_ref_serial",
                    "incident_status",
                    "incident_details",
                    "tier_vector",
                    "timestamp",
                ]
            )

    def record_field_data(
        self, pu_id, bvas_serial, incident_flag, incident_details, tier_vector
    ):
        self._ensure_initialized()
        new_entry = {
            "pu_id": pu_id,
            "bvas_ref_serial": bvas_serial,
            "incident_status": incident_flag,
            "incident_details": incident_details,
            "tier_vector": tier_vector,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        # Update the session state correctly
        st.session_state.war_room_sync = pd.concat(
            [st.session_state.war_room_sync, pd.DataFrame([new_entry])],
            ignore_index=True,
        )

    def fetch_latest_results_from_db(self, tier):
        self._ensure_initialized()
        df = st.session_state.war_room_sync
        if df.empty:
            return df
        return df[df["tier_vector"].str.contains(tier, na=False)]


# Instantiate the engine globally
engine = ElectionSyncEngine()
