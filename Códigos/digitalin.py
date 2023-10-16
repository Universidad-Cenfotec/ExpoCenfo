import board
import time
from ideaboard import IdeaBoard

ib = IdeaBoard()

#Digital In
# entrada = ib.DigitalIn(board.IO27, pull=ib.UP)
# pull can be ib.UP or ib.DOWN, default None)
entrada = ib.DigitalIn(board.IO27)
while True:
    print(entrada.value)
    time.sleep(0.5)