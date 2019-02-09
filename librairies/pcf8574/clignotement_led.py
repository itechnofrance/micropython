#
# Exemple utilisation librairie PCF8574
#
# Test effectue sur ESP32 Heltec Wifi Kit 32
#
# Branchement LED :
#   +3.3v --> LED  --> 220 Ohms --> port P0
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

while True:
    module_io.pinwrite(pcf8574.P0, "on")  # LED eteinte
    time.sleep(1)
    module_io.pinwrite(pcf8574.P0, "off")  # LED allume
    time.sleep(1)