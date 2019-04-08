#
# Utilisation d'un bras articulé
#
# Matériel :
#            Testé sur ESP32 WROOM et Heltec Wifi Kit 32
#            Bras impression 3D (https://www.thingiverse.com/thing:34829)
#            5 servos SG90
#            1 écran OLED SSD1306
#            1 capteur de gestes PAJ7620
#            MicroPython version 1.10
#
# Programme qui permet de piloter le bras articulé via  3 possibilités :
#           - Navigateur internet (socket TCP)
#           - Geste
#           - Protocole UDP
#
# Auteur : iTechnoFrance
#

import machine, time
import network, socket, _thread
import paj7620
import ssd1306

# paramètres des servos 
position_pivot = 0
position_bras_1 = 0
position_bras_2 = 0
position_bras_3 = 0
position_pince = 0

# définition des valeurs en fonction des servos
POSITION_PIVOT_MIN = 20
POSITION_PIVOT_MAX = 100
POSITION_BRAS_1_MIN = 90
POSITION_BRAS_1_MAX = 100
POSITION_BRAS_2_MIN = 100
POSITION_BRAS_2_MAX = 120
POSITION_BRAS_3_MIN = 50
POSITION_BRAS_3_MAX = 90
POSITION_PINCE_MIN = 80
POSITION_PINCE_MAX = 100

# permet de sauvegarder les mouvements pour les rejouer
mouvements_pivot = []
mouvements_bras_1 = []
mouvements_bras_2 = []
mouvements_bras_3 = []
mouvements_pince = []

# variable pour l'utilisation d'AJAX
XML = ''

# permet de quitter les Thread pour le mode Web
play_infini = False
web_server_thread = False
status_web_server_thread = False

# permet de quitter le Thread pour le mode UDP
udp_server_thread = False
status_udp_server_thread = False

# variables pour le traitement du menu        
selection_option = 0
attente = True

# définition des gestes
GESTE_AVANCE = 1
GESTE_RECULE = 2
GESTE_DROITE = 3
GESTE_GAUCHE = 4
GESTE_HAUT = 5
GESTE_BAS = 6
GESTE_HORAIRE = 7
GESTE_ANTI_HORAIRE = 8      
       
def config_wifi():
    # configure le module en point d'accès Wifi
    ap = network.WLAN(network.AP_IF)  # création point d'accès WiFi
    ap.active(True)  # activation du point d'accès WiFi   
    ap.config(essid='microarm', channel=11, hidden=False)
    ip = ap.ifconfig()[0]
    return ip
    
def initialisation_bras():
    # initialise le bras
    global position_pivot, position_bras_1, position_bras_2
    global position_bras_3, position_pince
    position_bras_1 = 80  # bras en haut
    servo_bras_1.duty(position_bras_1)
    time.sleep_ms(500)
    position_bras_2 = 110  # bras en haut
    servo_bras_2.duty(position_bras_2)
    time.sleep_ms(500)
    position_bras_3 = 60  # bras au milieu
    servo_bras_3.duty(position_bras_3)
    time.sleep_ms(500)
    position_pivot = 60   # pivot au milieu
    servo_pivot.duty(position_pivot)
    position_pince = 90  # pince mi ouverte
    servo_pince.duty(position_pince)
    
def construit_xml():
    # permet de générer le xml à transmettre à la page html
    global XML
    XML = "<?xml version='1.0'?>"
    XML += "<xml>"
    XML += "<slidervalue0>"
    XML += str(position_pivot)
    XML += "</slidervalue0>"
    XML += "<slidervalue1>"
    XML += str(position_bras_1)
    XML += "</slidervalue1>"
    XML += "<slidervalue2>"
    XML += str(position_bras_2)
    XML += "</slidervalue2>"
    XML += "<slidervalue3>"
    XML += str(position_bras_3)
    XML += "</slidervalue3>"
    XML += "<slidervalue4>"
    XML += str(position_pince)
    XML += "</slidervalue4>"
    XML += "</xml>"
    
def pivot(nouvelle_position):
    # positionne le pivot
    global position_pivot
    position_actuelle = position_pivot
    if nouvelle_position >= position_actuelle:
        for i in range(position_actuelle, nouvelle_position):
            servo_pivot.duty(i)
            time.sleep_ms(10)
    if nouvelle_position < position_actuelle:
        for i in range(position_actuelle, nouvelle_position, -1):
            servo_pivot.duty(i)
            time.sleep_ms(10)
    position_pivot = nouvelle_position
    
