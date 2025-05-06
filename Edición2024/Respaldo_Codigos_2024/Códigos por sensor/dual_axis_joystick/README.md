### Descripción del Código ControladorJoystickDireccional.py

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

### Descripción del Código CalibradorJoystickAndCardinalPoints.py

Este código está diseñado para leer y procesar los valores de un joystick de dos ejes conectado a un microcontrolador compatible con CircuitPython. El programa realiza una calibración inicial para determinar los valores promedio (cero) del joystick, y luego en un bucle infinito, lee los valores ajustados del joystick y determina la dirección en la que está siendo movido.

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

3. **Lista de Direcciones del Joystick**
   ```python
   direction_list = ["East", "Southeast", "South", "Southwest", "West", "Northwest", "North", "Northeast", "Centre"]
   ```

   - `direction_list` es una lista de las posibles direcciones en las que el joystick puede moverse.

4. **Función para Calcular el Valor Promedio (Cero) del Joystick**
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

5. **Función para Determinar la Dirección del Joystick**
   ```python
   def get_direction(zero=(32767, 32767)):
       x_axis = x_axis_pin.value - zero[0]
       y_axis = y_axis_pin.value - zero[1]
       
       if x_axis >= 10000 and -10000 < y_axis < 10000:
           return direction_list[0]  # East
       elif x_axis >= 10000 and y_axis <= -10000:
           return direction_list[1]  # Southeast
       elif -10000 < x_axis < 10000 and y_axis <= -10000:
           return direction_list[2]  # South
       elif x_axis <= -10000 and y_axis <= -10000:
           return direction_list[3]  # Southwest
       elif x_axis <= -10000 and -10000 < y_axis < 10000:
           return direction_list[4]  # West
       elif x_axis <= -10000 and y_axis >= 10000:
           return direction_list[5]  # Northwest
       elif -10000 < x_axis < 10000 and y_axis >= 10000:
           return direction_list[6]  # North
       elif x_axis >= 10000 and y_axis >= 10000:
           return direction_list[7]  # Northeast
       else:
           return direction_list[8]  # Centre
   ```

   - `get_direction(zero)`:
     - `zero`: Tupla con los valores promedio de `x` e `y`.
     - Lee y ajusta los valores actuales de `x` e `y` restando los valores promedio (`zero`).
     - Determina la dirección en la que se mueve el joystick basado en los valores ajustados de `x` e `y` y devuelve la dirección correspondiente de la lista `direction_list`.

6. **Cálculo del Valor Promedio Inicial**
   ```python
   zero = get_zero(times=50, sleep=0.01)
   print(zero)
   ```

   - Se llama a la función `get_zero` para obtener los valores promedio iniciales del joystick.
   - Imprime los valores promedio.

7. **Bucle Principal para Leer y Ajustar los Valores del Joystick**
   ```python
   while True:
       x_axis = x_axis_pin.value - zero[0]
       y_axis = y_axis_pin.value - zero[1]
       
       print((x_axis, y_axis))
       print(get_direction(zero=zero))
       
       time.sleep(0.1)
   ```

   - En un bucle infinito:
     - Se leen los valores actuales de `x` e `y` del joystick y se ajustan restando los valores promedio (`zero`).
     - Imprime los valores ajustados de `x` e `y`.
     - Llama a `get_direction(zero)` para determinar la dirección y la imprime.
     - Espera `0.1` segundos antes de la siguiente lectura.
