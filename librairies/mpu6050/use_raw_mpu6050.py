#
# Programme d'utilisation de la librairie MPU6050
#
# Auteur : iTechnoFrance
#

from machine import I2C, Pin
import ssd1306
import mpu6050
import time

# Declaration I2C
# // D1 -> GPIO05 --> SDA
# // D2 -> GPIO04 --> SCL
i2c = I2C(scl=Pin(4), sda=Pin(5), freq=400000)
# Declaration OLED SSD1306
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)  # 128 x 64 pixels

oled.fill(0)  # efface l'ecran 
oled.text("Calibr. MPU6050", 0, 0)
oled.show()
mpu_6050 = mpu6050.MPU6050(i2c)  # declaration mpu6050
oled.text("Adresse :", 0, 10)
oled.text(hex(mpu_6050.adresse), 80, 10)
mpu_6050.lecture_capteurs()
oled.text("Temp :", 0, 20)
oled.text("%2.1f" % mpu_6050.temperature, 80, 20)
oled.show()
time.sleep(10)
if (mpu_6050.detect()):
    while True:
        oled.fill(0)  # efface l'ecran 
        mpu_6050.lecture_capteurs()
        oled.text("GX:", 0, 0)
        oled.text("%i" % mpu_6050.gyroX, 30, 0)
        oled.text("%i" % mpu_6050.gyroX_calibre, 80, 0)
        oled.text("GY:", 0, 10)
        oled.text("%i" % mpu_6050.gyroY, 30, 10)
        oled.text("%i" % mpu_6050.gyroY_calibre, 80, 10)
        oled.text("GZ:", 0, 20)
        oled.text("%i" % mpu_6050.gyroZ, 30, 20)
        oled.text("%i" % mpu_6050.gyroZ_calibre, 80, 20)
        oled.text("AX:", 0, 30)
        oled.text("%i" % mpu_6050.accX, 30, 30)
        oled.text("%i" % mpu_6050.accX_calibre, 80, 30)
        oled.text("AY:", 0, 40)
        oled.text("%i" % mpu_6050.accY, 30, 40)
        oled.text("%i" % mpu_6050.accY_calibre, 80, 40)
        oled.text("AZ:", 0, 50)
        oled.text("%i" % mpu_6050.accZ, 30, 50)
        oled.text("%i" % mpu_6050.accZ_calibre, 80, 50)
        oled.show()
        time.sleep(0.1)
else:
    oled.fill(0)  # efface l'ecran 
    oled.text("MPU not detected", 0, 0)
    oled.show()