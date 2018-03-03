#
# Utilisation capteur de luminosite BH1750
# Tester sur Wemos D1 mini
# 
# Auteur : iTechnoFrance
#

import machine, time
import bh1750  # librairie capteur BH1750 
# Declaration I2C
# // D1 -> GPIO05 --> SCL
# // D2 -> GPIO04 --> SDA
i2c = machine.I2C(scl = machine.Pin(5), sda = machine.Pin(4), freq=400000)
capteur_lumiere = bh1750.BH1750(i2c)  # declaration BH1750

if (capteur_lumiere.detect()):
    # Resolutions et modes possibles pour les mesures
    # MODE_CONTINU_HAUTE_RESOLUTION = Mesure continue, résolution 1 Lux, temps de mesure 120ms
    # MODE_2_CONTINU_HAUTE_RESOLUTION = Mesure continue, résolution 0.5 Lux, temps de mesure 120ms
    # MODE_CONTINU_BASSE_RESOLUTION = Mesure continue, résolution 4 Lux, temps de mesure 16ms   
    # MODE_UNE_MESURE_HAUTE_RESOLUTION = 1 mesure puis passe en veille, résolution 1 Lux, temps de mesure 120ms
    # MODE_2_UNE_MESURE_HAUTE_RESOLUTION = 1 mesure puis passe en veille, résolution 0.5 Lux, temps de mesure 120ms
    # MODE_UNE_MESURE_BASSE_RESOLUTION = 1 mesure puis passe en veille, résolution 4 Lux, temps de mesure 16ms 
    while True:
        mesure_lux = capteur_lumiere.lecture_lumiere(bh1750.MODE_CONTINU_HAUTE_RESOLUTION)
        print(mesure_lux)
        time.sleep(1)
else:
   print("Capteur BH1750 non detecte")
  
