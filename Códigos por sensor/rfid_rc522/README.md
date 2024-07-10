## Descripción del Código rc522-read.py

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

## Descripción del Código rc522-write.py

Este código está diseñado para escribir datos en una tarjeta RFID usando el lector MFRC522 y un microcontrolador compatible con CircuitPython. El programa configura el lector, detecta la tarjeta, obtiene su UID y, si la autenticación es exitosa, escribe datos en una dirección específica de la tarjeta.

### Explicación del Código

1. **Importaciones de Librerías**
   ```python
   import board
   import mfrc522
   ```

   - `board`: Módulo que proporciona acceso a los pines del microcontrolador.
   - `mfrc522`: Módulo que permite interactuar con el lector RFID MFRC522.

2. **Función para Escribir Datos en la Tarjeta**
   ```python
   def escribir_tarjeta():
       """
       Función que escribe datos en una tarjeta RFID.
       """
   ```

   - `escribir_tarjeta()`: Función principal que realiza la escritura de datos en la tarjeta RFID.

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
   - `set_antenna_gain(0x07 << 4)`: Ajusta la ganancia de la antena para optimizar la lectura y escritura.

4. **Mensaje de Bienvenida**
   ```python
   print('')
   print("Acérquese la tarjeta al lector para escribir datos en la dirección 0x08")
   print('')
   ```

   - Imprime un mensaje indicando que el usuario debe acercar una tarjeta al lector para escribir datos.

5. **Bucle para Detectar y Escribir en la Tarjeta**
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
                           datos_a_escribir = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
                           estado = lector.write(8, datos_a_escribir)
                           lector.stop_crypto1()

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
   ```

   - En un bucle infinito, se solicita la lectura de una tarjeta:
     - `lector.request(lector.REQIDL)`: Solicita la presencia de una tarjeta.
     - Si se detecta una tarjeta (`estado == lector.OK`), se obtiene el UID de la tarjeta.
     - Imprime el tipo de tarjeta y el UID.
     - Intenta seleccionar la tarjeta usando el UID.
     - Usa una clave predeterminada para intentar autenticarse con la tarjeta.
     - Si la autenticación es exitosa, escribe datos en la dirección 8 de la tarjeta y lo indica en la consola.
     - Maneja interrupciones del teclado para detener el programa de manera segura.

6. **Bucle Principal para Repetir la Escritura**
   ```python
   while True:
       escribir_tarjeta()
   ```

   - Ejecuta la función `escribir_tarjeta()` en un bucle infinito para seguir escribiendo datos en las tarjetas detectadas.
  


## Descripción del Código rfid-demo.py

Este código está diseñado para leer datos de una tarjeta RFID utilizando el lector MFRC522 y un microcontrolador compatible con CircuitPython y la biblioteca `IdeaBoard`. Dependiendo del valor leído de la tarjeta RFID, se cambia el color de un LED RGB en la `IdeaBoard`.

### Explicación del Código

1. **Importaciones y Configuración Inicial**
   ```python
   import time
   import board
   from ideaboard import IdeaBoard
   import mfrc522
   ```

   - `time`: Módulo para manejar tiempos de espera.
   - `board`: Módulo que proporciona acceso a los pines del microcontrolador.
   - `ideaboard`: Módulo específico para el manejo de `IdeaBoard`.
   - `mfrc522`: Biblioteca para interactuar con el lector RFID MFRC522.

2. **Inicialización de IdeaBoard y el Lector RFID**
   ```python
   ib = IdeaBoard()
   reader = mfrc522.MFRC522(board.SCK, board.MOSI, board.MISO, board.IO4, board.IO5)
   ```

   - `ib` es una instancia de `IdeaBoard`, utilizada para interactuar con los pines del microcontrolador.
   - `reader` es una instancia de `MFRC522`, configurada con los pines necesarios para la comunicación SPI con el lector RFID.

3. **Función para Leer la Tarjeta RFID**
   ```python
   def leer_tag(rdr):
       rdr.set_antenna_gain(0x07 << 4)
       print("leyendo...")
       
       while True:
           (stat, tag_type) = rdr.request(rdr.REQIDL)
           if stat == rdr.OK:
               (stat, raw_uid) = rdr.anticoll()
               if stat == rdr.OK:
                   print(f"Tipo de tag: {tag_type:#x}")
                   print(f"UID: {raw_uid[0]:#x}{raw_uid[1]:x}{raw_uid[2]:x}{raw_uid[3]:x}")
                   if rdr.select_tag(raw_uid) == rdr.OK:
                       key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                       if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                           data = rdr.read(8)
                           rdr.stop_crypto1()
                           return data
                       else:
                           print("Error de autenticacion")
                   else:
                       print("Tag no seleccionado")
   ```

   - `leer_tag(rdr)`: Función que lee y autentica una tarjeta RFID.
     - `rdr.set_antenna_gain(0x07 << 4)`: Ajusta la ganancia de la antena del lector RFID.
     - En un bucle infinito:
       - `rdr.request(rdr.REQIDL)`: Solicita una tarjeta en el campo del lector.
       - Si se detecta una tarjeta:
         - `rdr.anticoll()`: Realiza un anticollision para obtener el UID de la tarjeta.
         - Si se obtiene el UID correctamente:
           - `rdr.select_tag(raw_uid)`: Selecciona la tarjeta.
           - Si la selección es exitosa:
             - `rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid)`: Autentica el bloque 8 de la tarjeta con una clave predeterminada.
             - Si la autenticación es exitosa:
               - `rdr.read(8)`: Lee datos del bloque 8.
               - `rdr.stop_crypto1()`: Detiene la encriptación.
               - Retorna los datos leídos.
           - Maneja errores de autenticación y selección de tarjeta.

4. **Bucle Principal para Leer y Procesar Datos de la Tarjeta RFID**
   ```python
   while True:
       data = leer_tag(reader)
       print(f"Data: {data[0]}")
       if data[0] == 255:
           ib.pixel = (255, 0, 0)
       elif data[0] == 0:
           ib.pixel = (0, 255, 0)
   ```

   - En un bucle infinito:
     - Llama a `leer_tag(reader)` para leer datos de la tarjeta RFID.
     - Imprime el primer byte de los datos leídos.
     - Si el primer byte es `255`, cambia el color del LED RGB a rojo (`ib.pixel = (255, 0, 0)`).
     - Si el primer byte es `0`, cambia el color del LED RGB a verde (`ib.pixel = (0, 255, 0)`).
