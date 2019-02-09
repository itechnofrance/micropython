#
# Exemple utilisation librairie PCF8574
#
# Test effectue sur ESP32 Heltec Wifi Kit 32
#
# Branchement LED :
#   +3.3v --> LED  --> 220 Ohms --> port Px
#
# Auteur : iTechnoFrance
#

import pcf8574, time

# Pin's I2C sur ESP32 Heltec Wifi Kit 32
# GPIO22 --> SCL
# GPIO21 --> SDA

# Declaration PCF8574
# Adresse I2C de 0x20 a 0x27 selon cavaliers A0 a A2
module_io = pcf8574.PCF8574(22, 21, 0x20)

# Definition de la liste des ports
gpio = [pcf8574.P0, pcf8574.P1, pcf8574.P2, pcf8574.P3, pcf8574.P4, pcf8574.P5, pcf8574.P6, pcf8574.P7]

while True:
   for i in range(0, 8):
        module_io.pinwrite(gpio[i], "off")  # LED allume
        time.sleep_ms(100)
        module_io.pinwrite(gpio[i], "on")  # LED eteinte 
   for i in range(6, 0, -1):
        module_io.pinwrite(gpio[i], "off")  # LED allume
        time.sleep_ms(100)
        module_io.pinwrite(gpio[i], "on")  # LED eteinte
     