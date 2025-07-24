from twilio.rest import Client
import config
import os

client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

def send_sms(message):
    recipients = config.TWILIO_TO_NUMBER  
    for number in recipients:
        client.messages.create(
            body=message,
            from_=config.TWILIO_FROM_NUMBER,
            to=number
        )
