from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np

PATH = '/Applications/chromedriver'

driver = webdriver.Chrome(PATH)

driver.get("https://www.glassdoor.co.uk")

# Fill in email
driver.find_element_by_css_selector(".d-none.d-lg-block.p-0.LockedHomeHeaderStyles__signInButton").click()
time.sleep(1)

# Fill in password
driver.find_element_by_id("userEmail").send_keys("tobywinn@rocketmail.com")
driver.find_element_by_id("userPassword").send_keys("Teddybear1!")

# click accept cookies to reveal sign up button
driver.find_element_by_id("onetrust-accept-btn-handler").click()

# try to click sign in
element = driver.find_element_by_name("submit")
driver.execute_script("arguments[0].click();", element)

time.sleep(2)

# navigate to companies section 
driver.find_element_by_link_text("Companies").click()

# Fill in companies to search
companies = ["Morgan Stanley"]
names = [] 
salaries = []

for i in companies:

    # clear search bar, search name of company
    driver.find_element_by_id("sc.keyword").clear()
    driver.find_element_by_id("sc.keyword").send_keys(i)
    driver.find_element_by_id("sc.keyword").send_keys(Keys.RETURN)

     # if company is not automatically navigated to 
    if driver.find_elements_by_css_selector(".companySearchHierarchies.gdGrid"):
        
        #click on first result (companies are all huge so will always be first result)
        driver.find_element_by_css_selector(".sqLogoLink").click()
        time.sleep(1)

        # go to salary section
        driver.find_element_by_css_selector("a[data-label='Salaries']").click()

        # finance and accounting ratings only and only yearly pay period
        driver.find_element_by_css_selector(".gd-ui-button.d-none.d-lg-inline-block.css-pitbid").click()
        driver.find_element_by_css_selector("div[data-test='ContentFiltersJobFunctionDropdownContent']").click()
        time.sleep(0.5)
        driver.find_element_by_id("option_1008").click()
        driver.find_element_by_css_selector("div[data-test='dropdown-filter-pay-periodContent']").click()
        time.sleep(0.5)
        driver.find_element_by_id("option_ANNUAL").click()

        # allow time for rating to load
        time.sleep(3)

        count = 0
        while count < 10:

            # grab html from current page and turn to soup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            # extract rating from soup
            salaryset = soup.findAll("div", class_="col-12 col-lg-3 d-flex flex-row flex-md-column justify-content-start justify-content-md-center align-items-end align-items-md-start")
            for j in salaryset:
                sep = '/'
                stripped = j.text.split(sep, 1)[0]
                stripped = stripped.replace("£","")
                stripped = stripped.replace("About","")
                stripped = stripped.replace("K","000")
                stripped = stripped.replace(",","")
                stripped = stripped.replace("SGD ","")
                sep1 = '-'
                if "€" in stripped:
                    continue
                if "$" in stripped:
                    continue
                if len(stripped.split(sep1, 1))==2:
                    stripped = (float(stripped = stripped.split(sep1, 1)[1]))+float(stripped = stripped.split(sep1, 1)[0])/2
                print(float(stripped))

            element = driver.find_element_by_css_selector("button[data-test='pagination-next']")
            driver.execute_script("arguments[0].click();", element)

            count+=1
        
        driver.execute_script("window.scrollTo(0, 0)") 

    # else company has been automatically navigated to
    else:
        time.sleep(1)
        # go to salary section
        driver.find_element_by_css_selector("a[data-label='Salaries']").click()

        # finance and accounting ratings only and only yearly pay period
        driver.find_element_by_css_selector(".gd-ui-button.d-none.d-lg-inline-block.css-pitbid").click()
        driver.find_element_by_css_selector("div[data-test='ContentFiltersJobFunctionDropdownContent']").click()
        time.sleep(0.5)
        driver.find_element_by_id("option_1008").click()
        driver.find_element_by_css_selector("div[data-test='dropdown-filter-pay-periodContent']").click()
        time.sleep(0.5)
        driver.find_element_by_id("option_ANNUAL").click()
        
        # allow time for salaries to load
        time.sleep(3)

        count = 1
        while count < 10:

            # grab html from current page and turn to soup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            # extract rating from soup
            salaryset = soup.findAll("div", class_="col-12 col-lg-3 d-flex flex-row flex-md-column justify-content-start justify-content-md-center align-items-end align-items-md-start")
            for j in salaryset:
                sep = '/'
                stripped = j.text.split(sep, 1)[0]
                stripped = stripped.replace("£","")
                stripped = stripped.replace("About","")
                stripped = stripped.replace("K","000")
                stripped = stripped.replace(",","")
                sep1 = '-'
                if "€" in stripped:
                    continue
                if "$" in stripped:
                    continue
                if len(stripped.split(sep1, 1))==2:
                    stripped = (float(stripped = stripped.split(sep1, 1)[1]))+float(stripped = stripped.split(sep1, 1)[0])/2
                print(float(stripped))

            element = driver.find_element_by_css_selector("button[data-test='pagination-next']")
            driver.execute_script("arguments[0].click();", element)

            count+=1

        driver.execute_script("window.scrollTo(0, 0)") 