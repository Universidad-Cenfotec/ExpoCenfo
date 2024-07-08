# Ejemplo sencillo toma una entrada analógica 
# y cambia el brillo del NeoPixel

import board
import time
from ideaboard import IdeaBoard

ib = IdeaBoard()
ib.pixel = (255,255,255)

#Analog In
entrada = ib.AnalogIn(board.IO33)
while True:
    print(entrada.value)
    ib.brightness = (entrada.value-2819)/(62139-2819)
    time.sleep(0.1)
