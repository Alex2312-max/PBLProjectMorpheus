import datetime
from datetime import timedelta
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from registration.models import user_model
from django.http import HttpResponseRedirect
from .GeneticAlgorithmPlanner import GANPlanner
from .models import Schedule
from django.contrib.auth import get_user_model
from updatePage.models import UpdatePage

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

data = {"installed": {
        "client_id": "622523895311-jr2ob2h12cpb9j7cavudsrkbtd8i1009.apps.googleusercontent.com",
        "project_id": "quickstart-1607716584806", "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "nT8d5mHmzqPcsxDR9HRNo3I7",
        "redirect_uris": []}
    }

def filter_date(list_of_events):
    schedule = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    for event in list_of_events:
        schedule[int(event['start'].split('T')[1].split(':')[0])] = 0
        for i in range(int(event['start'].split('T')[1].split(':')[0]), int(event['end'].split('T')[1].split(':')[0])+1):
            try:
                schedule[i] = 0
            except IndexError:
                break
    return schedule

def task():
    print('start')
    users = get_user_model()
    users = users.objects.all()
    user_data = UpdatePage.objects.all()
    for i in range(1, len(users)):
        creds = pickle.loads(users[i].bin_data)
        user_bio_data = user_data[i-1]

        service = build('calendar', 'v3', credentials=creds)

        now = datetime.datetime.utcnow()
        now = now.replace(hour=0, minute=0, second=0)
        now += timedelta(1)
        now = now.isoformat() + 'Z'

        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        list_of_events = []
        if not events:
            print('No upcoming events found.')
        for event in events:
            list_of_events.append(
                {'start': event['start'].get('dateTime', event['start'].get('date')),
                 'end': event['end'].get('dateTime', event['end'].get('date')),
                 'summary': event['summary']}
            )
        day_schedule = filter_date(list_of_events)
        gap = GANPlanner('forest.obj', 'DSI.obj')
        generated_schedule = gap.generate(day_schedule, user_bio_data.weight / user_bio_data.height ** 2)
        slept_hours = sum(generated_schedule)
        print(generated_schedule)

        users = get_user_model()
        user = users.objects.all()[i - 1]

        new_schedule = Schedule(
            user=user,
            IDS=gap.ids,
            Sleep_Quality=gap.sleep_quality,
            Slept_hours=slept_hours,
            date=now.split('T')[0],
            hour0_Real=day_schedule[0],
            hour1_Real=day_schedule[1],
            hour2_Real=day_schedule[2],
            hour3_Real=day_schedule[3],
            hour4_Real=day_schedule[4],
            hour5_Real=day_schedule[5],
            hour6_Real=day_schedule[6],
            hour7_Real=day_schedule[7],
            hour8_Real=day_schedule[8],
            hour9_Real=day_schedule[9],
            hour10_Real=day_schedule[10],
            hour11_Real=day_schedule[11],
            hour12_Real=day_schedule[12],
            hour13_Real=day_schedule[13],
            hour14_Real=day_schedule[14],
            hour15_Real=day_schedule[15],
            hour16_Real=day_schedule[16],
            hour17_Real=day_schedule[17],
            hour18_Real=day_schedule[18],
            hour19_Real=day_schedule[19],
            hour20_Real=day_schedule[20],
            hour21_Real=day_schedule[21],
            hour22_Real=day_schedule[22],
            hour23_Real=day_schedule[23],
            hour0_Generated=generated_schedule[0],
            hour1_Generated=generated_schedule[1],
            hour2_Generated=generated_schedule[2],
            hour3_Generated=generated_schedule[3],
            hour4_Generated=generated_schedule[4],
            hour5_Generated=generated_schedule[5],
            hour6_Generated=generated_schedule[6],
            hour7_Generated=generated_schedule[7],
            hour8_Generated=generated_schedule[8],
            hour9_Generated=generated_schedule[9],
            hour10_Generated=generated_schedule[10],
            hour11_Generated=generated_schedule[11],
            hour12_Generated=generated_schedule[12],
            hour13_Generated=generated_schedule[13],
            hour14_Generated=generated_schedule[14],
            hour15_Generated=generated_schedule[15],
            hour16_Generated=generated_schedule[16],
            hour17_Generated=generated_schedule[17],
            hour18_Generated=generated_schedule[18],
            hour19_Generated=generated_schedule[19],
            hour20_Generated=generated_schedule[20],
            hour21_Generated=generated_schedule[21],
            hour22_Generated=generated_schedule[22],
            hour23_Generated=generated_schedule[23],
        )
        new_schedule.save()