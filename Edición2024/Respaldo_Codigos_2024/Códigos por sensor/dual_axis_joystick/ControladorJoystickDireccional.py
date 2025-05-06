# Jeffry Valverde
# Universidad CENFOTEC
# Modificado de https://forum.banana-pi.org/t/bpi-picow-s3-use-a-dual-axis-joystick-circuitpython/14260

import board
import analogio
import time

# Configura los pines analógicos para leer el valor del joystick
x_axis_pin = analogio.AnalogIn(board.IO27)
y_axis_pin = analogio.AnalogIn(board.IO33)

def get_zero(times=500, sleep=0.01):
    # Función para calcular el valor promedio (cero) del joystick
    x_total = 0
    y_total = 0
    for i in range(times):
        # Lee los valores de los ejes x e y
        x_axis = x_axis_pin.value
        y_axis = y_axis_pin.value
        # Suma los valores leídos
        x_total += x_axis
        y_total += y_axis
        time.sleep(sleep)
    # Calcula el promedio de los valores leídos
    x_zero = x_total // times
    y_zero = y_total // times
    return (x_zero, y_zero)

# Calcula el valor promedio (cero) inicial del joystick
zero = get_zero(times=500, sleep=0.01)
print(zero)

while True:
    # Lee los valores de los ejes x e y ajustados por el valor cero
    x_axis = x_axis_pin.value - zero[0]
    y_axis = y_axis_pin.value - zero[1]
    
    # Imprime los valores ajustados de x e y
    print((x_axis, y_axis))
    
    time.sleep(0.1)  # Espera un poco antes de la siguiente lectura