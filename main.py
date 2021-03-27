"""
Developed by: Robert Mazza
"""

import datetime
import time
from seleniumrequests import Chrome
import requests
import functions
import json
import schedule


def main():
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

    """ unused "table_data", switched to using generators for more efficiency.
    print(">>> Fetching table data")
    table_data = functions.get_table_data(driver)
    """

    # Find what time the user is registering for (assume their input is correct)
    reservation_date_str, reservation_time_str = functions.find_time_slot(user_data)

    # find the SlotID of the reservation (to be used in HTTP request)
    slot_id = functions.find_slot_id(user_data["reserve_name"], reservation_date_str, reservation_time_str, driver)
    print("SlotID : %s" % slot_id)

    # logout to prevent session timout issue
    functions.logout(driver)

    # creating datetime object
    reservation_time_obj = datetime.datetime.strptime(reservation_date_str + " " + reservation_time_str, '%Y-%m-%d '
                                                                                                         '%H:%M:%S')

    # auto-request at the right time using scheduler
    # schedule.every().day.do(update_reservation_data(driver, user_data))

    # user is not logged in (0 = false)
    logged_in = 0

    # continuously run
    while 1:
        # Checks if a scheduled task is pending to run or not
        # schedule.run_pending()

        # login 5 mins before reservation time
        now = datetime.datetime.now()
        today = datetime.datetime.today()
        if logged_in == 0 and now.hour == (reservation_time_obj.hour - 1) and now.minute >= 59 and now.second >= 30:
            print(">>> Logging in as: %s" % user_data["email"])
            functions.login(user_data["email"], user_data["password"], driver)
            logged_in = 1

        elif logged_in == 1 and now.hour == reservation_time_obj.hour and now.minute == reservation_time_obj.minute and now.second < 10:
            functions.reserve(slot_id, driver)

        elif logged_in == 1 and now.minute > reservation_time_obj.minute and now.second > reservation_time_obj.second:
            print("logging out")
            functions.logout(driver)
            logged_in = 0

        if logged_in == 0:
            time.sleep(2)  # if still far from reservation time, use less CPU with time.sleep
            # schedule.run_pending()

        # used to sync data if ran 24/7 and days become out-of-sync
        if today.day + 4 != reservation_time_obj.day:
            # login to portal
            print(">>> Logging in as: %s" % user_data["email"])
            functions.login(user_data["email"], user_data["password"], driver)

            print(">>> Showing all entries")
            functions.open_table(driver)

            # update the slot_id and reservation time match the correct day (new day)
            slot_id, reservation_time_obj = sync_days(driver, user_data)

            # logout to prevent session timout issue
            print("logging out")
            functions.logout(driver)


def sync_days(driver, user_data):
    # Find what time the user is registering for (assume their input is correct)
    reservation_date_str, reservation_time_str = functions.find_time_slot(user_data)

    # find the SlotID of the reservation (to be used in HTTP request)
    slot_id = functions.find_slot_id(user_data["reserve_name"], reservation_date_str, reservation_time_str, driver)
    print("SlotID : %s" % slot_id)

    # creating datetime object
    reservation_time_obj = datetime.datetime.strptime(reservation_date_str + " " + reservation_time_str, '%Y-%m-%d '
                                                                                                         '%H:%M:%S')

    return slot_id, reservation_time_obj


print("Version - 1.11")
main()  # run the script
