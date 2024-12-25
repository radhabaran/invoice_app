# invoice_gen.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from datetime import datetime
import os

class InvoiceGenerator:
    def __init__(self):
        self.invoice_dir = 'invoices'
        if not os.path.exists(self.invoice_dir):
            os.makedirs(self.invoice_dir)


    def generate_invoice(self, data):
        """Generate PDF invoice"""
        filename = f"{self.invoice_dir}/INV_{data['transaction_id']}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        # Header
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, 750, "INVOICE")
        
        # Customer Details
        c.setFont("Helvetica", 12)
        c.drawString(50, 700, f"Customer ID: {data['cust_unique_id']}")
        c.drawString(50, 680, f"Name: {data['cust_fname']} {data['cust_lname']}")
        c.drawString(50, 660, f"Tax ID: {data['cust_tax_id']}")
        
        # Invoice Details
        c.drawString(50, 620, f"Transaction ID: {data['transaction_id']}")
        c.drawString(50, 600, f"Date: {data['transaction_date']}")
        c.drawString(50, 580, f"Due Date: {data['payment_due_date']}")
        
        # Amount
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 520, f"Amount: {data['currency']} {data['billed_amount']}")
        
        c.save()
        return filename