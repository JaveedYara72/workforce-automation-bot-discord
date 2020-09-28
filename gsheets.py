from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import random
import string
from datetime import datetime
import os
import json
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials

SAMPLE_SPREADSHEET_ID = '1P22aNEJDANd-2lLCzZAZS8X5hwIBG9u9C3GEQL5RET8'
SAMPLE_RANGE_NAME = 'A2:E'

def insert(username, work, time):
    scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
    secret_file = os.path.join(os.getcwd(), 'apikey.json')

    credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
    service = build('sheets', 'v4', credentials=credentials)


    # Call the Sheets API
    sheet = service.spreadsheets()
    values = [
        [

        ]
        # Additional rows ...
    ]
    body = {
        'values': [['Work Id', 'Timestamp', 'Work Title', 'Working Hours', 'Username']]
    }

    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range='A1:E1',
        valueInputOption='RAW', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

    random_id = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))
    # Write
    values = [
        [

        ]
        # Additional rows ...
    ]
    body = {
        'values': [[random_id, str(datetime.now()), work, time, username]]
    }

    result = service.spreadsheets().values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption='RAW', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Test:')
        for row in values:
            print('%s, %s ,%s,%s,%s' % (row[0], row[1], row[2], row[3], row[4]))

    response = []
    response.append(row[0])
    response.append(row[1])
    response.append(row[2])
    response.append(row[3])
    response.append(row[4])
    return response
