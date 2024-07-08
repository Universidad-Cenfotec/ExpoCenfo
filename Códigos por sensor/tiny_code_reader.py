# Jeffry Valverde
# Universidad CENFOTEC
# Modificado de https://github.com/usefulsensors/tiny_code_reader_circuit_python

# Ejemplo de cómo acceder al lector de códigos Tiny de Useful Sensors en un Trinkey usando CircuitPython.
# Consulte https://usfl.ink/tcr_dev para obtener la guía completa para desarrolladores.

import board
import busio
import struct
import time

# El lector de códigos tiene la ID I2C de hexadecimal 0c o decimal 12.
TINY_CODE_READER_I2C_ADDRESS = 0x0C

# Cuánto tiempo esperar entre sondeos del sensor.
TINY_CODE_READER_DELAY = 0.2

TINY_CODE_READER_LENGTH_OFFSET = 0
TINY_CODE_READER_LENGTH_FORMAT = "H"
TINY_CODE_READER_MESSAGE_OFFSET = TINY_CODE_READER_LENGTH_OFFSET + struct.calcsize(TINY_CODE_READER_LENGTH_FORMAT)
TINY_CODE_READER_MESSAGE_SIZE = 254
TINY_CODE_READER_MESSAGE_FORMAT = "B" * TINY_CODE_READER_MESSAGE_SIZE
TINY_CODE_READER_I2C_FORMAT = TINY_CODE_READER_LENGTH_FORMAT + TINY_CODE_READER_MESSAGE_FORMAT
TINY_CODE_READER_I2C_BYTE_COUNT = struct.calcsize(TINY_CODE_READER_I2C_FORMAT)

# Pico no admite board.I2C(), así que verifique antes de llamarlo. Si no está presente,
# entonces asumimos que estamos en un Pico y llamamos a una función explícita.
try:
  i2c = board.I2C()
except:
  i2c = busio.I2C(scl=board.GP5, sda=board.GP4)

# Espere hasta que podamos acceder al bus.
while not i2c.try_lock():
  pass

# Para fines de depuración, imprima las direcciones periféricas en el bus I2C.
# 98 (0x62 en hexadecimal) es la dirección de nuestro sensor de persona y debería estar
# presente en la lista. Descomente las siguientes tres líneas si desea ver
# qué direcciones I2C se encuentran.
# while True:
#  print(i2c.scan())
#  time.sleep(TINY_CODE_READER_DELAY)

while True:
  read_data = bytearray(TINY_CODE_READER_I2C_BYTE_COUNT)
  i2c.readfrom_into(TINY_CODE_READER_I2C_ADDRESS, read_data)

  message_length, = struct.unpack_from(TINY_CODE_READER_LENGTH_FORMAT, read_data, TINY_CODE_READER_LENGTH_OFFSET)
  message_bytes = struct.unpack_from(TINY_CODE_READER_MESSAGE_FORMAT, read_data, TINY_CODE_READER_MESSAGE_OFFSET)
  print(message_length)

  if message_length > 0:
    try:
      message_string = bytearray(message_bytes[0:message_length]).decode("utf-8")
      print(message_string)
    except:
      print("No se pudo decodificar como UTF-8")
      pass
