#
# Utilisation du détecteur de gestes PAJ7620 pour gérer des menus
# sur écran OLED SSD1306
#
# Materiel :
#            Testé sur ESP32 Heltec Wifi Kit 32
#            Ecran OLED SSD1306 integré
#            PAJ7620
#            MicroPython version 1.10
#
# Programme qui permet de sélectionner un menu par geste 
# Gestes utilisés :
#                   haut / bas pour la sélection d'une option
#                   rotation horaire du doigt pour entrer dans le menu suivant ou effectuer une action
#                   rotation anti-horaire du doigt pour revenir au menu precedent ou effectuer une action
#
# Auteur : iTechnoFrance
#

import machine, time, ssd1306, paj7620

# Déclaration I2C pour la gestion de l'afficheur OLED SSD1306
# GPIO15 --> SCL OLED, GPIO04 --> SDA OLED
i2c = machine.I2C(scl=machine.Pin(15), sda=machine.Pin(4))
# Activation OLED
reset_oled = machine.Pin(16, machine.Pin.OUT)  # GPIO16 --> Reset OLED
reset_oled.value(0)  # reset OLED
time.sleep(0.050)  # attente 50 ms
reset_oled.value(1)  # active OLED
# Declaration OLED SSD1306
oled = ssd1306.SSD1306_I2C(128, 64, i2c)  # 128 x 64 pixels

# Déclaration I2C pour la communication avec le capteur PAJ7620
# GPIO21 --> SDA, GPIO22 --> SCL
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
g = paj7620.PAJ7620(i2c = i2c)

def option_selection(x, y):
    # crée un rectangle plein de 10 pixels x 128 pixels
    for i in range(y, y+10):
        for j in range(x, 128):
            oled.pixel(j, i, 1) 

def affichage_menu(numero_menu, numero_option):
    if numero_menu == 0:
        # premier menu
        oled.text("Menu 1", 20, 0)
        oled.text("Web", 0, 12, 1)
        oled.text("Mouvement", 0, 23, 1)
        oled.text("Joystick", 0, 34, 1)
        if numero_option == 0:
            option_selection(0, 11)
            oled.text("Web", 0, 12, 0)
        elif numero_option == 1:
            option_selection(0, 22)
            oled.text("Mouvement", 0, 23, 0)
        else:
            option_selection(0, 33)
            oled.text("Joystick", 0, 34, 0)
    if numero_menu == 1:
        # second menu
        oled.text("Menu 2", 20, 0)
        oled.text("Imprimer", 0, 12, 1)
        oled.text("Fichier", 0, 23, 1)
        if numero_option == 0:
            option_selection(0, 11)
            oled.text("Imprimer", 0, 12, 0)
        else:
            option_selection(0, 22)
            oled.text("Fichier", 0, 23, 0)
    if numero_menu == 2:
        # troisième menu
        oled.text("Menu 3", 20, 0)
        oled.text("Aide", 0, 12, 1)
        oled.text("Lancer", 0, 23, 1)
        if numero_option == 0:
            option_selection(0, 11)
            oled.text("Aide", 0, 12, 0)
        else:
            option_selection(0, 22)
            oled.text("Lancer", 0, 23, 0)

# variables pour le choix du menu et d'option            
selection_menu = 0
selection_option = 0

# Définition du nombre d'options par menu
nbr_options = [3, 2, 3]

# Définition des gestes
GESTE_HAUT = 5
GESTE_BAS = 6
GESTE_HORAIRE = 7
GESTE_ANTI_HORAIRE = 8

while True:
    oled.fill(0)  # efface l'écran 
    affichage_menu(selection_menu, selection_option)
    oled.show()
    geste = g.gesture()
    if geste == GESTE_HAUT and selection_option > 0:
        selection_option -= 1
    if geste == GESTE_BAS and selection_option < nbr_options[selection_menu]:    
        selection_option += 1
    if geste == GESTE_HORAIRE:
        if selection_menu == 0:
            if selection_option == 0:
                selection_menu = 1
            if selection_option == 1:
                selection_option = 0
                selection_menu = 2
            if selection_option == 2:
                # action a traiter 
                pass
        elif selection_menu == 1:
            if selection_option == 0:
                # action à traiter
                pass
            if selection_option == 1:
                # action à traiter
                pass
        elif selection_menu == 2:
            if selection_option == 0:
                # action à traiter
                pass
            if selection_option == 1:
                # action à traiter
                pass
    if geste == GESTE_ANTI_HORAIRE:
        if selection_menu == 1:
            selection_option = 0
            selection_menu = 0
        elif selection_menu == 2:
            selection_option = 0
            selection_menu = 0