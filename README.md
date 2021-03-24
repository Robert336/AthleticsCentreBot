# AthleticsCentreBot
Basic functionality is complete.

Automatically reserve spots at the Athletic Centre faster than everyone else.

Uses Python and Selenium to automate the process of logging in and booking a time slot at the WLU Athletics Centre.
For reserving a spot faster than anyone else the bot sends a HTTP 'POST' request to the reservation server to reserve the time slot you are looking for.
Because of this the Bot does not need to interact with any HTML elements on the page and wait for different pages to load in order to book a slot.
Therefore, it's always faster than a human.

edit user_data.json for your own use.

includes the driver for Chrome v89, if you are running a different version of Chrome find the webdriver here: https://chromedriver.chromium.org/downloads then update the webdriver path in user_data.json file to your newly downloaded webdriver's path.



Next steps: (not in order)
 - [ ] (in-progress) Transform into web app using Flask
 - - [ ] Host Web App on Azure servers for 24/7 use
 - [ ] ~~Remotly Host on Raspberry Pi to run 24/7~~
 - [ ] ~~Impliment multi-thread processing to handle multiple users at the same time~~
 - [x] Fix login timeout issues
 - [x] Reduce CPU usage (used time.sleep() to stop the while loop from running as fast as possible)
 - [x] Reduce RAM usage (used generators instead of loading the whole data set into RAM) (RAM usage is now ~0.05MB MAX)
 - [ ] Add reserved times to Google Calendar


*secuirty flaw discovery*: The site has no authentication for canceling reservations, meaning if you send a 'POST' request to the server with the correct parameters it will remove the reservation. Even if it doesn't belong to you... yikes.
Disclaimer: I tested this using a booking made by my friend. No reservations were harmed in this discovery.
