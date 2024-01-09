import argparse  # Import the argparse module
import logging
import os
import sys
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# Load environment variables from the .env file
load_dotenv()

# Set up the command line argument parser
parser = argparse.ArgumentParser(description='Script for class swapping')
parser.add_argument('--class1', type=str, default='26742', help='Value for the first class')
parser.add_argument('--class2', type=str, default='30326', help='Value for the second class')
args = parser.parse_args()

# Get the current time in a specific format
current_time = time.strftime("%m%d_%H_%M_%S")

# Set up logging configuration with filename including class1 and class2
log_filename = f'logfile_class1_{args.class1}_class2_{args.class2}_{current_time}.log'
logging.basicConfig(filename=log_filename, filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


service = Service(executable_path='./chromedriver')

# Create Chrome options to avoid "selenium is being controlled by automated test software" notification
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# Disable password manager
prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
chrome_options.add_experimental_option("prefs", prefs)

# Create a new instance of the Chrome driver with Chrome options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to a website
driver.get("https://weblogin.asu.edu/cas/login?service=https%3A%2F%2Fweblogin.asu.edu%2Fcgi-bin%2Fcas-login%3Fcallapp%3Dhttps%253A%252F%252Fwebapp4.asu.edu%252Fmyasu%252F%253Finit%253Dfalse")

# Enter username
username = driver.find_element("name", "username")
username.send_keys(os.getenv("USERNAME"))

# Enter password
password = driver.find_element("name", "password")
password.send_keys(os.getenv("PASSWORD"))

# Press Enter
password.send_keys(Keys.RETURN)
driver.implicitly_wait(10)

is_class_full = True

# Wait for login to complete
time.sleep(10)
# Counter
i = 0
errors = 0

while True and errors <= 10:
    i += 1
    try:
        logging.info(25 * "*")
        logging.info("Beginning attempt %d", i)
        # Enter swap page
        path = "https://webapp4.asu.edu/myasu/?action=swapclass&strm=2237"
        driver.get(path)

        # Choose course to be swappped with
        curr = f"Choose course {args.class1}"
        logging.info("Started %s", curr)
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DERIVED_REGFRM1_DESCR50$4$"))
        )
        dropdown = Select(select_element)
        option_value = args.class1
        try:
            dropdown.select_by_value(option_value)
        except NoSuchElementException:
            logging.info(15 * "!")
            logging.info(15 * "!")
            logging.info(f"Option with value {option_value} not found in the dropdown.")
            logging.info("Hope you got the subject")
            logging.info(15 * "!")
            logging.info(15 * "!")
            driver.quit()
            break
        logging.info("Finished %s", curr)
        logging.info("-----------------------------------------------------------------")
        time.sleep(1)

        # Choose course to be swapped
        curr = f"Choose course {args.class2}"
        logging.info("Started %s", curr)
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DERIVED_REGFRM1_SSR_CLASSNAME_35"))
        )
        dropdown = Select(select_element)
        dropdown.select_by_value(args.class2)
        logging.info("Finished %s", curr)
        logging.info("-----------------------------------------------------------------")

        # Click next button
        curr = "Click next button"
        logging.info("Started %s", curr)
        button_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "SSR_SWAP_FL_WRK_SSR_PB_SRCH"))
        )
        button_element.click()
        logging.info("Finished %s", curr)
        logging.info("-----------------------------------------------------------------")

        # Click Submit at Confirm Class Swap
        curr = "Click Submit at Confirm Class Swap"
        logging.info("Started %s", curr)
        button_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "SSR_ENRL_FL_WRK_SUBMIT_PB"))
        )
        button_element.click()
        logging.info("Finished %s", curr)
        logging.info("-----------------------------------------------------------------")

        # Click Submit on the pop up
        curr = "Click Submit on the pop up"
        logging.info("Started %s", curr)
        button_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "#ICYes"))
        )
        button_element.click()
        # Wait till you get the page with the X
        button_element = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "win8div$ICField243$0"))
        )
        logging.info("Finished %s", curr)
        logging.info("-----------------------------------------------------------------")
        time.sleep(2)
        # if execution worked fully once reset error
        errors = 0
    except Exception as e:
        # Handle the exception if the element is not found within the specified time
        logging.info("Error at %s", curr)
        errors += 1

if errors >= 10:
    log_filename = 'main_logfile.log'
    logging.getLogger().setLevel(logging.INFO)  # Set the logging level
    file_handler = logging.FileHandler(log_filename, mode='a')  # Use append mode
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)

    logging.info(f'logfile for class1_{args.class1} and class2_{args.class2}')
    logging.info("Stopped at attempt %d due to error", i)
    logging.info(15 * "!")
    logging.info(15 * "!")
    file_handler.close()  # Close the file handler
    driver.quit()
    sys.exit(1)
else:
    log_filename = 'main_logfile.log'
    logging.getLogger().setLevel(logging.INFO)  # Set the logging level
    file_handler = logging.FileHandler(log_filename, mode='a')  # Use append mode
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)

    logging.info(f'Exiting class1_{args.class1} and class2_{args.class2}')
    logging.info("Hope you got the subject")
    logging.info(15 * "!")
    logging.info(15 * "!")
    file_handler.close()  # Close the file handler
    driver.quit()
    sys.exit(0)
