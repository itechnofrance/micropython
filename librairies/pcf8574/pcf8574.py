#
# Librairie pour la gestion du module d'extension I/O PCF8574
#
# Test effectue sur ESP32 Heltec Wifi Kit 32
#
# Auteur : iTechnoFrance
#

import machine

P0 = 0x01
P1 = 0x02
P2 = 0x04
P3 = 0x08
P4 = 0x10
P5 = 0x20
P6 = 0x40
P7 = 0x80

class PCF8574():
    def __init__(self, pin_scl, pin_sda, addr_i2c, pin_int=-1):
        self.sda = pin_sda
        self.scl = pin_scl
        self.int = pin_int
        self.i2c_adresse = addr_i2c
        self.i2c = machine.I2C(scl=machine.Pin(self.scl), sda=machine.Pin(self.sda))
        self.interrupt = False
        self.writeMode = 0
        self.data = bytearray(1)
        if self.int != -1:  # on utilise le signal d'interruption du PCF8574 pin INT
            # la pin est une entree avec liaison au +3.3v via resistance interne
            self.pin_interrupt = machine.Pin(self.int, machine.Pin.IN, machine.Pin.PULL_UP)
            # interruption sur un front montant ou descendant 
            self.pin_interrupt.irq(trigger = machine.Pin.IRQ_FALLING, handler = self.traite_interruption)
   
    def traite_interruption(self, pin):
        # un changement d'etat detecte sur les ports P0-P7
        self.interrupt = True
   
    def reset_interruption(self):
        self.state = machine.disable_irq()
        self.interrupt = False
        machine.enable_irq(self.state)

        
    def pinwrite(self, pin, value):
        self.pin = pin
        self.value = value
        self.data_read = self.i2c.readfrom(self.i2c_adresse, 1)[0]
        if self.value == "on":
            self.data[0]= self.data_read | self.pin
        if self.value == "off":
            self.data[0]= self.data_read & ~self.pin
        self.i2c.writeto(self.i2c_adresse, self.data)
   
    def pinread(self, pin):
        self.pin = pin
        self.data = self.i2c.readfrom(self.i2c_adresse, 1)[0]
        self.data = self.data & self.pin
        if self.data == 0:
            return("LOW")
        else:
            return("HIGH")
    