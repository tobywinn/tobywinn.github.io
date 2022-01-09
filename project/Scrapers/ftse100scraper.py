from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np

# create chrome driver
PATH = '/Applications/chromedriver'

driver = webdriver.Chrome(PATH)

url_base = "https://www.londonstockexchange.com/indices/ftse-100/constituents/table{}"

pages = ["", "?page=2", "?page=3", "?page=4", "?page=5", "?page=6"]

count = 0
companies = []


for i in pages:
    count+=1
    url = url_base.format(i) 

    driver.get(url)

    if count == 1:
        #accept cookies
        time.sleep(1)
        element = driver.find_element_by_id("ccc-notify-accept")
        driver.execute_script("arguments[0].click();", element)
        time.sleep(1)

    # sort highest to lowest
    element = driver.find_element_by_css_selector("div[title='Highest – lowest']")
    driver.execute_script("arguments[0].click();", element)
    time.sleep(1)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    try:
        # extract section on salary from soup
        nameset = soup.findAll("td", class_="clickable instrument-name gtm-trackable td-with-link")
        
        for i in nameset:
            name = i.text
            sep = ' PLC'
            name = name.split(sep, 1)[0]
            name = name.replace("SCOTTISH MORTGAGE INV TST","Baillie Gifford")
            name = name.replace("HSBC HLDGS","HSBC")
            name = name.replace("COCA-COLA HBC AG ORD CHF6.70 (CDI)","Coca Cola")
            name = name.replace("INTL CONSOLIDATED AIRLINES GROUP SA ORD EUR0.10 (CDI)","International Airlines Group")
            name = name.replace("B&M EUROPEAN VALUE RETAIL S.A. ORD 10P (DI)","B&M Retail")
            name = name.replace("AUTO TRADER GROUP","Auto Trader UK")
            name = name.replace("BT GROUP","BT")
            name = name.replace("AVAST","Avast Software")
            name = name.replace("BRITISH LAND CO","British Land Company")
            companies.append(name)
    except:
        name = soup.find("td", class_="clickable instrument-name gtm-trackable td-with-link")
        name = name.text
        sep = ' PLC'
        name = name.split(sep, 1)[0]
        name = name.replace("SCOTTISH MORTGAGE INV TST","Baillie Gifford")
        name = name.replace("HSBC HLDGS","HSBC")
        name = name.replace("COCA-COLA HBC AG ORD CHF6.70 (CDI)","Coca Cola")
        name = name.replace("INTL CONSOLIDATED AIRLINES GROUP SA ORD EUR0.10 (CDI)","International Airlines Group")
        name = name.replace("B&M EUROPEAN VALUE RETAIL S.A. ORD 10P (DI)","B&M Retail")
        name = name.replace("AUTO TRADER GROUP","Auto Trader UK")
        name = name.replace("BT GROUP","BT")
        name = name.replace("AVAST","Avast Software")
        name = name.replace("BRITISH LAND CO","British Land Company")
        companies.append(name)

companies.remove('ROYAL DUTCH SHELL')
companies.remove('FERGUSON')
companies.remove('POLYMETAL INTERNATIONAL')
companies.remove('PERSHING SQUARE HOLDINGS LTD ORD NPV')

print(companies)