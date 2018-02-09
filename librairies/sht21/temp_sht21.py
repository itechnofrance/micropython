#
# Tester sur NodeMCU Lolin
# Utilisation capteur de temperature SHT21 avec affichage sur OLED SSD1306
#
# Auteur : iTechnoFrance
#

import machine, time, ssd1306
import sht21 # librairie capteur SHT21 
# Declaration I2C
# // D1 -> GPIO05 --> SDA
# // D2 -> GPIO04 --> SCL
i2c = machine.I2C(scl = machine.Pin(4), sda = machine.Pin(5), freq=400000)
# Declaration OLED SSD1306
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c) # 128 x 64 pixels

if (sht21.SHT21_DETECT(i2c)):
    sht21.SHT21_RESET(i2c)
    serial_number_sht21 = sht21.SHT21_SERIAL(i2c)
    temperature = sht21.SHT21_TEMPERATURE(i2c)
    humidite = sht21.SHT21_HUMIDITE(i2c)
    # Resolutions possibles pour les mesures
    # 0 : Humidite=12 bits Temperature=14 bits (par defaut)
    # 1 : Humidite=8 bits  Temperature=12 bits
    # 2 : Humidite=10 bits Temperature=13 bits
    # 3 : Humidite=11 bits Temperature=11 bits
    resolution = 0
    sht21.SHT21_SET_RESOLUTION(i2c, resolution)
    if (temperature == -1) or (humidite == -1):
        oled.fill(0) # efface l'ecran
        oled.text("Erreur bus i2c", 0, 0)
        oled.show()
    else:
        Str_temperature = "%2.1f" % temperature + " C"
        Str_humidite = "%2.1f" % humidite + " %"
        oled.fill(0) # efface l'ecran
        oled.text(serial_number_sht21, 0, 0)
        oled.text(Str_temperature, 0, 10)
        oled.text(Str_humidite, 0, 20)
        if (sht21.SHT21_ALIMENTATION(i2c)):
            oled.text("Alimentation OK", 0, 30)
        else:
            oled.text("Alimentation NOK", O, 30)
        oled.text(sht21.SHT21_GET_RESOLUTION(i2c), 0, 40)
        oled.show()
else:
   oled.fill(0) # efface l'ecran 
   oled.text("SHT21 not detected", 0, 0)
   oled.show()
  
