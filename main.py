from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time 
import os 
import glob 
import smtplib
from email.message import EmailMessage

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')

User = {
    "User1":{"Prénom": "prénom", "Nom":"nom", "Lieu": "lieu", "Date": "date", "Adresse":"adresse", "Ville": "ville", "Zipcode": "zip", "Mail": "mail" }, 
    "User2":{"Prénom": "prénom", "Nom": "nom", "Lieu": "lieu", "Date": "date", "Adresse":"adresse", "Ville": "ville", "Zipcode": "Zipcode", "Mail": "mail"}
}

def latest_file():
    list_of_files = glob.glob("D:/Téléchargements/*")
    latest = max(list_of_files, key = os.path.getctime)
    return latest

def send_mail(qui):
    msg = EmailMessage()
    msg['Subject'] = "Attestation"
    msg['From'] = EMAIL
    msg['To'] = User[qui]['Mail']
    u = latest_file()
    files = [u]
    for file in files:
        with open (file, 'rb') as f:
            file_data = f.read()
            file_name = f.name

        msg.add_attachment(file_data, maintype = 'application', subtype = 'octet-stream', filename = file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)



while True: 
    qui = input("Quel utilisateur ? ?")
    if qui == "User1" or qui == "User2":
        break
    else: 
        ("Mauvais utilisateur")

heure_sortie = input('Heure de sortie ? format hhmm')

driver = webdriver.Chrome()

driver.get("https://media.interieur.gouv.fr/deplacement-covid-19/")

#Vérifier si nouvelle version 


"""driver.find_element_by_xpath('//*[@id="reload-btn"]').click()"""

firstname = driver.find_element_by_name("firstname")
firstname.send_keys(User[qui]["Prénom"])

lastname = firstname = driver.find_element_by_name("lastname")
lastname.send_keys(User[qui]["Nom"])

birthday = driver.find_element_by_name("birthday")
birthday.send_keys(User[qui]["Date"])

lieunaissance = driver.find_element_by_name("lieunaissance")
lieunaissance.send_keys(User[qui]["Lieu"])

address = driver.find_element_by_name("address")
address.send_keys(User[qui]["Adresse"])

town = driver.find_element_by_name("town")
town.send_keys(User[qui]["Ville"])

zipcode = driver.find_element_by_name("zipcode")
zipcode.send_keys(User[qui]["Zipcode"])

motif = driver.find_element_by_xpath('//*[@id="checkbox-sport"]')
motif.click()
time.sleep(0.5)

dt = datetime.datetime.today()
jour = dt.day
mois = dt.month 
annee = dt.year

if jour < 10:
    jour = str(jour)
    jour = jour.zfill(2)

date_sortie = driver.find_element_by_xpath('//*[@id="field-datesortie"]')
date_sortie.send_keys(jour)
time.sleep(0.1)
date_sortie.send_keys(mois)
time.sleep(0.1)
date_sortie.send_keys("2020")


sortie = driver.find_element_by_xpath('//*[@id="field-heuresortie"]')
sortie.send_keys(heure_sortie)

bouton = driver.find_element_by_xpath('//*[@id="generate-btn"]')
try : 
    bouton.click()
except:
    print("Error")

print("Attestation téléchargée")
time.sleep(0.4)
print("Envoi du mail")
send_mail(qui)

driver.quit()
