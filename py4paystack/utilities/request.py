import http.client
import json
from typing import Sequence, Union
from . import decorators


@decorators.class_type_checker
class Request:

    def __init__(self, secret_key: str) -> None:
        self.headers = {
            'authorization': f'bearer {secret_key}',
            'Content-type': 'application/json',
        }

    @classmethod
    def request(cls, path: str, method: str, headers: dict = None, payload: dict = None):
        connection = http.client.HTTPSConnection('api.paystack.co')
        connection.request(method, path, headers=headers, body=payload)
        return json.loads(connection.getresponse().read().decode('utf-8'))

    def get(self, path: str):
        return self.request(path, 'GET', headers={'authorization': self.headers.pop('authorization')})

    def post(self, path: str, payload: Union[dict, Sequence, set] = None):
        if payload:
            return self.request(path, 'POST', headers=self.headers, payload=json.dumps(payload))
        return self.request(path, 'POST', headers=self.headers)

    def put(self, path: str, payload: dict):
        return self.request(path, 'PUT', headers=self.headers, payload=json.dumps(payload))

    def delete(self, path: str, payload: dict = None):
        method = 'DELETE'
        if payload:
            return self.request(path, method, headers=self.headers, payload=payload)
        return self.request(path, method, headers={'authorization': self.headers.pop('authorization')})
    
