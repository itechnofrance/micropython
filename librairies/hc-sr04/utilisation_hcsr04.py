#
#                   Mesure de distance
#
# Programme permettant d'utiliser la librairie qui gere le capteur de 
# distance ultrason HC-SR04
# Tester sur NodeMCU Lolin et Wemos D1 mini
#
# Auteur iTechnoFrance
#

import hcsr04, time

# pin_echo : pin pour mesurer la distance
# pin_trig : pin pour envoyer les impulsions
pin_echo = 4  # sortie D2 --> GPIO04
pin_trigger = 5  # sortie D1 --> GPIO05

# initialisation librairie HC-SR04
hc_sr04 = hcsr04.HCSR04(pin_echo, pin_trigger)

while True:
    distance = hc_sr04.lecture_distance()
    if (distance == -1):
        print ("Mesure supérieure à 4 mètres")
    else:
        print ((distance), "cm")
    time.sleep(5)
