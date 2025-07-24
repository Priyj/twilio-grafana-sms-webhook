# Twilio Grafana SMS Webhook

This project is a **Flask-based webhook service** that integrates **Grafana alerts with Twilio SMS notifications**. It processes different types of alerts (CPU, RAM, Storage, Temperature) and sends formatted SMS messages to configured recipients.

---

## **Project Structure**

.    
├── main.py            
├── sms_webhook.py        
├── handle_cpu_alert.py    
├── handle_ram_alert.py    
├── handle_storage_alert.py    
├── handle_temp_alert.py    
├── utils.py    
├── config.py    
├── test.py    
├── requirements.txt    
└── .gitignore    

- **main.py** – Starts FastAPI app including sms_webhook routes  
- **sms_webhook.py** – Flask app with `/sms` endpoint to process and route alerts  
- **handle_*.py** – Alert handlers for CPU, RAM, Storage, Temperature alerts  
- **utils.py** – Twilio SMS sending logic  
- **config.py** – Stores Twilio credentials and recipient numbers  
- **test.py** – Quick test script to send an SMS  
- **requirements.txt** – Python dependencies  
- **.gitignore** – Ignores venv, pycache, and env files

---

## **Setup**

### **1. Clone the repository**

```bash
git clone https://github.com/Priyj/twilio-grafana-sms-webhook.git
cd twilio-grafana-sms-webhook
2. Create a virtual environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Configure Twilio credentials
Edit config.py with your Twilio account details:

python
Copy
Edit
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_FROM_NUMBER = '+1234567890'
TWILIO_TO_NUMBER = [
    "+19876543210",
    "+10987654321",
]
Tip: For production, use environment variables instead of hardcoded credentials.

Running the Webhook Service
Start the Flask app

python sms_webhook.py

The service will run and expose:

POST /sms – Receives Grafana alert JSON payloads

GET / – Health check page

GET /health – Returns service health status JSON

Testing SMS functionality
Run:

bash
Copy
Edit
python test.py
This sends a test SMS to configured recipients to validate integration.

Integrating with Grafana
Set up a Webhook contact point in Grafana.

Point it to your server’s /sms endpoint URL.

Alerts will be parsed by their grafana_folder label and routed to respective handlers.

Security Note
Do not commit secrets in public repos.

Rotate your Twilio credentials if accidentally pushed.

Secure your webhook endpoint with IP filtering or auth if exposed publicly.


Contributions
Pull requests and suggestions are welcome to enhance alert parsing and security.
