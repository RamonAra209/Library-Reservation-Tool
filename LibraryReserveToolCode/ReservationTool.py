from selenium.webdriver.support import select
from helpFunctions import *
from datetime import timedelta

PATH = "/Users/tahpramen/Desktop/LibraryReserveProject/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("https://pacific.libcal.com/booking/stocktoncampus")
tempDay = datetime(2021, 10, 1)
clickCalendarDate(tempDay, driver)
returnedDict = readTimeSlots(driver)
reserveRoom(driver, returnedDict, secondFloor=False) #! Make sure to comment back in the reserve function after done testing
time.sleep(10)

#! Worked Fully On September 30, 2021 @ 12:18pm. High Fived Shahbaj AKA Turban Boi
driver.close()