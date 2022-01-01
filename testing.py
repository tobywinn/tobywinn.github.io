from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd

PATH = '/Applications/chromedriver'

driver = webdriver.Chrome(PATH)

driver.get("https://www.glassdoor.co.uk")

# Fill in email
driver.find_element_by_css_selector(".d-none.d-lg-block.p-0.LockedHomeHeaderStyles__signInButton").click()
time.sleep(2)


# Fill in password
driver.find_element_by_id("userEmail").send_keys("tobywinn@rocketmail.com")
driver.find_element_by_id("userPassword").send_keys("Teddybear1!")

# click accept cookies to reveal sign up button
driver.find_element_by_id("onetrust-accept-btn-handler").click()

# try to click sign in
element = driver.find_element_by_name("submit")
driver.execute_script("arguments[0].click();", element)