# Ejemplo Oblique Strategies

Tomás de Camino Beck, Ph.D  
Universidad CENFOTEC

Oblique Strategies es una herramienta creativa desarrollada por el músico Brian Eno y el artista Peter Schmidt en los años 70, que consiste en una baraja de cartas con frases enigmáticas, provocativas o ambiguas, diseñadas para desbloquear bloqueos creativos. Cada carta ofrece una sugerencia o enfoque inesperado, como “Usa un error como una intención” o “Cambia el rol de los instrumentos”, que invita a reinterpretar el problema desde otro ángulo. La idea es interrumpir patrones mentales predecibles y fomentar la toma de decisiones intuitiva, especialmente útil en procesos artísticos como la música, el diseño o la escritura, aunque también puede aplicarse en otras disciplinas creativas o estratégicas.

En este ejemplo, utilizamos una [IdeaBoard](https://github.com/CRCibernetica/circuitpython-ideaboard) (basada en ESP32) que se conecta a una red WiFi y envía un prompt a la API de Gemini para recibir una frase generada por un modelo de lenguaje grande (LLM), al estilo de las Oblique Strategies.

Aunque se trata de un caso muy sencillo, ilustra el potencial de establecer una “conversación” entre microcontroladores y modelos de lenguaje, lo cual abre nuevas posibilidades en áreas como la robótica y los sistemas ciberfísicos, donde la interacción contextual e inteligente puede marcar una diferencia significativa.

## Hardware
- [Ideaboard](https://www.crcibernetica.com/crcibernetica-ideaboard/) (o cualquier ESP32)
- [Pantalla LCD 16x2](https://www.crcibernetica.com/16x2-lcd-with-i2c-blue/?searchid=2404090&search_query=lcd)


## Explicación de Código

Claro, aquí tienes una explicación muy didáctica del código `Oblique_Strategies.py`, ideal para estudiantes o personas que están aprendiendo a conectar microcontroladores con modelos de lenguaje e interfaces físicas como botones y pantallas:

---

## ¿Qué hace este programa?

Este programa `Oblique_Strategies.py` ejecuta en un **ESP32 con CircuitPython**. Al **presionar un botón**, el microcontrolador se conecta a internet, le **hace una pregunta a la IA de Google Gemini** y **muestra la respuesta en una pantalla LCD I2C**. La pregunta que se le hace a la IA es:

> “¿Puedes generar una frase corta, estilo Oblique Strategies?”

---

## Partes del código

### 1. **Importación de librerías**

```python
import time, board, busio, keypad
import socketpool, ssl, wifi
import adafruit_requests as requests
from lcd import LCD, CursorMode
from i2c_pcf8574_interface import I2CPCF8574Interface
from secrets import secrets
```

Se importan las librerías necesarias para:

* Controlar pines (`board`)
* Conectarse al WiFi (`wifi`)
* Usar HTTPS (`requests`)
* Leer el botón (`keypad`)
* Controlar la pantalla LCD
* Leer datos confidenciales desde `secrets.py` (SSID, contraseña y API Key)

---

### 2. **Conexión a WiFi**

```python
wifi.radio.connect(secrets["ssid"], secrets["password"])
```

El ESP32 se conecta a la red WiFi usando las credenciales guardadas en `secrets.py`.

---

### 3. **Preparación de la sesión HTTPS**

```python
socket = socketpool.SocketPool(wifi.radio)
https = requests.Session(socket, ssl.create_default_context())
```

Se crea una conexión segura para enviar solicitudes por internet. Esto es necesario para hablar con la API de Gemini.

---

### 4. **Inicialización de la pantalla LCD**

```python
i2c = board.I2C()
addresses = i2c.scan()
```

Se detecta la dirección del LCD (normalmente `0x27` o `0x3F`) y se inicializa la pantalla. Si no se encuentra, el programa lo avisa.

---

### 5. **Preparación de la API de Gemini**

```python
endpoint = f"https://...{api_key}"
```

Se prepara el **URL de la API de Gemini**, incluyendo la clave (`api_key`) para autenticarse.

---

### 6. **Función para preguntar a Gemini**

```python
def preguntar_gemini(pregunta):
    ...
```

Esta función se encarga de:

* Enviar la pregunta
* Leer la respuesta
* Devolver el texto que responde la IA

---

### 7. **Lectura del botón**

```python
keys = keypad.Keys((board.IO0,), value_when_pressed=False, pull=True)
```

Se configura el botón conectado al pin `IO0`. Se usa `event.released` para detectar cuándo se suelta el botón (no cuándo se presiona).

---

### 8. **Loop principal**

```python
while True:
    ...
```

Aquí está el corazón del programa. Hace lo siguiente en un bucle infinito:

1. Espera que se presione el botón.
2. Limpia la pantalla LCD y escribe "Consultando..."
3. Pregunta a Gemini por una nueva estrategia.
4. Muestra la respuesta en dos líneas del LCD (máx. 32 caracteres en total).
5. Espera un poco y vuelve a empezar.

---

## Flujo completo del programa

1. Conectarse al WiFi ✔️
2. Esperar a que se presione el botón 🔘
3. Preguntar a Gemini una frase estilo "Oblique Strategies" 🧠
4. Mostrarla en la pantalla LCD 📺

---

## ¿Qué puedes experimentar?

* Cambia el texto de la pregunta para obtener respuestas diferentes.
* Usa sensores en lugar del botón para activar la consulta.
* Conecta un altavoz y convierte el texto en audio (text-to-speech).
* Agrega almacenamiento para guardar un historial de frases creativas.


