# validator.py

import re
from datetime import datetime

class DataValidator:
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))


    @staticmethod
    def validate_customer_data(data):
        """Validate all customer data"""
        errors = []
        
        # Required fields
        required_fields = ['cust_unique_id', 'cust_tax_id', 'cust_email', 
                          'billed_amount', 'currency']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"{field} is required")

        # Email format
        if data.get('cust_email') and not DataValidator.validate_email(data['cust_email']):
            errors.append("Invalid email format")

        # Billed amount
        try:
            if float(data.get('billed_amount', 0)) <= 0:
                errors.append("Billed amount must be positive")
        except ValueError:
            errors.append("Invalid billed amount")

        return errors