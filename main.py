from dotenv import load_dotenv
import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()

# Укажите путь к файлу с учетными данными (credentials.json)
creds = Credentials.from_authorized_user_file('./token.json', ['https://www.googleapis.com/auth/spreadsheets'])
URL = 'https://docs.google.com/spreadsheets/d/1ujwhD5WiN7-CK7bIORmzXZ-PcqXBT5ZVyDZN1ruKO4s/edit?usp=sharing'
# ID таблицы Google Sheets
sheet_id = 'Лист7'

# Чтение данных из таблицы
sheets_service = build('sheets', 'v4', credentials=creds)
sheet = sheets_service.spreadsheets()
result = sheet.values().get(spreadsheetId=sheet_id, range='Sheet1!A2:C').execute()
data = result.get('values', [])
print(data)

# ,
#   "service_account_email": "demchak@cherkasov-451916.iam.gserviceaccount.com"