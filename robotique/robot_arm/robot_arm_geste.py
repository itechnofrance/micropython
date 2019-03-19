#
# Utilisation d'un bras articule par les gestes
#
# Matériel :
#            Testé sur ESP32 WROOM 
#            Bras impression 3D (https://www.thingiverse.com/thing:34829)
#            5 servos SG90
#            Capteur de gestes PAJ7620
#            MicroPython version 1.10
#
# Programme qui permet de piloter le bras articule via des gestes 
#
# Gestes utilisés :
#                   haut / bas pour déplier le bras
#                   gauche / droite pour tourner le pivot
#                   avance / recule pour ouvrir ou fermer la pince
#
# Auteur : iTechnoFrance
#

import machine, time, paj7620

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

# Définition des valeurs en fonction des servos
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

# Définition des gestes
GESTE_AVANCE = 1
GESTE_RECULE = 2
GESTE_DROITE = 3
GESTE_GAUCHE = 4
GESTE_HAUT = 5
GESTE_BAS = 6

# Déclaration I2C pour la communication avec le capteur PAJ7620
# GPIO21 --> SDA, GPIO22 --> SCL
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
g = paj7620.PAJ7620(i2c = i2c)

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
      
initialisation_bras()
nouvelle_position_pivot = position_pivot
nouvelle_position_bras_1 = position_bras_1
nouvelle_position_bras_2 = position_bras_2
nouvelle_position_bras_3 = position_bras_3

while True:
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
    time.sleep(0.1)
    