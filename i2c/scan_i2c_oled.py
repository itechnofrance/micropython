#
# Tester sur NodeMCU Lolin
# Detection des peripheriques I2C
# Affichage sur OLED SSD1306
#
import machine, time, ssd1306
# Declaration I2C
# // D1 -> GPIO05 --> SDA
# // D2 -> GPIO04 --> SCL
i2c = machine.I2C(scl = machine.Pin(4), sda = machine.Pin(5), freq=400000)
# Declaration OLED SSD1306
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c) # 128 x 64 pixels

def affiche():
    oled.text("Scan bus i2c...", 0, 0)
    oled.text((nbr_devices_i2c), 0, 10)
    oled.text("devices", 25, 10)
    oled.text("%2i" % page + "/" + "%2i" % nbr_pages, 85,10)
    oled.show() 


while True:
    page = 1
    i2c_peripheriques = i2c.scan()
    nbr_devices_i2c = "%2i" % len(i2c_peripheriques) # transforme le nbr de device en String
    nbr_pages = int(len(i2c_peripheriques) / 12) # permet de definir le nbr de pages a afficher
    # modulo, on teste si le resultat de la division nbr devices / 12 n'est pas egale a 0
    if (len(i2c_peripheriques) % 12 > 0): 
        nbr_pages = nbr_pages + 1
    x = 0
    y = 0 
    oled.fill(0)
    for i2c_peripherique in i2c_peripheriques: 
        oled.text(hex(i2c_peripherique), 40 * x, 10 * (y + 2))
        affiche()
        x = x + 1
        if (x == 3): # 3 devices affichees par ligne
            x = 0
            y = y + 1 # ligne suivante
        if (y == 4): # 4 lignes affichees par page
            x = 0
            y = 0
            time.sleep(5)
            oled.fill(0)
            if (page == nbr_pages):
                page = 1
            else:
                page = page + 1
    if (len(i2c_peripheriques) % 12 > 0):
        time.sleep(5)
    
    