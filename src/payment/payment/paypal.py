import requests
import base64
import environ
from rest_framework import viewsets, status

env = environ.Env()
environ.Env.read_env()

CLIENT_ID = env('PAYPAL_CLIENT_ID')
CLIENT_SECRET = env('PAYPAL_CLIENT_SECRET')


def PaypalToken(client_ID, client_Secret):

    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    data = {
        "client_id": client_ID,
        "client_secret": client_Secret,
        "grant_type": "client_credentials"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic {0}".format(base64.b64encode((client_ID + ":" + client_Secret).encode()).decode())
    }

    token = requests.post(url, data, headers=headers)
    return token


class PayPalView(viewsets.ViewSet):
    PaypalToken(CLIENT_ID, CLIENT_SECRET)
