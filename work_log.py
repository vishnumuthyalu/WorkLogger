import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Daily Work Log", layout="centered")

st.title("🗓️ Daily Work Log")

# Display today's date and current time
current_time = datetime.now()
st.markdown(f"**📅 Date:** {current_time.strftime('%A, %B %d, %Y')}")
st.markdown(f"**⏰ Time:** {current_time.strftime('%I:%M %p')}")

st.divider()

# Define work hours
hours = [f"{h}:00 {'AM' if h < 12 else 'PM'}" for h in range(8, 18)]

# Initialize session state
if "work_log" not in st.session_state:
    st.session_state.work_log = {hour: "" for hour in hours}

st.markdown("Fill in what you're working on for each hour:")

# Input form
for hour in hours:
    st.session_state.work_log[hour] = st.text_area(
        f"{hour}", value=st.session_state.work_log[hour], key=hour
    )

# Convert to DataFrame
log_df = pd.DataFrame(
    list(st.session_state.work_log.items()), columns=["Time", "Activity"]
)

# Export as CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

# Export as Word
def convert_df_to_docx(df):
    doc = Document()
    doc.add_heading("Daily Work Log", level=1)
    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Time"
    hdr_cells[1].text = "Activity"
    
    for _, row in df.iterrows():
        row_cells = table.add_row().cells
        row_cells[0].text = row["Time"]
        row_cells[1].text = row["Activity"]
    
    doc_io = BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    return doc_io

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        "📤 Download as CSV",
        data=convert_df_to_csv(log_df),
        file_name=current_time.strftime('%A, %B %d, %Y') + "_" + "daily_work_log.csv",
        mime="text/csv",
    )

with col2:
    docx_file = convert_df_to_docx(log_df)
    st.download_button(
        "📄 Download as Word Document",
        data=docx_file,
        file_name=current_time.strftime('%A, %B %d, %Y') + "_" + "daily_work_log.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

st.success("✅ Fill out your log above and download it when ready.", icon="✅")
