import http.client
import json


class Request:

    headers = {
        'authorization': 'bearer {}',
        'Content-type': 'application/json',
    }

    def __new__(cls):
        if cls == Request:
            return RuntimeError('Do not instantiate me!!')

    @classmethod
    def request(cls, path: str, method: str, headers: dict = None, payload: dict = None):
        connection = http.client.HTTPSConnection('https://api.paystack.co')
        if payload is not None:
            connection.request(method, path, headers=headers, body=payload)
        else:
            connection.request(method, path, headers=headers)
        return connection.getresponse().read().decode('utf-8')

    @classmethod
    def get(cls, path: str, secret_key: str):
        auth = cls.headers.pop('authorization').format(secret_key)
        return cls.request(path, 'GET', headers={'authorization': auth})

    @classmethod
    def change_headers(cls, secret_key: str):
        headers = cls.headers
        headers['authorization'].format(secret_key)
        return headers

    @classmethod
    def post(cls, path: str, secret_key: str, payload: dict):
        return cls.request(path, 'POST', headers=cls.change_headers(secret_key), payload=json.dumps(payload))

    @classmethod
    def put(cls, path: str, secret_key: str, payload: dict):
        return cls.request(path, 'PUT', headers=cls.change_headers(secret_key), payload=json.dumps(payload))
    
    @classmethod
    def delete(cls, path: str, secret_key: str, payload: dict = None):
        method = 'DELETE'
        if payload:
            return cls.request(path, method, headers=cls.change_headers(secret_key), payload=payload)
        auth = cls.headers.pop('authorization').format(secret_key)
        return cls.request(path, method, headers={ 'authorization': auth })
