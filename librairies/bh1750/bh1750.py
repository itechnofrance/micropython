#
# Librairie permettant de gerer le capteur de luminosite
# BH1750
# Tester sur Wemos D1 mini
#
# Auteur : iTechnoFrance
#

from machine import I2C, Pin
import time

BH1750_ADDRESS_ADD_LOW  = 0x5C
BH1750_ADDRESS_ADD_HIGH = 0x23
BH1750_POWER_DOWN = 0x00  # Mise en veille
BH1750_POWER_ON = 0x01  # Attente pour une commande
BH1750_RESET = 0x07  # Mise à 0 du registre de données seulement en mode POWER_ON
# Mesure continue, résolution 1 Lux, temps de mesure 120ms
MODE_CONTINU_HAUTE_RESOLUTION = 0x10
# Mesure continue, résolution 0.5 Lux, temps de mesure 120ms
MODE_2_CONTINU_HAUTE_RESOLUTION = 0x11
# Mesure continue, résolution 4 Lux, temps de mesure 16ms
MODE_CONTINU_BASSE_RESOLUTION = 0x13
# 1 mesure puis passe en veille, résolution 1 Lux, temps de mesure 120ms
MODE_UNE_MESURE_HAUTE_RESOLUTION = 0x20
# 1 mesure puis passe en veille, résolution 0.5 Lux, temps de mesure 120ms
MODE_2_UNE_MESURE_HAUTE_RESOLUTION = 0x21
# 1 mesure puis passe en veille, résolution 4 Lux, temps de mesure 16ms
MODE_UNE_MESURE_BASSE_RESOLUTION = 0x23 

class BH1750():
       
    def __init__(self, i2c):
        self.i2c = i2c
        if self.detect():
            self.reset()
        
    def detect(self):
        detect_bh1750 = False
        i2c_peripheriques = self.i2c.scan()
        for i2c_peripherique in i2c_peripheriques:    
            if (i2c_peripherique == BH1750_ADDRESS_ADD_LOW):
                self.adresse = BH1750_ADDRESS_ADD_LOW
                detect_bh1750 = True
            if (i2c_peripherique == BH1750_ADDRESS_ADD_HIGH):
                self.adresse = BH1750_ADDRESS_ADD_HIGH
                detect_bh1750 = True
        return detect_bh1750
    
    def reset(self):
        self.data = bytearray(1)
        self.data[0] = BH1750_POWER_ON
        self.i2c.writeto(self.adresse, self.data)  
        time.sleep(0.01)  # delai de 10ms
        self.data[0] = BH1750_RESET
        self.i2c.writeto(self.adresse, self.data)  
        time.sleep(0.01)  # delai de 10ms
    
    def lecture_lumiere(self, mode_mesure): 
        self.BH1750_MODE = mode_mesure
        self.mode_mesure_ok = False
        self.luminosite = 0
        self.data_mode = bytearray(1)
        self.lux = bytearray(2)
        self.delai = 0
        # configuration du mode de mesure
        if (self.BH1750_MODE == MODE_CONTINU_HAUTE_RESOLUTION):
            self.mode_mesure_ok = True
        if (self.BH1750_MODE == MODE_2_CONTINU_HAUTE_RESOLUTION):
            self.mode_mesure_ok = True
        if (self.BH1750_MODE == MODE_CONTINU_BASSE_RESOLUTION):
            self.mode_mesure_ok = True
        if (self.BH1750_MODE == MODE_UNE_MESURE_HAUTE_RESOLUTION):
            self.mode_mesure_ok = True
            self.delai = 0.120
        if (self.BH1750_MODE == MODE_2_UNE_MESURE_HAUTE_RESOLUTION):
            self.mode_mesure_ok = True
            self.delai = 0.120
        if (self.BH1750_MODE == MODE_UNE_MESURE_BASSE_RESOLUTION):
            self.mode_mesure_ok = True
            self.delai = 0.016
        if (self.mode_mesure_ok):
            self.data_mode[0] = self.BH1750_MODE
            self.i2c.writeto(self.adresse, self.data_mode)
            time.sleep(self.delai)
            self.i2c.readfrom_into(self.adresse, self.lux)
            self.lux = self.lux[0] * 256 + self.lux[1]
            self.lux = int(float(self.lux) / 1.2)  # Voir la documentation du capteur
            return(self.lux)
        else:
            print("Erreur : mode invalide")
        