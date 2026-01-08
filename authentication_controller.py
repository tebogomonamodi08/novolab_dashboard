from email_service import send_mail, has_email_provider
from otp_generator import generate_otp
import os

# in-memory store for OTPs (for demo/simple use)
user_otp = {}

def send_otp(email: str) -> bool:
    """
    Generate an OTP, store it and attempt sending it.
    Returns True on success, False on failure.
    """
    email = email.strip()
    if not email:
        print('send_otp: empty email provided')
        return False

    otp = generate_otp()
    user_otp[email] = otp

    # If no external provider configured, for convenience return True but log the OTP
    # (you can set DEV_SHOW_OTP to true in main to show it in the UI during testing)
    if not has_email_provider():
        print(f'No email provider configured; OTP for {email}: {otp}')
        return True

    try:
        success = send_mail(email, otp)
        if success:
            print(f'OTP sent to {email}')
            return True
        else:
            print(f'Failed to send OTP to {email}')
            return False
    except Exception as e:
        print(f'Exception in send_otp: {e}')
        return False
