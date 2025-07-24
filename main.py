from fastapi import FastAPI, Request
from sms_webhook import router as sms_router

app = FastAPI()

app.include_router(sms_router)
