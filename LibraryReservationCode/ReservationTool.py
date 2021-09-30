from selenium.webdriver.support import select
from helperFunctions import *
from datetime import timedelta

PATH = "/Users/tahpramen/Desktop/LibraryReserveProject/chromedriver"
Shahbajdriver = webdriver.Chrome(PATH)

Shahbajdriver.get("https://pacific.libcal.com/booking/stocktoncampus")
tempDay = datetime(2021, 10, 1)
clickCalendarDate(tempDay, Shahbajdriver)
returnedDict = readTimeSlots(Shahbajdriver)
time.sleep(5)

Shahbajdriver.close()