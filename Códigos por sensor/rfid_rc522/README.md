### Descripción del Código rc522-read.py

Este código está diseñado para leer la información de una tarjeta RFID usando el lector MFRC522 y un microcontrolador compatible con CircuitPython. El programa configura el lector, detecta la tarjeta, obtiene su UID y opcionalmente intenta autenticar y leer datos de una dirección específica de la tarjeta.

### Explicación del Código

1. **Importaciones de Librerías**
   ```python
   import board
   import mfrc522
   ```

   - `board`: Módulo que proporciona acceso a los pines del microcontrolador.
   - `mfrc522`: Módulo que permite interactuar con el lector RFID MFRC522.

2. **Función para Leer la Tarjeta**
   ```python
   def leer_tarjeta():
       """
       Función que lee la información de una tarjeta RFID.
       """
   ```

   - `leer_tarjeta()`: Función principal que realiza la lectura y procesamiento de la tarjeta RFID.

3. **Configuración del Lector RFID**
   ```python
   lector = mfrc522.MFRC522(
       board.SCK,  # Pin SCK
       board.MOSI,  # Pin MOSI
       board.MISO,  # Pin MISO
       board.IO4,   # Pin RST
       board.IO5,   # Pin SDA
   )

   lector.set_antenna_gain(0x07 << 4)
   ```

   - Se crea una instancia del lector MFRC522 configurando los pines necesarios.
   - `set_antenna_gain(0x07 << 4)`: Ajusta la ganancia de la antena para optimizar la lectura.

4. **Mensaje de Bienvenida**
   ```python
   print('')
   print("Acérquese la tarjeta al lector para leer datos de la dirección 0x08")
   print('')
   ```

   - Imprime un mensaje indicando que el usuario debe acercar una tarjeta al lector.

5. **Bucle para Detectar y Leer la Tarjeta**
   ```python
   try:
       while True:
           estado, tipo_tarjeta = lector.request(lector.REQIDL)

           if estado == lector.OK:
               estado, uid = lector.anticoll()

               if estado == lector.OK:
                   print("Nueva tarjeta detectada")
                   print("  - Tipo de tarjeta: 0x%02x" % tipo_tarjeta)
                   print("  - UID: 0x%02x%02x%02x%02x" % (uid[0], uid[1], uid[2], uid[3]))
                   print('')

                   if lector.select_tag(uid) == lector.OK:
                       clave = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                       if lector.auth(lector.AUTHENT1A, 8, clave, uid) == lector.OK:
                           datos = lector.read(8)
                           print("Datos de la dirección 8: %s" % datos)
                           lector.stop_crypto1()
                       else:
                           print("Error de autenticación")
                   else:
                       print("Error al seleccionar la tarjeta")

   except KeyboardInterrupt:
       print("Detenido por Ctrl+C")
   ```

   - En un bucle infinito, se solicita la lectura de una tarjeta:
     - `lector.request(lector.REQIDL)`: Solicita la presencia de una tarjeta.
     - Si se detecta una tarjeta (`estado == lector.OK`), se obtiene el UID de la tarjeta.
     - Imprime el tipo de tarjeta y el UID.
     - Intenta seleccionar la tarjeta usando el UID.
     - Usa una clave predeterminada para intentar autenticarse con la tarjeta.
     - Si la autenticación es exitosa, lee los datos de la dirección 8 y los imprime.
     - Maneja interrupciones del teclado para detener el programa de manera segura.

6. **Bucle Principal para Repetir la Lectura**
   ```python
   while True:
       leer_tarjeta()
   ```

   - Ejecuta la función `leer_tarjeta()` en un bucle infinito para seguir leyendo tarjetas.
