import streamlit as st
import os

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

def show_help_section():
    st.sidebar.header("📚 Help & Support")
    
    # Display three buttons directly
    if st.sidebar.button("📖 Show User Guide"):
        show_readme_guide()
    
    if st.sidebar.button("🐛 Report Issue"):
        show_issue_form()
    
    if st.sidebar.button("💡 Request Feature"):
        show_feature_request_form()

def show_readme_guide():
    """Display the README content as a user guide"""
    st.subheader("📖 WorkLogger User Guide")
    
    # Try to read the README file
    try:
        readme_path = os.path.join(os.path.dirname(__file__), "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as f:
                readme_content = f.read()
            st.markdown(readme_content)
        else:
            st.error("README.md file not found. Please check the project directory.")
    except Exception as e:
        st.error(f"Error loading README: {str(e)}")
        
        # Fallback content
        st.markdown("""
        ## WorkLogger User Guide
        
        ### Quick Start
        1. **Select Date**: Use the calendar to choose your logging date
        2. **Set Time Range**: Configure work hours in the sidebar
        3. **Fill Hourly Logs**: Expand time slots and add your activities
        4. **Preview**: Review your logs in table or list format
        5. **Save**: Store logs in the database
        6. **Export**: Download or email your logs
        
        ### Features
        - Interactive calendar for date selection
        - Hourly time slot logging
        - Meeting tracking
        - Multiple export formats (CSV, Word, Text)
        - Email integration
        - Historical log viewing
        
        For more detailed information, please check the README.md file in the project directory.
        """)

def show_issue_form():
    """Display a form for users to report issues"""
    st.subheader("🐛 Report an Issue")
    
    with st.form("issue_form"):
        st.markdown("Help us improve WorkLogger by reporting any issues you encounter:")
        
        # Issue details
        issue_type = st.selectbox(
            "Issue Type:",
            ["Bug Report", "Performance Issue", "UI/UX Problem", "Data Loss", "Other"]
        )
        
        issue_title = st.text_input(
            "Issue Title:",
            placeholder="Brief description of the issue"
        )
        
        issue_description = st.text_area(
            "Detailed Description:",
            placeholder="Please describe the issue in detail, including steps to reproduce...",
            height=150
        )
        
        # System information
        st.markdown("**System Information (Optional):**")
        col1, col2 = st.columns(2)
        
        with col1:
            os_info = st.text_input("Operating System:", placeholder="e.g., Windows 11, macOS 12, Ubuntu 20.04")
            browser_info = st.text_input("Browser:", placeholder="e.g., Chrome 91, Firefox 89")
        
        with col2:
            python_version = st.text_input("Python Version:", placeholder="e.g., 3.9.7")
            streamlit_version = st.text_input("Streamlit Version:", placeholder="e.g., 1.28.0")
        
        # Contact information
        user_email = st.text_input(
            "Your Email (Optional):",
            placeholder="your.email@example.com",
            help="Provide your email if you'd like updates on the issue resolution"
        )
        
        # Priority level
        priority = st.select_slider(
            "Priority Level:",
            options=["Low", "Medium", "High", "Critical"],
            value="Medium"
        )
        
        submitted = st.form_submit_button("📤 Submit Issue Report")
        
        if submitted:
            if issue_title and issue_description:
                # Create issue summary
                issue_summary = f"""
**Issue Type:** {issue_type}
**Priority:** {priority}
**Title:** {issue_title}

**Description:**
{issue_description}

**System Information:**
- OS: {os_info if os_info else 'Not provided'}
- Browser: {browser_info if browser_info else 'Not provided'}
- Python: {python_version if python_version else 'Not provided'}
- Streamlit: {streamlit_version if streamlit_version else 'Not provided'}

**Contact:** {user_email if user_email else 'Not provided'}
**Submitted:** {st.session_state.get('current_time', 'Unknown')}
"""
                
                # Store in session state for developer review
                if 'issues' not in st.session_state:
                    st.session_state.issues = []
                
                st.session_state.issues.append({
                    'type': issue_type,
                    'title': issue_title,
                    'description': issue_description,
                    'priority': priority,
                    'email': user_email,
                    'system_info': {
                        'os': os_info,
                        'browser': browser_info,
                        'python': python_version,
                        'streamlit': streamlit_version
                    },
                    'timestamp': st.session_state.get('current_time', 'Unknown')
                })
                
                st.success("✅ Issue report submitted successfully!")
                st.info("Your issue has been recorded. Thank you for helping improve WorkLogger!")
                
                # Show GitHub link for additional support
                st.markdown("""
                **Additional Support:**
                - Visit our [GitHub Issues](https://github.com/vishnumuthyalu/WorkLogger/issues) page
                - Check existing issues or create a new one
                - Join our community discussions
                """)
                
            else:
                st.error("Please fill in the required fields (Title and Description)")

def show_feature_request_form():
    """Display a form for users to request new features"""
    st.subheader("💡 Request a Feature")
    
    with st.form("feature_request_form"):
        st.markdown("Have an idea to make WorkLogger better? We'd love to hear it!")
        
        # Feature details
        feature_category = st.selectbox(
            "Feature Category:",
            ["User Interface", "Export/Import", "Calendar/Scheduling", "Reporting", "Integration", "Performance", "Other"]
        )
        
        feature_title = st.text_input(
            "Feature Title:",
            placeholder="Brief name for your feature idea"
        )
        
        feature_description = st.text_area(
            "Feature Description:",
            placeholder="Describe your feature idea in detail. What problem would it solve? How would it work?",
            height=150
        )
        
        # Use case
        use_case = st.text_area(
            "Use Case/Scenario:",
            placeholder="Describe a specific scenario where this feature would be useful...",
            height=100
        )
        
        # Priority and impact
        col1, col2 = st.columns(2)
        
        with col1:
            importance = st.select_slider(
                "How important is this feature to you?",
                options=["Nice to have", "Somewhat important", "Very important", "Critical"],
                value="Somewhat important"
            )
        
        with col2:
            user_impact = st.selectbox(
                "Who would benefit?",
                ["Just me", "Some users", "Most users", "All users"]
            )
        
        # Contact for follow-up
        contact_email = st.text_input(
            "Your Email (Optional):",
            placeholder="your.email@example.com",
            help="We may contact you for clarification or updates"
        )
        
        submitted = st.form_submit_button("🚀 Submit Feature Request")
        
        if submitted:
            if feature_title and feature_description:
                # Store feature request
                if 'feature_requests' not in st.session_state:
                    st.session_state.feature_requests = []
                
                st.session_state.feature_requests.append({
                    'category': feature_category,
                    'title': feature_title,
                    'description': feature_description,
                    'use_case': use_case,
                    'importance': importance,
                    'user_impact': user_impact,
                    'email': contact_email,
                    'timestamp': st.session_state.get('current_time', 'Unknown')
                })
                
                st.success("✅ Feature request submitted successfully!")
                st.info("Thank you for your suggestion! We'll review it for future development.")
                
                # Show contribution info
                st.markdown("""
                **Want to contribute?**
                - Check our [GitHub repository](https://github.com/vishnumuthyalu/WorkLogger)
                - Fork the project and submit a pull request
                - Join our development discussions
                """)
                
            else:
                st.error("Please fill in the required fields (Title and Description)")



