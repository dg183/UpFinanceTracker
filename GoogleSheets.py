from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import AppConfig

class GoogleSheets():
    def __init__(self, 
                scopes=['https://www.googleapis.com/auth/spreadsheets']):
        self.scopes = scopes
        self.sheet = self._initSheet()
        self.config = AppConfig.config

    def _initSheet(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        return sheet

    # def readRange(self,
    #                 spreadsheetID='1XbFflGI5sn_w4Bxt-rRg-mb-AYFrDfGWS7-qMSJZomY',
    #                 rangeName='Sheet1!A2:E'):
    #     result = self.sheet.values().get(spreadsheetId=spreadsheetID,
    #                             range=rangeName).execute()
    #     values = result.get('values', [])

    #     if not values:
    #         print('No data found.')
    #     else:
    #         print('Name, Major:')
    #         for row in values:
    #             # Print columns A and E, which correspond to indices 0 and 4.
    #             print('%s, %s' % (row[0], row[4]))


    # This function will write inputted transaction into Google Sheets
    '''
    Example row data for Google Sheets
        values = [
            ['row1','aa','ascc','as'],
            ['row2','sad','s','xa'],
            ['row3','asds','sad','eas']
        ]
    '''
    def writeTransactions(self, 
                            transactionsList, 
                            spreadsheetID='',
                            rangeName=''):
        print("Writing transactions to sheets")

        if not spreadsheetID:
            spreadsheetID = self.config["spreadsheetID"]
        if not rangeName:
            rangeName = self.config["spreadsheetRange"]

        colParser = TransactionColumnParser()

        # Initialise column names for first row
        sheetData = [
            self.getColumnHeaders
        ]

        for t in transactionsList:
            transactionRow = colParser.parse(t)
            sheetData.append(transactionRow)

        # Send data to be written
        body = {
            'values': sheetData
        }

        value_input_option = "RAW" # ["RAW","USER_ENTERED"]
        result = self.sheet.values().update(
            spreadsheetId=spreadsheetID, range=rangeName,
            valueInputOption=value_input_option, body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))


    def _getTransactionColumnDetails(self):
        pass


class TransactionColumnParser():
    def __init__(self):
        self.x = 1

    def getColumnHeaders(self):
        headers = [
            "id",
            "status",
            "rawText",
            "description",
            "message",
            "holdInfo",
            "roundUp",
            "cashback",
            "amount",
            "foreignAmount",
            "settledTimestamp",
            "createdTimestamp",
            "account"
        ]
        return headers

    def parse(self, t):
        transactionRow = [
            self._parseDirect(t["id"]),
            self._parseDirect(t["attributes"]["status"]),
            self._parseDirect(t["attributes"]["rawText"]),
            self._parseDirect(t["attributes"]["description"]),
            self._parseDirect(t["attributes"]["message"]),
            self._parseAmount(t["attributes"]["holdInfo"]),
            self._parseDirect(t["attributes"]["roundUp"]),
            self._parseDirect(t["attributes"]["cashback"]),
            self._parseAmount(t["attributes"]["amount"]),
            self._parseAmount(t["attributes"]["foreignAmount"]),
            self._parseDirect(t["attributes"]["settledAt"]),
            self._parseDirect(t["attributes"]["createdAt"]),
            self._parseDirect(t["relationships"]["account"]["data"]["id"])
        ]
        return transactionRow


    def _parseDirect(self, attribute):
        if not attribute:
            return ""
        return attribute

    def _parseAmount(self, amountObj):
        if not amountObj:
            return ""

        # For this case
        '''
        "holdInfo": {
            "amount": {
                "currencyCode": "AUD",
                "value": "-107.92",
                "valueInBaseUnits": -10792
            },
            "foreignAmount": null
        },
        '''
        if type(amountObj) == dict and "amount" in amountObj:
            print("dictionary found")
            print(amountObj)

            if amountObj["amount"]:
                return self._parseAmount(amountObj["amount"])
            else:
                return self._parseAmount(amountObj["foreignAmount"])

        
        return amountObj["currencyCode"] + amountObj["value"]
    

