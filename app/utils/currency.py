"""
Currency Localization & Conversion Utility
Provides real-time currency formatting, conversion rates, and global currency selector.
Default currency is Indian Rupee (₹ - INR).
"""

import streamlit as st
from typing import Dict, Any

CURRENCY_CONFIG: Dict[str, Dict[str, Any]] = {
    "INR": {
        "symbol": "₹",
        "name": "🇮🇳 Indian Rupee (INR)",
        "rate": 83.0,
        "symbol_first": True,
        "format": "₹{:,.2f}",
        "format_int": "₹{:,.0f}"
    },
    "USD": {
        "symbol": "$",
        "name": "🇺🇸 US Dollar (USD)",
        "rate": 1.0,
        "symbol_first": True,
        "format": "${:,.2f}",
        "format_int": "${:,.0f}"
    },
    "EUR": {
        "symbol": "€",
        "name": "🇪🇺 Euro (EUR)",
        "rate": 0.92,
        "symbol_first": True,
        "format": "€{:,.2f}",
        "format_int": "€{:,.0f}"
    },
    "GBP": {
        "symbol": "£",
        "name": "🇬🇧 British Pound (GBP)",
        "rate": 0.79,
        "symbol_first": True,
        "format": "£{:,.2f}",
        "format_int": "£{:,.0f}"
    },
    "AED": {
        "symbol": "AED ",
        "name": "🇦🇪 UAE Dirham (AED)",
        "rate": 3.67,
        "symbol_first": True,
        "format": "AED {:,.2f}",
        "format_int": "AED {:,.0f}"
    },
    "SGD": {
        "symbol": "S$",
        "name": "🇸🇬 Singapore Dollar (SGD)",
        "rate": 1.35,
        "symbol_first": True,
        "format": "S${:,.2f}",
        "format_int": "S${:,.0f}"
    },
    "CAD": {
        "symbol": "C$",
        "name": "🇨🇦 Canadian Dollar (CAD)",
        "rate": 1.36,
        "symbol_first": True,
        "format": "C${:,.2f}",
        "format_int": "C${:,.0f}"
    },
    "JPY": {
        "symbol": "¥",
        "name": "🇯🇵 Japanese Yen (JPY)",
        "rate": 155.0,
        "symbol_first": True,
        "format": "¥{:,.0f}",
        "format_int": "¥{:,.0f}"
    }
}

DEFAULT_CURRENCY = "INR"

def get_active_currency() -> str:
    """Returns the currently active currency code (default: INR)."""
    if "active_currency" not in st.session_state:
        st.session_state["active_currency"] = DEFAULT_CURRENCY
    return st.session_state["active_currency"]

def get_currency_symbol() -> str:
    """Returns the active currency symbol (e.g. ₹, $, €)."""
    curr = get_active_currency()
    return CURRENCY_CONFIG.get(curr, CURRENCY_CONFIG[DEFAULT_CURRENCY])["symbol"]

def get_currency_rate() -> float:
    """Returns the active currency exchange rate relative to baseline USD."""
    curr = get_active_currency()
    return CURRENCY_CONFIG.get(curr, CURRENCY_CONFIG[DEFAULT_CURRENCY])["rate"]

def convert_amount(amount_usd: float) -> float:
    """Converts a baseline USD amount into the active currency."""
    return float(amount_usd) * get_currency_rate()

def format_currency(amount_usd: float, include_symbol: bool = True, decimals: int = 2) -> str:
    """
    Converts and formats a monetary amount according to active currency settings.
    Example: 95.0 USD -> ₹7,885.00
    """
    curr = get_active_currency()
    cfg = CURRENCY_CONFIG.get(curr, CURRENCY_CONFIG[DEFAULT_CURRENCY])
    converted = float(amount_usd) * cfg["rate"]
    
    if not include_symbol:
        if decimals == 0 or curr == "JPY":
            return f"{converted:,.0f}"
        return f"{converted:,.{decimals}f}"
        
    if decimals == 0 or curr == "JPY":
        return cfg["format_int"].format(converted)
    return cfg["format"].format(converted)

def render_currency_selector() -> None:
    """
    Renders an interactive currency selector widget in the sidebar.
    Allows users to switch between INR (default), USD, EUR, GBP, AED, SGD, CAD, JPY.
    """
    current_curr = get_active_currency()
    options = list(CURRENCY_CONFIG.keys())
    
    curr_index = options.index(current_curr) if current_curr in options else 0
    
    st.sidebar.markdown('<div style="margin-top: 10px;"></div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        '<span style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748B; letter-spacing: 0.5px;">💱 Currency Localization</span>', 
        unsafe_allow_html=True
    )
    selected_curr = st.sidebar.selectbox(
        "Display Currency",
        options=options,
        index=curr_index,
        format_func=lambda code: CURRENCY_CONFIG[code]["name"],
        key="currency_select_box",
        label_visibility="collapsed"
    )
    
    if selected_curr != current_curr:
        st.session_state["active_currency"] = selected_curr
        st.rerun()
