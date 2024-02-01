# -*- coding: utf-8 -*-
import os.path
import base64
import email
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:\\Users\\divas\\Downloads\\client_secret_516206527826-83eg88munipjhcorodo70vva832j0fo8.apps.googleusercontent.com(1).json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def list_messages(service, user_id, max_results=200):
    try:
        response = service.users().messages().list(userId=user_id, maxResults=max_results).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        return messages
    except Exception as error:
        print(f'An error occurred: {error}')

def get_message_subject_and_sender(service, user_id, message_id):
    try:
        message = service.users().messages().get(userId=user_id, id=message_id, format='metadata').execute()
        headers = message['payload']['headers']
        subject = next(header['value'] for header in headers if header['name'] == 'Subject')
        sender = next(header['value'] for header in headers if header['name'] == 'From')
        return subject, sender
    except Exception as error:
        print(f'An error occurred: {error}')

def main():
    service = get_gmail_service()
    messages = list_messages(service, 'me')

    if not messages:
        print('No messages found.')
        return

    for message in messages:
        subject, sender = get_message_subject_and_sender(service, 'me', message['id'])
        print(f'From: {sender}, Subject: {subject}')

if __name__ == '__main__':
    main()