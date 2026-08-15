"""
Security Utilities Module
Provides centralized security functions for authentication, input validation,
data sanitization, rate limiting, and bot protection.
"""

import os
import hmac
import hashlib
import html
import time
import secrets
import logging
from typing import Tuple, Optional, Dict, Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 1. Password Hashing (PBKDF2 + SHA-256)
# ---------------------------------------------------------------------------

def hash_password(password: str, salt: Optional[bytes] = None) -> Tuple[str, str]:
    """
    Hash a password using PBKDF2-HMAC-SHA256 with a random salt.
    Returns (hashed_hex, salt_hex) tuple.
    """
    if salt is None:
        salt = secrets.token_bytes(32)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations=100_000)
    return dk.hex(), salt.hex()


def verify_password(password: str, stored_hash: str, salt_hex: str) -> bool:
    """
    Verify a password against a stored PBKDF2 hash using constant-time comparison.
    Returns True if password matches.
    """
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations=100_000)
    return hmac.compare_digest(dk.hex(), stored_hash)


# ---------------------------------------------------------------------------
# 2. Fail-Closed Admin Auth Check
# ---------------------------------------------------------------------------

def get_admin_credentials() -> Tuple[Optional[str], Optional[str]]:
    """
    Retrieve admin credentials from environment variables.
    Returns (username, password) or (None, None) if not configured.
    """
    user = os.getenv("ADMIN_USER")
    passwd = os.getenv("ADMIN_PASS")
    return user, passwd


def verify_admin_credentials(input_user: str, input_pass: str) -> bool:
    """
    Verify admin credentials using constant-time comparison.
    Implements FAIL-CLOSED: returns False if env vars are missing or empty.
    """
    env_user, env_pass = get_admin_credentials()

    # Fail-closed: if credentials are not configured, deny all access
    if not env_user or not env_pass:
        logger.warning("Admin credentials not configured in environment variables. Access denied (fail-closed).")
        return False

    # Prevent empty input from matching
    if not input_user or not input_pass:
        return False

    # Constant-time comparison to prevent timing attacks
    user_match = hmac.compare_digest(input_user.encode('utf-8'), env_user.encode('utf-8'))
    pass_match = hmac.compare_digest(input_pass.encode('utf-8'), env_pass.encode('utf-8'))

    return user_match and pass_match


# ---------------------------------------------------------------------------
# 3. Rate Limiting (Session-based login lockout)
# ---------------------------------------------------------------------------

MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_SECONDS = 300  # 5 minutes


