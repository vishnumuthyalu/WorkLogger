import streamlit as st
import pandas as pd
from datetime import datetime, date

from settings import get_time_range, show_help_section
from log_utils import initialize_log, get_log_records
from export_utils import convert_df_to_csv, convert_df_to_docx
from email_utils import send_email_with_attachments
from db_utils import init_db, save_log_to_db, get_all_logs
from timezone_utils import get_current_time_in_timezone, format_time_with_timezone, get_timezone_display_name

# Add this import for clearing logs
from sqlalchemy import text
from db_utils import engine

def clear_all_logs():
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM work_logs"))

st.set_page_config(page_title="WorkLogger", layout="wide")
st.title("🗓️ WorkLogger v1.0")

# Store current time in session state for help system (timezone-aware)
if 'current_time' not in st.session_state:
    st.session_state.current_time = format_time_with_timezone()

# Email config from secrets or defaults
_email_cfg = st.secrets.get("email", {}) if hasattr(st, "secrets") else {}
SMTP_SERVER = _email_cfg.get("server", "smtp.gmail.com")
SMTP_PORT = int(_email_cfg.get("port", 465))
SMTP_USER = _email_cfg.get("user", "your_email@example.com")
SMTP_PASSWORD = _email_cfg.get("password", "CHANGE_ME")
SENDER_NAME = _email_cfg.get("sender_name", "Daily Work Logger")
DEFAULT_TO = _email_cfg.get("default_to", "")
DEFAULT_CC = _email_cfg.get("default_cc", "")
DEFAULT_SUBJECT_TEMPLATE = _email_cfg.get("default_subject", "{date_str} Daily Work Log")

left_col, right_col = st.columns([2, 1])

with left_col:
    # Interactive Calendar Date Selection
    st.subheader("📅 Select Date for Work Log")
    
    # Create columns for calendar and date info
    cal_col1, cal_col2 = st.columns([2, 1])
    
    with cal_col1:
        # Enhanced date input with calendar widget
        today = date.today()
        min_date = today - pd.Timedelta(days=365)  # Allow up to 1 year back
        max_date = today + pd.Timedelta(days=30)   # Allow up to 30 days future
        
        log_date = st.date_input(
            "📆 Choose your logging date:",
            value=today,
            min_value=min_date,
            max_value=max_date,
            help="Select any date within the last year or next 30 days"
        )
    
    with cal_col2:
        # Date information display
        if log_date:
            days_diff = (log_date - today).days
            if days_diff == 0:
                date_status = "📍 Today"
            elif days_diff == -1:
                date_status = "⏮️ Yesterday"
            elif days_diff == 1:
                date_status = "⏭️ Tomorrow"
            elif days_diff < 0:
                date_status = f"⏪ {abs(days_diff)} days ago"
            else:
                date_status = f"⏩ {days_diff} days ahead"
            
            st.metric("Date Status", date_status)
    
    file_date_str = log_date.strftime('%A_%B_%d_%Y')
    current_time = get_current_time_in_timezone()
    
    # Enhanced date display with more information
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**📅 Logging for:** {log_date.strftime('%A, %B %d, %Y')}")
    with col2:
        timezone_info = get_timezone_display_name()
        st.info(f"**⏰ Current Time:** {current_time.strftime('%I:%M %p')} ({timezone_info})")
    
    # Add day of week and week number info
    week_number = log_date.isocalendar()[1]
    day_of_year = log_date.timetuple().tm_yday
    st.caption(f"📊 Week {week_number} of {log_date.year} • Day {day_of_year} of year • {log_date.strftime('%B')} month")
    
with right_col:
    st.markdown("""
    ### 👋 Welcome to WorkLogger!
    This app helps you stay organized and productive by providing:
    
    ✅ **Daily Work Logging** – Record tasks, meetings, and notes  
    ✅ **Preview Options** – View your logs as a table or a clean list  
    ✅ **Download & Share** – Export your logs as CSV, Word, or Text  
    ✅ **Email Integration** – Send your work log directly from the app  
    ✅ **Database Storage** – Save logs for future reference  

    """)

st.divider()
# Get time range & hours from settings.py
start_hour, end_hour, hours = get_time_range()

# Add help section to sidebar
show_help_section()

left_col, right_col = st.columns([2, 1])

with left_col:
    st.header("📝 Fill Your Daily Work Log")
    log_key = f"structured_log_{log_date}_{start_hour}_{end_hour}"

    initialize_log(log_key, hours)

    for hour in hours:
        with st.expander(f"🕒 {hour}", expanded=False):
            entry = st.session_state[log_key][hour]
            entry["meeting"] = st.checkbox("Was there a meeting during this hour?", key=f"{log_key}_{hour}_meeting")
            if entry["meeting"]:
                entry["meeting_info"] = st.text_area("📝 Meeting Information", key=f"{log_key}_{hour}_meeting_info")
            entry["tasks"] = st.text_area("✅ Tasks Worked On", key=f"{log_key}_{hour}_tasks")
            entry["general"] = st.text_area("🗒️ General Information", key=f"{log_key}_{hour}_general")

log_df = pd.DataFrame(get_log_records(log_key, hours))

