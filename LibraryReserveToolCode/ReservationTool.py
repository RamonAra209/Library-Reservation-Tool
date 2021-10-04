from email.message import EmailMessage
from selenium.webdriver.support import select
from helpFunctions import *
from emailNotification import *
from datetime import timedelta

PATH = "/Users/tahpramen/Desktop/LibraryReserveProject/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://pacific.libcal.com/booking/stocktoncampus")

nextDay = nextMondayOrWednesday(todayObject)

if (todayObject.weekday() == 0 or todayObject.weekday() == 5): 
    """
    If today Monday or Saturday: 
        Saturday -> checks upcoming monday
        Monday -> checks upcoming wednesday
    """
    try:    
        
        clickCalendarDate(nextDay, driver)
        returnedDict = readTimeSlots(driver)
        reserveRoom(driver, returnedDict, secondFloor=False) #! Make sure to comment back in the reserve function after done testing

        #! Worked Fully On September 30, 2021 @ 12:18pm. High Fived Shahbaj AKA Turban Boi
        print("\n\n The Reservation Process was Successful! \n\n")
        
    except:
        print("\n\n Oh No! Something Went Wrong Feller, You Better Go In and Fix it :( \n\n")
        sendEmailNotification()
        
driver.close()