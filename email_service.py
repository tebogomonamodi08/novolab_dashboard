'''
This module allows you to send an email over the smtp

create a mime obj->define mime object->ssl context->open connect->login->send message
'''
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
from smtplib import SMTP_SSL


def send_mail(receiver_addr:str, sender_addr:str, password:str, otp:str):
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



    

