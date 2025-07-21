# 🗓️ WorkLogger v1.0

A comprehensive Streamlit-based daily work logging application that helps you stay organized and productive by tracking your daily activities, meetings, and tasks.

## ✨ Features

- **📅 Interactive Calendar** - Select dates with an enhanced calendar widget
- **🗓️ Daily Work Logging** - Record tasks, meetings, and notes with hourly time slots
- **🕒 Customizable Time Range** - Set your work hours (24-hour format)
- **🤝 Meeting Tracking** - Log meetings with detailed information
- **📊 Multiple Preview Modes** - View your logs as a table or formatted list
- **💾 Database Storage** - Persistent storage using SQLite database
- **📤 Export Options** - Download logs as CSV, Word documents, or text files
- **📧 Email Integration** - Send work logs directly via email with attachments
- **📚 Historical Logs** - View and access previously saved work logs
- **🗑️ Data Management** - Clear all logs when needed
- **📚 Help & Support System** - Built-in user guide, issue reporting, and feature requests

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vishnumuthyalu/WorkLogger.git
   cd WorkLogger
   ```

2. **Install required dependencies:**
   ```bash
   pip install streamlit pandas sqlalchemy python-docx
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

## 📖 Usage

### Basic Workflow

1. **Select Date**: Use the interactive calendar to choose your logging date
2. **Set Time Range**: Configure your work hours in the sidebar (default: 8 AM - 5 PM)
3. **Fill Hourly Logs**: 
   - Expand each hour slot
   - Mark if there was a meeting
   - Add meeting information (if applicable)
   - Record tasks worked on
   - Add general notes
4. **Preview**: Choose between Table or List view to review your log
5. **Save**: Save your log to the database for future reference
6. **Export/Share**: Download as files or email directly from the app

### Interactive Calendar Features
- **Date Selection**: Click on any date within the allowed range (past year to 30 days future)
- **Date Information**: See relative date status (today, yesterday, days ago/ahead)
- **Calendar Context**: View week numbers, day of year, and month information

### Help & Support System
- **📖 User Guide**: Access the complete README documentation within the app
- **🐛 Issue Reporting**: Submit bug reports with detailed system information
- **💡 Feature Requests**: Suggest new features and improvements
- **📞 Developer Contact**: Direct communication channel for support

### Email Configuration

For email functionality, configure your SMTP settings in Streamlit secrets:

```toml
# .streamlit/secrets.toml
[email]
server = "smtp.gmail.com"
port = 465
user = "your_email@gmail.com"
password = "your_app_password"
sender_name = "Your Name"
default_to = "recipient@example.com"
default_cc = ""
default_subject = "{date_str} Daily Work Log"
```

## 📁 Project Structure

```
WorkLogger/
├── app.py              # Main Streamlit application
├── db_utils.py         # Database operations (SQLAlchemy)
├── settings.py         # Configuration management
├── log_utils.py        # Log data handling
├── export_utils.py     # Export functionality
├── email_utils.py      # Email integration
├── run_db.py          # Database utility script
├── work_logs.db       # SQLite database (auto-created)
├── Log_tests/         # Sample exported files
└── README.md          # This file
```

## 🔧 Configuration

### Time Range Settings
- Configure your work hours using the sidebar controls
- Supports 24-hour format (0-23)
- Default range: 8 AM to 5 PM

### Database Settings
- Uses SQLite by default for local storage
- Database file: `work_logs.db`
- Automatic table creation on first run

## 📊 Export Formats

### CSV Export
- Structured table format
- All hourly entries with meeting info, tasks, and notes
- Easy to import into spreadsheet applications

### Word Document
- Professional formatted document
- Table layout with proper headers
- Includes date and formatted content

### Text List
- Simple text format
- Hierarchical structure
- Perfect for quick sharing or note-taking

## 🛠️ Technical Details

### Dependencies
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **SQLAlchemy** - Database ORM
- **python-docx** - Word document generation
- **smtplib** - Email functionality (built-in)

### Database Schema
```sql
CREATE TABLE work_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_date TEXT UNIQUE,
    log_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)







