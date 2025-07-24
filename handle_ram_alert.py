from utils import send_sms
import re

def handle_ram_alert(alert, status):
    host = alert["labels"].get("host", "Unknown Host")
    
    if status == "resolved":
        return f"✅ RAM Recovered\nHost: {host}\nMemory usage back to normal."
    
    # Handle both formats
    if "values" in alert:
        ram_usage = alert["values"].get("B", "N/A")
    else:
        match = re.search(r"var='B'[^]]*value=([\d.]+)", alert.get("valueString", ""))
        ram_usage = match.group(1) if match else "N/A"

    try:
        ram_usage = round(float(ram_usage), 2) if ram_usage != "N/A" else "N/A"
    except (ValueError, TypeError):
        ram_usage = "N/A"

    return f"💾 RAM Alert\nHost: {host}\nUsage: {ram_usage}%"
