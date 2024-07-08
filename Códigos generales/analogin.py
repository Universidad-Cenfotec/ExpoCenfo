import board
import time
from ideaboard import IdeaBoard

ib = IdeaBoard()

#Analog In
entrada = ib.AnalogIn(board.IO33)
while True:
    print(entrada.value)
    time.sleep(0.5)