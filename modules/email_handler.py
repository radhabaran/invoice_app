# email_handler.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

class EmailHandler:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv('GMAIL_USER')
        self.sender_password = os.getenv('GMAIL_PASSWORD')


    def send_invoice(self, recipient_email, invoice_data, invoice_path):
        """Send invoice email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = "Payment Due"

            body = f"""Dear {invoice_data['cust_fname']},

Your payment of {invoice_data['currency']} {invoice_data['billed_amount']} is due by {invoice_data['payment_due_date']}.
Please do the payment at the earliest.

Best regards,
Your Company Name"""

            msg.attach(MIMEText(body, 'plain'))

            # Attach PDF
            with open(invoice_path, "rb") as f:
                pdf = MIMEApplication(f.read(), _subtype="pdf")
                pdf.add_header('Content-Disposition', 'attachment', 
                             filename=os.path.basename(invoice_path))
                msg.attach(pdf)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            return True
        except Exception as e:
            print(f"Email error: {str(e)}")
            return False