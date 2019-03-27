#
# Utilisation d'un bras articulé via le protocole UDP
#
# Matériel :
#            Testé sur ESP8266 Lolin
#            1 capteur de mouvements MPU6050
#            MicroPython version 1.10
#
# Programme qui permet de piloter le bras articulé via  le protocole UDP :
#
# Auteur : iTechnoFrance
#

import machine, time
import network, socket
import mpu6050

def config_wifi():
    sta = network.WLAN(network.STA_IF)  # création client d'accès WiFi
    sta.active(True)  # activation du client d'accès WiFi   
    sta.connect('microarm')  # connexion au point d'accès WiFi
    while(sta.isconnected() == False):
        time.sleep(1)
    ip = sta.ifconfig()[0]
    return ip

def communication(commande):
    com_net.sendto(commande, (('192.168.4.1', 18000)))  # envoi la commande au recepteur sur le port 18000 

ip = config_wifi()        
com_net = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # initialise un socket UDP
# Déclaration I2C sur ESP8266
# // GPIO05 --> SDA
# // GPIO04 --> SCL
i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5), freq=400000)
mpu_6050 = mpu6050.MPU6050(i2c)  # déclaration mpu6050
if (mpu_6050.detect()):
    while True:
        mpu_6050.lecture_capteurs()
        if (mpu_6050.AngleX > 5):  # gauche
            communication(b'g')
        if (mpu_6050.AngleX < -5):  # droite
            communication(b'd')
        if (mpu_6050.AngleY < -5):  # haut
            communication(b'h')
        if (mpu_6050.AngleY > 5):  # bas
            communication(b'b')