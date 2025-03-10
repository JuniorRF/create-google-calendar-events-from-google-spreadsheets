import os.path

from google.oauth2.credentials import Credentials
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']


creds = Credentials.from_authorized_user_file('./token.json', SCOPES)
