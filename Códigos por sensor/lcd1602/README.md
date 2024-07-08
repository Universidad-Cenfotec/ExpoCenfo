# Ejemplo sencillo de LCD con ESP32 y CircuitPython

Código para utilizar la pantalla LCD 16 x 2 ([como esta](https://www.crcibernetica.com/16x2-lcd-with-i2c-blue/)), con conexión i2c. Utilizar el código `code.py`. Asegurarse de incluir los archivos `lcd.py` y `i2c_pcf8574_interface.py`. Esta librería fue tomada y modificada de este [sitio](https://wokwi.com/projects/380230722673959937)

## Funciones de `lcd`

1. **`__init__(self, interface, num_cols=20, num_rows=4, char_height=8)`**:
   - Inicializa el controlador LCD.
   - `interface`: Interfaz de comunicación (como `I2CInterface`).
   - `num_cols`: Número de columnas por fila.
   - `num_rows`: Número de filas en el display.
   - `char_height`: Altura del carácter, que puede ser 8 o 10 pixeles.

2. **`close(self)`**:
   - Desactiva la interfaz de comunicación.

3. **`set_backlight(self, value)`**:
   - Establece el estado del retroiluminado.

4. **`set_display_enabled(self, value)`**:
   - Habilita o deshabilita el display.

5. **`set_cursor_mode(self, value)`**:
   - Configura el modo del cursor (`CursorMode.HIDE`, `CursorMode.LINE`, `CursorMode.BLINK`).

6. **`cursor_pos(self)`**:
   - Devuelve la posición actual del cursor como una tupla (fila, columna).

7. **`set_cursor_pos(self, row, col)`**:
   - Establece la posición del cursor en la pantalla.

8. **`print(self, string)`**:
   - Imprime una cadena de texto en la pantalla, maneja saltos de línea y el desbordamiento de texto automáticamente.

9. **`clear(self)`**:
   - Limpia la pantalla y restablece la posición del cursor.

10. **`home(self)`**:
    - Restablece la posición del cursor a la inicial.

11. **`shift_display(self, amount)`**:
    - Desplaza la pantalla a la izquierda o derecha según el valor de `amount`.

12. **`create_char(self, location, bitmap)`**:
    - Crea un carácter personalizado en una ubicación específica (0-7) con un mapa de bits dado.

13. **`command(self, value)`**:
    - Envía un comando directamente al LCD.

14. **`write(self, value)`**:
    - Escribe un byte de carácter en el LCD.
