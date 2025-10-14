from smtplib import SMTP_SSL
import ssl

port = 465
password = input('Enter password:')
#create a ssl context
context = ssl.create_default_context()
with SMTP_SSL('smtp.gmail.com',port, context=context) as server:
    server.login('tebogomonamodi08@gmail.com', password)
    server.sendmail(
        from_addr='tebogomonamodi08gmail.com',
        to_addrs='tebogomonamodi64@gmail.com',
        msg='subject: test mail\nWell this is '
    )