import webbrowser
from MeetLinks import google_calendar as calendarapi
import datetime

OPEN_BEFORE_X_MINUTES = 2

class OpenMeetLecture:
    def __init__(self, delta_time):
        self.delta_time = delta_time

    def get_meetings(self):
        meetings = calendarapi.GetMeetings(delta_time=self.delta_time)
        meetings_dict = meetings.get_next_meeting_details()
        return meetings_dict
    
    def check_past_or_future(self, start_time, meeting_link):
        current_time = datetime.datetime.utcnow() + datetime.delta(hours = 5, minutes = 30)
        if(abs(start_time - current_time) <= 2):
            webbrowser.open_new(meeting_link)
        elif(current_time > start_time):
            print(f"THE MEETING HAS ALREADY STARTED AND HAS PASSED {current_time - start_time}")
            print(f"DO YOU STILL WANT TO ATTEND THE MEETING")
            s = input("Yes or No")
            if(s[0].lower() == 'y'):
                webbrowser.open_new(meeting_link)
            else:
                print("GOOD CHOICE, ATTENDING LECTURE ISN'T FRUITFUL ANYWAYS")



if __name__ == "__main__":
    meetings = calendarapi.GetMeetings(delta_time=4)
    meetings_dict = meetings.get_next_meeting_details()
    print(meetings_dict)