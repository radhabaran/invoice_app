# workflow.py

from langgraph.graph import StateGraph
from datetime import datetime, timedelta
import uuid

class WorkflowManager:
    def __init__(self, data_manager, invoice_generator, email_handler):
        self.data_manager = data_manager
        self.invoice_generator = invoice_generator
        self.email_handler = email_handler
        self.graph = self.setup_workflow()


    def setup_workflow(self):
        """Setup LangGraph workflow"""
        workflow = StateGraph()
        
        workflow.add_node("validate", self.validate_step)
        workflow.add_node("generate_invoice", self.generate_invoice_step)
        workflow.add_node("send_notification", self.send_notification_step)
        
        return workflow


    def validate_step(self, state):
        """Validation step"""
        if self.data_manager.check_duplicate(state['cust_unique_id']):
            return {"valid": False, "error": "Duplicate customer ID"}
        return {"valid": True}


    def generate_invoice_step(self, state):
        """Invoice generation step"""
        state['transaction_id'] = str(uuid.uuid4())[:8]
        state['transaction_date'] = datetime.now().strftime('%m-%d-%Y')
        state['payment_due_date'] = (datetime.now() + timedelta(days=30)).strftime('%m-%d-%Y')
        state['payment_status'] = 'pending'
        
        invoice_path = self.invoice_generator.generate_invoice(state)
        return {"invoice_path": invoice_path}


    def send_notification_step(self, state):
        """Email notification step"""
        email_sent = self.email_handler.send_invoice(
            state['cust_email'],
            state,
            state['invoice_path']
        )
        return {"email_sent": email_sent}


    def run_workflow(self, data):
        """Execute complete workflow"""
        state = data.copy()
        
        # Run validation
        validation_result = self.validate_step(state)
        if not validation_result['valid']:
            return validation_result

        # Generate invoice
        invoice_result = self.generate_invoice_step(state)
        state.update(invoice_result)

        # Send notification
        notification_result = self.send_notification_step(state)
        state.update(notification_result)

        # Save to database
        self.data_manager.save_record(state)

        return state