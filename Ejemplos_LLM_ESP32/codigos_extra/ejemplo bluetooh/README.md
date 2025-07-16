# Ejemplo de uso de BLE en el IdeaBoard
Tomás de Camino Beck, Ph.D.
Universidad CENFOTEC


> El IdeaBoard debe ser "flasheado" primero en [este enlace.](https://crcibernetica.github.io/ideaboard-experimental/)

##  ¿Qué hace este proyecto?

Permite controlar el color de un LED **NeoPixel** en una placa **IdeaBoard** desde una página web usando **Bluetooth Low Energy (BLE)**. Simplemente escribes un color como `(255,0,0)` en el navegador y el LED se vuelve rojo.

---

## ¿Qué necesitas entender?

Este proyecto se compone de dos partes:

1. **Microcontrolador con CircuitPython** (archivo `ble_neopixel_color.py`)
2. **Página web con Web Bluetooth API** (archivo `ble_text_commander.html`)

---

## Parte 1: El microcontrolador

Este programa está escrito en **Python para CircuitPython** y corre en el IdeaBoard.

### ¿Qué hace?

* Activa el Bluetooth del microcontrolador.
* Espera a que un dispositivo (como un navegador) se conecte.
* Lee lo que le envía ese dispositivo (por ejemplo `(0,255,0)`).
* Convierte ese texto en una tupla de 3 números.
* Cambia el color del NeoPixel en la placa a ese color RGB.

### Fragmento clave:

```python
ib.pixel = text_to_tuple(text)
```

Esta línea cambia el color del LED.

---

## Parte 2: La página web

La página HTML usa **Web Bluetooth API** de JavaScript. Esto permite que el navegador detecte y se conecte al microcontrolador.

### ¿Qué hace?

* Tiene un botón para conectar al microcontrolador por BLE.
* Permite escribir un texto como `(255,0,255)` para enviar.
* Muestra logs del proceso de conexión y comandos enviados.

### Fragmento clave:

```javascript
const data = encoder.encode(command);
await this.characteristic.writeValue(data);
```

Este código convierte el texto en datos binarios y los envía al microcontrolador.

---

## ¿Cómo escribir los comandos?

Usa el formato:

```
(R,G,B)
```

* R = rojo (0 a 255)
* G = verde (0 a 255)
* B = azul (0 a 255)

Por ejemplo:

* `(255,0,0)` = rojo
* `(0,255,0)` = verde
* `(0,0,255)` = azul

---

## ¿Cómo probarlo?

1. **Carga el script `ble_neopixel_color.py` en tu IdeaBoard** con CircuitPython.
2. **Abre el archivo `ble_text_commander.html` en un navegador que soporte Web Bluetooth** (como Chrome).
3. Haz clic en “Conectar a Dispositivo BLE” y selecciona el dispositivo que empieza con `IdeaBoard_BLE_1`.
4. Escribe un color en formato `(R,G,B)` y haz clic en “Enviar comando”.
5. ¡El NeoPixel debe cambiar de color!

---

## ¿Qué estás aprendiendo con esto?

* Cómo usar BLE para comunicar una computadora (o celular) con un microcontrolador.
* Cómo enviar comandos desde el navegador usando Web Bluetooth.
* Cómo procesar esos comandos en CircuitPython.
* Cómo controlar hardware físico (como LEDs) desde una página web.


