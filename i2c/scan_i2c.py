#
# Tester sur NodeMCU Lolin
# Detection des peripheriques I2C
#
import machine, time
# Declaration I2C
# // D1 -> GPIO05 --> SDA
# // D2 -> GPIO04 --> SCL
i2c = machine.I2C(scl = machine.Pin(4), sda = machine.Pin(5), freq=400000)
while True:
    print("Scanne du bus i2c...")
    i2c_peripheriques = i2c.scan()
    if len(i2c_peripheriques) == 0:
        print("Aucun peripheriques i2c detectes !")
    else:
        print(len(i2c_peripheriques), " peripheriques i2c trouves")
        for i2c_peripherique in i2c_peripheriques: 
            print(hex(i2c_peripherique))
    time.sleep(10)