from utils import send_sms
import re

def handle_storage_alert(alert, status):
    host = alert["labels"].get("host", "Unknown Host")
    
    if status == "resolved":
        return f"✅ Storage Recovered\nHost: {host}\nDisk usage back to normal."
    
    # Handle both formats
    if "values" in alert:
        storage_usage = alert["values"].get("B", "N/A")
    else:
        match = re.search(r"var='B'[^]]*value=([\d.]+)", alert.get("valueString", ""))
        storage_usage = match.group(1) if match else "N/A"

    try:
        storage_usage = round(float(storage_usage), 2) if storage_usage != "N/A" else "N/A"
    except (ValueError, TypeError):
        storage_usage = "N/A"

    return f"📦 Storage Alert\nHost: {host}\nUsage: {storage_usage}%"