def check_rate_limit(session_state: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Check if the user is rate-limited based on failed login attempts.
    Returns (is_allowed, message).
    """
    attempts = session_state.get('login_attempts', 0)
    lockout_time = session_state.get('lockout_until', 0)
    current_time = time.time()

    if lockout_time > current_time:
        remaining = int(lockout_time - current_time)
        return False, f"Account locked. Try again in {remaining} seconds."

    if attempts >= MAX_LOGIN_ATTEMPTS:
        session_state['lockout_until'] = current_time + LOCKOUT_DURATION_SECONDS
        session_state['login_attempts'] = 0
        return False, f"Too many failed attempts. Locked out for {LOCKOUT_DURATION_SECONDS // 60} minutes."

    return True, ""


def record_failed_login(session_state: Dict[str, Any]) -> int:
    """Record a failed login attempt and return total attempts."""
    attempts = session_state.get('login_attempts', 0) + 1
    session_state['login_attempts'] = attempts
    logger.warning(f"Failed login attempt #{attempts}")
    return attempts


def reset_login_attempts(session_state: Dict[str, Any]) -> None:
    """Reset login attempt counter on successful login."""
    session_state['login_attempts'] = 0
    session_state['lockout_until'] = 0


# ---------------------------------------------------------------------------
# 4. Bot Protection (Honeypot)
# ---------------------------------------------------------------------------

def verify_honeypot(honeypot_value: str) -> bool:
    """
    Honeypot bot detection: returns True if NOT a bot (honeypot is empty).
    Bots auto-fill hidden fields; legitimate users leave them blank.
    """
    if honeypot_value and honeypot_value.strip():
        logger.warning("Honeypot triggered — potential bot submission detected.")
        return False
    return True


# ---------------------------------------------------------------------------
# 5. HTML Sanitization (XSS Prevention)
# ---------------------------------------------------------------------------

def sanitize_html(text: str) -> str:
    """
    Escape HTML special characters to prevent XSS attacks.
    Applies multi-pass escaping via html.escape.
    """
    if text is None:
        return ""
    return html.escape(str(text), quote=True)


# ---------------------------------------------------------------------------
# 6. Input Validation (Schema + Bounds)
# ---------------------------------------------------------------------------

VALID_GENDERS = {"Female", "Male"}
VALID_YES_NO = {"Yes", "No"}
VALID_CONTRACTS = {"Month-to-month", "One year", "Two year"}
VALID_INTERNET = {"Fiber optic", "DSL", "No"}
VALID_PAYMENT_METHODS = {
    "Electronic check", "Mailed check",
    "Bank transfer (automatic)", "Credit card (automatic)"
}
VALID_MULTIPLE_LINES = {"No", "Yes", "No phone service"}
VALID_INTERNET_SERVICES = {"No", "Yes", "No internet service"}


def validate_prediction_input(data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validate all prediction input fields against allowed values and numerical bounds.
    Returns (is_valid, error_message).
    """
    # Gender validation
    gender = data.get('gender')
    if gender not in VALID_GENDERS:
        return False, f"Invalid gender value: '{sanitize_html(str(gender))}'. Allowed: {VALID_GENDERS}"

    # Yes/No field validation
    yes_no_fields = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']
    for field in yes_no_fields:
        val = data.get(field)
        if val not in VALID_YES_NO:
            return False, f"Invalid value for {field}: '{sanitize_html(str(val))}'. Allowed: Yes, No"

    # Contract validation
    contract = data.get('Contract')
    if contract not in VALID_CONTRACTS:
        return False, f"Invalid contract type: '{sanitize_html(str(contract))}'. Allowed: {VALID_CONTRACTS}"

    # Internet service validation
    internet = data.get('InternetService')
    if internet not in VALID_INTERNET:
        return False, f"Invalid internet service: '{sanitize_html(str(internet))}'. Allowed: {VALID_INTERNET}"

    # Payment method validation
    payment = data.get('PaymentMethod')
    if payment not in VALID_PAYMENT_METHODS:
        return False, f"Invalid payment method: '{sanitize_html(str(payment))}'"

    # Multiple lines validation
    ml = data.get('MultipleLines')
    if ml not in VALID_MULTIPLE_LINES:
        return False, f"Invalid multiple lines value: '{sanitize_html(str(ml))}'"

    # Internet-dependent service fields validation
    inet_service_fields = [
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies'
    ]
    for field in inet_service_fields:
        val = data.get(field)
        if val not in VALID_INTERNET_SERVICES:
            return False, f"Invalid value for {field}: '{sanitize_html(str(val))}'. Allowed: Yes, No, No internet service"

    # Numerical bounds validation
    tenure = data.get('tenure', 0)
    try:
        tenure = int(tenure)
    except (ValueError, TypeError):
        return False, "Tenure must be an integer."
    if tenure < 0 or tenure > 120:
        return False, "Tenure must be between 0 and 120 months."

    monthly = data.get('MonthlyCharges', 0.0)
    try:
        monthly = float(monthly)
    except (ValueError, TypeError):
        return False, "Monthly Charges must be a number."
    if monthly < 0.0 or monthly > 500.0:
        return False, "Monthly Charges must be between $0.0 and $500.0."

    total = data.get('TotalCharges', 0.0)
    try:
        total = float(total)
    except (ValueError, TypeError):
        return False, "Total Charges must be a number."
    if total < 0.0 or total > 50000.0:
        return False, "Total Charges must be between $0.0 and $50,000.0."

    return True, None


# ---------------------------------------------------------------------------
# 7. Data Hashing (SHA-256 for sensitive identifiers)
# ---------------------------------------------------------------------------

def hash_identifier(value: str) -> str:
    """
    Hash a sensitive identifier using SHA-256.
    Used for logging and audit trails without storing PII.
    """
    if not value:
        return ""
    return hashlib.sha256(value.encode('utf-8')).hexdigest()[:16]


# ---------------------------------------------------------------------------
# 8. File Upload Validation
# ---------------------------------------------------------------------------

MAX_UPLOAD_SIZE_MB = 10
ALLOWED_EXTENSIONS = {'.csv'}


def validate_file_upload(file_obj) -> Tuple[bool, Optional[str]]:
    """
    Validate uploaded file: check extension, size, and basic structure.
    Returns (is_valid, error_message).
    """
    if file_obj is None:
        return False, "No file uploaded."

    # Check file extension
    filename = getattr(file_obj, 'name', '')
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Invalid file type '{ext}'. Only .csv files are allowed."

    # Check file size
    file_size = getattr(file_obj, 'size', 0)
    max_bytes = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file_size > max_bytes:
        return False, f"File too large ({file_size / (1024*1024):.1f}MB). Maximum allowed: {MAX_UPLOAD_SIZE_MB}MB."

    return True, None


# ---------------------------------------------------------------------------
# 9. Path Traversal Protection
# ---------------------------------------------------------------------------

def safe_resolve_path(base_dir: str, requested_path: str) -> Optional[str]:
    """
    Safely resolve a file path ensuring it stays within base_dir.
    Prevents path traversal attacks (e.g., ../../etc/passwd).
    Returns the resolved path or None if traversal is detected.
    """
    base = os.path.realpath(base_dir)
    resolved = os.path.realpath(os.path.join(base_dir, requested_path))
    if not resolved.startswith(base + os.sep) and resolved != base:
        logger.warning(f"Path traversal attempt detected: {requested_path}")
        return None
    return resolved
