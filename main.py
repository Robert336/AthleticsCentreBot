import datetime
import time
from seleniumrequests import Chrome
import functions
import json
import schedule


# Load the user data from JSON file
with open('user_data.json') as f:
    user_data = json.load(f)

# path of the webdriver
DRIVER_PATH = user_data["webdriver_path"]

driver = Chrome(DRIVER_PATH)  # open chrome driver

print(">>> STARTING")

# login to portal
print(">>> Logging in as: %s" % user_data["email"])
functions.login(user_data["email"], user_data["password"], driver)

print(">>> Showing all entries")
functions.open_table(driver)

print(">>> Fetching table data")
table_data = functions.get_table_data(driver)

# Find what time the user is registering for (assume their input is correct)
reservation_date_str, reservation_time_str = functions.find_time_slot(user_data)

# find the SlotID of the reservation (to be used in HTTP request)
slot_id = functions.find_slot_id(user_data["reserve_name"], reservation_date_str, reservation_time_str, table_data)
print("SlotID : %s" % slot_id)


# TODO the user will need to restart the app every day for the this to work
# auto-request at the right time using scheduler
schedule.every().day.at(reservation_time_str[0:5]).do(functions.reserve, slot_id=slot_id, driver=driver)

# continuously run
while 1:
    # Checks if a scheduled task is pending to run or not
    schedule.run_pending()
    time.sleep(1)

