from datetime import datetime, timedelta
import time
import string

from apiclient import discovery
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError
import pandas as pd

import settings

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/calendar.events',
]




# CALENDAR_ID = '8b472d96c37bc493132343832aeb43f5345b5a7d2f282bf36d0e2631d5374d99@group.calendar.google.com'

CREDENTIALS_FILE = 'keys.json'
CREDENTIALS = Credentials.from_service_account_file(filename=CREDENTIALS_FILE, scopes=SCOPES)

sheets_service = discovery.build('sheets', 'v4', credentials=CREDENTIALS)
calendar_service = discovery.build('calendar', 'v3', credentials=CREDENTIALS)


def read_google_sheet():
    try:
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=settings.SPREED_SHEETS_ID,
            range=settings.NAME_LIST
        ).execute()
        # print(result)
        values = result.get('values', [])
        return values

    except HttpError as error:
        print(f"Произошла ошибка: {error}")
        return []
    

def parse_events(data):
    events = []
    df = pd.DataFrame(data)
    df.columns = df.iloc[0]
    for index, row in df.iterrows():
        link = row[settings.LINK]
        if link:
            continue
        name = row[settings.NAME]
        address = row[settings.ADDRESS]
        telephone = row[settings.TELEPHONE]

        date = row[settings.DATE]
        if date:
        #     try:
        #         datetime.strptime(date, '%d-%m-%Y')
        #     except ValueError as e:
        #         print('Дата не соответствует', date, '-', e)
        #         continue
            date = date.replace(".", "-")

        start = row[settings.START_TIME]
        # if start:
        #     try:
        #         datetime.strptime(start, '%H:%M"')
        #     except ValueError as e:
        #         print('Время начала не соответствует', start, '-', e)
        #         continue

        end = row[settings.END_TIME]
        if not all([name, address, telephone, date, start, end]):
            continue
        events.append([index + 1, name, address, telephone, date, start, end])
    return events


def create_calendar_event(
    summary: str,
    location: str,
    description: str,
    date: str,
    start_time: str,
    end_time: str = None
):
    timezone: str = 'Europe/Moscow',
    try:
        start_dt = datetime.strptime(f"{date} {start_time}", "%d-%m-%Y %H:%M")
        if end_time:
            end_dt = datetime.strptime(f"{date} {end_time}", "%d-%m-%Y %H:%M")
        else:
            end_dt = start_dt + timedelta(minutes=90)
        
        event = {
            'summary': f'{summary} {location}',
            'location': location,
            'description': description,
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
            calendarId=settings.CALENDAR_ID,
            body=event
        ).execute()
        link = created_event.get('htmlLink')        
        print(f"Событие '{summary}' создано: {link}")
        return link
    
    except HttpError as error:
        print(f"Ошибка Google API: {error}")
    except ValueError as e:
        print(f"Неверный формат даты/времени: {e}")


def update_cell(row, value):
    """Обновляет конкретную ячейку"""
    try:
        body = {
            'values': [[value]]
        }
        sheets_service.spreadsheets().values().update(
            spreadsheetId=settings.SPREED_SHEETS_ID,
            range=f"{settings.NAME_LIST}!{letter_link}{row}",
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        print(f"Запись в {letter_link}{row} успешна")
    except HttpError as e:
        print(f"Ошибка записи: {e}")


def find_column(headers, target):
    for i, header in enumerate(headers):
        if header == target:
            return i
    raise ValueError(f"Столбец '{target}' не найден")


if __name__ == "__main__":
    headers = read_google_sheet()[0]
    try:
        ADDR_COL = find_column(headers, settings.ADDRESS)
        NAME_COL = find_column(headers, settings.NAME)
        PHONE_COL = find_column(headers, settings.TELEPHONE)
        DATE_COL = find_column(headers, settings.DATE)
        START_COL = find_column(headers, settings.START_TIME)
        END_COL = find_column(headers, settings.END_TIME)
        LINK_COL = find_column(headers, settings.LINK)

    except ValueError as e:
        print(e)
        exit()

    letter_link =string.ascii_uppercase[15]

    while True:
        data = read_google_sheet()
        new_events = parse_events(data)
        for event in new_events:
            name, address, telephone, date, start, end = event[1], event[2],event[3], event[4], event[5], event[6]
            link = create_calendar_event(name, address, telephone, date, start, end)
            update_cell(event[0], link)
        time.sleep(20)
