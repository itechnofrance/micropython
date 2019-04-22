#
# Récupère les informations météo sur le site OpenWeatherMap
# Récupère l'heure et l'offset UTC sur le site Worldtimeapi.org
#
# Matériel :
#             ESP32 ou ESP8266
#             MicroPython 1.10
#
# Auteur : iTechnoFrance
#
import network
import time
import machine
import json
import urequests
from machine import RTC

ssid = "Livebox-C176"
password = "6mYkruxEfmxcwZeS5e"
adresse_openweathermap = "http://api.openweathermap.org/data/2.5/weather?lat=50.02&lon=1.31&units=metric&APPID="
cle_api_openweathermap = "d4b13a3b9b03a89d13a7613b32d69955"
url_openweathermap = adresse_openweathermap + cle_api_openweathermap
url_worldtimeapi = "http://worldtimeapi.org/api/timezone/Europe/Paris"
requete_web_delai = 60000  # effectue une requête toutes les 60s
liste_jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
liste_mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
              "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

def connect_wifi():
    global wifi
    wifi = network.WLAN(network.STA_IF)  # création client d'accès WiFi
    wifi.active(True)  # activation du client d'accès WiFi   
    wifi.connect(ssid, password)
    while not wifi.isconnected():  # connexion au point d'accès WiFi
        pass

def convert_epoch_time(temps):
    # Epoch time Linux démarre le 1 janvier 1970
    # Epoch time ESP32 démarre le 1 janvier 2000
    # donc il faut soustraire le temps de 946,684,800 secondes (30 ans)
    temps -= 946684800
    (u_annee, u_mois, u_jour, u_heure, u_minute, u_seconde, u_jour_semaine, u_jour_annee) = time.localtime(temps)
    return u_annee, u_mois, u_jour, u_heure, u_minute, u_seconde, u_jour_semaine

def traite_date_heure():
    global heure_offset, operation_offset, annee, mois, date, heure, minute, seconde, jour, rtc
    reponse = urequests.get(url_worldtimeapi)  # effectue la requête Web
    if reponse.status_code == 200:  # requête ok
        data = json.loads(reponse.text)  # transforme les données JSON en objet Python
        temps_unix = int(data.get("unixtime"))
        annee, mois, date, heure, minute, seconde, jour = convert_epoch_time(temps_unix)
        heure_offset = data.get("utc_offset")  # on récupére l'offset 
        operation_offset = heure_offset[0]  # récupère l'opérateur + ou -
        heure_offset = int(heure_offset[2:3]) # récupère uniquement les heures
        if operation_offset == "+":
            heure += heure_offset
        if operation_offset == "-":
            heure -= heure_offset
        rtc.datetime((annee, mois, date, 0, heure, minute, seconde, 0))  # MAJ horloge interne
        mois = liste_mois[int(mois) - 1]
        jour = liste_jours[jour]
        
def traite_openweathermap():
    global temperature, pression, humidite, lever_soleil, coucher_soleil, vent_vitesse, vent_orientation
    reponse = urequests.get(url_openweathermap)  # effectue la requête Web
    if reponse.status_code == 200:  # requête ok
        data = json.loads(reponse.text)  # transforme les données JSON en objet Python
        temperature = data.get("main").get("temp")
        pression = data.get("main").get("pressure")
        humidite = data.get("main").get("humidity")
        annee_s, mois_s, date_s, heure_s, minute_s, seconde_s, jour_s = convert_epoch_time(data.get("sys").get("sunrise"))
        if operation_offset == "+":
            heure_s += heure_offset
        if operation_offset == "-":
            heure_s -= heure_offset
        lever_soleil = "{0:02}:{1:02}:{2:02}".format(heure_s, minute_s, seconde_s)
        annee_s, mois_s, date_s, heure_s, minute_s, seconde_s, jour_s = convert_epoch_time(data.get("sys").get("sunset"))
        if operation_offset == "+":
            heure_s += heure_offset
        if operation_offset == "-":
            heure_s -= heure_offset
        coucher_soleil = "{0:02}:{1:02}:{2:02}".format(heure_s, minute_s, seconde_s)
        vent_vitesse = data.get("wind").get("speed")  # vitesse du vent en m/s
        vent_vitesse *= 3.6  # conversion du vent en Km/h
        vent_orientation = data.get("wind").get("deg")  # origine du vent en ° (0° --> Nord)
        
rtc = RTC()  # horloge temps réel interne
connect_wifi()
compteur = time.ticks_ms() - requete_web_delai  # initialise le compteur

while True:
    if not wifi.isconnected():  # si perte connexion WiFi alors reboot
        machine.reset()
    if time.ticks_ms() - compteur >= requete_web_delai: # test si 60s sont passées
        traite_date_heure()
        traite_openweathermap()
        time_str = "{:02}:{:02}:{:02}".format(rtc.datetime()[4], rtc.datetime()[5], rtc.datetime()[6])
        print((jour) + " " + str(date) + " " + (mois) + " " + str(annee))
        print(time_str)
        print("Température : " + str(temperature) + "°C, Pression : " + str(pression) + " hPa, Taux d'humidité : " + str(humidite) + "%")    
        print("Lever Soleil : " + (lever_soleil) + ", Coucher Soleil : " + (coucher_soleil))
        print("Vitesse du vent : " + str(vent_vitesse) + " Km/h, Orientation : " + str(vent_orientation) + "°")
        compteur = time.ticks_ms()  # maj du compteur