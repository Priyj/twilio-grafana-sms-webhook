import os
import re
import logging
from flask import Flask, request, jsonify
from config import TWILIO_TO_NUMBER
from utils import send_sms
from handle_temp_alert import handle_temp_alert
from handle_cpu_alert import handle_cpu_alert
from handle_ram_alert import handle_ram_alert
from handle_storage_alert import handle_storage_alert
from logging.handlers import RotatingFileHandler
app = Flask(__name__)
handler = RotatingFileHandler(
    '/var/log/sms_webhook.log',
    maxBytes=1000000,
    backupCount=3
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route('/sms', methods=['POST'])
def sms_alert():
    try:
        data = request.json
        print(f"Received alert: {data}")
    except Exception as e:
        print(f"Failed to parse JSON: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400

    try:
        alert = data["alerts"][0]
        labels = alert.get("labels", {})
        folder = labels.get("grafana_folder", "").lower()
        status = alert.get("status", "unknown")


        # Default fallback: parse summary/value from any alert
        def fallback_alert_parser(alert, status):
            host = labels.get("host", "Unknown host")
            value_string = alert.get("valueString", "")

            match = re.search(r"value=([\d.]+)", value_string)
            numeric_value = match.group(1) if match else "N/A"

            if status == "resolved":
                return f"✅ Alert resolved\nHost: {host}\nValue: {numeric_value}"
            else:
                summary = alert.get("annotations", {}).get("summary", "No summary provided")
                return f"{summary}\nHost: {host}\nValue: {numeric_value}"

        # Dispatch based on grafana_folder
        if folder == "temp sms":
            msg=handle_temp_alert(alert, status)
        elif folder == "cpu-lxc-sms":
            msg=handle_cpu_alert(alert, status)
        elif folder == "ram-lxc-sms":
            msg=handle_ram_alert(alert, status)
        elif folder == "storage-lxc-sms":
            msg=handle_storage_alert(alert, status)
        else:
            msg = fallback_alert_parser(alert, status)
        print("this was sent : ", msg)
        send_sms(msg)
    except Exception as e:
        msg = f"Failed to parse alert: {str(e)}"
        print(msg)
    return jsonify({"status": "received"}), 200

@app.route("/", methods=["GET"])
def home():
    return "Alert SMS Webhook is running."

@app.route('/health')
def health():
    try:
        return jsonify({
            "status": "healthy",
            "service": "SMS Webhook",
            "version": "1.0",
            "message": "Service is running normally"
        })
    except Exception as e:
        app.logger.error(f"Health check failed: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='172.16.10.16', port=port)
