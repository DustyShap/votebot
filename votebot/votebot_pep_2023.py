import csv
import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
from random import randrange, choice

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

screen_dims = [(375, 667), (411, 731), (360, 640), (414, 736), (375, 812),
               (768, 1024), (1024, 1366), (540, 720)]
ZIP_CODES = [63123,63021,63011,63137,63134,63144,63044,
             63017,63105,63128,63126,63141,63131,63045,
             63025,63026,63135,63031,63033,63042,63136,
             63140,63122,63124,63125,63143,63043,63121,
             63129,63034,63132,63114,63133,63117,63146,
             63074,63127,63130,63088,63119,63038,63040]


def get_options():
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    print(f"Using user agent {userAgent}")
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_argument(f'--proxy-server={proxy}')
    return options

def random_year():
    years = list(range(50,99))
    year_choice = choice(years)
    return str(year_choice)

def get_proxies():
    response = requests.get('https://www.sslproxies.org/')
    soup = BeautifulSoup(response.text,"html.parser")
    proxies = []
    for item in soup.select("table.table tbody tr"):
        if not item.select_one("td"):break
        ip = item.select_one("td").text
        port = item.select_one("td:nth-of-type(2)").text
        proxies.append(f"{ip}:{port}")
    return proxies



def run(iterations):
    proxy_list = get_proxies()
    count = 0
    print(f'Running the bot {iterations} times!')
    time.sleep(2)
    for i in range(iterations):
        with open('names.csv') as names:
            reader = csv.reader(names)
            next(reader)
            chosen_row = choice(list(reader))
            # chosen_proxy = choice(proxy_list)
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=get_options())
            time.sleep(3)
            print(f'Chosen Proxy: {chosen_proxy}')
            driver.get("https://embed-953108.secondstreetapp.com/embed/7f6dc4de-93fc-4e72-b487-56fa670a8063/gallery/363342601")
            time.sleep(10)
            nomination = driver.find_element(By.CLASS_NAME, "ssButtonPrimary")
            nomination.click()


            time.sleep(2)
            email = driver.find_element(By.CLASS_NAME, "ssEmailTextboxField")
            email.send_keys(chosen_row[2])
            print(f"Filling in email address with {chosen_row[2]}")
            time.sleep(2)
            email.send_keys(Keys.RETURN)
            time.sleep(3)


            first_name = driver.find_element("xpath", '//span[text()="First Name"]/following::span/following::input')
            first_name.clear()
            print(f"Filling in first name with {chosen_row[0]}")
            first_name.send_keys(chosen_row[0])

            time.sleep(2)
            last_name = driver.find_element('xpath', '//span[text()="Last Name"]/following::span/following::input')
            last_name.clear()
            last_name.send_keys(chosen_row[1])
            print(f"Filling in last name with {chosen_row[1]}")

            time.sleep(2)
            postal_code = driver.find_element('xpath', '//span[text()="Postal Code"]/following::span/following::input')
            postal_code.clear()
            zip_code = choice(ZIP_CODES)
            postal_code.send_keys(str(zip_code))
            time.sleep(2)
            postal_code.send_keys(Keys.RETURN)

            time.sleep(30)
            driver.close()
            count +=1

            print(f'Total submissions: {count}')


if __name__ == '__main__':

    run(int(sys.argv[1]))
else:
    print(f'Need to provide a job name (iggy, biffnshow, archview, designaire) and a number of runs')
