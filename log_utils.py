import streamlit as st

def initialize_log(log_key, hours):
    if log_key not in st.session_state:
        st.session_state[log_key] = {
            hour: {"meeting": False, "meeting_info": "", "tasks": "", "general": ""}
            for hour in hours
        }

def get_log_records(log_key, hours):
    records = []
    for hour in hours:
        entry = st.session_state[log_key][hour]
        records.append({
            "Time": hour,
            "Meeting": "Yes" if entry["meeting"] else "No",
            "Meeting Information": entry["meeting_info"] if entry["meeting"] else "",
            "Tasks": entry["tasks"],
            "General Information": entry["general"]
        })
    return records
