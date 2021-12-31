from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

PATH = '/Applications/chromedriver'

driver = webdriver.Chrome(PATH)

ratings = []
names=[]

firms = ['Numis-Securities', 'JPMorgan-Chase', 'Goldman-Sachs', 'Citi', 'Barclays', 'Credit-Suisse', 'UBS', 'Morgan-Stanley','Bank-of-America']

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

# click sign up
element = driver.find_element_by_css_selector(".gd-ui-button.minWidthBtn.css-1dqhu4c")
driver.execute_script("arguments[0].click();", element)

#allow time to click sign in
time.sleep(5)

driver.find_element_by_link_text("Companies").click()

companies = ["Numis", "Goldman Sachs", "Morgan Stanley"]
for i in companies:

    driver.find_element_by_id("sc.keyword").clear()
    driver.find_element_by_id("sc.keyword").send_keys(i)
    driver.find_element_by_id("sc.keyword").send_keys(Keys.RETURN)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    rating = soup.find("div", class_="mr-xsm css-1c86vvj eky1qiu0")
    print(float(rating.text))


