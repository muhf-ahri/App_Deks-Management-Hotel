# utils/helpers.py
from datetime import datetime
from utils.constants import SUCCESS, DANGER, WARNING, TEXT_DIM, TEXT

def fmt_currency(val):
    return f"Rp {val:,.0f}".replace(",", ".")

def days_between(d1, d2):
    try:
        return (datetime.strptime(d2, "%Y-%m-%d") - datetime.strptime(d1, "%Y-%m-%d")).days
    except Exception:
        return 0

def status_color(status):
    return {
        "Available":  SUCCESS,
        "Occupied":   DANGER,
        "Reserved":   WARNING,
        "Maintenance": TEXT_DIM,
        "Checked In": SUCCESS,
        "Checked Out": TEXT_DIM,
    }.get(status, TEXT)