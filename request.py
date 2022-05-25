import http.client


class Request:

    headers = {
        'authorization': 'bearer {}',
        'Content-type': 'application/json',
    }

    def __new__(cls):
        if cls == Request:
            return RuntimeError('Only subclasses can be instanciated')

    @classmethod
    def request(cls, path: str, method: str, headers: dict = None, payload: dict = None):
        connection = http.client.HTTPSConnection('https://api.paystack.co')
        connection.request(method, path, headers=headers, body=payload) if payload is not None else connection.request(
            method, path, headers=headers)
        return connection.getresponse().read().decode('utf-8')

    @classmethod
    def get(cls, path: str, secret_key: str):
        auth = cls.headers.pop('authorization').format(secret_key)
        return cls.request(path, 'GET', headers={'authorization': auth})

    @classmethod
    def post(cls, path: str, secret_key: str, payload: dict):
        assert payload is not None, 'provide payload that will be sent via POST request.'
        assert isinstance(payload, dict), 'payload must be of type dict.'
        headers = cls.headers
        headers['authorization'].format(secret_key)
        return cls.request(path, 'POST', headers=headers, payload=json.dumps(payload))
