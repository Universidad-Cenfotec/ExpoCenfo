import board
from ideaboard import IdeaBoard

ib = IdeaBoard()

pot = ib.AnalogIn(board.IO33)

servo = ib.Servo(board.IO4)

while True:
    val = pot.value
    val = ib.map_range(val, 0, 65535, 0, 180)
    servo.angle = val