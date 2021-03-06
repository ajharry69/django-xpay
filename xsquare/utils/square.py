from uuid import uuid4

from django.conf import settings
from square.client import Client
from xauth.utils import valid_str


class Square:
    __SQUARE_SETTING = settings.PAYMENT.get('SQUARE', {})
    __ACCESS_TOKEN = __SQUARE_SETTING.get('ACCESS_TOKEN', )

    def __init__(self, access_token=__ACCESS_TOKEN, production: bool = False, ):
        access_token = access_token if valid_str(access_token) else self.__ACCESS_TOKEN
        self.client = Client(access_token=access_token, environment='production' if production else 'sandbox', )

    def create_payment(self, nonce, body: dict):
        body['idempotency_key'] = uuid4().hex
        if body.get('app_fee_money') is None:
            body.pop('app_fee_money')
        if body.get('source_id') is None:
            body['source_id'] = "cnon:card-nonce-ok"  # used in test/sandbox
        return self.client.payments.create_payment(body=body, )
