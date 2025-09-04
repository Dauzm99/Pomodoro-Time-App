# services/google_calendar.py
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import settings

class GoogleCalendarService:
    def __init__(self):
        self.creds = None
        self._authenticate()

    def _authenticate(self):
        # ... (authentication code is unchanged)
        if os.path.exists(settings.TOKEN_PATH):
            self.creds = Credentials.from_authorized_user_file(settings.TOKEN_PATH, settings.API_SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    print(f"Token refresh failed: {e}. Re-authenticating.")
                    self.creds = None 
            
            if not self.creds:
                flow = InstalledAppFlow.from_client_secrets_file(settings.CREDENTIALS_PATH, settings.API_SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open(settings.TOKEN_PATH, 'w') as token:
                token.write(self.creds.to_json())
        
        try:
            self.service = build('calendar', 'v3', credentials=self.creds)
        except HttpError as e:
            print(f"An error occurred building the service: {e}")
            self.service = None

    def get_upcoming_events(self, max_results=15):
        # ... (get events code is unchanged)
        if not self.service: return []
            
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        try:
            events_result = self.service.events().list(
                calendarId='primary', timeMin=now,
                maxResults=max_results, singleEvents=True,
                orderBy='startTime'
            ).execute()
            return events_result.get('items', [])
        except HttpError as e:
            print(f"An error occurred fetching events: {e}")
            return []

    # RENAMED from create_event to be more specific
    def create_all_day_event(self, summary, date_str):
        if not self.service: return None
        event = {
            'summary': summary,
            'start': {'date': date_str},
            'end': {'date': date_str},
        }
        return self._execute_event_creation(event)

    # <<< NEW FUNCTION FOR TIMED EVENTS >>>
    def create_timed_event(self, summary, start_iso, end_iso):
        """Creates a timed event on the user's primary calendar."""
        if not self.service: return None
        event = {
            'summary': summary,
            'start': {'dateTime': start_iso, 'timeZone': str(datetime.datetime.now().astimezone().tzinfo)},
            'end': {'dateTime': end_iso, 'timeZone': str(datetime.datetime.now().astimezone().tzinfo)},
        }
        return self._execute_event_creation(event)

    def _execute_event_creation(self, event):
        try:
            created_event = self.service.events().insert(calendarId='primary', body=event).execute()
            print(f"Event created: {created_event.get('htmlLink')}")
            return created_event
        except HttpError as e:
            print(f"An error occurred creating the event: {e}")
            return None