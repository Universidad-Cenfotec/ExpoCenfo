### Descripción del Código

Este código está diseñado para controlar dos relés conectados a un microcontrolador compatible con CircuitPython y la biblioteca `IdeaBoard`. Alterna el encendido y apagado de los relés conectados a los pines `IO27` e `IO33` cada tres segundos.

### Explicación del Código

1. **Importaciones y Configuración Inicial**
   ```python
   import board
   from ideaboard import IdeaBoard
   import time
   ```

   - `board`: Módulo que proporciona acceso a los pines del microcontrolador.
   - `ideaboard`: Módulo específico para el manejo de `IdeaBoard`.
   - `time`: Módulo para manejar tiempos de espera.

2. **Inicialización de IdeaBoard**
   ```python
   ib = IdeaBoard()
   ```

   - `ib` es una instancia de `IdeaBoard`, utilizada para interactuar con los pines del microcontrolador.

3. **Declaración de los Pines a Utilizar**
   ```python
   in1 = ib.DigitalOut(board.IO27)
   in2 = ib.DigitalOut(board.IO33)
   ```

   - `in1` y `in2` son configurados como salidas digitales conectadas a los pines `IO27` e `IO33` respectivamente.

4. **Bucle Principal para Controlar los Relés**
   ```python
   while True:
       in1.value = True  # Activa el relé conectado a IO27
       in2.value = False # Desactiva el relé conectado a IO33
       time.sleep(3)
       
       in1.value = False # Desactiva el relé conectado a IO27
       in2.value = True  # Activa el relé conectado a IO33
       time.sleep(3)
   ```

   - En un bucle infinito:
     - Activa el relé conectado a `IO27` (`in1.value = True`).
     - Desactiva el relé conectado a `IO33` (`in2.value = False`).
     - Espera 3 segundos (`time.sleep(3)`).
     - Desactiva el relé conectado a `IO27` (`in1.value = False`).
     - Activa el relé conectado a `IO33` (`in2.value = True`).
     - Espera otros 3 segundos (`time.sleep(3)`).
