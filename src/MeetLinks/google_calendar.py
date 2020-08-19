from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time
import pytz
from pprint import pprint
from datetime import date
import os
# import pyttsx3


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GetMeetings:
    def __init__(self, delta_time):
        self.delta_time = delta_time        
        
    def initiate_credentials(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.environ("DESKTOP_CREDENTIALS"), SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def get_next_meeting_details(self):
        creds = self.initiate_credentials()
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        now_plus_window = (datetime.datetime.utcnow() + datetime.timedelta(hours=delta_time)).isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=now_plus_window,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if len(events) == 0:
            print('No upcoming events found.')
        for event in events:
            start_time = datetime.datetime.fromisoformat(event['start'].get('dateTime')[:-1])
            # print(start_time + datetime.timedelta(hours = 5, minutes = 30))
            meeting_link = event.get('hangoutLink')
            if meeting_link and self.is_time_in_future(start_time):
                return {'meeting_link': meeting_link,
                # Convert the time from UTC to IST
                        'start_time': start_time + datetime.timedelta(hours = 5, minutes = 30),
                        'meeting_name': event.get('summary')}
        return {}

    def is_time_in_future(self, time_to_check):
        # print(datetime.datetime.utcnow())
        return time_to_check > datetime.datetime.utcnow()

    def open_meeting_in_browser(self, meeting_link):
        print(f"Initiating meeting {meeting_link}")
        webbrowser.open(meeting_link)

    def get_secs_till_next_meeting(self, meeting_start_time):
        if meeting_start_time:
            return (meeting_start_time - datetime.datetime.utcnow().replace(tzinfo=pytz.utc) -
                datetime.timedelta(minutes=OPEN_MEETING_MINUTES_BEFORE)).seconds
        return SLEEP_WINDOW_SECS + 10

    # def alert_on_meeting(meeting_name):
    #     alert_message = f"{meeting_name} will start in {OPEN_MEETING_MINUTES_BEFORE} minutes"
    #     speech_engine.say(alert_message)
    #     speech_engine.runAndWait()

    # def main():
    #     meeting_should_be_shown_soon = False
    #     meeting_link = None
    #     secs_till_next_meeting = SLEEP_WINDOW_SECS + 10
    #     meeting_name = ''

    #     while True:
    #         # showing the next meeting
    #         if meeting_should_be_shown_soon and meeting_link:
    #             open_meeting_in_browser(meeting_link)
    #             meeting_should_be_shown_soon = False
    #             meeting_link = None
    #             alert_on_meeting(meeting_name)
    #             meeting_name = ''
    #         # getting the next meeting
    #         else:
    #             meeting_details = get_next_meeting_details()
    #             meeting_link = meeting_details.get('meeting_link')
    #             meeting_start_time = meeting_details.get('start_time')
    #             meeting_name = meeting_details.get('meeting_name')
    #             secs_till_next_meeting = get_secs_till_next_meeting(meeting_start_time)
    #         if SLEEP_WINDOW_SECS > secs_till_next_meeting:
    #             meeting_should_be_shown_soon = True
    #         time.sleep(min(SLEEP_WINDOW_SECS, secs_till_next_meeting))

if __name__ == '__main__':
    obj = GetMeetings()
    dict = obj.get_next_meeting_details()
    pprint(dict)