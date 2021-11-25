import requests
import AppConfig
import json

class UpHandler():
    def __init__(self):
        # self.config = AppConfig.config
        self.accessToken = AppConfig.config['upPersonalAccessToken']

    # Get helper method - adds authorisation token to all requests
    def _get(self,url, headersObj={}):
        try:
            headersObj["Authorization"] = f"Bearer {self.accessToken}"
            print(headersObj)
            res = requests.get(url, headers=headersObj)
            return res.json()
        except Exception as e:
            print(e)
            return {}

    # Get all transactions for this account
    def getAllTransactions(self):
        url = "https://api.up.com.au/api/v1/transactions"
        allTransactions = self._get(url)

        transactionList = allTransactions["data"]
        # Get list of all transactions
        print("All transactions")
        print(json.dumps(transactionList, indent=4))

        # Get each transaction individuallu
        # transactionList = allTransactions["data"]
        # for tObj in transactionList:
        #     transaction = self.getTransaction(tObj["id"])
        return transactionList

    # Get a single transaction
    def getTransaction(self, tid):
        url = f"https://api.up.com.au/api/v1/transactions/{tid}"
        transaction = self._get(url)
        print(f"Transaction - {tid}")
        print(json.dumps(transaction, indent=4))
        return transaction