import board
from ideaboard import IdeaBoard
from time import sleep

ib = IdeaBoard()

AZUL = (0,0,255)
VERDE = (0,255,0)
ROJO = (255,0,0)
NEGRO = (0,0,0)

while True:
    ib.pixel = AZUL
    sleep(1)
    ib.pixel = NEGRO
    sleep(1)
