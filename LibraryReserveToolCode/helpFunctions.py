from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from datetime import *
import time

todayObject = datetime.date(datetime.now())

def monthConversion(today: datetime) -> int:
    return (today.month - 1)

def dayConversion(today: datetime) -> int:
    return today.day

def yearConversion(today: datetime) -> int:
    return today.year

def isMondayWednesday(today: datetime) -> bool:
    return (today.weekday() == 0 or today.weekday() == 2)  
    
def next_weekday(date, weekday): #! Status = Done
    day_gap = weekday - date.weekday()
    if day_gap <= 0:
        day_gap += 7
    return date + timedelta(days=day_gap)

def nextMondayOrWednesday(today:datetime) -> datetime: #! Status = Done
    if today.weekday() == 0 or today.weekday() == 1:
        return next_weekday(today, 2) # returns next wednesday
    elif today.weekday() > 1 and today.weekday() <= 6:
        return next_weekday(today, 0) # returns next monday

def clickCalendarDate(day: datetime, driver:webdriver) -> None: #TODO Change the day parameter to today:datetime
    #! OR, we can call nextMondayOrWednesday outside of the function, pass it through when calling here, parameter = day: datetime
    search = Select(driver.find_element_by_class_name("ui-datepicker-month"))
    search.select_by_index(monthConversion(day)) #TODO if monday/wed fall into next month, we need to change the month here
    #! day.month()

    rows = driver.find_elements_by_xpath("/html/body/div[2]/div[3]/section/div/div/div[2]/div[1]/div[3]/div/div/table/tbody/tr")
                                         #/html/body/div[2]/div[3]/section/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr[2]/td[1]/table/tbody
                                         #"/html/body/div[2]/div[3]/section/div/div/div[2]/div[1]/div[3]/div/div/table/tbody/tr"
                                         #/html/body/div[2]/div[3]/section/div/div/div[2]/div[2]/div[1]/div/table
    rows = int(len(rows))
    threeValidDays = []
    threeValidXPaths = []
    for row in range(rows + 1):
        for col in range(7):
            xPath = "/html/body/div[2]/div[3]/section/div/div/div[2]/div[1]/div[3]/div/div/table/tbody/tr[{}]/td[{}]/a".format(row, col)
            try: 
                threeValidDays.append(driver.find_element_by_xpath(xPath))
                threeValidXPaths.append(xPath)
                # print("\nIT WORKED\n")
            except: 
                pass
    for i in threeValidXPaths:
        # print("Three Valid XPaths (Line 54): {}".format(i))
        if int(driver.find_element_by_xpath(i).text) == day.day: #TODO Change this so that it takes nextMondayOrWednesday
            #! day.day()
            driver.find_element_by_xpath(i).click()
    
def readTimeSlots(driver:webdriver) -> dict:
    # # rows = driver.find_elements_by_xpath("/html/body/div[2]/div[3]/section/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr")
    # # rows = driver.find_elements_by_xpath("/html/body/div[2]/div[3]/section/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody")
    # rows = driver.find_elements_by_xpath("/html/body/div[2]/div[3]/section/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr[2]/td[2]/div")
    # # rows = driver.find_elements_by_xpath("/html/body/div[2]/div[3]/section/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr[2]/td[2]/div/table")
    # "/html/body/div[2]/div[3]/section/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[1]")
    # print("Just Print(Rows): {}".format(rows))
    
    validXPaths = []
    validXPathsDict = {} #key : val ---> room: arr[] == 1 then dont do it, if 2 == click()
    # print("Num Rows in readTimeSlots: ", rows)
    for row in range(17 + 1): # range is inclusive, WAS range(rows + 1)
        tempList = [] #! Values
        tempRoom = "" #! key
        # print("Line 70 for loop: {}".format(row))
        for col in range(24):
            
            xPath = "/html/body/div[2]/div[3]/section/div/div/div[2]/div[2]/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[{}]/td/a[{}]".format(row, col)
            try:
                cell = driver.find_element_by_xpath(xPath)
                validXPaths.append(cell)
                tempRoom = cell.get_attribute("title")[:8] 
                tempList.append(cell)
                # print("Cell (Line 76): {}".format(cell))
                
            except:
                pass
        # print(tempList)
        validXPathsDict[tempRoom] = tempList
    
    filteredDict = {}
    for key, values in validXPathsDict.items():
        tempList = []
        # print("Room: {}    Len of Val: {}".format(key,len(values)))
        for val in values:
            if ("12:00pm to 1:00pm" in val.get_attribute("title") or "1:00pm to 2:00pm" in val.get_attribute("title") and \
                "Project Room" not in val.get_attribute("title")):
                tempList.append(val)
                # print(val.get_attribute("title"))
        filteredDict[key] = tempList
        # print("Appended: {}".format(filteredDict[key]))
        # print("Len of Appended: {}\n\n".format(len(filteredDict[key])))
    
    # print("\n\n\n SUPER DUPER FILTERED")
    superDuperFilteredDict = {}
    for key, values in filteredDict.items():
        tempList = []
        if (len(values) == 2):
            for val in values:
                tempList.append(val)
            superDuperFilteredDict[key] = tempList
            # print("Appended: {}".format(superDuperFilteredDict[key]))
            # print("Len of Appended: {}\n\n".format(len(superDuperFilteredDict[key])))
    
    # print("Len of Super Duper Filtered: {}".format(len(superDuperFilteredDict)))
    # print("\n\n {} \n\n".format(validXPathsDict))
    # print("\n\n {} \n\n".format(filteredDict))
    # print("\n\n {} \n\n".format(superDuperFilteredDict))
    return superDuperFilteredDict
    
def reserveRoom(driver:webdriver, availableDates: dict, secondFloor=True) -> None:
    if secondFloor == True:
        lastKey = list(availableDates)[-1]
        testValues = availableDates[lastKey]
        for values in testValues:
            values.click()
            print("CLICKED! Second Floor")
    else:
        firstKey = list(availableDates)[0]
        testValues = availableDates[firstKey]
        for values in testValues:
            values.click()
            print("CLICKED! First Floor")
    
    # firstName, lastName, email, universityID, school, [CLICK BOOKING]
    with open("/Users/tahpramen/Desktop/BookingInformation/bookingInfo.txt") as file: #! Change this once its on raspberry pi 
        lines = file.readlines()
        firstName = lines[0]
        lastName = lines[1]
        studentEmail = lines[2]
        studentID = lines[3]
        dropDownNum = int(lines[4])
        
        continueButton = driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div/div[2]/div[2]/div[3]/form/fieldset/div[2]/div/button[1]")
        continueButton.click()
        
        driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div/div[2]/div[2]/div[3]/form/fieldset/div[3]/div[2]/div[1]/input").send_keys(firstName)
        driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div/div[2]/div[2]/div[3]/form/fieldset/div[3]/div[2]/div[2]/input").send_keys(lastName)
        driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div/div[2]/div[2]/div[3]/form/fieldset/div[3]/div[3]/div/input").send_keys(studentEmail)
        driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div/div[2]/div[2]/div[3]/form/fieldset/div[3]/div[4]/div/input").send_keys(studentID)
        dropDownMenu = Select(driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div/div[2]/div[2]/div[3]/form/fieldset/div[3]/div[6]/div/select"))
        dropDownMenu.select_by_value("Engineering")
        
        
    
def sendEmailNotification() -> None:
    pass
        