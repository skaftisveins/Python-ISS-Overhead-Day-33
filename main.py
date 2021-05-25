from config import *
import requests
from datetime import datetime as dt
from twilio.rest import Client


def is_iss_overhead():
    """Your position is within +5 or -5 degrees of the ISS position."""

    response = requests.get(api_open_notify_iss_endpoint)
    response.raise_for_status()
    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    print(f"Lat: {iss_latitude} | Long: {iss_longitude}")

    if float(my_lat) - 5 <= iss_latitude <= float(my_lat) + 5 and float(my_long) - 5 <= iss_longitude <= float(my_long) + 5:
        return True
    else:
        print("Nothing to see here!")


def is_night():
    parameters = {
        "lat": my_lat,
        "lng": my_long,
        "formatted": 0
    }

    response = requests.get(
        api_sunrise_sunset_endpoint, parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = dt.now().hour

    if time_now >= sunset or time_now <= sunrise:  # Find out if it's night
        return True


if is_iss_overhead() and is_night():
    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.messages \
        .create(
            body="Take a look outside boooiiii!\n\nYou might spot the ISS 🚀 above you in the night sky!",
            from_=twilio_phone_number,
            to=my_phone_number
        )
    print(message.status)


is_night()
