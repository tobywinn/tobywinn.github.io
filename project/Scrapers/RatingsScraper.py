from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd

PATH = '/Applications/chromedriver'

driver = webdriver.Chrome(PATH)

ratings = []
names=[]

driver.get("https://www.glassdoor.co.uk")

# Fill in email
driver.find_element_by_css_selector(".d-none.d-lg-block.p-0.LockedHomeHeaderStyles__signInButton").click()
time.sleep(2)


# Fill in password
driver.find_element_by_id("userEmail").send_keys("tobywinn@rocketmail.com")
driver.find_element_by_id("userPassword").send_keys("Teddybear1!")

# click accept cookies to reveal sign up button
driver.find_element_by_id("onetrust-accept-btn-handler").click()

time.sleep(1)

# try to click sign in
element = driver.find_element_by_name("submit")
driver.execute_script("arguments[0].click();", element)

time.sleep(3)

# navigate to companies section 
driver.find_element_by_link_text("Companies").click()

# Fill in companies to search
companies = ["Morgan Stanley", "Goldman Sachs", "JP Morgan", "Barclays", "UBS", "Credit Suisse", "Citi", "Bank of America", "Deutsche Bank"]

for i in companies:

    # clear search bar, search name of company
    driver.find_element_by_id("sc.keyword").clear()
    driver.find_element_by_id("sc.keyword").send_keys(i)
    driver.find_element_by_id("sc.keyword").send_keys(Keys.RETURN)

    # if company is not automatically navigated to 
    if driver.find_elements_by_css_selector(".companySearchHierarchies.gdGrid"):
        
        #click on first result (companies are all huge so will always be first result)
        driver.find_element_by_css_selector(".sqLogoLink").click()

        # go to reviews section
        driver.find_element_by_css_selector("a[data-label='Reviews']").click()

        """
        # finance and accounting ratings only
        driver.find_element_by_css_selector(".gd-ui-button.d-none.d-lg-inline-block.css-pitbid").click()
        driver.find_element_by_css_selector("div[data-test='ContentFiltersJobFunctionDropdownContent']").click()
        time.sleep(1)
        driver.find_element_by_id("option_1008").click()
        """

        # allow time for refresh
        time.sleep(2)

        # uk only
        driver.find_element_by_css_selector(".gd-ui-button.d-none.d-lg-inline-block.css-pitbid").click()
        driver.find_element_by_css_selector("div[data-test='ContentFiltersSelectalocationDropdownContent']").click()
        driver.find_element_by_id("option_N,2").click()

        # allow time for rating to load
        time.sleep(3)
        
        driver.execute_script("window.scrollTo(0, 0)") 

        # grab html from current page and turn to soup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # extract rating from soup
        rating = soup.find("div", class_="v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__large")
        ratings.append(float(rating.text))
        names.append(i)

    # else company has been automatically navigated to
    else:
        # go to reviews section
        driver.find_element_by_css_selector("a[data-label='Reviews']").click()

        """
        # finance and accounting ratings only
        driver.find_element_by_css_selector(".gd-ui-button.d-none.d-lg-inline-block.css-pitbid").click()
        driver.find_element_by_css_selector("div[data-test='ContentFiltersJobFunctionDropdownContent']").click()
        time.sleep(2)
        driver.find_element_by_id("option_1008").click()
        """

        # allow time for refresh
        time.sleep(2)

        # uk only
        driver.find_element_by_css_selector(".gd-ui-button.d-none.d-lg-inline-block.css-pitbid").click()
        driver.find_element_by_css_selector("div[data-test='ContentFiltersSelectalocationDropdownContent']").click()
        driver.find_element_by_id("option_N,2").click()

        # allow time for rating to load
        time.sleep(3)

        driver.execute_script("window.scrollTo(0, 0)") 

        # grab html from current page and turn to soup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # extract rating from soup
        rating = soup.find("div", class_="v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__large")
        ratings.append(float(rating.text))
        names.append(i)

print(names,ratings)

names1 = []
ratings1 = []

while len(names1)<54:
    for i in names:
        names1.append(i)

while len(ratings1)<54:
    for i in ratings:
        ratings1.append(i)
    
#plug in data manually from arkensden
compensation = [174, 170, 171, 170, 165, 151, 150, 160, 158, 
                195, 198, 212, 213, 203, 175, 180, 189, 188, 
                232, 233, 239, 228, 226, 202, 218, 218, 225, 
                270, 248, 297, 270, 256, 242, 262, 266, 254, 
                304, 295, 314, 289, 291, 269, 287, 282, 293, 
                332, 315, 342, 320, 316, 287, 306, 308, 309]

seniority = []

for i in ["Associate 1/2", "Associate 2/3", "Associate 3/4", "VP 1", "VP 2", "VP 3"]:
  counter = 0
  while counter < 9:
    counter += 1
    seniority.append(i)

df = pd.DataFrame([[i for i in names], [i for i in ratings]]).T
df.columns = ['Firm', 'Rating']

df.to_csv("BanksRatings.csv")

df = pd.DataFrame([[i for i in names1],[i for i in ratings1], [i for i in compensation], [i for i in seniority]]).T
df.columns = ['Firm', 'Rating', 'Compensation', 'Seniority']
print(df)

# export csv
# df.to_csv('GlassdoorRatings&Salary.csv')