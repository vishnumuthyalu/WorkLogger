import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Daily Work Log", layout="centered")
st.title("🗓️ Daily Work Log")

# Show current date and time
current_time = datetime.now()
st.markdown(f"**📅 Date:** {current_time.strftime('%A, %B %d, %Y')}")
st.markdown(f"**⏰ Time:** {current_time.strftime('%I:%M %p')}")

st.divider()

# Define work hours
hours = [f"{h}:00 {'AM' if h < 12 else 'PM'}" for h in range(8, 18)]

# Initialize session state for structured logging
if "structured_log" not in st.session_state:
    st.session_state.structured_log = {
        hour: {
            "meeting": False,
            "meeting_info": "",
            "tasks": "",
            "general": ""
        } for hour in hours
    }

st.markdown("Fill out your log below for each hour:")

# Create UI for each hour
for hour in hours:
    with st.expander(f"🕒 {hour}"):
        st.session_state.structured_log[hour]["meeting"] = st.checkbox(
            "Was there a meeting during this hour?",
            key=f"{hour}_meeting"
        )
        if st.session_state.structured_log[hour]["meeting"]:
            st.session_state.structured_log[hour]["meeting_info"] = st.text_area(
                "📝 Meeting Information", key=f"{hour}_meeting_info"
            )
        st.session_state.structured_log[hour]["tasks"] = st.text_area(
            "✅ Tasks Worked On", key=f"{hour}_tasks"
        )
        st.session_state.structured_log[hour]["general"] = st.text_area(
            "🗒️ General Information", key=f"{hour}_general"
        )

# Convert to DataFrame
records = []
for hour in hours:
    entry = st.session_state.structured_log[hour]
    records.append({
        "Time": hour,
        "Meeting": "Yes" if entry["meeting"] else "No",
        "Meeting Information": entry["meeting_info"] if entry["meeting"] else "",
        "Tasks": entry["tasks"],
        "General Information": entry["general"]
    })
log_df = pd.DataFrame(records)

# Export as CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

# Export as Word
def convert_df_to_docx(df):
    doc = Document()
    doc.add_heading("Daily Work Log", level=1)
    doc.add_paragraph(f"Date: {current_time.strftime('%A, %B %d, %Y')}")
    table = doc.add_table(rows=1, cols=len(df.columns))
    table.style = "Table Grid"
    
    # Header
    hdr_cells = table.rows[0].cells
    for i, col in enumerate(df.columns):
        hdr_cells[i].text = col
    
    # Rows
    for _, row in df.iterrows():
        row_cells = table.add_row().cells
        for i, col in enumerate(df.columns):
            row_cells[i].text = str(row[col])
    
    doc_io = BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    return doc_io

st.divider()

# Download buttons
col1, col2 = st.columns(2)

with col1:
    st.download_button(
        "📤 Download as CSV",
        data=convert_df_to_csv(log_df),
        file_name=current_time.strftime("%A_%B_%d_%Y") + "_daily_work_log.csv",
        mime="text/csv",
    )

with col2:
    docx_file = convert_df_to_docx(log_df)
    st.download_button(
        "📄 Download as Word Document",
        data=docx_file,
        file_name=current_time.strftime("%A_%B_%d_%Y") + "_daily_work_log.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

st.success("✅ Log your day and export when ready!", icon="✅")
