from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import time

from apiclient import discovery
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError
import pandas as pd

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/drive'
]



SPREED_SHEETS_ID = '1_q_nfruEGkjPxhL53uwuLGM7YIZlHlGvp-KJ3yALBkQ'
CALENDAR_ID = '8b472d96c37bc493132343832aeb43f5345b5a7d2f282bf36d0e2631d5374d99@group.calendar.google.com'

CREDENTIALS_FILE = 'keys.json'
CREDENTIALS = Credentials.from_service_account_file(filename=CREDENTIALS_FILE, scopes=SCOPES)

sheets_service = discovery.build('sheets', 'v4', credentials=CREDENTIALS)
calendar_service = discovery.build('calendar', 'v3', credentials=CREDENTIALS)


def read_google_sheet(spreadsheet_id, range_name):
    try:
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        return values

    except HttpError as error:
        print(f"Произошла ошибка: {error}")
        return []
    

def parse_events(df):
    events = []
    df.columns = df.iloc[0]
    for _, row in df.iterrows():
        name = row['название']
        if not row['название'] or name == 'название':
            continue
        date_str = row['дата'].replace(".", "-")
        # date_format(date_str)
        start_time = row['начало']
        end_time = row['конец']
        if all([name, date_str, start_time]):
            events.append([name, date_str, start_time, end_time])
    return events


def create_calendar_event(
    summary: str,
    date: str,
    start_time: str,
    end_time: str = None,
    calendar_id: str = 'primary'
):
    timezone: str = 'Europe/Moscow',
    try:
        start_dt = datetime.strptime(f"{date} {start_time}", "%d-%m-%Y %H:%M")
        if end_time:
            end_dt = datetime.strptime(f"{date} {end_time}", "%d-%m-%Y %H:%M")
        else:
            end_dt = start_dt + timedelta(minutes=90)
        
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_dt.isoformat(),
                'timeZone': timezone
            },
            'end': {
                'dateTime': end_dt.isoformat(),
                'timeZone': timezone
            }
        }
        
        created_event = calendar_service.events().insert(
            calendarId=calendar_id,
            body=event
        ).execute()
        
        print(f"Событие '{summary}' создано: {created_event.get('htmlLink')}")
    
    except HttpError as error:
        print(f"Ошибка Google API: {error}")
    except ValueError as e:
        print(f"Неверный формат даты/времени: {e}")


if __name__ == "__main__":
    completed_events = []
    while True:
        test = read_google_sheet(SPREED_SHEETS_ID, 'Лист1')
        df = pd.DataFrame(test)
        events = parse_events(df)
        for event in events:
            if event not in completed_events:
                print(event[0], event[1],event[2], event[3], CALENDAR_ID)
                create_calendar_event(event[0], event[1],event[2], event[3], CALENDAR_ID)
                completed_events.append(event)
        time.sleep(60)