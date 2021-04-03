import csv
import os
import sys
import time

from datetime import timedelta, datetime
from random import randrange, choice

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


ZIP_CODES = [63123,63021,63011,63137,63134,63144,63044,
             63017,63105,63128,63126,63141,63131,63045,
             63025,63026,63135,63031,63033,63042,63136,
             63140,63122,63124,63125,63143,63043,63121,
             63129,63034,63132,63114,63133,63117,63146,
             63074,63127,63130,63088,63119,63038,63040]


def get_job_data(job):
    with open('jobs_final.csv') as jobs:
        reader = csv.reader(jobs)
        next(reader)
        for row in reader:
            if row[0] == job:
                print(f'Found bot job for {row[0]}!')
                return row
        print('No matching jobs!')


def get_options():
    options = Options()
    # ua = UserAgent()
    # userAgent = ua.random
    # options.add_argument(f'user-agent={userAgent}')
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    return options

def random_year():
    years = list(range(50,99))
    year_choice = choice(years)
    return str(year_choice)



def run(category, iterations):
    # proxy_list = get_proxies()
    count = 0
    print(f'Running the bot {iterations} times!')
    time.sleep(2)
    job_data = get_job_data(category)
    for i in range(iterations):
        with open('names.csv') as names:
            reader = csv.reader(names)
            next(reader)
            chosen_row = choice(list(reader))
            # chosen_proxy = choice(proxy_list)
            driver = webdriver.Chrome('./chromedriver', options=get_options())

            # Open URL in webdriver
            driver.get(job_data[1])
            time.sleep(5)
            strode_element = driver.find_element_by_xpath("//*[contains(text(), 'Strode')]")
            strode_element.click()
            time.sleep(4)

            vote = driver.find_element_by_css_selector('button.vote-button')
            vote.click()

            time.sleep(2)
            email = driver.find_element_by_class_name('ssEmailTextboxField')
            email.send_keys(chosen_row[2])
            print(f"Filling in email input with {chosen_row[2]}")
            time.sleep(1)
            email.send_keys(Keys.RETURN)
            time.sleep(4)

            # try:
            first_name = driver.find_element_by_xpath('//span[text()="First Name"]/following::span/following::input')
            first_name.clear()
            print(f"Filling in first name with {chosen_row[0]}")
            first_name.send_keys(chosen_row[0])
            time.sleep(1)

            last_name = driver.find_element_by_xpath('//span[text()="Last Name"]/following::span/following::input')
            last_name.clear()
            print(f"Filling in first name with {chosen_row[1]}")
            last_name.send_keys(chosen_row[1])
            time.sleep(1)

            postal_code = driver.find_element_by_xpath('//span[text()="Postal Code"]/following::span/following::input')
            postal_code.clear()
            zip_code = choice(ZIP_CODES)
            postal_code.send_keys(str(zip_code))
            time.sleep(1)

            birthdate = driver.find_element_by_xpath('//span[text()="Birthdate"]/following::input')
            birthdate.send_keys(f'{randrange(12)}{randrange(27)}19{random_year()}')
            birthdate.send_keys(Keys.RETURN)
            time.sleep(10)


    #         email = driver.find_element_by_class_name('ssEmailTextboxField')
    #         email.send_keys(chosen_row[2])
    #         print(f"Filling in email address with {chosen_row[2]}")
    #         time.sleep(2)
    #         email.send_keys(Keys.RETURN)
    #         time.sleep(2)
    #
    #         try:
    #             first_name = driver.find_element_by_xpath('//span[text()="First Name"]/following::span/following::input')
    #             first_name.clear()
    #             print(f"Filling in first name with {chosen_row[0]}")
    #             first_name.send_keys(chosen_row[0])
    #         except NoSuchElementException:
    #             driver.close()
    #             print("Can't get around the captcha")
    #             time.sleep(2)
    #             continue
    #
    #         last_name = driver.find_element_by_xpath('//span[text()="Last Name"]/following::span/following::input')
    #         last_name.clear()
    #         last_name.send_keys(chosen_row[1])
    #         print(f"Filling in last name with {chosen_row[1]}")
    #
    #         postal_code = driver.find_element_by_xpath('//span[text()="Postal Code"]/following::span/following::input')
    #         postal_code.clear()
    #         zip_code = choice(ZIP_CODES)
    #         postal_code.send_keys(str(zip_code))
    #
    #         birthdate = driver.find_element_by_xpath('//span[text()="Birthdate"]/following::input')
    #         birthdate.send_keys(f'{randrange(12)}/{randrange(27)}/19{random_year()}')
    #         birthdate.send_keys(Keys.RETURN)
    #
    #         time.sleep(2)
    #         driver.close()
    #         count +=1
    #         time.sleep(5)
    #         print(count)
    # print(f'Successful submissions: {count}')
    #

if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(sys.argv[1],3)
    elif len(sys.argv) == 3:
        run(sys.argv[1],int(sys.argv[2]))
    else:
        print(f'Need to provide a job name (iggy, biffnshow, archview, designaire) and a number of runs')
