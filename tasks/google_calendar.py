from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.conf import settings
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_flow():
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/oauth/callback/'
    )
    flow.autogenerate_code_verifier = True
    return flow

def get_service(token_data):
    creds = Credentials(
        token=token_data['token'],
        refresh_token=token_data['refresh_token'],
        token_uri='https://oauth2.googleapis.com/token',
        client_id=token_data['client_id'],
        client_secret=token_data['client_secret'],
    )
    return build('calendar', 'v3', credentials=creds)

def get_busy_slots(service, days=7):
    from datetime import datetime, timedelta, timezone
    now = datetime.now(timezone.utc)
    body = {
        'timeMin': now.isoformat(),
        'timeMax': (now + timedelta(days=days)).isoformat(),
        'items': [{'id': 'primary'}]
    }
    result = service.freebusy().query(body=body).execute()
    return result['calendars']['primary']['busy']

def create_event(service, title, start_time, end_time):
    event = {
        'summary': title,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Tokyo'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Tokyo'},
    }
    return service.events().insert(calendarId='primary', body=event).execute()