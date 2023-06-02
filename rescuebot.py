#!/usr/bin/env python3

from flask import Flask
from twilio.rest import Client
import os

app = Flask(__name__)

RECIPIENT_PHONE_NUMBER = os.environ['RECIPIENT_PHONE_NUMBER']

@app.route('/make_call')
def make_call():
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        to=RECIPIENT_PHONE_NUMBER,
        from_=os.environ['TWILIO_PHONE_NUMBER'],
        twiml='<Response><Say>voice=Polly.Amy"Where do you want me, Ritchie?</Say></Response>'
    )

    return str(call.sid)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
