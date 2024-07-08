# Jeffry Valverde
# Universidad CENFOTEC

import board
from ideaboard import IdeaBoard
import time

ib = IdeaBoard()

# Se declaran los pines a utilizar
in1 = ib.DigitalOut(board.IO27)
in2 = ib.DigitalOut(board.IO33)

while True:
    in1.value = True # Enciende el LED conectado a IO27
    in2.value = False # Apaga el LED conectado a IO33
    time.sleep(3)
    
    in1.value = False # Apaga el LED conectado a IO27
    in2.value = True # Enciende el LED conectado a IO33
    time.sleep(3)