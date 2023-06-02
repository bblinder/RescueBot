#!/usr/bin/env python3

"""
A simple Flask app that interacts with Twilio's API to kick off
phone calls. The phone call plays a specific audio message when answered.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from flask import Flask
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

# Set up logging
LOGGER = logging.getLogger("rescuebot_logger")
LOGGER.setLevel(logging.INFO)

HANDLER = RotatingFileHandler("rescuebot.log", maxBytes=2000, backupCount=1)
LOGGER.addHandler(HANDLER)

APP = Flask(__name__)


def validate_env_vars():
    """
    Validates that all required environment variables are present.
    """
    required_env_vars = [
        "RECIPIENT_PHONE_NUMBER",
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
        "TWILIO_PHONE_NUMBER",
    ]
    for var in required_env_vars:
        if var not in os.environ:
            LOGGER.error("Missing required environment variable: %s", var)
            sys.exit(1)
        LOGGER.info("Loaded environment variable: %s", var)


validate_env_vars()
RECIPIENT_PHONE_NUMBER = os.environ["RECIPIENT_PHONE_NUMBER"]


@APP.route("/make_call")
def make_call():
    """
    Makes a phone call to the recipient phone number.
    The call plays a specific audio message when answered.

    Returns:
        str: "Success!" if the call was initiated successfully,
             "Failure!" along with HTTP 500 status code in case of an error.
    """
    try:
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(account_sid, auth_token)

        call = client.calls.create(
            to=RECIPIENT_PHONE_NUMBER,
            from_=os.environ["TWILIO_PHONE_NUMBER"],
            twiml="<Response><Say>Its priest. Have a little priest. \
            Is it really good? Sir, its too good at least.</Say></Response>",
        )

        LOGGER.info("Call initiated with SID: %s", call.sid)

        return "Success!"
    except TwilioRestException as ex:
        LOGGER.error("Twilio API error: %s", ex)
        return "Failure!", 500
    except Exception as ex:
        LOGGER.error("Unexpected error: %s", ex)
        return "Failure!", 500


if __name__ == "__main__":
    APP.run(port=8080, debug=False)
