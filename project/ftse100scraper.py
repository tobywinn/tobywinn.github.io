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

pages = ["", "?page=2"]

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

    # extract section on salary from soup
    nameset = soup.findAll("td", class_="clickable instrument-name gtm-trackable td-with-link")
    
    for i in nameset:
        name = i.text
        sep = ' PLC'
        name = name.split(sep, 1)[0]
        name = name.replace("SCOTTISH MORTGAGE INV TST","Baillie Gifford")
        name.replace(" HLDGS","")
        companies.append(name)

companies.remove('ROYAL DUTCH SHELL')
companies.remove('FERGUSON')
companies.remove('CRH')
companies.remove('ASHTEAD GROUP')
companies.remove('FLUTTER ENTERTAINMENT')
companies.remove('BAE SYSTEMS')
companies.remove('SEGRO')
companies.remove('3I GROUP')

print(companies)


    
