from utils import send_sms
import re

def handle_temp_alert(alert, status):
    host = alert["labels"].get("host", "Unknown Host")
    
    if status == "resolved":
        return f"✅ Temperature Recovered\nHost: {host}\nTemperature back to normal."
    
    # Handle both formats
    if "values" in alert:
        temperature = alert["values"].get("B", "N/A")
    else:
        match = re.search(r"var='B'[^]]*value=([\d.]+)", alert.get("valueString", ""))
        temperature = match.group(1) if match else "N/A"

    try:
        temperature = round(float(temperature), 2) if temperature != "N/A" else "N/A"
    except (ValueError, TypeError):
        temperature = "N/A"

    return f"🌡️ Temp Alert\nHost: {host}\nTemperature: {temperature}°C"
