from .request import Request

class SplitTransaction(Request):
    """
    Create, list, retrieve, update split transaction configuration with one or more SubAccounts (You should have subaccounts on your integration to use this)  
    """

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def create(self):
        pass

    def list_search(self, *kwargs):
        pass

    def fetch(self):
        pass

    def update(self, *kwargs):
        pass

    def add(self):
        pass

    def remove(self):
        pass