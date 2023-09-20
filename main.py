# Packages used: Selenium, Twilio, Schedule

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from twilio.rest import Client
from datetime import date
import datetime
import schedule
import time

phoneNumbers = ["+15163033852", "+17187363742", "+15165677828", "+15168592181"]

delay = 0.5
account_sid = 'AC316f2ea1b4f5e16203df8f6217de17ea'
auth_token = '9958ae5b713eff71e636666ce5bb0018'

startURL = "https://finviz.com/map.ashx?t=sec"
chrome_options = Options() # Initializing options parameter 
chrome_options.add_argument("--headless=new") # Enabling headless mode
driver = webdriver.Chrome(options=chrome_options)

def getStockMap():
    # Going to Finviz Stock Map website
    driver.get(startURL)
    time.sleep(delay)

    # Clicking the share button
    shareButton = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[3]/button[2]').click()
    time.sleep(delay)

    # Getting text from the share textbox
    shareBox = driver.find_element(By.TAG_NAME, 'TEXTAREA')
    first = shareBox.text
    time.sleep(delay)

    # Going to 1st image URL
    driver.get(first)
    time.sleep(delay)
    imgURL = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/a[1]/img').get_attribute("src")

    # Quitting Selenium
    driver.quit()

    # Print and return the results
    print(imgURL)
    return(imgURL)
    
def getDate():
    today = date.today()
    return today.strftime("%B %d, %Y")

def checkDate():
    today = datetime.date.today()
    return today.weekday()

# Sending text (utilizing Twilio)
def sendTexts():
    imgURL, todayDate, day = getStockMap(), getDate(), checkDate()
    if (day == 5 or day == 6):
        # If it's Sat/Sun don't do anything
        return
    else:
        for num in phoneNumbers:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
            from_ = '+18444040726',
            body = ('Stock Map - ' + todayDate),
            media_url = imgURL,
            to = num,    
            )
            print(message.sid)
            time.sleep(delay*5)

schedule.every().day.at("16:05").do(sendTexts)

while True:
    schedule.run_pending()
    time.sleep(60)