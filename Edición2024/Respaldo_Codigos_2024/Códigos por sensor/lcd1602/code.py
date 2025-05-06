# Tomás de Camino Beck
# Universidad CENFOTEC
# Modificado de https://wokwi.com/projects/380230722673959937 

# Ejemplo de uso de pantalla LCD

import time
import board
import busio
from lcd import LCD
from i2c_pcf8574_interface import I2CPCF8574Interface
from lcd import CursorMode

# Columnas y filas de la pantalla
lcd_columns = 16
lcd_rows = 2

# Inicializa el bus i2c.
i2c = board.I2C()



# Hace una instanciación de el lcd
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=2, num_cols=16)

# Muestra texto en lcd (posición 0,0)
lcd.print("Hola")

# Limpia pantalla
# lcd.clear()

# Muestra algo en inicio de la segunda fila
lcd.set_cursor_pos(1, 0)
lcd.print("Acá estamos")

# Mostrar el cursor como línea
lcd.set_cursor_mode(CursorMode.LINE)