def bras_1(nouvelle_position):
    # positionne le 1er bras
    global position_bras_1
    position_actuelle = position_bras_1
    if nouvelle_position >= position_actuelle:
        for i in range(position_actuelle, nouvelle_position):
            servo_bras_1.duty(i)
            time.sleep_ms(30)
    if nouvelle_position < position_actuelle:
        for i in range(position_actuelle, nouvelle_position, -1):
            servo_bras_1.duty(i)
            time.sleep_ms(30)
    position_bras_1 = nouvelle_position

def bras_2(nouvelle_position):
    # positionne le second bras
    global position_bras_2
    position_actuelle = position_bras_2
    if nouvelle_position >= position_actuelle:
        for i in range(position_actuelle, nouvelle_position):
            servo_bras_2.duty(i)
            time.sleep_ms(30)
    if nouvelle_position < position_actuelle:
        for i in range(position_actuelle, nouvelle_position, -1):
            servo_bras_2.duty(i)
            time.sleep_ms(30)
    position_bras_2 = nouvelle_position

def bras_3(nouvelle_position):
    # positionne le 3ème bras
    global position_bras_3
    position_actuelle = position_bras_3
    if nouvelle_position >= position_actuelle:
        for i in range(position_actuelle, nouvelle_position):
            servo_bras_3.duty(i)
            time.sleep_ms(30)
    if nouvelle_position < position_actuelle:
        for i in range(position_actuelle, nouvelle_position, -1):
            servo_bras_3.duty(i)
            time.sleep_ms(30)
    position_bras_3 = nouvelle_position


def pince(nouvelle_position):
    # positionne la pince
    global position_pince
    position_actuelle = position_pince
    if nouvelle_position >= position_actuelle:
        for i in range(position_actuelle, nouvelle_position):
            servo_pince.duty(i)
            time.sleep_ms(30)
    if nouvelle_position < position_actuelle:
        for i in range(position_actuelle, nouvelle_position, -1):
            servo_pince.duty(i)
            time.sleep_ms(30)
    position_pince = nouvelle_position

def mouvements_init():
    # clic sur bouton 'init', on initialise le scénario
    global mouvements_pivot, mouvements_bras_1
    global mouvements_bras_2, mouvements_bras_3, mouvements_pince
    mouvements_pivot = []
    mouvements_bras_1 = []
    mouvements_bras_2 = []
    mouvements_bras_3 = []
    mouvements_pince = []
   
def mouvements_sauve():
    # clic sur bouton 'sauve', on sauvegarde la position de chaque servo
    global mouvements_pivot, mouvements_bras_1
    global mouvements_bras_2, mouvements_bras_3, mouvements_pince
    mouvements_pivot.append(position_pivot)
    mouvements_bras_1.append(position_bras_1)
    mouvements_bras_2.append(position_bras_2)
    mouvements_bras_3.append(position_bras_3)
    mouvements_pince.append(position_pince)

def mouvements_play():
    # clic sur bouton 'exécuter une fois', on exécute une seule
    # fois les différentes positions des servos
    mouvements = len(mouvements_pivot)
    for mouvement in range(0, mouvements):
        pivot(mouvements_pivot[mouvement])
        bras_1(mouvements_bras_1[mouvement])
        bras_2(mouvements_bras_2[mouvement])
        bras_3(mouvements_bras_3[mouvement])
        pince(mouvements_pince[mouvement])
        time.sleep_ms(100)
 
def mouvements_play_infini():
    # clic sur bouton 'exécuter en boucle', on exécute en boucle
    # les différentes positions des servos
    global play_infini
    while play_infini:  # thread lance
        mouvements = len(mouvements_pivot)
        for mouvement in range(0, mouvements):
            pivot(mouvements_pivot[mouvement])
            bras_1(mouvements_bras_1[mouvement])
            bras_2(mouvements_bras_2[mouvement])
            bras_3(mouvements_bras_3[mouvement])
            pince(mouvements_pince[mouvement])
            time.sleep_ms(100)

def delai_initialisation():
    # barre de progression à l'écran
    for i in range(0, 121):
        oled.pixel(i, 40, 1)
        oled.pixel(i, 45, 1)
    for i in range(41, 45):
        oled.pixel(0, i, 1)
        oled.pixel(120, i, 1)
    oled.show()
    for i in range(0, 30):
        for j in range(41, 45):
            oled.pixel(i * 4, j, 1)
            oled.pixel((i * 4) + 1, j, 1)
            oled.pixel((i * 4) + 2, j, 1)
            oled.pixel((i * 4) + 3, j, 1)
        oled.show()

def option_selection(x, y):
    # crée un rectangle plein de 10 pixels x 128 pixels
    for i in range(y, y+10):
        for j in range(x, 128):
            oled.pixel(j, i, 1) 

