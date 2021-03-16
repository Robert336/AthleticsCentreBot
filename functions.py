from selenium.webdriver.support.select import Select
import time
import datetime


# TODO: handle exceptions and errors like wrong email/password

# login - used to login the user to the athletics centre website
# Parameters:   email - String
#               password - String
#               driver - webdriver object
def login(email, password, driver):
    driver.get('https://www.laurierathletics.com/ecommerce/user/index.php')  # search the login page

    # Inputs the email and password into it's respective text box on the login page
    inputEmailElement = driver.find_element_by_name("UserLogin")
    inputEmailElement.send_keys(email)
    inputPasswordElement = driver.find_element_by_name("Password")
    inputPasswordElement.send_keys(password)

    # Simulates clicking the login button
    loginButtonElement = driver.find_element_by_name("submit_Login")
    loginButtonElement.click()


# uses the search function on the website to narrow search
# Parameters:   key - String
#               driver - webdriver object
def open_table(driver):
    # selects the "All" option from the dropdown menu on the table
    dropdown = Select(driver.find_element_by_xpath('//*[@id="DataTables_Table_1_length"]/label/select'))
    dropdown.select_by_visible_text("All")


# XPath to Data Table >>>  //*[@id="DataTables_Table_1"]/tbody
# XPath to table Header >>> //*[@id="DataTables_Table_1"]/thead

# pulls all data from the table and turns it into a 2d list
# Parameters:   driver - webdriver object
# Return: table_data - 2d list, Strings
def get_table_data(driver):
    # initialize 2d list to store all the row and column data
    table_data = list()

    table = driver.find_element_by_xpath('//*[@id="DataTables_Table_1"]/tbody')

    # linearly iterate through table add pull all row and column data
    for row in table.find_elements_by_xpath(".//tr"):
        # test if it can read the table >>>
        # print([td.text for td in row.find_elements_by_xpath('.//td')])

        # temp list to store column data
        colData = list()
        # goes to each column and appends data
        for td in row.find_elements_by_xpath('.//td'):
            colData.append(td.text)

        # append the column data list for this row to the table list
        table_data.append(colData)

    return table_data


# returns the SlotID that contains the same data as the args
def find_slot_id(name_str, date_str, time_str, table_data):
    slot_id = None
    # iterate through rows of the table
    for row in table_data:
        # Check if the current row matches the parameters
        if name_str in row[1] and date_str == row[3] and time_str == row[4]:
            slot_id = row[0]  # found SlotID for reservation

    return slot_id


# Executes HTTP POST request to reserve the specified slot (slot_id)
def reserve(slot_id, driver):
    t0 = time.time()  # start timer
    # sending HTTP 'POST' reservation request to server
    response = driver.request('POST', 'https://www.laurierathletics.com/ecommerce/user/backendcrud.php',
                              data={"waiver1": "Agree", "waiver2": "Agree", "SlotID": slot_id, "makereservation": "1"})
    print(response)

    t1 = time.time()  # end timer
    total_time = t1 - t0
    print("Execution time = %d" % total_time)

    if '200' in response:
        print("HTTP request success!")

    return response


def find_time_slot(user_data):
    # Get today's date
    today_date = datetime.datetime.today()

    reservation_date = today_date + datetime.timedelta(days=4)  # reservation date (4 days in advance)
    reservation_date_str = reservation_date.strftime("%Y-%m-%d")  # date conversion to String YYYY-MM-DD

    # find what time slot the user wants to book for
    reservation_time_str = None  # initializing
    for day in user_data["reserve_day_and_time"]:
        if reservation_date.strftime("%A") == day[0]:  # %A displays the day of the week
            reservation_time_str = day[1]  # get the time of day for registration from JSON file
            break

    return reservation_date_str, reservation_time_str
