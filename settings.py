import streamlit as st

def hour_label(h):
    suffix = "AM" if h < 12 else "PM"
    hour12 = h if 1 <= h <= 12 else (h - 12 if h > 12 else 12)
    return f"{hour12}:00 {suffix}"

def get_time_range():
    st.sidebar.header("Select Time Range (24-hour format)")
    start_hour = st.sidebar.number_input("Start Hour", min_value=0, max_value=23, value=8, step=1)
    end_hour = st.sidebar.number_input("End Hour", min_value=0, max_value=23, value=17, step=1)

    if start_hour >= end_hour:
        st.sidebar.error("Start Hour must be less than End Hour")
        st.stop()

    hours = [hour_label(h) for h in range(start_hour, end_hour + 1)]
    return start_hour, end_hour, hours

def get_database_settings():
    st.sidebar.header("Database Settings")
    db_type = st.sidebar.selectbox("Select Database", ["sqlite", "postgres"], index=0)
    return db_type

