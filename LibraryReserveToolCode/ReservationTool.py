from selenium.webdriver.support import select
from helpFunctions import *
from datetime import timedelta

PATH = "/Users/tahpramen/Desktop/LibraryReserveProject/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("https://pacific.libcal.com/booking/stocktoncampus")
tempDay = datetime(2021, 10, 1)
clickCalendarDate(tempDay, driver)
returnedDict = readTimeSlots(driver)
reserveRoom(driver, returnedDict, True)
time.sleep(5)

driver.close()