from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import os
import logging
import stat
import time
import pytz
import schedule
import datetime
import random
import requests
import json
from datetime import datetime, timedelta

# Set the timezone and allowed days
PARIS_TZ = pytz.timezone("Europe/Paris")

# Set color for better printing
GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"

# Set variable with env from docker-compose
USERNAME = os.getenv("Us")
PASSWORD = os.getenv("Pa")
FORMATION = os.getenv("FORMATION")
A = os.getenv("ANNEE")
TP = os.getenv("TP")
blacklist = os.getenv("blacklist")

if USERNAME == 'USER' or PASSWORD == 'PASS' or A == "X" or TP == "X" or FORMATION == "X":
    print(f"[{RED}-{RESET}] Vous devez d'abord définir les variables d'environnements dans le docker-compose.yml")
    time.sleep(5)
    quit()

TP = int(TP)
if not 1 <= TP <= 6:
    print(f"[{RED}-{RESET}] Votre TP doit être compris entre 1 et 6")
    quit()

if not (FORMATION == "cyberdefense" or FORMATION == "cyberdata" or FORMATION == "cyberlog"):
    print(f"[{RED}-{RESET}] Votre FORMATION doit être cyberdefense, cyberdata ou cyberlog")
    quit()

if A == "3":
    S = 5
    URL_PLANNING =  f"https://planningsup.app/api/v1/calendars?p=ensibs.{FORMATION}.{A}emeannee.semestre{S}s{S}.tp{TP}"
    URL_PLANNING += f",ensibs.{FORMATION}.{A}emeannee.semestre{S+1}s{S+1}.tp{TP}"
elif A == "4":
    S = 7
    URL_PLANNING =  f"https://planningsup.app/api/v1/calendars?p=ensibs.{FORMATION}.{A}emeannee.semestre{S}s{S}.tp{TP}"
    URL_PLANNING += f",ensibs.{FORMATION}.{A}emeannee.semestre{S+1}s{S+1}.tp{TP}"
elif A == "5":
    URL_PLANNING =  f"https://planningsup.app/api/v1/calendars?p=ensibs.{FORMATION}.{A}emeannee.tp{TP}"
else:
    print(f"[{RED}-{RESET}] Votre ANNEE doit être 3, 4 ou 5")
    quit()

if blacklist:
    blacklists = blacklist.split(", ")
else:
    blacklists = []

