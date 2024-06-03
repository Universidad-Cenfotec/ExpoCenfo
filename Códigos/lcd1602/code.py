# Tomás de Camino Beck
# Universidad CENFOTEC

#Ejemplo de uso de pantalla LCD

import time
import board
import busio
from lcd import LCD
from i2c_pcf8574_interface import I2CPCF8574Interface
from lcd import CursorMode

# Modify this if you have a different sized Character LCD
lcd_columns = 16
lcd_rows = 2

# Initialise I2C bus.
i2c = board.I2C()



# Talk to the LCD at I2C address 0x27.
# The number of rows and columns defaults to 4x20, so those
# arguments could be omitted in this case.
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=2, num_cols=16)

lcd.print("Hola")

#lcd.clear()

# Start at the second line, from 0.
lcd.set_cursor_pos(1, 0)
lcd.print("Acá estamos")

# Make the cursor visible as a line.
lcd.set_cursor_mode(CursorMode.LINE)

