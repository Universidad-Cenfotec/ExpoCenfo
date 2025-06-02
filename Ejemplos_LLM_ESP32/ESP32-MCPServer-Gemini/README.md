# Tutorial: Comunicación de un ESP32 con un servidor MCP (Model Context Protocol) usando IA generativa

Tomás de Camino Beck, Ph.D.  
Universidad CENFOTEC

[Pueden ver un video de este tutorial en este link](https://youtu.be/1puI7Ir59Hg?si=hgGYNTDJo2P2js4b)

![ESP32](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/Ejemplos_LLM_ESP32/ESP32-MCPServer-Gemini/ESP32_MCP.JPG)


Este tutorial muestra cómo un microcontrolador ESP32 puede comunicarse con un servidor MCP (Model Context Protocol) desplegado en la nube, enviar información contextual (temperatura y humedad) y recibir una secuencia de instrucciones generadas por un modelo de lenguaje (LLM), en este caso una melodía. Aunque el ejemplo es trivial, ilustra cómo un dispositivo en el borde puede adaptar su comportamiento dinámicamente en función del contexto ambiental, delegando el razonamiento de alto nivel a una IA generativa.

Este enfoque permite crear arquitecturas distribuidas donde el comportamiento de los dispositivos no está preprogramado, sino que es generado en tiempo real por un sistema inteligente, abriendo nuevas posibilidades en robótica, agricultura de precisión, educación y sistemas ciberfísicos adaptativos.

---

## Requisitos

### Hardware

* ESP32 con CircuitPython
* Sensor AHT20 (temperatura y humedad)
* Pantalla LCD con controlador PCF8574 (opcional pero recomendado)
* Buzzer o parlante pasivo conectado a IO26
* Botón conectado a IO0

### Software

* Cuenta en GitHub
* Cuenta en Render.com
* API Key de Gemini (desde Google Cloud Console)

---

## Estructura del repositorio GitHub

```
mcp-melodia/
│
├── main.py                 # Servidor FastAPI (MCP)
├── requirements.txt        # Dependencias para Render
├── render.yaml             # Configuración del servicio Render
├── code.py             # Código del ESP32 con LCD y buzzer
├── secrets.py      # WiFi y URL del MCP
├── lcd.py              # Driver para la pantalla LCD (PCF8574)
├── i2c_pcf8574_interface.py  # Interfaz I2C del LCD
```

---

## Parte 1: Servidor MCP en Render

### Archivo: `main.py`

```python
from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

API_KEY = "TU_API_KEY_DE_GEMINI"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

TEMPLATE = """
Basado en los siguientes datos:
Ubicación: {location}
Tipo de cultivo: {plant_type}
Humedad del suelo: {soil_moisture}%
Temperatura: {temperature}°C
Humedad relativa: {humidity}%

Genera una melodía breve y alegre en formato "nota,duración,nota,duración,...", usando notas musicales estándar de C3,C#3, hasta c7 y R para silencios), ideal para representar el estado del cultivo en forma musical. que las duraciones vayan entre 0 y 1. EN la respuesta solo quiero la melodía, sin texto antes ni depues.
"""

class ContextData(BaseModel):
    location: str
    plant_type: str
    soil_moisture: float
    temperature: float
    humidity: float

@app.post("/consulta")
def consulta(data: ContextData):
    prompt = TEMPLATE.format(**data.dict())
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 100}
    }
    headers = {"Content-Type": "application/json"}
    r = requests.post(ENDPOINT, headers=headers, json=payload)

    if r.status_code == 200:
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return {"respuesta": text}
    else:
        return {"error": r.text}
```

### Archivo: `requirements.txt`

```txt
fastapi
uvicorn
requests
```

### Archivo: `render.yaml`

```yaml
services:
  - type: web
    name: mcp-server
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port 10000
```

### Despliegue en Render

1. Sube estos archivos a un repositorio en GitHub.
2. Ingresa a [Render.com](https://render.com), conecta tu cuenta de GitHub y crea un nuevo servicio web.
3. Selecciona tu repositorio, asegúrate de que detecte el archivo `render.yaml`.
4. Render desplegará el servidor y te dará una URL del tipo `https://mcp-server.onrender.com`.

---

## Parte 2: Código para el ESP32

Ubicado en `code.py`:

```python
# Tomás de Camino Beck - Universidad CENFOTEC

import time
import board
import busio
import keypad
import wifi
import socketpool
import ssl
import adafruit_requests as requests
import adafruit_ahtx0
import pwmio
from lcd import LCD, CursorMode
from i2c_pcf8574_interface import I2CPCF8574Interface
from secrets_MCP import secrets

wifi.radio.connect(secrets["ssid"], secrets["password"])
pool = socketpool.SocketPool(wifi.radio)
https = requests.Session(pool, ssl.create_default_context())

i2c = board.I2C()
sensor = adafruit_ahtx0.AHTx0(i2c)
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=2, num_cols=16)
lcd.set_cursor_mode(CursorMode.HIDE)

keys = keypad.Keys((board.IO0,), value_when_pressed=False, pull=True)
buzzer = pwmio.PWMOut(board.IO26, duty_cycle=0, frequency=440, variable_frequency=True)

NOTAS = {
    "C3": 131, "C#3": 139, "D3": 147, "D#3": 156, "E3": 165, "F3": 175, "F#3": 185,
    "G3": 196, "G#3": 208, "A3": 220, "A#3": 233, "B3": 247,
    "C4": 262, "C#4": 277, "D4": 294, "D#4": 311, "E4": 330, "F4": 349, "F#4": 370,
    "G4": 392, "G#4": 415, "A4": 440, "A#4": 466, "B4": 494,
    "C5": 523, "C#5": 554, "D5": 587, "D#5": 622, "E5": 659, "F5": 698, "F#5": 740,
    "G5": 784, "G#5": 831, "A5": 880, "A#5": 932, "B5": 988,
    "C6": 1047, "C#6": 1109, "D6": 1175, "D#6": 1245, "E6": 1319, "F6": 1397, "F#6": 1480,
    "G6": 1568, "G#6": 1661, "A6": 1760, "A#6": 1865, "B6": 1976,
    "C7": 2093, "R": 0
}

def tocar_melodia(melodia_str):
    partes = melodia_str.split(",")
    for i in range(0, len(partes) - 1, 2):
        nota = partes[i].strip()
        dur = float(partes[i + 1])
        freq = NOTAS.get(nota, 0)
        if freq == 0:
            buzzer.duty_cycle = 0
        else:
            buzzer.frequency = freq
            buzzer.duty_cycle = 32768
        time.sleep(dur)
        buzzer.duty_cycle = 0
        time.sleep(0.05)

while True:
    event = keys.events.get()
    temp = sensor.temperature
    hum = sensor.relative_humidity
    lcd.clear()
    lcd.set_cursor_pos(0, 0)
    lcd.print("T: {:.1f}C".format(temp))
    lcd.set_cursor_pos(1, 0)
    lcd.print("H: {:.1f}%".format(hum))
    if event and event.released:
        print(f"Temp: {temp:.1f} C | Hum: {hum:.1f} %")
        payload = {
            "location": "Estación 1",
            "plant_type": "desconocido",
            "soil_moisture": 0,
            "temperature": temp,
            "humidity": hum
        }

        url = secrets["url_mcp"] + "/consulta"
        print("Enviando a MCP:", url)
        lcd.clear()
        lcd.set_cursor_pos(0, 0)
        lcd.print("Enviando a IA...")
        r = https.post(url, json=payload)

        if r.status_code == 200:
            melodia = r.json().get("respuesta", "")
            print("Melodía recibida:", melodia)
            lcd.clear()
            lcd.set_cursor_pos(0, 0)
            lcd.print("Melodía recibida...")
            tocar_melodia(melodia)
        else:
            print("Error al consultar MCP:", r.status_code)
            print(r.text)

    time.sleep(0.3)
```

---

## Archivo: `secrets.py`

Ubicado en `secrets.py`:

```python
secrets = {
    "ssid": "NOMBRE_DE_TU_WIFI",
    "password": "CONTRASEÑA_WIFI",
    "url_mcp": "https://<tu-subdominio>.onrender.com"
}
```

---

## Notas finales

Este sistema demuestra cómo dispositivos en el borde pueden operar bajo control flexible mediante instrucciones generadas por LLMs. En lugar de tener un comportamiento fijo, el microcontrolador cambia su acción en función de la entrada contextual, modelada a través de prompts generativos. Esta arquitectura representa una nueva frontera para sistemas embebidos, control adaptativo e inteligencia ambiental distribuida.

---

## Explicación general de la arquitectura

![arq](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/Ejemplos_LLM_ESP32/ESP32-MCPServer-Gemini/Arquitectura_ESP32_MCP_Gemini.png)

La imagen representa una arquitectura típica de **sistemas ciberfísicos inteligentes**, en la que un microcontrolador (en este caso, un **IdeaBoard basado en ESP32**) interactúa con su entorno mediante sensores y actuadores, y amplía su capacidad de decisión conectándose a un modelo de lenguaje de gran escala (LLM) a través de un **servidor MCP (Model Context Protocol)**.

### Componentes:

1. **Entorno**

   * Es el mundo físico en el que opera el sistema.
   * Proporciona señales que el microcontrolador puede medir (por ejemplo, temperatura, humedad, luz) y sobre el cual puede actuar (por ejemplo, activando un motor o emitiendo sonido).

2. **Microcontrolador (IdeaBoard–ESP32)**

   * Mide variables del entorno a través de sensores.
   * Envía los datos recogidos como **parámetros en formato JSON** al servidor MCP.
   * Recibe de vuelta instrucciones generadas por la IA, que pueden alterar su comportamiento (como tocar una melodía o realizar un movimiento).

3. **Servidor MCP**

   * Su función es traducir los datos del microcontrolador en un **prompt textual**, es decir, una solicitud en lenguaje natural que será enviada al modelo de lenguaje.
   * Se comunica con el LLM mediante una **API** y recibe una **respuesta generativa**.
   * Procesa esta respuesta y la convierte en instrucciones estructuradas que el microcontrolador puede interpretar.

4. **Modelo de Lenguaje (LLM: Gemini, ChatGPT, etc.)**

   * Procesa el prompt generado por el MCP y produce una salida que no está predefinida, sino que se genera a partir de patrones aprendidos por el modelo.
   * Esta salida puede ser una melodía, una secuencia de instrucciones, una tabla de transiciones, o incluso código.

### Flujo general:

* El **microcontrolador mide el entorno** (por ejemplo, detecta temperatura y humedad).
* Envía los datos al **servidor MCP**, que construye un **prompt** como:
  *“Genera una melodía basada en temperatura 24.5°C y humedad 70%”*.
* El prompt es enviado a un **modelo de lenguaje** como Gemini o ChatGPT.
* El modelo devuelve una **respuesta generativa**, por ejemplo:
  `"C4,0.3,E4,0.3,G4,0.5,..."`
* El servidor MCP reenvía esa respuesta como instrucciones al ESP32.
* El ESP32 las ejecuta, por ejemplo, **tocando la melodía en un buzzer**.

### ¿Por qué es importante esta arquitectura?

Esta arquitectura demuestra cómo dispositivos de bajo consumo, como microcontroladores, pueden beneficiarse de capacidades de razonamiento complejas al delegar parte de su lógica a modelos de lenguaje. Permite construir sistemas donde el comportamiento **no está codificado de antemano**, sino que se **genera en tiempo real** a partir del contexto, haciendo que los sistemas sean más adaptativos, creativos y abiertos a nuevas posibilidades.
