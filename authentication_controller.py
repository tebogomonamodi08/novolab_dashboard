from email_service import send_mail
from otp_generator import generate_otp
from dotenv import load_dotenv
import os

load_dotenv()
email = os.getenv('SENDER_EMAIL')
password = os.getenv('SENDER_PASSWORD')


'''
This module will implement otp generation and sending the otp to the user using the provided email
'''
user_otp = {}

def send_otp(email:str):
    '''
    generate_otp->send it to the email address provided->store email with the otp in dictionary
    '''
    otp = generate_otp()
    user_otp[email]=otp
    success = send_mail(email,otp)
    if success:
        return True
    else:
        return False
    