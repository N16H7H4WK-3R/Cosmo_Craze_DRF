from rest_framework_simplejwt.tokens import RefreshToken
import os
import smtplib
from email.mime.text import MIMEText


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    access_token_lifetime = access_token.lifetime.total_seconds()
    # Convert seconds to Days, Hours, Minutes, and Seconds
    days, remainder = divmod(access_token_lifetime, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    expires_in = f"{int(days)}d:{int(hours)}h:{int(minutes)}m:{int(seconds)}s"
    return {
        "refresh": str(refresh),
        "access": str(access_token),
        "expires_in": expires_in,
    }


def send_email(to_email, subject, message):
    # Configure Gmail SMTP server details
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = os.environ.get("smtp_email")
    smtp_password = os.environ.get("smtp_password")
    sender_email = os.environ.get("sender_email")

    # Create a MIME message
    msg = MIMEText(message)
    msg["Subject"] = subject[0]
    msg["From"] = sender_email
    msg["To"] = to_email

    # Send the email
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
