import pandas as pd
from typing import Dict, Any
from fpdf import FPDF
import io
from datetime import datetime

def generate_csv_report(input_data: Dict[str, Any], prediction_result: Dict[str, Any]) -> bytes:
    data = {}
    data.update(input_data)
    data.update(prediction_result)
    
    # Convert lists or dicts to strings
    for k, v in data.items():
        if isinstance(v, (dict, list)):
            data[k] = str(v)
            
    df = pd.DataFrame([data])
    csv_str = df.to_csv(index=False)
    return csv_str.encode('utf-8')

def generate_text_report(input_data: Dict[str, Any], prediction_result: Dict[str, Any]) -> str:
    prob = prediction_result.get('probability', 0.0)
    risk_level = prediction_result.get('risk_level', 'Unknown')
    pred_str = 'Likely to Churn' if prediction_result.get('prediction') == 1 else 'Likely to Stay'
    
    report = "".join([
        "======================================================================\n",
        "CUSTOMER CHURN DIAGNOSTIC REPORT\n",
        "======================================================================\n",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n",
        "CUSTOMER PROFILE:\n",
        "-----------------\n",
        f"  - Gender: {input_data.get('gender')}\n",
        f"  - Senior Citizen: {'Yes' if input_data.get('SeniorCitizen') == 1 else 'No'}\n",
        f"  - Partner: {input_data.get('Partner')}\n",
        f"  - Dependents: {input_data.get('Dependents')}\n",
        f"  - Tenure: {input_data.get('tenure')} months\n",
        f"  - Contract Type: {input_data.get('Contract')}\n",
        f"  - Paperless Billing: {input_data.get('PaperlessBilling')}\n",
        f"  - Payment Method: {input_data.get('PaymentMethod')}\n",
        f"  - Monthly Spend: ${input_data.get('MonthlyCharges', 0.0):.2f}\n",
        f"  - Total Spend: ${input_data.get('TotalCharges', 0.0):.2f}\n\n",
        "ACTIVE SERVICES:\n",
        "----------------\n",
        f"  - Phone Service: {input_data.get('PhoneService')}\n",
        f"  - Multiple Lines: {input_data.get('MultipleLines')}\n",
        f"  - Internet Service: {input_data.get('InternetService')}\n",
        f"  - Online Security: {input_data.get('OnlineSecurity')}\n",
        f"  - Online Backup: {input_data.get('OnlineBackup')}\n",
        f"  - Device Protection: {input_data.get('DeviceProtection')}\n",
        f"  - Tech Support: {input_data.get('TechSupport')}\n",
        f"  - Streaming TV: {input_data.get('StreamingTV')}\n",
        f"  - Streaming Movies: {input_data.get('StreamingMovies')}\n\n",
        "MODEL DIAGNOSTICS:\n",
        "------------------\n",
        f"  - Prediction Verdict: {pred_str}\n",
        f"  - Churn Probability: {prob:.2%}\n",
        f"  - Risk Classification: {risk_level.upper()}\n\n",
        "RECOMMENDED ACTIONS:\n",
        "--------------------\n"
    ])
    
    if risk_level.lower() == 'low':
        report += (
            "  - Maintain active service quality.\n"
            "  - Pitch premium service upgrades (e.g. streaming packs).\n"
            "  - Offer loyalty reward milestones.\n"
        )
    elif risk_level.lower() == 'medium':
        report += (
            "  - Recommend transition to automated payment channels (Auto-pay credit card/bank transfer).\n"
            "  - Monitor customer satisfaction metrics.\n"
            "  - Provide proactive health-check check-in call.\n"
        )
    elif risk_level.lower() == 'high':
        report += (
            "  - Incentivize long-term contract migration (Transition from month-to-month to annual plan).\n"
            "  - Apply retention promotional discounts to lower billing friction.\n"
            "  - Flag for direct loyalty support team outreach.\n"
        )
    else:
        report += (
            "  - Deploy emergency executive customer support callback.\n"
            "  - Offer immediate service billing credit or custom plan downgrade.\n"
            "  - Bundle premium online security/tech support for free to anchor customer.\n"
        )
        
    report += "\n======================================================================\n"
    return report

