from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import os
import logging
import stat
import time
import pytz
import schedule
import datetime
import random

# Set the timezone and allowed days
PARIS_TZ = pytz.timezone("Europe/Paris")
ALLOWED_DAYS = {0, 1, 2, 3, 4}

# Set color for better printing
GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"

# Set variable with env from docker-compose
USERNAME = os.getenv("Us")
PASSWORD = os.getenv("Pa")
if USERNAME == 'USER' or PASSWORD == 'PASS':
    print(f"[{RED}-{RESET}] Vous devez d'abord définir vos identifiants dans le docker-compose.yml")
    quit()
COURSE_URL = "https://moodle.univ-ubs.fr/course/view.php?id=" + os.getenv("CourseID")
ATTENDANCE_URL = "https://moodle.univ-ubs.fr/mod/attendance/view.php?id=" + os.getenv("AttendanceID")

logging.basicConfig(
    filename='emargement.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

# Set options for selenium
options = Options()
options.add_argument('-headless')

service = Service(executable_path=f"geckodriver")

def emarge():
    """Perform all the process like a normal student to emerge"""
    driver = webdriver.Firefox(options=options, service=service)

    logging.info("Ouverture du navigateur Selenium")
    print(f"[{BLUE}+{RESET}] Ouverture du navigateur Selenium")

    driver.get("https://moodle.univ-ubs.fr/")
    time.sleep(0.5)

    # Select UBS on the mir
    select_element = driver.find_element(By.ID, "idp")
    dropdown = Select(select_element)
    dropdown.select_by_visible_text("Université Bretagne Sud - UBS")
    select_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary')]")
    select_button.click()
    time.sleep(1)

    # Enter USERNAME / PASSWORD and submit them
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(USERNAME)
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(PASSWORD)
    login_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary')]")
    login_button.click()

    # Check if the mir accepted our credentials
    try:
        driver.find_element(By.ID, "loginErrorsPanel")
        print(f"[{RED}-{RESET}] Mauvais identifiant ou mot de passe")
        logging.warning("Mauvais identifiant ou mot de passe")
        driver.quit()
        quit()
    except NoSuchElementException:
        logging.info("Connection réussi")
        print(f"[{GREEN}*{RESET}] Connection réussi")
    time.sleep(2)

    # Go to the right URL to emerge
    driver.get(COURSE_URL)
    time.sleep(1)
    driver.get(ATTENDANCE_URL)
    time.sleep(1)

    # Check if the button to emerge is here, if yes, we click it
    try:
        link_element = driver.find_element(By.XPATH, "//a[contains(text(), 'Envoyer le statut de présence')]")
        link_href = link_element.get_attribute("href")
        driver.get(link_href)
        time.sleep(2)
        logging.info("Emargement réussi")
        print(f"[{GREEN}*{RESET}] Emargement réussi")

    except NoSuchElementException:
        logging.warning("Impossible d'émarger")
        print(f"[{RED}-{RESET}] Impossible d'émarger")

    driver.quit()
    print(f"[{GREEN}*{RESET}] Fermeture du navigateur Selenium")
    time.sleep(50)

def schedule_random_times():
    """Randomly choose when to emerge"""
    schedule.clear()
    now = datetime.datetime.now(PARIS_TZ)
    time = []

    if now.weekday() in ALLOWED_DAYS:
        time.append(f"08:{random.randint(5, 14):02d}")
        time.append(f"09:{random.randint(50, 59):02d}")
        time.append(f"11:{random.randint(35, 44):02d}")
        time.append(f"13:{random.randint(5, 14):02d}")
        time.append(f"14:{random.randint(50, 59):02d}")
        time.append(f"16:{random.randint(35, 44):02d}")
        time.append(f"18:{random.randint(20, 29):02d}")

        for item in time:
            schedule.every().day.at(item).do(emarge)

        logging.info(f"Emargement prévu à {', '.join(time)}")
        print(f"[{BLUE}+{RESET}] Emargement prévu à {', '.join(time)}")

# Emerge right away to be sure we don't miss the first one
emarge()
schedule_random_times()

# Choose a new random times to emerge for today
schedule.every().day.at("00:00").do(schedule_random_times)

# While loop to check every minute if it's the time to emerge
while True:
    now = datetime.datetime.now(PARIS_TZ)

    for job in schedule.get_jobs():
        job_time = job.at_time
        if now.time().hour == job_time.hour and now.time().minute == job_time.minute:
            job.job_func()

    schedule.run_pending()
    time.sleep(60)
