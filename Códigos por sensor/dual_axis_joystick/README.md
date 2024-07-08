### Descripción del Código

Este código está diseñado para leer y procesar los valores de un joystick de dos ejes conectado a un microcontrolador compatible con CircuitPython. El programa realiza una calibración inicial para determinar los valores promedio (cero) del joystick y luego, en un bucle infinito, lee los valores ajustados del joystick para determinar su posición.

### Explicación del Código

1. **Importaciones y Configuración Inicial**
   ```python
   import board
   import analogio
   import time
   ```

   - `board`: Módulo que proporciona acceso a los pines del microcontrolador.
   - `analogio`: Módulo que permite leer valores analógicos de los pines.
   - `time`: Módulo para manejar tiempos de espera.

2. **Configuración de los Pines del Joystick**
   ```python
   x_axis_pin = analogio.AnalogIn(board.IO27)
   y_axis_pin = analogio.AnalogIn(board.IO33)
   ```

   - `x_axis_pin` y `y_axis_pin` se configuran para leer los valores analógicos del joystick en los pines IO27 y IO33 respectivamente.

3. **Función para Calcular el Valor Promedio (Cero) del Joystick**
   ```python
   def get_zero(times=500, sleep=0.01):
       x_total = 0
       y_total = 0
       for i in range(times):
           x_axis = x_axis_pin.value
           y_axis = y_axis_pin.value
           x_total += x_axis
           y_total += y_axis
           time.sleep(sleep)
       x_zero = x_total // times
       y_zero = y_total // times
       return (x_zero, y_zero)
   ```

   - `get_zero(times, sleep)`:
     - `times`: Número de veces que se lee el valor del joystick para calcular el promedio.
     - `sleep`: Tiempo de espera entre lecturas.
     - Se inicializan `x_total` y `y_total` a cero.
     - Se lee el valor de los ejes `x` e `y` `times` veces, acumulando los valores.
     - Se calcula el promedio dividiendo el total acumulado por el número de lecturas.
     - Retorna una tupla con los valores promedio de `x` e `y`.

4. **Cálculo del Valor Promedio Inicial**
   ```python
   zero = get_zero(times=500, sleep=0.01)
   print(zero)
   ```

   - Se llama a la función `get_zero` para obtener los valores promedio iniciales del joystick.
   - Imprime los valores promedio.

5. **Bucle Principal para Leer y Ajustar los Valores del Joystick**
   ```python
   while True:
       x_axis = x_axis_pin.value - zero[0]
       y_axis = y_axis_pin.value - zero[1]
       print((x_axis, y_axis))
       time.sleep(0.1)
   ```

   - En un bucle infinito:
     - Se leen los valores actuales de `x` e `y` del joystick y se ajustan restando los valores promedio (`zero`).
     - Imprime los valores ajustados de `x` e `y`.
     - Espera `0.1` segundos antes de la siguiente lectura.

### Cómo Utilizar el Código

1. **Hardware Necesario**:
   - Un microcontrolador compatible con CircuitPython.
   - Un joystick de dos ejes.
   - Conexiones adecuadas entre el joystick y los pines analógicos del microcontrolador (`IO27` para `x` y `IO33` para `y` en este caso).

2. **Configuración de CircuitPython**:
   - Asegúrate de tener CircuitPython instalado en tu microcontrolador.
   - Copia el código en un archivo `.py` y cárgalo en el microcontrolador.

3. **Ejecución**:
   - Conecta el microcontrolador a una fuente de alimentación.
   - El código se ejecutará automáticamente, calibrando el joystick y luego leyendo y mostrando los valores ajustados en la consola.

Este código te permitirá leer y utilizar los valores del joystick en tus proyectos de manera precisa, gracias a la calibración inicial.
