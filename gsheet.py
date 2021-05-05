from __future__ import print_function
import os
import os.path
import random
import string
from google.oauth2 import service_account
from googleapiclient.discovery import build

# TODO
# Set Creds from config.py file
SAMPLE_SPREADSHEET_ID = '1dInZP6NY8X9Nsmys8FaIpjLh8PMNFjfZ3T0GmYn9WB4'
SAMPLE_RANGE_NAME = 'A2:C'


def insert(date, time, username):
    scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file",
              "https://www.googleapis.com/auth/spreadsheets"]
    secret_file = os.path.join(os.getcwd(), 'apikey.json')

    credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Write
    values = [
        [

        ]
        # Additional rows ...
    ]
    body = {
        'values': [[str(date), str(time), str(username)]]
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
            print('%s, %s ,%s' % (row[0], row[1], row[2]))

    response = [row[0], row[1], row[2]]
    return response