def format_log_as_list(df):
    lines = []
    for _, row in df.iterrows():
        lines.append(f"Time: {row['Time']}")
        lines.append(f"  Meeting: {row['Meeting']}")
        if row['Meeting'] == "Yes" and row['Meeting Information'].strip():
            lines.append(f"  Meeting Info: {row['Meeting Information']}")
        if row['Tasks'].strip():
            lines.append(f"  Tasks: {row['Tasks']}")
        if row['General Information'].strip():
            lines.append(f"  General Info: {row['General Information']}")
        lines.append("")
    return "\n".join(lines)

log_list_text = format_log_as_list(log_df)
list_bytes = log_list_text.encode("utf-8")

csv_bytes = convert_df_to_csv(log_df)
docx_io = convert_df_to_docx(log_df, log_date)
docx_bytes = docx_io.getvalue()

with right_col:
    
    st.header("📊 Log Preview")
    preview_mode = st.radio("Choose preview format:", options=["Table", "List"])


    if preview_mode == "Table":
        st.subheader("Table")
        st.dataframe(log_df)
    else:
        st.subheader("List")
        st.text_area("Detailed Log List Preview", value=log_list_text, height=400)

# Helper to build a single day summary text from the hourly logs
def build_summary(records):
    summary_lines = []
    for r in records:
        if r["Meeting"] == "Yes" or r["Tasks"].strip() or r["General Information"].strip():
            summary_lines.append(f"{r['Time']}: Meeting: {r['Meeting']}")
            if r['Meeting'] == 'Yes' and r['Meeting Information'].strip():
                summary_lines.append(f"  Info: {r['Meeting Information']}")
            if r['Tasks'].strip():
                summary_lines.append(f"  Tasks: {r['Tasks']}")
            if r['General Information'].strip():
                summary_lines.append(f"  General: {r['General Information']}")
            summary_lines.append("")
    return "\n".join(summary_lines) if summary_lines else "No details logged."

# Initialize DB
st.divider()
left_col, right_col = st.columns([2, 1])

init_db()

with left_col:
    st.header("💾 Save Work Log")
    if st.button("Save to Database"):
        summary_text = build_summary(get_log_records(log_key, hours))
        save_log_to_db(log_date, summary_text)
        st.success("✅ Log saved to database!")
    
    

    # Add Clear Logs button
    if st.button("🗑️ Clear All Logs"):
        clear_all_logs()
        st.success("✅ All logs cleared from database!")
   
with right_col:   
    st.header("📥 Download & Share")

    if preview_mode == "Table":
        st.download_button(
            "📤 Download as CSV",
            data=csv_bytes,
            file_name=f"{file_date_str}_daily_work_log.csv",
            mime="text/csv"
        )
        st.download_button(
            "📄 Download as Word Document",
            data=docx_bytes,
            file_name=f"{file_date_str}_daily_work_log.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.download_button(
            "📄 Download as Text List",
            data=list_bytes,
            file_name=f"{file_date_str}_daily_work_log.txt",
            mime="text/plain"
        )
        
st.divider()
left_col, right_col = st.columns([2, 1])
        
with left_col:
    

    st.subheader("📧 Email This Work Log")

    default_subject = DEFAULT_SUBJECT_TEMPLATE.format(date_str=file_date_str)
    to_input = st.text_input("To", value=DEFAULT_TO, placeholder="recipient@example.com")
    cc_input = st.text_input("CC", value=DEFAULT_CC, placeholder="cc1@example.com; cc2@example.com")
    subject_input = st.text_input("Subject", value=default_subject)
    from_display = st.text_input("From Name", value=SENDER_NAME)
    default_body = f"Please find attached the work log for {log_date.strftime('%A, %B %d, %Y')}."
    body_input = st.text_area("Body", value=default_body, height=100)

    if st.button("📧 Send Email with Attachments"):
        if preview_mode == "Table":
            attachments = [
                (csv_bytes, "text", "csv", f"{file_date_str}_daily_work_log.csv"),
                (docx_bytes, "application", "vnd.openxmlformats-officedocument.wordprocessingml.document",
                 f"{file_date_str}_daily_work_log.docx"),
            ]
        else:
            attachments = [
                (list_bytes, "text", "plain", f"{file_date_str}_daily_work_log.txt"),
            ]

        status, message = send_email_with_attachments(
            smtp_server=SMTP_SERVER,
            smtp_port=SMTP_PORT,
            smtp_user=SMTP_USER,
            smtp_password=SMTP_PASSWORD,
            from_name=from_display,
            to=to_input,
            cc=cc_input,
            subject=subject_input,
            body=body_input,
            attachments=attachments,
        )
        if status:
            st.success(message)
        else:
            st.error(message)
with right_col:
    st.header("📚 View Previous Logs")
    logs_df = get_all_logs()
    if not logs_df.empty:
        st.dataframe(logs_df[['log_date', 'created_at']])
        for _, row in logs_df.iterrows():
            with st.expander(f"Logs for {row['log_date']} (saved {row['created_at']}):"):
                st.text(row['log_summary'])
    else:
        st.info("No logs found yet.")        
st.divider()

