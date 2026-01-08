"""
Email sending module with:
- SendGrid API (recommended on Render — uses HTTPS)
- fallback to SMTP (if SENDGRID_API_KEY not set and SMTP env vars present)
"""

import os
import json
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPAuthenticationError, SMTPConnectError
import requests

def has_email_provider() -> bool:
    """
    Returns True if either SendGrid or SMTP env vars are configured.
    """
    if os.getenv('SENDGRID_API_KEY'):
        return True
    if os.getenv('SENDER_EMAIL') and os.getenv('SENDER_PASSWORD'):
        return True
    return False

def send_mail(receiver_addr: str, otp: str) -> bool:
    """
    Send the OTP to receiver_addr.
    Tries SendGrid first (if SENDGRID_API_KEY is present), otherwise falls back to SMTP.
    Returns True on success, False on failure.
    """
    sender_addr = os.getenv('SENDER_EMAIL')
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')

    # Prefer SendGrid (HTTPS) — tends to work reliably on cloud hosts
    if sendgrid_api_key and sender_addr:
        try:
            url = 'https://api.sendgrid.com/v3/mail/send'
            headers = {
                'Authorization': f'Bearer {sendgrid_api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                "personalizations": [{"to": [{"email": receiver_addr}]}],
                "from": {"email": sender_addr},
                "subject": "Your OTP code",
                "content": [{"type": "text/plain", "value": f"Your OTP is {otp}"}]
            }
            resp = requests.post(url, headers=headers, json=data, timeout=10)
            if resp.status_code in (200, 202):
                return True
            else:
                print(f'SendGrid error: status={resp.status_code} body={resp.text}')
        except Exception as e:
            print(f'Exception while sending via SendGrid: {e}')

    # Fallback to SMTP SSL (requires SENDER_EMAIL and SENDER_PASSWORD)
    if sender_addr and os.getenv('SENDER_PASSWORD'):
        try:
            password = os.getenv('SENDER_PASSWORD')
            msg = MIMEMultipart()
            msg['To'] = receiver_addr
            msg['From'] = sender_addr
            msg['Subject'] = 'Your OTP code'
            body = f'Your OTP is {otp}'
            msg.attach(MIMEText(body, 'plain'))

            context = ssl.create_default_context()
            port = int(os.getenv('SMTP_PORT', 465))
            server_addr = os.getenv('SMTP_SERVER', 'smtp.gmail.com')

            with SMTP_SSL(server_addr, port, context=context) as server:
                server.login(sender_addr, password)
                server.send_message(msg)
                return True
        except SMTPConnectError:
            print('Connection: Failed to connect to mail server')
        except SMTPAuthenticationError:
            print('Authentication: Wrong Password, please check password')
        except Exception as e:
            print(f'Unexpected error sending email via SMTP: {e}')

    # If we get here, no provider succeeded
    print('send_mail: No email provider succeeded or no credentials provided.')
    return False





    

