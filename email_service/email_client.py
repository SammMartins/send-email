import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

class EmailClient:
    def __init__(self):
        self.email_user = os.getenv('EMAIL_USER')
        self.email_pass = os.getenv('EMAIL_PASS')
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587

    def send_email(self, recipient, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.email_user
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_pass)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            return False
