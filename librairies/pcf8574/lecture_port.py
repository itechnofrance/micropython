#
# Exemple utilisation librairie PCF8574
#
# Test effectue sur ESP32 Heltec Wifi Kit 32
#
# Lecture d'une entree P0 et allume la LED interne en fonction de l'etat de P0
#
# Auteur : iTechnoFrance
#

import machine, pcf8574

# Definition de la LED interne
led_interne = machine.Pin(25, machine.Pin.OUT) # GPIO25

# Pin's I2C sur ESP32 Heltec Wifi Kit 32
# GPIO22 --> SCL
# GPIO21 --> SDA

# Declaration PCF8574
# Adresse I2C de 0x20 a 0x27 selon cavaliers A0 a A2
module_io = pcf8574.PCF8574(22, 21, 0x20)

while True:
    if module_io.pinread(pcf8574.P0) == "HIGH":
        led_interne.value(1)
    else:
        led_interne.value(0)
   
  