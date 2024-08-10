# eleves/utils.py
import requests
from django.conf import settings

def envoyer_sms(numero, message):
    response = requests.post('https://textbelt.com/text', {
        'phone': numero,
        'message': message,
        'key': settings.TEXTBELT_API_KEY
    })
    return response.json()
