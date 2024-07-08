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
Ejemplo de escritura en una tarjeta usando el módulo `mfrc522`.
"""

# Importaciones de librerías
import board
import mfrc522

def escribir_tarjeta():
  """
  Función que escribe datos en una tarjeta RFID.

  Esta función se encarga de:
    - Configurar el lector MFRC522.
    - Solicitar la lectura de la tarjeta.
    - Obtener el identificador único (UID) de la tarjeta.
    - Intentar autenticarse con la tarjeta (opcional).
    - Escribir datos en una dirección específica.

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
  print("Acérquese la tarjeta al lector para escribir datos en la dirección 0x08")
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
              # Datos a escribir (16 bytes)
              datos_a_escribir = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"

              # Intenta escribir los datos en la dirección 8
              estado = lector.write(8, datos_a_escribir)
              lector.stop_crypto1()  # Detiene la autenticación

              if estado == lector.OK:
                print("Datos escritos en la tarjeta")
              else:
                print("Error al escribir datos en la tarjeta")
            else:
              print("Error de autenticación")
          else:
            print("Error al seleccionar la tarjeta")

  except KeyboardInterrupt:
    print("Detenido por Ctrl+C")

# Bucle infinito para repetir la escritura en la tarjeta
while True:
  escribir_tarjeta()