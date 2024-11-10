
import smtplib
from email.mime.text import MIMEText
import time

file_path = "aaa.txt"
SMTP_SERVER = 'smtp.naver.com'
SMTP_PORT = 587
USERNAME = 'chlwlsgh1996@naver.com'
PASSWORD = 'jinho1996'

def send_email(subject, body, to):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = USERNAME
    msg['To'] = to
    smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp_server.starttls()
    smtp_server.login(USERNAME, PASSWORD)
    smtp_server.sendmail(USERNAME, to, msg.as_string())
    smtp_server.quit()

while True:
    with open(file_path, 'r') as file:
        file_contents = file.read()
        if '112' in file_contents or '도와줘' in file_contents:
            send_email('danger', file_contents, 'dpcks367@naver.com')
            time.sleep(60)
