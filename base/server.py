import http.server
import socketserver
import json
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/add_event':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            event = json.loads(post_data.decode('utf-8'))

            # Add event to the event list
            event_list.append(event)
            print("Received event:", event)

            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')



# Create an empty list to store received events
event_list = []

# Priority mapping: Assign numerical values to priorities
priority_mapping = {
    "high": 1,
    "medium": 2,
    "low": 3,
}

# Function to calculate event priority value
def calculate_priority_value(event):
    return priority_mapping.get(event['priority'], 3)

# Initialize Google Calendar API
def initialize_google_calendar():
    credentials = service_account.Credentials.from_service_account_file(
        'client_secret_19769659267-tfiqfr1hpu9l1jm4600i6nbimncelgr0.apps.googleusercontent.com.json', scopes=['https://www.googleapis.com/auth/calendar']
    )
    service = build('calendar', 'v3', credentials=credentials)
    return service

# Retrieve available time slots from Google Calendar
def get_free_time_slots(service, start_datetime, end_datetime):
    events = service.events().list(
        calendarId='primary',
        timeMin=start_datetime.isoformat() + 'Z',
        timeMax=end_datetime.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime',
    ).execute()

    # Extract existing event start and end times
    busy_times = []
    for event in events.get('items', []):
        start_time = event['start']['dateTime']
        end_time = event['end']['dateTime']
        busy_times.append((start_time, end_time))

    # Calculate free time slots
    free_time_slots = []
    current_time = start_datetime
    for start, end in sorted(busy_times):
        if current_time < datetime.fromisoformat(start):
            free_time_slots.append((current_time, datetime.fromisoformat(start)))
        current_time = datetime.fromisoformat(end)

    if current_time < end_datetime:
        free_time_slots.append((current_time, end_datetime))

    return free_time_slots

# Schedule events into free time slots
def schedule_events(events, free_time_slots):
    scheduled_events = []
    for event in events:
        for start, end in free_time_slots:
            if event['deadline'] <= end.isoformat() and calculate_priority_value(event) <= calculate_priority_value(scheduled_events[-1]):
                event['start'] = {
                    'dateTime': start.isoformat(),
                    'timeZone': 'Your-Timezone',
                }
                event['end'] = {
                    'dateTime': (start + timedelta(hours=2)).isoformat(),  # Adjust event duration as needed
                    'timeZone': 'Your-Timezone',
                }
                scheduled_events.append(event)
                break
    return scheduled_events

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        event = json.loads(post_data.decode('utf-8'))
        event_list.append(event)
        print("Received event:", event)

        # Sort the event list based on deadline and priority
        event_list.sort(key=lambda x: (x['deadline'], calculate_priority_value(x)))

        # Initialize Google Calendar API
        service = initialize_google_calendar()

        # Define the time range for free time slots (adjust as needed)
        start_datetime = datetime.now()
        end_datetime = start_datetime + timedelta(days=7)  # Look for free time slots for the next 7 days

        # Retrieve free time slots
        free_time_slots = get_free_time_slots(service, start_datetime, end_datetime)

        # Schedule events into free time slots
        scheduled_events = schedule_events(event_list, free_time_slots)

        # Add scheduled events to Google Calendar
        for event in scheduled_events:
            event = service.events().insert(calendarId='primary', body=event).execute()
            print("Scheduled event:", event)


# Start a simple HTTP server
PORT = 8000

with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print("Python server listening on port", PORT)
    httpd.serve_forever()