class ChurnPDFReport(FPDF):
    def header(self):
        self.set_fill_color(108, 99, 255)
        self.rect(0, 0, 210, 8, 'F')
        self.ln(10)
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(26, 29, 46)
        self.cell(0, 10, 'CUSTOMER CHURN RISK ANALYSIS', ln=True, align='L')
        self.set_font('Helvetica', '', 10)
        self.set_text_color(108, 117, 125)
        self.cell(0, 5, 'Predictive Churn Risk Analytics Report - Machine Learning Portfolio Project', ln=True, align='L')
        self.ln(5)
        self.set_draw_color(233, 236, 239)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(108, 117, 125)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_pdf_report(input_data: Dict[str, Any], prediction_result: Dict[str, Any]) -> bytes:
    prob = prediction_result.get('probability', 0.0)
    risk_level = prediction_result.get('risk_level', 'Unknown')
    pred_str = 'Likely to Churn' if prediction_result.get('prediction') == 1 else 'Likely to Stay'
    
    pdf = ChurnPDFReport()
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(26, 29, 46)
    pdf.cell(0, 8, 'Risk Assessment Summary', ln=True)
    pdf.ln(2)
    
    if risk_level.lower() == 'low':
        pdf.set_fill_color(40, 167, 69)
        txt_color = (255, 255, 255)
    elif risk_level.lower() == 'medium':
        pdf.set_fill_color(255, 193, 7)
        txt_color = (0, 0, 0)
    elif risk_level.lower() == 'high':
        pdf.set_fill_color(255, 128, 0)
        txt_color = (255, 255, 255)
    else: # Critical
        pdf.set_fill_color(220, 53, 69)
        txt_color = (255, 255, 255)
        
    pdf.rect(10, pdf.get_y(), 190, 20, 'F')
    pdf.set_text_color(*txt_color)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_y(pdf.get_y() + 4)
    pdf.cell(10, 5) # padding
    pdf.cell(90, 5, f'Risk Verdict: {risk_level.upper()} RISK ({pred_str})', ln=False)
    pdf.cell(80, 5, f'Churn Probability: {prob:.2%}', ln=True, align='R')
    
    pdf.ln(12)
    pdf.set_text_color(26, 29, 46)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(95, 8, 'Customer & Financial Profile', ln=False)
    pdf.cell(95, 8, 'Subscribed Services', ln=True)
    pdf.ln(2)
    
    pdf.set_font('Helvetica', '', 10)
    start_y = pdf.get_y()
    
    # Left Column
    pdf.set_x(10)
    pdf.cell(40, 6, 'Gender:', ln=False)
    pdf.cell(50, 6, f"{input_data.get('gender')}", ln=True)
    
    pdf.cell(40, 6, 'Senior Citizen:', ln=False)
    pdf.cell(50, 6, 'Yes' if input_data.get('SeniorCitizen') == 1 else 'No', ln=True)
    
    pdf.cell(40, 6, 'Partner & Dependents:', ln=False)
    pdf.cell(50, 6, f"{input_data.get('Partner')} / {input_data.get('Dependents')}", ln=True)
    
    pdf.cell(40, 6, 'Tenure:', ln=False)
    pdf.cell(50, 6, f"{input_data.get('tenure')} months", ln=True)
    
    pdf.cell(40, 6, 'Contract Type:', ln=False)
    pdf.cell(50, 6, f"{input_data.get('Contract')}", ln=True)
    
    pdf.cell(40, 6, 'Payment Channel:', ln=False)
    pdf.cell(50, 6, f"{input_data.get('PaymentMethod')}", ln=True)
    
    pdf.cell(40, 6, 'Monthly Charges:', ln=False)
    pdf.cell(50, 6, f"${input_data.get('MonthlyCharges', 0.0):.2f}", ln=True)
    
    pdf.cell(40, 6, 'Total Charges:', ln=False)
    pdf.cell(50, 6, f"${input_data.get('TotalCharges', 0.0):.2f}", ln=True)
    
    end_y_1 = pdf.get_y()
    
    # Right Column
    pdf.set_y(start_y)
    pdf.set_x(105)
    pdf.cell(40, 6, 'Phone Service:', ln=False)
    pdf.cell(50, 6, f"{input_data.get('PhoneService')} ({input_data.get('MultipleLines')})", ln=True)
    
    pdf.set_x(105)
    pdf.cell(40, 6, 'Internet Service:', ln=False)
    pdf.cell(50, 6, f"{input_data.get('InternetService')}", ln=True)
    
    pdf.set_x(105)
    pdf.cell(40, 6, 'Online Security:', ln=False)
    pdf.cell(50, 6, f"{input_data.get('OnlineSecurity')}", ln=True)
    
    pdf.set_x(105)
    pdf.cell(40, 6, 'Online Backup:', ln=False)
    pdf.cell(50, 6, f"{input_data.get('OnlineBackup')}", ln=True)
    
    pdf.set_x(105)
    pdf.cell(40, 6, 'Device Protection:', ln=False)
    pdf.cell(50, 6, f"{input_data.get('DeviceProtection')}", ln=True)
    
    pdf.set_x(105)
    pdf.cell(40, 6, 'Tech Support:', ln=False)
    pdf.cell(50, 6, f"{input_data.get('TechSupport')}", ln=True)
    
    pdf.set_x(105)
    pdf.cell(40, 6, 'Streaming TV / Movies:', ln=False)
    pdf.cell(50, 6, f"{input_data.get('StreamingTV')} / {input_data.get('StreamingMovies')}", ln=True)
    
    end_y_2 = pdf.get_y()
    
    pdf.set_y(max(end_y_1, end_y_2) + 8)
    
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Recommended Retention Strategy', ln=True)
    pdf.ln(2)
    
    pdf.set_font('Helvetica', '', 10)
    
    recs = []
    if risk_level.lower() == 'low':
        recs = [
            'Maintain active service quality check-ins.',
            'Upsell premium value packages like high-speed options or movie subscriptions.',
            'Establish loyalty milestone rewards program inputs.'
        ]
    elif risk_level.lower() == 'medium':
        recs = [
            'Provide switch to automated payment incentive (e.g. $5 monthly billing credit).',
            'Establish tech health check calls to confirm reliable line connectivity.',
            'Proactively resolve billing issues via early check-ins.'
        ]
    elif risk_level.lower() == 'high':
        recs = [
            'Target with contract migration incentives (Transition from month-to-month to annual plan).',
            'Offer a monthly billing discount package (e.g., 10-15% deduction for 12 months).',
            'Establish prioritized call list queue for high-touch care agent support.'
        ]
    else: # Critical
        recs = [
            'Initiate immediate customer success callbacks.',
            'Apply high-priority retention promotions and custom lower-cost packaging.',
            'Bundle essential premium tech support and online security at no charge.'
        ]
        
    for r in recs:
        pdf.cell(5)
        pdf.cell(0, 6, f"- {r}", ln=True)
        
    pdf.ln(10)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 6, 'This analysis is produced by the Customer Churn Prediction Engine and is confidential.', align='C')
    
    pdf_bytes = pdf.output(dest='S')
    if isinstance(pdf_bytes, bytearray):
        pdf_bytes = bytes(pdf_bytes)
    return pdf_bytes
