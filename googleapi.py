import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Google Calendar API setup
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_google_calendar_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service

# Add a task as an event to Google Calendar
def add_task_to_calendar(service, task_name, task_priority, task_deadline, task_duration):
    event = {
        'summary': f"Task: {task_name} (Priority: {task_priority})",
        'description': f"Priority: {task_priority}",
        'start': {
            'dateTime': task_deadline.isoformat(),
            'timeZone': 'America/New_York',  # Set your time zone here
        },
        'end': {
            'dateTime': (task_deadline + datetime.timedelta(hours=task_duration)).isoformat(),
            'timeZone': 'YOUR_TIME_ZONE',  # Set your time zone here
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Task '{task_name}' added to Google Calendar.")

def main():
    service = get_google_calendar_service()
    
    task_name = input("Enter task name: ")
    task_priority = int(input("Enter task priority (1 to 10): "))
    task_deadline = datetime.datetime.strptime(input("Enter task deadline (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
    task_duration = float(input("Enter task duration in hours: "))
    
    add_task_to_calendar(service, task_name, task_priority, task_deadline, task_duration)

if __name__ == "__main__":
    main()