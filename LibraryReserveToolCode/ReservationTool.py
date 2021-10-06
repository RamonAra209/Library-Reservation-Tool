from email.message import EmailMessage
from selenium.webdriver.support import select
from helpFunctions import *
from emailNotification import *
from datetime import timedelta

WEBDRIVER_PATH = "/Users/tahpramen/Desktop/LibraryReserveProject/chromedriver"

nextDay = nextMondayOrWednesday(todayObject)

if (todayObject.weekday() == 0 or todayObject.weekday() == 5): 
    """
    If today Monday or Saturday: 
        Saturday -> checks upcoming monday
        Monday -> checks upcoming wednesday
    """
    driver = webdriver.Chrome(WEBDRIVER_PATH)
    driver.get("https://pacific.libcal.com/booking/stocktoncampus")
    
    try:    
        clickCalendarDate(nextDay, driver)
    except:
        sendEmailNotification("Something went wrong with clicking the calendar date!")
    
    try:
        returnedDict = readTimeSlots(driver)
    except:
        message = "Something went wrong when reading the Time Slots, either no slots are available or something went wronng with the code."
        sendEmailNotification(message)
    
    try:
        reserveRoom(driver, returnedDict, secondFloor=True) #! Make sure to comment back in the reserve function after done testing
        #! Worked Fully On September 30, 2021 @ 12:18pm. High Fived Shahbaj AKA Turban Boi
        print("\n\n The Reservation Process was Successful! \n\n") 
    except:
        sendEmailNotification("Could not click on selected room, or was unable to input reservation text into input boxes")

    driver.close()