def affichage_menu(numero_option):
    # affiche le menu
        oled.text("Menu", 40, 0)
        oled.text("Web", 0, 12, 1)
        oled.text("Mouvement", 0, 23, 1)
        oled.text("UDP", 0, 34, 1)
        if numero_option == 0:
            option_selection(0, 11)
            oled.text("Web", 0, 12, 0)
        elif numero_option == 1:
            option_selection(0, 22)
            oled.text("Mouvement", 0, 23, 0)
        else:
            option_selection(0, 33)
            oled.text("UDP", 0, 34, 0)

def web_server():
    # utilisation du bras robotique par le Web
    global play_infini, web_server_thread, status_web_server_thread
    # initialise un socket TCP
    communication = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    communication.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    communication.bind((ip, 80))  # liaison port http--> TCP 80
    communication.listen(5)
    mouvements_init()
    while web_server_thread:
        status_web_server_thread = True
        client_sock, addr = communication.accept() 
        requete = client_sock.recv(1024)  # attente connexion du client, on récupère la requête
        requete = str(requete)
        if requete.find('GET /construit_xml') > 0:  # on construit le XML de base
            if not play_infini:  # si le thread ne tourne pas
                construit_xml()  # construit le xml avec les positions des servos
                client_sock.send(XML)  # met à jour la page html concernant les sliders
        elif requete.find('GET /set_servo') > 0:  # un slider a été déplacé
            play_infini = False  # quitte le thread
            tempo1 = requete.find('set_servo')  # récupère l'emplacement set_servo
            tempo2 = requete.find(' ', tempo1)  # récupère l'emplacement 1er espace
            numero_slider = requete[tempo1 + 9]  # récupère le numéro de servo
            valeur_slider = requete[tempo1 + 11 : tempo2]  # récupère la position du slider
            if numero_slider == "0":  # on traite le servo moteur du pivot
                pivot(int(valeur_slider))  # positionne le pivot
                construit_xml()
                client_sock.send(XML)  # met à jour la page html concernant les sliders
            if numero_slider == "1":  # on traite le servo moteur du bras 1
                bras_1(int(valeur_slider))
                construit_xml()
                client_sock.send(XML)  # met à jour la page html concernant les sliders
            if numero_slider == "2":  # on traite le servo moteur du bras 2
                bras_2(int(valeur_slider))
                construit_xml()
                client_sock.send(XML)  # met à jour la page html concernant les sliders
            if numero_slider == "3":  # on traite le servo moteur du bras 3
                bras_3(int(valeur_slider))
                construit_xml()
                client_sock.send(XML)   # met à jour la page html concernant les sliders
            if numero_slider == "4":  # on traite le servo moteur de la pince
                pince(int(valeur_slider))
                construit_xml()
                client_sock.send(XML)  # met à jour la page html concernant les sliders  
        elif requete.find('GET /?CMD=init_scenario') > 0:  # appuie sur le bouton 'init'
            play_infini = False  # quitte le thread
            with open('robot_arm_web.html', 'r') as html:  # on envoi la page HTML
                client_sock.send(html.read())
            mouvements_init()
        elif requete.find('GET /?CMD=sauve') > 0:  # appuie sur le bouton 'sauve'
            play_infini = False  # quitte le thread
            with open('robot_arm_web.html', 'r') as html:  # on envoi la page HTML
                client_sock.send(html.read())
            mouvements_sauve()  # enregistre la position des servos
        elif requete.find('GET /?CMD=play_one') > 0:  # appuie sur le bouton 'exécuter une fois'
            play_infini = False  # quitte le thread
            with open('robot_arm_web.html', 'r') as html:  # on envoi la page HTML
                client_sock.send(html.read())
            mouvements_play()  # exécute les mouvements sauvegardés
        elif requete.find('GET /?CMD=play_infini') > 0:  # appuie sur le bouton 'exécuter en boucle'
            with open('robot_arm_web.html', 'r') as html:  # on envoi la page HTML
                client_sock.send(html.read())
            if not play_infini:  # on vérifie que le thread ne tourne pas déjà
                play_infini = True  # autorise le thread à se lancer
                # on lance le Thread qui tourne en tâche de fond
                _thread.start_new_thread(mouvements_play_infini, ())
        else:
            with open('robot_arm_web.html', 'r') as html:  # on envoi la page HTML
                client_sock.send(html.read())
        client_sock.close()  # fermeture de la connexion du client
    communication.close()
    status_web_server_thread = False

