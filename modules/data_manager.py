# data_manager.py

import pandas as pd
from datetime import datetime
import os

class DataManager:
    def __init__(self):
        self.csv_file = 'data/invoice_data.csv'
        self.ensure_data_file()


    def ensure_data_file(self):
        """Create data file if it doesn't exist"""
        if not os.path.exists('data'):
            os.makedirs('data')
        
        if not os.path.exists(self.csv_file):
            columns = [
                'cust_unique_id', 'cust_tax_id', 'cust_fname', 'cust_lname',
                'cust_email', 'transaction_id', 'transaction_date',
                'billed_amount', 'currency', 'payment_due_date', 'payment_status'
            ]
            pd.DataFrame(columns=columns).to_csv(self.csv_file, index=False)


    def save_record(self, data):
        """Save new record to CSV"""
        df = pd.read_csv(self.csv_file)
        new_record = pd.DataFrame([data])
        df = pd.concat([df, new_record], ignore_index=True)
        df.to_csv(self.csv_file, index=False)
        return True


    def check_duplicate(self, cust_unique_id):
        """Check for duplicate customer ID"""
        df = pd.read_csv(self.csv_file)
        return cust_unique_id in df['cust_unique_id'].values


    def get_all_records(self):
        """Retrieve all records"""
        return pd.read_csv(self.csv_file)


    def update_payment_status(self, transaction_id, status):
        """Update payment status"""
        df = pd.read_csv(self.csv_file)
        df.loc[df['transaction_id'] == transaction_id, 'payment_status'] = status
        df.to_csv(self.csv_file, index=False)