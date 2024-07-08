import time
import board
from ideaboard import IdeaBoard

ib = IdeaBoard()

# Note that there are only two pins on the IdeaBoard
# that support AnalogOut: board.IO25 and board.IO26
dac = ib.AnalogOut(board.IO26)
dac.value = 32768 # 1.60V in pin board.IO26   