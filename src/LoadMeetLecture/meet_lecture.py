import webbrowser
from MeetLinks import google_calendar as calendarapi


if __name__ == "__main__":
    meetings = calendarapi.GetMeetings(delta_time=4)
    meetings_dict = meetings.get_next_meeting_details()

    print(meetings_dict)