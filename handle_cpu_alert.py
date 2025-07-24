from utils import send_sms
import re

def handle_cpu_alert(alert, status):
    host = alert["labels"].get("host", "Unknown Host")
    value_string = alert.get("valueString", "")

    if status == "resolved":
        return f"✅ CPU Recovered\nHost: {host}\nCPU usage back to normal."
    
    # Handle both old and new Grafana formats
    if "values" in alert:  # New format
        b_value = alert["values"].get("B", "N/A")
        c_value = alert["values"].get("C", "N/A")
    else:  # Old format
        b_match = re.search(r"var='B'[^]]*value=([\d.]+)", value_string)
        c_match = re.search(r"var='C'[^]]*value=([\d.]+)", value_string)
        b_value = b_match.group(1) if b_match else "N/A"
        c_value = c_match.group(1) if c_match else "N/A"

    try:
        b_value = round(float(b_value), 2) if b_value != "N/A" else "N/A"
        c_value = round(float(c_value), 2) if c_value != "N/A" else "N/A"
    except (ValueError, TypeError):
        b_value = c_value = "N/A"

    return f"🔥 CPU Alert\nHost: {host}\nUsage: {b_value}%"
