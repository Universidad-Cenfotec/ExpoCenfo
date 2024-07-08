# Bentley Born
# CrCibernetica
# Modificado de https://github.com/domdfcoding/circuitpython-mfrc522

"""
Conexiones:
RC-522 ---> IdeaBoard

GND --> GND
3.3v --> 3.3v
SDA --> IO5
SCK --> IO18
MOSI --> IO23
MISO --> IO19
RST --> IO4
"""

"""
Ejemplo de lectura de una tarjeta usando el módulo `mfrc522`.
"""

# Importaciones de librerías
import board
import mfrc522

def leer_tarjeta():
  """
  Función que lee la información de una tarjeta RFID.

  Esta función se encarga de:
    - Configurar el lector MFRC522.
    - Solicitar la lectura de la tarjeta.
    - Obtener el identificador único (UID) de la tarjeta.
    - Intentar autenticarse con la tarjeta (opcional).
    - Leer datos de una dirección específica (opcional).

  No retorna ningún valor.
  """

  # Crea una instancia del lector MFRC522
  lector = mfrc522.MFRC522(
      board.SCK,  # Pin SCK
      board.MOSI,  # Pin MOSI
      board.MISO,  # Pin MISO
      board.IO4,   # Pin RST
      board.IO5,   # Pin SDA
  )

  # Configura la ganancia de la antena
  lector.set_antenna_gain(0x07 << 4)

  # Mensaje de bienvenida
  print('')
  print("Acérquese la tarjeta al lector para leer datos de la dirección 0x08")
  print('')

  try:
    while True:
      # Solicita la lectura de una tarjeta compatible
      estado, tipo_tarjeta = lector.request(lector.REQIDL)

      if estado == lector.OK:
        # Obtiene el identificador único (UID) de la tarjeta
        estado, uid = lector.anticoll()

        if estado == lector.OK:
          print("Nueva tarjeta detectada")
          print("  - Tipo de tarjeta: 0x%02x" % tipo_tarjeta)
          print("  - UID: 0x%02x%02x%02x%02x" % (uid[0], uid[1], uid[2], uid[3]))
          print('')

          # Intenta seleccionar la tarjeta (opcional)
          if lector.select_tag(uid) == lector.OK:
            # Clave predeterminada (generalmente se debe configurar una específica)
            clave = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

            # Intenta autenticarse con la tarjeta (opcional)
            if lector.auth(lector.AUTHENT1A, 8, clave, uid) == lector.OK:
              # Lee datos de la dirección 8 (opcional)
              datos = lector.read(8)
              print("Datos de la dirección 8: %s" % datos)
              lector.stop_crypto1()  # Detiene la autenticación
            else:
              print("Error de autenticación")
          else:
            print("Error al seleccionar la tarjeta")

  except KeyboardInterrupt:
    print("Detenido por Ctrl+C")

# Bucle infinito para repetir la lectura de la tarjeta
while True:
  leer_tarjeta()