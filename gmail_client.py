from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import base64

import os

import pickle

 

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

 

def get_gmail_service():

    creds = None

    if os.path.exists('token.pkl'):

        with open('token.pkl', 'rb') as token:

            creds = pickle.load(token)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(

                'credentials.json', SCOPES)

            creds = flow.run_local_server(port=0)

        with open('token.pkl', 'wb') as token:

            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service

 

def get_latest_email():

    service = get_gmail_service()

    results = service.users().messages().list(userId='me', maxResults=1).execute()

    messages = results.get('messages', [])

 

    if not messages:

        return None, None

 

    msg = service.users().messages().get(userId='me', id=messages[0]['id'], format='full').execute()

    payload = msg['payload']

    headers = payload['headers']

 

    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")

    parts = payload.get('parts', [])

    body = ""

 

    if parts:

        for part in parts:

            if part['mimeType'] == 'text/plain':

                data = part['body']['data']

                body = base64.urlsafe_b64decode(data).decode('utf-8')

                break

    else:

        data = payload['body'].get('data')

        if data:

            body = base64.urlsafe_b64decode(data).decode('utf-8')

 

    return subject, body