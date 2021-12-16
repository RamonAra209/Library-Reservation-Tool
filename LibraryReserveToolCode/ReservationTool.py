from email.message import EmailMessage
from selenium.webdriver.support import select
from helpFunctions import *
from emailNotification import *
from datetime import timedelta
# from pyvirtualdisplay import Display


# PATH = "/Users/tahpramen/Desktop/LibraryReserveProject/chromedriver"

PATH = "/usr/bin/chromedriver"

nextDay = nextMondayOrWednesday(todayObject)
# nextDay = datetime(2021, 11, 19)
if (todayObject.weekday() == 0 or todayObject.weekday() == 5): # was 0
    """
    If today Monday or Saturday: 
        Saturday -> checks upcoming monday
        Monday -> checks upcoming wednesday
    """
    # display = Display(visible=0, size=(800,600))
    driver = webdriver.Chrome(PATH)
    driver.get("https://pacific.libcal.com/booking/stocktoncampus")
    try:    
        clickCalendarDate(nextDay, driver)
        returnedDict = readTimeSlots(driver)
        reserveRoom(driver, returnedDict, secondFloor=True) #! Make sure to comment back in the reserve function after done testing

        #! Worked Fully On September 30, 2021 @ 12:18pm. High Fived Shahbaj AKA Turban Boi
        print("\n\n The Reservation Process was Successful! \n\n")
        
    except:
         
        # print("\n\n Oh No! Something Went Wrong Feller, You Better Go In and Fix it :( \n\n")
        sendEmailNotification("Something went wrong with the code!")
    # time.sleep(10)
    driver.close()