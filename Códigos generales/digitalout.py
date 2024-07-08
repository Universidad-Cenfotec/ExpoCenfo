import board
import time
from ideaboard import IdeaBoard

ib = IdeaBoard()

#Digital Out
salida = ib.DigitalOut(board.IO27)
while True:
    salida.value = True
    time.sleep(0.5)
    salida.value = False
    time.sleep(0.5)