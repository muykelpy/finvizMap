from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from twilio.rest import Client
from datetime import date
import datetime
import schedule
import time
import json

delay = 0.5

# Gathering data from config.json
f = open('config.json')
data = json.load(f)
phoneNumbers = data["phoneNumbers"]
account_sid = data["account_sid"]
auth_token = data["auth_token"]

# Closing file
f.close()

startURL = "https://finviz.com/map.ashx?t=sec"
chrome_options = Options() # Initializing options parameter 
# chrome_options.add_argument("--headless=new") # Enabling headless mode
driver = webdriver.Chrome(options=chrome_options)

def getStockMap():
    # Going to Finviz Stock Map website
    driver.get(startURL)
    time.sleep(delay)

    # Clicking the share button
    shareButton = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[3]/button[2]').click()
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

schedule.every().day.at("16:04").do(sendTexts)

while True:
    schedule.run_pending()
    time.sleep(60)