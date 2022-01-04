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
companies = ["Morgan Stanley", "Goldman Sachs", "JP Morgan", "Barclays", "UBS", "Credit Suisse", "Citi", "Bank of America", "Deutsche Bank"]
names = [] 
salaries = []
reports = []

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

        # ( toggled off - finance and accounting ratings only) and only yearly pay period
        """
        driver.find_element_by_css_selector(".gd-ui-button.d-none.d-lg-inline-block.css-pitbid").click()
        driver.find_element_by_css_selector("div[data-test='ContentFiltersJobFunctionDropdownContent']").click()
        time.sleep(0.5)
        driver.find_element_by_id("option_1008").click()
        """
        driver.find_element_by_css_selector("div[data-test='dropdown-filter-pay-periodContent']").click()
        time.sleep(0.5)
        driver.find_element_by_id("option_ANNUAL").click()

        # allow time for rating to load
        time.sleep(3)

        # iterate over num pages
        num = 10
        for x in range(num):
            # click next page (unclear on why this works but has to be before beautiful soup callout)
            element = driver.find_element_by_css_selector("button[data-test='pagination-next']")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(1)

            # grab html from current page and turn to soup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            # extract section on salary from soup
            salaryset = soup.findAll("div", class_="css-1u4lhyp py")
            # for each salary in set of salaries on each page
            for j in salaryset:
                # find salary within salary section
                salarydirty = j.findAll("div", class_="col-12 col-lg-3 d-flex flex-row flex-md-column justify-content-start justify-content-md-center align-items-end align-items-md-start")
                # remove /yr
                sep = '/'
                stripped = salarydirty[0].text.split(sep, 1)[0]
                # ignore salaries in other strange currencies (only want pounds)
                if "PLN" in stripped:
                    continue
                if "CHF" in stripped:
                    continue
                if "GGP" in stripped:
                    continue
                if "SGD" in stripped:
                    continue
                if "€" in stripped:
                    continue
                if "$" in stripped:
                    continue
                if "₹" in stripped:
                    continue
                if "AED" in stripped:
                    continue
                # format number
                stripped = stripped.replace("£","")
                stripped = stripped.replace("About","")
                stripped = stripped.replace("K","")
                stripped = stripped.replace(",","")
                # initialise separator
                sep1 = '-'
                # if over 1 million
                if "M" in stripped:
                    # remove M
                    stripped = stripped.replace("M","")
                    # if salary range given
                    if len(stripped.split(sep1, 1))==2:
                        # split string and take average of range
                        stripped = (float(stripped.split(sep1, 1)[1])+float(stripped.split(sep1, 1)[0]))*1000000/2
                else:
                    # if salary range given
                    if len(stripped.split(sep1, 1))==2:
                        # split string and take average of range
                        stripped = (float(stripped.split(sep1, 1)[1])+float(stripped.split(sep1, 1)[0]))*1000/2
                # find number of salaries for specific role reported
                reportsdirty = j.findAll("div", class_="col-12 col-lg-3 d-flex justify-content-center pt-sm pt-lg-0 align-items-center")[0].find("strong")
                # clean it
                report = reportsdirty.text
                report = report.replace(" Salaries", "")
                # add salary and name
                salaries.append(float(stripped))
                names.append(i)
                reports.append(float(report))
        
        # scroll to top to reveal searchbar
        driver.execute_script("window.scrollTo(0, 0)") 

    # else company has been automatically navigated to
    else:
        time.sleep(1)
        # go to salary section
        driver.find_element_by_css_selector("a[data-label='Salaries']").click()

        # ( toggled off - finance and accounting ratings only) and only yearly pay period
        """
        driver.find_element_by_css_selector(".gd-ui-button.d-none.d-lg-inline-block.css-pitbid").click()
        driver.find_element_by_css_selector("div[data-test='ContentFiltersJobFunctionDropdownContent']").click()
        time.sleep(0.5)
        driver.find_element_by_id("option_1008").click()
        """
        driver.find_element_by_css_selector("div[data-test='dropdown-filter-pay-periodContent']").click()
        time.sleep(0.5)
        driver.find_element_by_id("option_ANNUAL").click()
        
        # allow time for salaries to load
        time.sleep(3)

        # iterate over num pages
        num = 10
        for x in range(num):
            element = driver.find_element_by_css_selector("button[data-test='pagination-next']")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(1)

            # grab html from current page and turn to soup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            # extract rating from soup
            salaryset = soup.findAll("div", class_="css-1u4lhyp py")
            # for each salary in set of salaries on each page
            for j in salaryset:
                # find salary within salary section
                salarydirty = j.findAll("div", class_="col-12 col-lg-3 d-flex flex-row flex-md-column justify-content-start justify-content-md-center align-items-end align-items-md-start")
                # remove /yr
                sep = '/'
                stripped = salarydirty[0].text.split(sep, 1)[0]
                # ignore salaries in other strange currencies (only want pounds)
                if "PLN" in stripped:
                    continue
                if "CHF" in stripped:
                    continue
                if "GGP" in stripped:
                    continue
                if "SGD" in stripped:
                    continue
                if "€" in stripped:
                    continue
                if "$" in stripped:
                    continue
                if "₹" in stripped:
                    continue
                if "AED" in stripped:
                    continue
                # format number
                stripped = stripped.replace("£","")
                stripped = stripped.replace("About","")
                stripped = stripped.replace("K","")
                stripped = stripped.replace(",","")
                # initialise separator
                sep1 = '-'
                # if salary 1 million plus
                if "M" in stripped:
                    # remove M
                    stripped = stripped.replace("M","")
                    # if salary range given
                    if len(stripped.split(sep1, 1))==2:
                        # split string and take average of range
                        stripped = (float(stripped.split(sep1, 1)[1])+float(stripped.split(sep1, 1)[0]))*1000000/2
                else:
                    # if salary range given
                    if len(stripped.split(sep1, 1))==2:
                        # split string and take average of range
                        stripped = (float(stripped.split(sep1, 1)[1])+float(stripped.split(sep1, 1)[0]))*1000/2
                # find number of salaries for pecific role reported
                reportsdirty = j.findAll("div", class_="col-12 col-lg-3 d-flex justify-content-center pt-sm pt-lg-0 align-items-center")[0].find("strong")
                # clean it
                report = reportsdirty.text
                report = report.replace(" Salaries", "")
                #add name and salary to list
                salaries.append(float(stripped))
                names.append(i)
                reports.append(float(report))

        # scroll to top to reveal searchbar
        driver.execute_script("window.scrollTo(0, 0)") 

# convert list to dataframe
df = pd.DataFrame([[i for i in names],[i for i in salaries],[i for i in reports]]).T

#name columns
df.columns = ['Firm', 'Salary', 'Reports']

# remove strangely large outliers
df = df.loc[df['Salary'] <= 1000000]

# remove below pro rata 40 hr week UK min wage
df = df.loc[df['Salary'] > 16500]

df.to_csv('BanksData_all.csv')

dfs = []
# create df with weightings for each firm
for i in companies:
    # create df for each firm
    df1 = df.loc[df['Firm'] == i]
    # sum of reports
    totalreports = df1['Reports'].sum()
    # weight = no of report over total reports
    df1['weight'] = df1['Reports']/totalreports
    # add to list of dfs
    dfs.append(df1)

# stack the dfs from each firm
df = pd.concat(dfs)

# salary * weight to get contribution to weighted average from each role
df['Average salary'] = df['Salary']*df['weight']

# sum up total for weighted average in average salary column
df = df.groupby("Firm").sum()
df.to_csv('BanksAverage.csv')
print(df)