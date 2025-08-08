import smtplib
from email.message import EmailMessage
from config import EMAIL_PASSWORD

import mimetypes
import os

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  

class Email:
    def send_email(self, subject: str, body: str, to_email: str, attachment_path: str = None):
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = "quizemaster.mca@gmail.com"
        msg["To"] = to_email

        if attachment_path:
            file_name = os.path.basename(attachment_path)
            mime_type, _ = mimetypes.guess_type(attachment_path)
            maintype, subtype = mime_type.split("/") if mime_type else ("application", "octet-stream")

            with open(attachment_path, "rb") as f:
                file_data = f.read()
                msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("quizemaster.mca@gmail.com", EMAIL_PASSWORD)
            smtp.send_message(msg)



        