import smtplib
import ssl
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
