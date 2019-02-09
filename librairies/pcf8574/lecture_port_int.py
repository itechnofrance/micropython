#
# Exemple utilisation librairie PCF8574
#
# Test effectue sur ESP32 Heltec Wifi Kit 32
#
# detection interruption et affichage sur la LED interne
#
# Auteur : iTechnoFrance
#

import machine, pcf8574, time

# Definition de la LED interne
led_interne = machine.Pin(25, machine.Pin.OUT) # GPIO25
led_etat = True

# Pin's I2C sur ESP32 Heltec Wifi Kit 32
# GPIO22 --> SCL
# GPIO21 --> SDA

# Pin utilisee pour traiter l'interruption, port INT du PCF8574 --> GPIO13 

# Declaration PCF8574
# Adresse I2C de 0x20 a 0x27 selon cavaliers A0 a A2
module_io = pcf8574.PCF8574(22, 21, 0x20, 13)

while True:
    if module_io.interrupt == True:
        time.sleep_ms(50)  
        module_io.reset_interruption()
        led_etat = not led_etat
    if led_etat:
        led_interne.value(1)
    else:
        led_interne.value(0)

  