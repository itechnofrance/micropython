#
# Librairie permettant d'utiliser le capteur Accelerometre / Gyroscope MPU6050
# Tester sur NodeMCU Lolin
#
# Auteur iTechnoFrance
#

from machine import I2C
import time, math

MPU6050_ADDRESS_AD0_LOW  = 0x68
MPU6050_ADDRESS_AD0_HIGH = 0x69
MPU6050_REG_POWER_MGMT_1 = 0x6B  # registre qui permet d'effectuer un reset
MPU6050_REG_POWER_MGMT_2 = 0x6C  # registre pour activer les capteurs
MPU6050_REG_READ_SENSORS = 0x3B  # registre qui permet de lire 14 octets des capteurs acc, gyro et temperature
MPU6050_REG_CONFIG       = 0x1A  # registre qui permet de configurer le filtre passe bas
MPU6050_REG_SMPRT_DIV    = 0x19  # registre qui permet de definir le taux d'echantillonage
MPU6050_REG_CONFIG_GYRO  = 0x1B  # registre qui permet de configurer le gyroscope
MPU6050_REG_CONFIG_ACC   = 0x1C  # registre qui permet de configurer l'accelerometre

class MPU6050():
        
    def __init__(self, i2c):
        self.capteurs = bytearray(14)  # 14 registres a lire
        self.AngleX = 0
        self.AngleY = 0
        self.AngleZ = 0
        self.i2c = i2c
        if self.detect():
           self.reset()
           self.config()
           self.calibration()
           self.temps = time.ticks_ms()
        
    def detect(self):
        detect_mpu6050 = False
        i2c_peripheriques = self.i2c.scan()
        for i2c_peripherique in i2c_peripheriques:    
            if (i2c_peripherique == MPU6050_ADDRESS_AD0_LOW):
                self.adresse = MPU6050_ADDRESS_AD0_LOW
                detect_mpu6050 = True
            if (i2c_peripherique == MPU6050_ADDRESS_AD0_HIGH):
                self.adresse = MPU6050_ADDRESS_AD0_HIGH
                detect_mpu6050 = True
        return detect_mpu6050
    
    def reset(self):
        self.data = bytearray(2)
        self.data[0] = MPU6050_REG_POWER_MGMT_1
        self.data[1] = 1 << 7  # bit 7 a 1 : reset mpu6050
        self.i2c.writeto(self.adresse, self.data)  
        time.sleep(0.100)  # delai de 100ms

    def config(self):
        self.data = bytearray(2)
        self.data[0] = MPU6050_REG_POWER_MGMT_1
        self.data[1] = 1  # desactive le mode sleep et source horloge = X Gyro
        self.i2c.writeto(self.adresse, self.data)  
        self.data[0] = MPU6050_REG_POWER_MGMT_2
        self.data[1] = 0  # active tous les capteurs
        self.i2c.writeto(self.adresse, self.data)
        self.data[0] = MPU6050_REG_CONFIG
        self.data[1] = 1  # active le filtre passe bas acc=184Hz gyro=188Hz
        self.i2c.writeto(self.adresse, self.data)
        self.data[0] = MPU6050_REG_SMPRT_DIV
        self.data[1] = 32 # taux d'echantillonage environ 1000Hz / 32 = 31Hz = 32ms
        self.i2c.writeto(self.adresse, self.data) 
        self.data[0] = MPU6050_REG_CONFIG_GYRO
        self.data[1] = 0  # configuration plage de mesure gyroscope +/- 250 deg/seconde
        self.i2c.writeto(self.adresse, self.data)
        self.data[0] = MPU6050_REG_CONFIG_ACC
        self.data[1] = 0  # configuration plage de mesure accelometre +/- 2g
        self.i2c.writeto(self.adresse, self.data)
        
    def lecture_capteurs(self):
        self.i2c.readfrom_mem_into(self.adresse, MPU6050_REG_READ_SENSORS, self.capteurs)
        self.temp()
        self.acc()
        self.gyro()
        self.angle()
        
    def temp(self):
        self.temp_high_byte = self.capteurs[6] # octet haut temperature
        self.temp_low_byte = self.capteurs[7]  # octet bas temperature
        self.temperature = self.bytes_to_int(self.temp_high_byte, self.temp_low_byte)
        self.temperature = self.temperature / 340.00 + 36.53
    
    def acc(self):
        self.accX_high_byte = self.capteurs[0] # octet haut pour l'axe X de l'accelerometre
        self.accX_low_byte = self.capteurs[1] # octet bas pour l'axe X de l'accelerometre
        self.accX = self.bytes_to_int(self.accX_high_byte, self.accX_low_byte)
        self.accX_calibre = self.accX - self.accX_calibration
        self.accY_high_byte = self.capteurs[2] # octet haut pour l'axe Y de l'accelerometre
        self.accY_low_byte = self.capteurs[3] # octet bas pour l'axe Y de l'accelerometre
        self.accY = self.bytes_to_int(self.accY_high_byte, self.accY_low_byte)
        self.accY_calibre = self.accY - self.accY_calibration
        self.accZ_high_byte = self.capteurs[4] # octet haut pour l'axe Z de l'accelerometre
        self.accZ_low_byte = self.capteurs[5] # octet bas pour l'axe Z de l'accelerometre
        self.accZ = self.bytes_to_int(self.accZ_high_byte, self.accZ_low_byte)
        self.accZ_calibre = self.accZ - self.accZ_calibration
        
    def gyro(self):
        self.gyroX_high_byte = self.capteurs[8] # octet haut pour l'axe X du gyro
        self.gyroX_low_byte = self.capteurs[9] # octet bas pour l'axe X du gyro
        self.gyroX = self.bytes_to_int(self.gyroX_high_byte, self.gyroX_low_byte)
        self.gyroX_calibre = self.gyroX - self.gyroX_calibration
        self.gyroY_high_byte = self.capteurs[10] # octet haut pour l'axe Y du gyro
        self.gyroY_low_byte = self.capteurs[11] # octet bas pour l'axe Y du gyro
        self.gyroY = self.bytes_to_int(self.gyroY_high_byte, self.gyroY_low_byte)
        self.gyroY_calibre = self.gyroY - self.gyroY_calibration
        self.gyroZ_high_byte = self.capteurs[12] # octet haut pour l'axe Z du gyro
        self.gyroZ_low_byte = self.capteurs[13] # octet bas pour l'axe Z du gyro
        self.gyroZ = self.bytes_to_int(self.gyroZ_high_byte, self.gyroZ_low_byte)
        self.gyroZ_calibre = self.gyroZ - self.gyroZ_calibration
        
    def bytes_to_int(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return (firstbyte << 8 | secondbyte)
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)  # complement a 2
    
    def calibration(self):
        i = 0
        self.gyroX_calibration = 0
        self.gyroY_calibration = 0
        self.gyroZ_calibration = 0
        self.accX_calibration = 0
        self.accY_calibration = 0
        self.accZ_calibration = 0
        while i < 100:
            self.i2c.readfrom_mem_into(self.adresse, MPU6050_REG_READ_SENSORS, self.capteurs)
            self.gyro()
            self.gyroX_calibration += self.gyroX
            self.gyroY_calibration += self.gyroY
            self.gyroZ_calibration += self.gyroZ
            self.acc()
            self.accX_calibration += self.accX
            self.accY_calibration += self.accY
            self.accZ_calibration += self.accZ
            i += 1
            time.sleep(0.100)
        self.gyroX_calibration /= 100
        self.gyroY_calibration /= 100
        self.gyroZ_calibration /= 100
        self.accX_calibration /= 100
        self.accY_calibration /= 100
        self.accZ_calibration /= 100

    def angle(self):
        # Calcul en utilisant un filtre complementaire
        # Pour l'utilisation de l'axe Z il est nécessaire d'y adjoindre un magnetometre 
        # si on veut des mesures utilisables
        self.temps_precedent = self.temps
        self.temps = time.ticks_ms()
        self.intervalle = time.ticks_diff(self.temps, self.temps_precedent) / 1000
        self.aX = self.accX_calibre / 16384.0  # 16384 pour le choix plage de mesure accelerometre +/- 2g
        self.aY = self.accY_calibre / 16384.0
        self.aZ = self.accZ_calibre / 16384.0
        self.accX_angle = math.degrees (math.atan(self.aY / math.sqrt((self.aX * self.aX) + (self.aZ * self.aZ))))
        self.accY_angle = math.degrees (math.atan(-1 * self.aX / math.sqrt((self.aY * self.aY) + (self.aZ * self.aZ))))
        self.accZ_angle = math.degrees (math.atan(math.sqrt((self.aX * self.aX) + (self.aY * self.aY)) / self.aZ ))
        self.gyroX_angle = self.gyroX_calibre / 131  # 131 pour le choix de mesure +/- 250 deg/s
        self.gyroY_angle = self.gyroY_calibre / 131
        self.gyroZ_angle = self.gyroZ_calibre / 131
        self.AngleX = 0.98 * (self.AngleX + self.gyroX_angle * self.intervalle) + 0.02 * self.accX_angle
        self.AngleY = 0.98 * (self.AngleY + self.gyroY_angle * self.intervalle) + 0.02 * self.accY_angle
        self.AngleZ = 0.98 * (self.AngleZ + self.gyroZ_angle * self.intervalle) + 0.02 * self.accZ_angle
        