logging.basicConfig(
    filename='emargement.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

# Set options for selenium
options = Options()
options.add_argument('-headless')

def filter_events(events):
    """Filter the events to only keep the ones we want to emerge"""
    filtered_events = []
    for event in events:
        if not any(blacklist in event["name"] for blacklist in blacklists):
            filtered_events.append(event)
    return filtered_events

def hours_Emarge():
    """From the API, get each courses and their starting hours for today"""
    response = requests.get(URL_PLANNING)
    try:
        data = response.json()
    except json.decoder.JSONDecodeError:
        logging.error("Impossible de récupérer les données de l'API, vérifiez votre ANNEE, SEMESTRE et TP")
        print(f"[{RED}-{RESET}] Impossible de récupérer les données de l'API, vérifiez votre ANNEE, SEMESTRE et TP")
        quit()

    today_str = datetime.now(PARIS_TZ).strftime("%Y-%m-%d")
    # Extract relevant fields and convert timestamps
    events = [
        {
            "name": event["name"],
            "start": datetime.fromtimestamp(event["start"] / 1000, tz=PARIS_TZ),
            "end": datetime.fromtimestamp(event["end"] / 1000, tz=PARIS_TZ),
        }
        for planning in data.get("plannings", [])
        for event in planning.get("events", [])
        if (datetime.fromtimestamp(event["start"] / 1000, tz=PARIS_TZ)).strftime("%Y-%m-%d") == today_str
        and (datetime.fromtimestamp(event["start"] / 1000, tz=PARIS_TZ)) + timedelta(minutes=15) > datetime.now(PARIS_TZ)
        and 8 <= (datetime.fromtimestamp(event["start"] / 1000, tz=PARIS_TZ)).hour <= 18
    ]

    # Return the list of events of today
    return events

def emarge(course_name):
    """Perform all the process like a normal student to emerge"""
    options.set_preference("general.useragent.override", f"{UserAgent(os='Linux').random}")
    driver = webdriver.Firefox(options=options, service=Service("geckodriver"))

    logging.info(f"Ouverture du navigateur Selenium pour {course_name}")
    print(f"[{BLUE}+{RESET}] Ouverture du navigateur Selenium pour {course_name}")

    driver.get("https://moodle.univ-ubs.fr/")
    time.sleep(5)

    # Select UBS on the mir
    select_element = driver.find_element(By.ID, "idp")
    dropdown = Select(select_element)
    dropdown.select_by_visible_text("Université Bretagne Sud - UBS")
    select_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary')]")
    select_button.click()
    time.sleep(5)

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
        print(f"[{RED}-{RESET}] Identifiant ou mot de passe incorrect")
        logging.warning("Identifiant ou mot de passe incorrect")
        driver.quit()
        quit()
    except NoSuchElementException:
        logging.info("Connexion réussie")
    time.sleep(10)

    try: 
        # Click on the first result that contains "Émargement"
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        target_span = soup.find('span', class_='sr-only', string='ENSIBS : Émargement')
        link = target_span.find_next('a')
        href = link.get('href')
        driver.get(href)
        time.sleep(5)

    except:
        logging.warning("Impossible de trouver le lien d'émargement")
        print(f"[{RED}-{RESET}] Impossible de trouver le lien d'émargement")
        driver.quit()
        quit()

    # Click on the "Présence" link
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        activity_divs = soup.find_all('div', class_='activityname')
        for div in activity_divs:
            if "Présence" in div.text:
                link = div.find('a')['href']
                driver.get(link)
                time.sleep(5)
                break
    except:
        logging.warning("Impossible de trouver le lien d'attendance")
        print(f"[{RED}-{RESET}] Impossible de trouver le lien d'attendance")
        driver.quit()
        quit()

    # Click on the "Envoyer le statut de présence"
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        link = soup.find('a', string='Envoyer le statut de présence')
        href = link.get('href')
        driver.get(href)
        time.sleep(2)
        print(f"[{GREEN}*{RESET}] Emargement réussi")
        logging.info("Emargement réussi")
    except:
        logging.warning("Impossible d'émarger")
        print(f"[{RED}-{RESET}] Impossible d'émarger")

    driver.quit()
    time.sleep(20)

def schedule_random_times():
    """Randomly choose when to emerge for each events for today"""
    schedule.clear()
    schedule.every().day.at("7:00").do(schedule_random_times)
    times = []

    # Check if current day is weekend (5 = Saturday, 6 = Sunday)
    if datetime.now(PARIS_TZ).weekday() >= 5:
        return

    # Get from the API all the courses of the student for today
    events_today = hours_Emarge()
    events_filtered = filter_events(events_today)

    for event in events_filtered:
        start_hour = (event["start"] + timedelta(minutes=random.randint(15, 25))).strftime("%H:%M")
        schedule.every().day.at(start_hour).do(lambda event_name=event["name"]: emarge(event_name))
        times.append(f"{start_hour}")

    if times:
        times.sort()
        logging.info(f"Emargement prévu à {', '.join(times)}")
        print(f"[{BLUE}+{RESET}] Emargement prévu à {', '.join(times)}")
    else:
        logging.info("Aucun cours à venir aujourd'hui")
        print(f"[{BLUE}+{RESET}] Aucun cours à venir aujourd'hui")

schedule_random_times()

# While loop to check every minute if it's the time to emarge
while True:  
    schedule.run_pending()
    time.sleep(60)
