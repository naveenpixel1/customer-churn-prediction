from typing import Tuple, Optional

def validate_numeric_inputs(tenure: int, monthly_charges: float, total_charges: float) -> Tuple[bool, Optional[str]]:
    if tenure < 0 or tenure > 120:
        return False, 'Tenure must be between 0 and 120 months.'
        
    if monthly_charges < 0.0 or monthly_charges > 500.0:
        return False, 'Monthly Charges must be between $0.0 and $500.0.'
        
    if total_charges < 0.0 or total_charges > 50000.0:
        return False, 'Total Charges must be between $0.0 and $50000.0.'
        
    if tenure == 0 and total_charges != 0.0:
        return False, 'Total Charges must be 0.0 for new customers (tenure = 0).'
        
    return True, None
