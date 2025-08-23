import smtplib
import ssl
import streamlit as st
from email.message import EmailMessage

def send_email_with_attachments(smtp_server, smtp_port, smtp_user, smtp_password,
                                from_name, to, cc, subject, body, attachments):
    if smtp_password == "CHANGE_ME":
        return False, "SMTP password not configured. Set credentials in st.secrets."
    if not to.strip():
        return False, "Please provide at least one recipient email address."

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"{from_name} <{smtp_user}>"
        msg["To"] = to

        cc_clean = [e.strip() for e in cc.replace(";", ",").split(",") if e.strip()]
        if cc_clean:
            msg["Cc"] = ", ".join(cc_clean)

        msg.set_content(body)

        for attachment in attachments:
            file_bytes, maintype, subtype, filename = attachment
            msg.add_attachment(file_bytes, maintype=maintype, subtype=subtype, filename=filename)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(smtp_user, smtp_password)
            all_recipients = [to] + cc_clean
            server.send_message(msg, from_addr=smtp_user, to_addrs=all_recipients)

        return True, "Email sent successfully! ✅"
    except Exception as e:
        return False, f"Failed to send email: {e}"

def show_email_configuration_form():
    """Show form for users to input their own email credentials for testing"""
    
    # Check if secrets are configured
    email_configured = False
    try:
        email_cfg = st.secrets.get("email", {})
        if email_cfg.get("password", "CHANGE_ME") != "CHANGE_ME":
            email_configured = True
    except:
        pass
    
    if email_configured:
        st.success("✅ Email is pre-configured by the app administrator.")
        return True, {}
    else:
        # Add section break before configuration form
        st.divider()
        st.subheader("📧 Email Configuration for Testing")
        st.warning("⚠️ Email not configured by app administrator. You can test the email functionality by providing your own credentials below.")
        
        with st.expander("📧 Email Credentials (For Testing Only)", expanded=False):
            st.info("""
            **For Gmail users:**
            1. Enable 2-Factor Authentication
            2. Generate an App Password: [Google App Passwords](https://myaccount.google.com/apppasswords)
            3. Use the generated app password below (not your regular password)
            
            **Security Note:** These credentials are only used for this session and are not stored.
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                user_smtp_server = st.text_input(
                    "SMTP Server", 
                    value="smtp.gmail.com",
                    help="Gmail: smtp.gmail.com, Outlook: smtp-mail.outlook.com"
                )
                user_smtp_port = st.number_input(
                    "SMTP Port", 
                    value=587, 
                    min_value=25, 
                    max_value=993,
                    help="Gmail: 587 or 465, Outlook: 587"
                )
                use_tls = st.checkbox("Use TLS", value=True, help="Recommended for most providers")
                
            with col2:
                user_email = st.text_input(
                    "Your Email Address",
                    placeholder="your_email@gmail.com"
                )
                user_password = st.text_input(
                    "Email Password/App Password", 
                    type="password",
                    help="Use App Password for Gmail, not your regular password"
                )
                user_name = st.text_input(
                    "Sender Name",
                    value="WorkLogger User",
                    help="Name that will appear as sender"
                )
            
            # Test connection button
            if st.button("🔍 Test Email Connection"):
                if user_email and user_password:
                    success, message = test_email_connection(
                        user_smtp_server, user_smtp_port, user_email, 
                        user_password, use_tls
                    )
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.warning("Please provide email and password to test connection.")
            
            # Check if all fields are filled
            if user_email and user_password and user_name:
                return True, {
                    'server': user_smtp_server,
                    'port': user_smtp_port,
                    'user': user_email,
                    'password': user_password,
                    'sender_name': user_name,
                    'use_tls': use_tls
                }
            else:
                st.info("👆 Fill in the email credentials above to enable email functionality.")
                return False, {}

def test_email_connection(smtp_server, smtp_port, smtp_user, smtp_password, use_tls=True):
    """Test email connection without sending an email"""
    try:
        if use_tls:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
        else:
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
        
        server.login(smtp_user, smtp_password)
        server.quit()
        return True, "Connection successful!"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

def send_email_with_user_credentials(user_config, to, cc, subject, body, attachments):
    """Send email using user-provided credentials"""
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"{user_config['sender_name']} <{user_config['user']}>"
        msg["To"] = to

        cc_clean = [e.strip() for e in cc.replace(";", ",").split(",") if e.strip()]
        if cc_clean:
            msg["Cc"] = ", ".join(cc_clean)

        msg.set_content(body)

        for attachment in attachments:
            file_bytes, maintype, subtype, filename = attachment
            msg.add_attachment(file_bytes, maintype=maintype, subtype=subtype, filename=filename)

        if user_config.get('use_tls', True):
            server = smtplib.SMTP(user_config['server'], user_config['port'])
            server.starttls()
        else:
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(user_config['server'], user_config['port'], context=context)
        
        server.login(user_config['user'], user_config['password'])
        all_recipients = [to] + cc_clean
        server.send_message(msg, from_addr=user_config['user'], to_addrs=all_recipients)
        server.quit()

        return True, "Email sent successfully! ✅"
    except Exception as e:
        return False, f"Failed to send email: {e}"
