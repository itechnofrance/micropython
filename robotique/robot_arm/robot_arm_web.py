#
# Utilisation d'un bras articule par un navigateur Web
#
# Materiel :
#            Testé sur ESP32 WROOM et Heltec Wifi Kit 32
#            Bras impression 3D (https://www.thingiverse.com/thing:34829)
#            5 servos SG90
#            MicroPython version 1.10
#
# Programme qui permet de piloter le bras articule via un navigateur 
# internet en WiFi et de jouer un scenario sauvegarde
#
# Auteur : iTechnoFrance
#

import machine, time, network, socket, _thread

# declaration des servos avec une frequence de 50 Hertz
servo_pivot = machine.PWM(machine.Pin(12), freq=50)
servo_bras_1 = machine.PWM(machine.Pin(13), freq=50)
servo_bras_2 = machine.PWM(machine.Pin(14), freq=50)
servo_bras_3 = machine.PWM(machine.Pin(26), freq=50)
servo_pince = machine.PWM(machine.Pin(27), freq=50)

# parametres des servos 
position_pivot = 0
position_bras_1 = 0
position_bras_2 = 0
position_bras_3 = 0
position_pince = 0

# permet de sauvegarder les mouvements pour les rejouer
mouvements_pivot = []
mouvements_bras_1 = []
mouvements_bras_2 = []
mouvements_bras_3 = []
mouvements_pince = []

# variable pour l'utilisation d'AJAX
XML = ''

# permet de quitter le Thread
play_infini = False
        
def config_wifi():
    # configure le module en point d'acces Wifi
    ap = network.WLAN(network.AP_IF)  # creation point d'acces WiFi
    ap.active(True)  # activation du point d'acces WiFi   
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
    # permet de generer le xml a transmettre a la page html
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
    # positionne le 3eme bras
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
    # clic sur bouton 'init', on initialise le scenario
    global mouvements_pivot, mouvements_bras_1
    global mouvements_bras_2, mouvements_bras_3, mouvements_pince
    mouvements_pivot = []
    mouvements_bras_1 = []
    mouvements_bras_2 = []
    mouvements_bras_3 = []
    mouvements_pince = []
   
def mouvements_sauve():
    # clic sur bouton 'sauve', on sauvegarde chaque servo
    global mouvements_pivot, mouvements_bras_1
    global mouvements_bras_2, mouvements_bras_3, mouvements_pince
    mouvements_pivot.append(position_pivot)
    mouvements_bras_1.append(position_bras_1)
    mouvements_bras_2.append(position_bras_2)
    mouvements_bras_3.append(position_bras_3)
    mouvements_pince.append(position_pince)

def mouvements_play():
    # clic sur bouton 'executer une fois', on execute une seule
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
    # clic sur bouton 'executer en boucle', on execute en boucle
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
      
ip = config_wifi()
communication = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
communication.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
communication.bind((ip, 80))  # liaison port http--> TCP 80
communication.listen(5)
initialisation_bras()

while True:
    client_sock, addr = communication.accept()  # attente connexion du client
    requete = client_sock.recv(1024)  # on recupere la requete
    requete = str(requete)
    if requete.find('GET /construit_xml') > 0:  # on construit le XML de base
        if not play_infini:  # si le tread ne tourne pas
            construit_xml()  # construit le xml avec les positions des servos
            client_sock.send(XML)  # met a jour la page html concernant les sliders
    elif requete.find('GET /set_servo') > 0:  # un slider a ete deplace
        play_infini = False  # quitte le thread
        tempo1 = requete.find('set_servo')  # recupere l'emplacement set_servo
        tempo2 = requete.find(' ', tempo1)  # recupere l'emplacement 1er espace
        numero_slider = requete[tempo1 + 9]  # recupere le numero de servo
        valeur_slider = requete[tempo1 + 11 : tempo2]  # recupere la position du slider
        if numero_slider == "0":  # on traite le servo moteur du pivot
            pivot(int(valeur_slider))  # positione le pivot
            construit_xml()
            client_sock.send(XML)  # met a jour la page html concernant les sliders
        if numero_slider == "1":  # on traite le servo moteur du bras 1
            bras_1(int(valeur_slider))
            construit_xml()
            client_sock.send(XML)  # met a jour la page html concernant les sliders
        if numero_slider == "2":  # on traite le servo moteur du bras 2
            bras_2(int(valeur_slider))
            construit_xml()
            client_sock.send(XML)  # met a jour la page html concernant les sliders
        if numero_slider == "3":  # on traite le servo moteur du bras 3
            bras_3(int(valeur_slider))
            construit_xml()
            client_sock.send(XML)   # met a jour la page html concernant les sliders
        if numero_slider == "4":  # on traite le servo moteur de la pince
            pince(int(valeur_slider))
            construit_xml()
            client_sock.send(XML)  # met a jour la page html concernant les sliders  
    elif requete.find('GET /?CMD=init_scenario') > 0:
        # appuie sur le bouton 'init'
        play_infini = False  # quitte le thread
        # on envoi la page HTML
        with open('robot_arm_web.html', 'r') as html:  
            client_sock.send(html.read())
        mouvements_init()
    elif requete.find('GET /?CMD=sauve') > 0:
        # appuie sur le bouton 'sauve'
        play_infini = False  # quitte le thread
        # on envoi la page HTML
        with open('robot_arm_web.html', 'r') as html:  
            client_sock.send(html.read())
        # enregistre la position
        mouvements_sauve()
    elif requete.find('GET /?CMD=play_one') > 0:
        # appuie sur le bouton 'executer une fois'
        play_infini = False  # quitte le thread
        # on envoi la page HTML
        with open('robot_arm_web.html', 'r') as html:  
            client_sock.send(html.read())
        # execute les mouvements sauvegardes
        mouvements_play()
    elif requete.find('GET /?CMD=play_infini') > 0:
        # appuie sur le bouton 'executer en boucle'
        # on envoi la page HTML
        with open('robot_arm_web.html', 'r') as html:  
            client_sock.send(html.read())
        if not play_infini:  # on verifie que le thread ne tourne pas deja
            play_infini = True  # autorise le thread a se lancer
            # on lance le Thread qui tourne en tâche de fond
            _thread.start_new_thread(mouvements_play_infini, ())
    else:
        # on envoi la page HTML
        with open('robot_arm_web.html', 'r') as html:  
            client_sock.send(html.read())
    client_sock.close()  # fermeture de la connexion du client