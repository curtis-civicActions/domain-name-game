import os
import gspread
from google.oauth2 import service_account
from flask_mongoengine import MongoEngine

db = MongoEngine()

_google_service_client = None

def init_google_service_client(app):
    global _google_service_client
    creds_path = app.config.get('GOOGLE_CREDENTIALS_PATH')
    scopes = app.config.get('GOOGLE_SHEETS_SCOPES')

    # Load credentials from service account file
    credentials = service_account.Credentials.from_service_account_file(
        creds_path,
        scopes=scopes
    )

    # Build the service
    _google_service_client = gspread.authorize(credentials)
    return _google_service_client

def get_google_service_client():
    if _google_service_client is None:
        raise RuntimeError("Google service has not been initialized. Call init_google_service(app) first.")
    return _google_service_client