def udp_server():
    # utilisation du bras robotique par le protocole udp
    global udp_server_thread, status_udp_server_thread
    global nouvelle_position_pivot, nouvelle_position_bras_1
    global nouvelle_position_bras_2, nouvelle_position_bras_3
    # initialise un socket UDP
    communication = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    communication.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    communication.bind((ip, 18000))  # liaison port UDP 18000
    while udp_server_thread:
        status_udp_server_thread = True
        reception = communication.recvfrom(1024)
        if reception[0] == b'g':  # commande pivot à gauche
            nouvelle_position_pivot += 1
            if nouvelle_position_pivot > POSITION_PIVOT_MAX:
                nouvelle_position_pivot = POSITION_PIVOT_MAX
            pivot(nouvelle_position_pivot)
        if reception[0] == b'd':  # commande pivot à droite
            nouvelle_position_pivot -= 1
            if nouvelle_position_pivot < POSITION_PIVOT_MIN:
                nouvelle_position_pivot = POSITION_PIVOT_MIN
            pivot(nouvelle_position_pivot)
        if reception[0] == b'h':  # commande bras vers haut
            if nouvelle_position_bras_1 < POSITION_BRAS_1_MAX:
                nouvelle_position_bras_1 += 1
                bras_1(nouvelle_position_bras_1)
            elif nouvelle_position_bras_2 < POSITION_BRAS_2_MAX:
                nouvelle_position_bras_2 += 1
                bras_2(nouvelle_position_bras_2)
            elif nouvelle_position_bras_3 < POSITION_BRAS_3_MAX:
                nouvelle_position_bras_3 += 1
                bras_3(nouvelle_position_bras_3)
        if reception[0] == b'b':  # commande bras vers le bas
            if nouvelle_position_bras_3 > POSITION_BRAS_3_MIN:
                nouvelle_position_bras_3 -= 1
                bras_3(nouvelle_position_bras_3)
            elif nouvelle_position_bras_2 > POSITION_BRAS_2_MIN:
                nouvelle_position_bras_2 -= 1
                bras_2(nouvelle_position_bras_2)
            elif nouvelle_position_bras_1 > POSITION_BRAS_1_MIN:
                nouvelle_position_bras_1 -= 1
                bras_1(nouvelle_position_bras_1)
    #communication.close()
    status_udp_server_thread = False

# déclaration I2C pour la communication avec le capteur PAJ7620 et l'écran OLED SSD1306
# GPIO21 --> SDA, GPIO22 --> SCL
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)
# déclaration OLED SSD1306
oled = ssd1306.SSD1306_I2C(128, 64, i2c)  # 128 x 64 pixels
oled.fill(0)  # efface l'écran 
oled.text("Initialisation", 8, 0)
oled.text("Bras", 48, 10)
oled.text("Robotique", 32, 20)
oled.show()
delai_initialisation()  # délai 
i2c_peripheriques = i2c.scan()  # corrige pb accès PAJ7620 à la mise sous tension
time.sleep(1)
# déclaration PAJ7620
g = paj7620.PAJ7620(i2c)
# déclaration des servos avec une fréquence de 50 Hertz
servo_pivot = machine.PWM(machine.Pin(12), freq=50)
servo_bras_1 = machine.PWM(machine.Pin(13), freq=50)
servo_bras_2 = machine.PWM(machine.Pin(14), freq=50)
servo_bras_3 = machine.PWM(machine.Pin(26), freq=50)
servo_pince = machine.PWM(machine.Pin(27), freq=50)
initialisation_bras()
nouvelle_position_pivot = position_pivot
nouvelle_position_bras_1 = position_bras_1
nouvelle_position_bras_2 = position_bras_2
nouvelle_position_bras_3 = position_bras_3
ip = config_wifi()

