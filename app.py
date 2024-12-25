# app.py

import streamlit as st
from modules.data_manager import DataManager
from modules.invoice_gen import InvoiceGenerator
from modules.email_handler import EmailHandler
from modules.validator import DataValidator
from modules.workflow import WorkflowManager


def init_systems():
    """Initialize all system components"""
    data_manager = DataManager()
    invoice_generator = InvoiceGenerator()
    email_handler = EmailHandler()
    workflow_manager = WorkflowManager(data_manager, invoice_generator, email_handler)
    return workflow_manager


def main():
    st.title("Invoice Management System")

    # Initialize
    workflow_manager = init_systems()

    # Customer Information Section
    st.header("Customer Information")
    cust_unique_id = st.text_input("Customer Unique ID*")
    cust_tax_id = st.text_input("Customer Tax ID*")
    cust_fname = st.text_input("First Name", value="na")
    cust_lname = st.text_input("Last Name", value="na")
    cust_email = st.text_input("Customer Email*")

    # Invoice Details Section
    st.header("Invoice Details")
    billed_amount = st.number_input("Billed Amount*", min_value=0.0)
    currency = st.selectbox("Currency*", ["USD", "EUR", "GBP", "JPY"])

    if st.button("Generate Invoice"):
        # Collect data
        data = {
            'cust_unique_id': cust_unique_id,
            'cust_tax_id': cust_tax_id,
            'cust_fname': cust_fname,
            'cust_lname': cust_lname,
            'cust_email': cust_email,
            'billed_amount': billed_amount,
            'currency': currency
        }

        # Validate
        errors = DataValidator.validate_customer_data(data)
        if errors:
            for error in errors:
                st.error(error)
            return

        # Process
        result = workflow_manager.run_workflow(data)
        
        if result.get('error'):
            st.error(result['error'])
        else:
            st.success(f"Invoice generated and sent to {cust_email}")
            st.info(f"Transaction ID: {result['transaction_id']}")

if __name__ == "__main__":
    main()