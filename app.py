import streamlit as st
import pandas as pd
from datetime import datetime, date

from log_utils import initialize_log, get_log_records
from export_utils import convert_df_to_csv, convert_df_to_docx
from email_utils import send_email_with_attachments

# ----------------------------------------------------------
# App Config
# ----------------------------------------------------------
st.set_page_config(page_title="Daily Work Log", layout="wide")
st.title("🗓️ Daily Work Log")

# Load Email Config
_email_cfg = st.secrets.get("email", {}) if hasattr(st, "secrets") else {}
SMTP_SERVER = _email_cfg.get("server", "smtp.gmail.com")
SMTP_PORT = int(_email_cfg.get("port", 465))
SMTP_USER = _email_cfg.get("user", "your_email@example.com")
SMTP_PASSWORD = _email_cfg.get("password", "CHANGE_ME")
SENDER_NAME = _email_cfg.get("sender_name", "Daily Work Logger")
DEFAULT_TO = _email_cfg.get("default_to", "")
DEFAULT_CC = _email_cfg.get("default_cc", "")
DEFAULT_SUBJECT_TEMPLATE = _email_cfg.get("default_subject", "{date_str} Daily Work Log")

# ----------------------------------------------------------
# Date & Current Time
# ----------------------------------------------------------
log_date = st.date_input("📆 Select the date to log for", value=date.today())
file_date_str = log_date.strftime('%A_%B_%d_%Y')
current_time = datetime.now()

st.write(f"**📅 Logging for:** `{file_date_str}` | **⏰ Current Time:** `{current_time.strftime('%I:%M %p')}`")
st.divider()

# ----------------------------------------------------------
# Layout with Two Columns
# ----------------------------------------------------------
left_col, right_col = st.columns([2, 1])  # Left = form, Right = download/email

# ----------------------------------------------------------
# Left Column: Daily Work Log Form
# ----------------------------------------------------------
with left_col:
    st.header("📝 Fill Your Daily Work Log")
    hours = [f"{h}:00 {'AM' if h < 12 else 'PM'}" for h in range(8, 18)]
    log_key = f"structured_log_{log_date}"
    initialize_log(log_key, hours)

    for hour in hours:
        with st.expander(f"🕒 {hour}", expanded=False):
            entry = st.session_state[log_key][hour]
            entry["meeting"] = st.checkbox("Was there a meeting during this hour?", key=f"{log_key}_{hour}_meeting")
            if entry["meeting"]:
                entry["meeting_info"] = st.text_area("📝 Meeting Information", key=f"{log_key}_{hour}_meeting_info")
            entry["tasks"] = st.text_area("✅ Tasks Worked On", key=f"{log_key}_{hour}_tasks")
            entry["general"] = st.text_area("🗒️ General Information", key=f"{log_key}_{hour}_general")

# ----------------------------------------------------------
# Convert data for export and email
# ----------------------------------------------------------
log_df = pd.DataFrame(get_log_records(log_key, hours))
csv_bytes = convert_df_to_csv(log_df)
docx_io = convert_df_to_docx(log_df, log_date)
docx_bytes = docx_io.getvalue()

# ----------------------------------------------------------
# Right Column: Download & Email Options
# ----------------------------------------------------------
with right_col:
    st.header("📥 Download & Share")

    st.subheader("Download Files")
    st.download_button("📤 Download as CSV", data=csv_bytes,
                       file_name=f"{file_date_str}_daily_work_log.csv", mime="text/csv")
    st.download_button("📄 Download as Word Document", data=docx_bytes,
                       file_name=f"{file_date_str}_daily_work_log.docx",
                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    st.divider()
    st.subheader("📧 Email This Work Log")

    default_subject = DEFAULT_SUBJECT_TEMPLATE.format(date_str=file_date_str)
    to_input = st.text_input("To", value=DEFAULT_TO, placeholder="recipient@example.com")
    cc_input = st.text_input("CC", value=DEFAULT_CC, placeholder="cc1@example.com; cc2@example.com")
    subject_input = st.text_input("Subject", value=default_subject)
    from_display = st.text_input("From Name", value=SENDER_NAME)
    default_body = f"Please find attached the work log for {log_date.strftime('%A, %B %d, %Y')}."
    body_input = st.text_area("Body", value=default_body, height=100)

    if st.button("📧 Send Email with Attachments"):
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
            attachments=[
                (csv_bytes, "text", "csv", f"{file_date_str}_daily_work_log.csv"),
                (docx_bytes, "application", "vnd.openxmlformats-officedocument.wordprocessingml.document",
                 f"{file_date_str}_daily_work_log.docx")
            ]
        )
        if status:
            st.success(message)
        else:
            st.error(message)