while True:
    oled.fill(0)  # efface l'écran 
    affichage_menu(selection_option)
    oled.show()
    geste = g.gesture()
    if geste == GESTE_HAUT and selection_option > 0:
        selection_option -= 1
    if geste == GESTE_BAS and selection_option < 2:    
        selection_option += 1
    if geste == GESTE_HORAIRE:
        if selection_option == 0:  # pilote le bras robotique via le Web
            if not status_web_server_thread:  # on vérifie que le thread ne tourne pas déjà
                web_server_thread = True  # autorise le thread à se lancer
                # on lance le Thread qui tourne en tâche de fond
                _thread.start_new_thread(web_server, ())
                oled.fill(0)  # efface l'écran 
                oled.text("Mode WEB", 30, 0)
                oled.text("WiFi : microarm", 0, 10)
                oled.text("Adr  : ", 0, 20)
                oled.text("  192.168.4.1", 0, 30)
                oled.text("Stop : geste", 0, 40)
                oled.text("  anti-horaire", 0, 50)
                oled.show()
            else:
                oled.fill(0)  # efface l'écran 
                oled.text("Mode WEB", 30, 0)
                oled.text("Connexion Web", 0, 10)
                oled.text("en cours !!!", 0, 20)
                oled.text("Menu : geste", 0, 40)
                oled.text("  anti-horaire", 0, 50)
                oled.show()
            while attente:
                geste = g.gesture()
                if geste == GESTE_ANTI_HORAIRE:
                    if status_web_server_thread == True:
                        web_server_thread = False
                    attente = False
                time.sleep(0.5)  # délai pour le traitement du capteur PAJ7620
            attente = True
        if selection_option == 1:  # pilote le bras robotique par les gestes
            bras_par_geste = True
            oled.fill(0)  # efface l'écran 
            oled.text("Mode Geste", 30, 0)
            oled.text("Stop : geste", 0, 10)
            oled.text("  anti-horaire", 0, 20)
            oled.show()
            while bras_par_geste:
                geste = g.gesture()
                if geste == GESTE_GAUCHE:
                    nouvelle_position_pivot += 10
                    if nouvelle_position_pivot > POSITION_PIVOT_MAX:
                        nouvelle_position_pivot = POSITION_PIVOT_MAX
                    pivot(nouvelle_position_pivot)
                if geste == GESTE_DROITE:
                    nouvelle_position_pivot -= 10
                    if nouvelle_position_pivot < POSITION_PIVOT_MIN:
                        nouvelle_position_pivot = POSITION_PIVOT_MIN
                    pivot(nouvelle_position_pivot)
                if geste == GESTE_HAUT:
                    if position_bras_2 == POSITION_BRAS_2_MAX:
                        nouvelle_position_bras_1 = POSITION_BRAS_1_MAX
                        bras_1(nouvelle_position_bras_1)
                    if position_bras_3 == POSITION_BRAS_3_MAX:
                        nouvelle_position_bras_2 = POSITION_BRAS_2_MAX
                        bras_2(nouvelle_position_bras_2)
                    if position_bras_3 >= POSITION_BRAS_3_MIN:
                        nouvelle_position_bras_3 = POSITION_BRAS_3_MAX
                        bras_3(nouvelle_position_bras_3)
                if geste == GESTE_BAS:
                    if position_bras_2 == POSITION_BRAS_2_MIN:
                        nouvelle_position_bras_1 = POSITION_BRAS_1_MIN
                        bras_1(nouvelle_position_bras_1)
                    if position_bras_3 == POSITION_BRAS_3_MIN:
                        nouvelle_position_bras_2 = POSITION_BRAS_2_MIN
                        bras_2(nouvelle_position_bras_2)
                    if position_bras_3 <= POSITION_BRAS_3_MAX:
                        nouvelle_position_bras_3 = POSITION_BRAS_3_MIN
                        bras_3(nouvelle_position_bras_3)
                if geste == GESTE_AVANCE:
                    pince(POSITION_PINCE_MIN)
                if geste == GESTE_RECULE:
                    pince(POSITION_PINCE_MAX)
                if geste == GESTE_ANTI_HORAIRE:
                    bras_par_geste = False
                time.sleep(0.5)  # délai pour le traitement du capteur PAJ7620
        if selection_option == 2:  # pilote le bras robotique par le protocole UDP
            if not status_udp_server_thread:  
                # on vérifie que le thread pour le mode UDP n'est pas lancé
                udp_server_thread = True  # autorise le thread à se lancer
                # on lance le Thread qui tourne en tâche de fond
                _thread.start_new_thread(udp_server, ())
                oled.fill(0)  # efface l'écran 
                oled.text("Mode UDP", 30, 0)
                oled.text("Stop : geste", 0, 10)
                oled.text("  anti-horaire", 0, 20)
                oled.show()
            else:
                oled.fill(0)  # efface l'écran 
                oled.text("Mode UDP", 30, 0)
                oled.text("Connexion UDP", 0, 10)
                oled.text("en cours !!!", 0, 20)
                oled.text("Menu : geste", 0, 40)
                oled.text("  anti-horaire", 0, 50)
                oled.show()
            while attente:
                geste = g.gesture()
                if geste == GESTE_ANTI_HORAIRE:
                    if status_udp_server_thread == True:
                        udp_server_thread = False
                    attente = False
                time.sleep(0.5)  # délai pour le traitement du capteur PAJ7620
            attente = True
    time.sleep(0.5)  # délai pour le traitement du capteur PAJ7620