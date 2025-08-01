# 🗓️ WorkLogger v1.0

A thoughtfully designed Streamlit-based daily work logging application that I built to demonstrate modern web development skills while solving a real productivity challenge. This application showcases clean architecture, user-centered design, and robust functionality for tracking daily activities, meetings, and tasks.

## ✨ Key Features & Technical Highlights

- **📅 Interactive Calendar** - Custom-built date selection with enhanced UX and validation logic
- **🗓️ Dynamic Work Logging** - Flexible hourly time slots with persistent session management
- **🕒 Smart Time Range** - Configurable work hours with intelligent 24-hour format handling
- **🤝 Meeting Integration** - Structured data capture for professional meeting documentation
- **📊 Dual Preview Modes** - Responsive table and list views with real-time data transformation
- **💾 Robust Database Layer** - SQLAlchemy ORM with SQLite backend and automated schema management
- **📤 Multi-Format Export** - Programmatic generation of CSV, Word, and text documents
- **📧 SMTP Email Integration** - Secure email delivery with attachment handling and error management
- **📚 Historical Data Access** - Complete audit trail with chronological log retrieval
- **🗑️ Data Management** - Safe bulk operations with confirmation workflows
- **📚 Integrated Help System** - Self-documenting interface with built-in user support and feedback collection

## 🚀 Getting Started

### Technology Stack
- **Python 3.7+** - Core runtime environment
- **Streamlit** - Modern web framework for data applications
- **SQLAlchemy** - Professional ORM with database abstraction
- **Pandas** - Advanced data manipulation and analysis

### Quick Setup

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

## 📖 Application Architecture & User Experience

### Core Workflow Design

I designed this application with a logical, intuitive workflow that mirrors real-world productivity patterns:

1. **Smart Date Selection**: Engineered calendar interface with intelligent date validation and contextual information
2. **Flexible Time Management**: Configurable work hours with sidebar controls supporting various schedule patterns
3. **Structured Data Entry**: Expandable hourly sections with conditional fields that adapt to user input
4. **Real-time Preview**: Instant data transformation between table and list formats for different use cases
5. **Persistent Storage**: Automated database operations with conflict resolution and data integrity
6. **Seamless Export**: Multi-format document generation with professional styling and email integration

### Advanced Calendar Implementation
- **Smart Date Boundaries**: Programmatically enforced date ranges (past year to 30 days future)
- **Contextual Information**: Real-time calculation of relative dates and calendar statistics
- **Responsive Design**: Adaptive layout with status indicators and metric displays

### Integrated Support Framework
- **📖 Dynamic Documentation**: In-app README rendering with fallback content handling
- **🐛 Structured Issue Tracking**: Comprehensive bug reporting with system information collection
- **💡 Feature Pipeline**: User-driven enhancement requests with categorization and impact assessment
- **📞 Direct Communication**: Seamless developer feedback loop with GitHub integration

### Production-Ready Email System

I implemented a robust SMTP integration with comprehensive error handling and security considerations:

```toml
# .streamlit/secrets.toml - Secure configuration management
[email]
server = "smtp.gmail.com"
port = 465
user = "your_email@gmail.com"
password = "your_app_password"  # Supports OAuth2 and App Passwords
sender_name = "Your Name"
default_to = "recipient@example.com"
default_cc = ""
default_subject = "{date_str} Daily Work Log"  # Dynamic templating
```

## 📁 System Architecture

This application demonstrates clean separation of concerns through a modular architecture:

```
WorkLogger/
├── app.py              # Main application controller with Streamlit integration
├── db_utils.py         # Database abstraction layer with SQLAlchemy ORM
├── settings.py         # Configuration management and UI component library
├── log_utils.py        # Session state management and data transformation
├── export_utils.py     # Document generation engine (CSV, DOCX, TXT)
├── email_utils.py      # SMTP client with SSL security and error handling
├── run_db.py          # Database inspection utilities for development
├── requirements.txt    # Dependency specification for reproducible environments
├── work_logs.db       # SQLite database (auto-provisioned)
├── Log_tests/         # Sample output files demonstrating export capabilities
└── README.md          # Comprehensive documentation and technical specifications
```

## 🔧 Technical Configuration

### Intelligent Time Management
- **Dynamic Sidebar Controls**: Real-time work hour configuration with instant validation
- **24-Hour Format Support**: Professional time handling with automatic conversion utilities
- **Smart Defaults**: Configurable 8 AM - 5 PM range with user override capabilities

### Database Architecture
- **SQLite Integration**: Lightweight, serverless database perfect for single-user applications
- **Automated Schema**: Self-initializing database with migration-ready structure
- **Data Integrity**: UNIQUE constraints and timestamp tracking for audit trails

## 📊 Export Engine & Document Generation

I built a sophisticated document generation system supporting multiple professional formats:

### CSV Export Engine
- **Structured Data Output**: Clean tabular format optimized for spreadsheet applications
- **Complete Data Integrity**: All hourly entries with meeting metadata and task details
- **Cross-Platform Compatibility**: UTF-8 encoding ensures universal file support

### Microsoft Word Integration
- **Professional Document Generation**: Automated DOCX creation using python-docx library
- **Corporate-Ready Formatting**: Structured tables with proper headers and styling
- **Dynamic Content**: Date-aware templates with contextual information

### Plain Text Solutions
- **Lightweight Format**: Simple, readable text output for universal compatibility
- **Hierarchical Structure**: Logical organization perfect for email bodies and quick sharing
- **Platform Independent**: Works across all systems without software dependencies

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







