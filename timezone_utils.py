"""
Timezone utilities for WorkLogger application
Handles timezone conversions for deployment environments
"""

import pytz
from datetime import datetime
import streamlit as st

def get_user_timezone():
    """Get the user's preferred timezone from secrets or default to EST/EDT"""
    try:
        # Try to get timezone from secrets
        timezone_name = st.secrets.get("app", {}).get("timezone", "America/New_York")
    except:
        # Default to Eastern Time if no secrets configured
        timezone_name = "America/New_York"
    
    try:
        return pytz.timezone(timezone_name)
    except:
        # Fallback to UTC if timezone is invalid
        return pytz.UTC

def get_current_time_in_timezone():
    """Get current time in the user's timezone"""
    user_tz = get_user_timezone()
    utc_now = datetime.now(pytz.UTC)
    return utc_now.astimezone(user_tz)

def format_time_with_timezone(dt=None):
    """Format datetime with timezone info"""
    if dt is None:
        dt = get_current_time_in_timezone()
    
    return dt.strftime("%Y-%m-%d %H:%M:%S %Z")

def get_timezone_display_name():
    """Get a user-friendly timezone name for display"""
    user_tz = get_user_timezone()
    now = get_current_time_in_timezone()
    
    # Get the timezone abbreviation (like EST, EDT, PST, etc.)
    tz_name = now.strftime("%Z")
    
    return f"{user_tz.zone} ({tz_name})"
