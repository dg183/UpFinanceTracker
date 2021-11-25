
import AppConfig
from GoogleSheets import GoogleSheets
from UpHandler import UpHandler


def main():
    print('as')
    AppConfig.init()
    gs = GoogleSheets()
    # gs.readRange()

    up = UpHandler()
    transactionsList = up.getAllTransactions()

    gs.writeTransactions(transactionsList)

if __name__=='__main__':
    main()