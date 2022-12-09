
import AppConfig
from GoogleSheets import GoogleSheets
from UpHandler import UpHandler


def main():
    print('Initialising..')
    AppConfig.init()
    gs = GoogleSheets()
    # gs.readRange()

    up = UpHandler()
    print("Initialised")
    transactionsList = up.getAllTransactions()

    print("Writing to Google Sheets")
    gs.writeTransactions(transactionsList)

    print("Done")

if __name__=='__main__':
    main()