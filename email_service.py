'''
This module allows you to send an email over the smtp

create a mime obj->define mime object->ssl context->open connect->login->send message
'''
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
from smtplib import SMTP_SSL, SMTPAuthenticationError, SMTPConnectError
from dotenv import load_dotenv
import os

load_dotenv()


def send_mail(receiver_addr:str, otp:str):
    '''
    This function sends an otp email to a sender address
    '''
    try:
        sender_addr = os.getenv('SENDER_EMAIL')
        password = os.getenv('SENDER_PASSWORD')
        msg = MIMEMultipart()
        msg['To']=receiver_addr
        msg['From']=sender_addr
        msg['Subject']='Your OTP code'
        body = f'Your OTP is {otp}'
        msg.attach(MIMEText(body,'plain'))

        context = ssl.create_default_context()
        port=465
        server_addr = 'smtp.gmail.com'

        with SMTP_SSL(server_addr,port,context=context) as server:
            server.login(sender_addr,password)

            server.send_message(msg)
            return True
    except SMTPConnectError:
        print('Connection: Failed to connect to mail server')
    except SMTPAuthenticationError:
        print('Authentication:Wrong Password, please check password')
    except Exception:
        print('An unexpected error occured')
    
    return False





    

