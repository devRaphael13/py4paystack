from . import util
from .request import Request

class Plan(Request):

    """
    The Plans API allows you create and manage installment payment options on your integration
    """

    path = '/plan'

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def create(self):
        pass

    def list_plans(self):
        pass

    def fetch(self):
        pass

    def update(self):
        path = ''
        payload = {}
        return self.put(path, self.secret_key, payload)