
def init():
    global config
    config = {
        # Get this from Up (https://api.up.com.au/getting_started)
        "upPersonalAccessToken": "lalalala",

        # Get this from the URL of your spreadsheet
        "spreadsheetID": "1XbFflGI5sn_w4Bxt-rRg-mb-AYFrDfGWS7-qMSJZomY",

        # This is the name of the sheet you want to update
        # Note: This script will OVERRIDE whatever is in that range
        # You can also specify a range like this: "MySheet!A3:M8"
        "spreadsheetRange": "Sheet1"
    }