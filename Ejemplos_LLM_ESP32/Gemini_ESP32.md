# **Cómo conectar Gemini AI a un ESP32 — Guía paso a paso**

Tomás de Camino Beck, Ph.D.  
Director de Escuea de Sistemas Inteligentes  
Universidad Cenfotec  

Con esta guía podrás hacer que tu ESP32 sea un asistente inteligente que se comunique con Gemini AI para responder cualquier pregunta. [En este link el profesor Tomás de Camino Beck, explica con detalles](https://youtu.be/rFI_8TIMCNI?si=Z5YtiBwS3AZMw9da)

---

## **Materiales necesarios**

* ESP32 (cualquier versión compatible con Wi-Fi)
* Cable USB
* PC con Arduino IDE instalado
* Cuenta de Google
* Aplicación **Postman** (opcional, para pruebas)

---

## **Paso 1: Obtener la API Key de Gemini**

1. Entra a [Gemini API Docs](https://ai.google.dev/gemini-api/docs) buscando en Google "Gemini API docs".
2. Haz clic en el primer enlace.
3. Marca todas las casillas y haz clic en **Continue**.
4. Crea un proyecto y genera tu **API Key**.
   👉 Copia esta API Key, la necesitarás más adelante.

---

## **Paso 2 (opcional): Probar la API en Postman**

*Este paso es para verificar que la API funciona antes de usarla en el ESP32.*

1. Descarga e instala Postman ([https://www.postman.com/downloads/](https://www.postman.com/downloads/)).
2. Abre Postman, haz clic en el botón "+" para crear una nueva solicitud.
3. Selecciona método **POST**.
4. Escribe la URL del endpoint de Gemini (consultar documentación oficial).
   Ejemplo: `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=TU_API_KEY`
5. En la pestaña **Headers**, agrega:

   * `Content-Type` → `application/json`
6. En **Body** selecciona "raw" → JSON, y escribe algo como:

```json
{
  "contents": [{
    "parts": [{"text": "¿Quién eres?"}]
  }],
  "generationConfig": {
    "maxOutputTokens": 100
  }
}
```

7. Presiona **Send**.
   👉 Deberías recibir una respuesta de Gemini con un texto.

---

## **Paso 3: Preparar el ESP32**

Para este paso recomendamos trabajar con Thonny, que es un software que facilita la programación de microcontroladores con Circuit Python. [Pueden ver este video para apreder sobre el IdeaBoard y Thonny](https://youtu.be/GzA7peI1woc?si=t7AypJyVjUAOKnQ7)

### En Thonny con CitcuitPython

```python
import time
import wifi
import socketpool
import ssl
import adafruit_requests as requests
import json
from secrets import secrets  # Archivo con tus credenciales

# --- CONEXIÓN A INTERNET ---
print("Conectando al WiFi...")
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Conectado a", secrets["ssid"])
print("Dirección IP:", wifi.radio.ipv4_address)

# --- CONFIGURACIÓN DE SESIÓN HTTPS ---
socket = socketpool.SocketPool(wifi.radio)
https = requests.Session(socket, ssl.create_default_context())

# --- CONFIGURACIÓN DE GEMINI ---
api_key = secrets["api_key"]
endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

def preguntar_gemini(pregunta):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": pregunta}]
        }],
        "generationConfig": {
            "maxOutputTokens": 100
        }
    }

    print("Enviando pregunta a Gemini...")
    response = https.post(endpoint, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        print("Respuesta de Gemini:")
        print(data["candidates"][0]["content"]["parts"][0]["text"])
    else:
        print("Error:", response.status_code)
        print(response.text)

# --- LOOP PRINCIPAL ---

try:
    pregunta = "¿Quién Eres?\n"
    if pregunta:
        preguntar_gemini(pregunta)
    print("-" * 40)
except Exception as e:
    print("Error:", e)
time.sleep(5)
```

Crear el archivo `secrets.py` con el siguiente código:

```python
secrets = {
    "ssid": "TU_SSID",
    "password": "TU_PASSWORD",
    "api_key": "TU_API_KEY"
}
```

---

## **Paso 4: Subir y probar**

1. Conecta el ESP32 a la computadora.
2. Selecciona la placa y puerto correctos en Arduino IDE.
3. Sube el código.
4. Abre el **Serial Monitor**.
5. Escribe una pregunta como: `¿Quién eres?` y presiona Enter.

👉 El ESP32 enviará la pregunta a Gemini y mostrará la respuesta en el Serial Monitor.

---

## **Consejos adicionales**

* Puedes agregar filtros en el código para limpiar respuestas (quitar caracteres como \* y espacios).
* Las respuestas son gratis mientras no pases los límites de uso:

  * 15 preguntas por minuto.
  * 1 millón de tokens por minuto.
  * 1500 preguntas por día.

---

## **¿ChatGPT o Gemini?**

* **Gemini** es más fácil de usar para estudiantes porque:

  * Se vincula directamente con tu cuenta Google.
  * Su plan gratuito es más generoso para proyectos educativos.
  * No requiere pagos mientras estés dentro de los límites.

---

## **Ejemplos con este código**

- [Microcontrolador pide a Gemini reprogramarse](https://github.com/Universidad-Cenfotec/ExpoCenfo/tree/main/Ejemplos_LLM_ESP32/Micro%20Se%20Reprograma)
- [Generación de frases únicas con el microcontrolador y Gemini](https://github.com/Universidad-Cenfotec/ExpoCenfo/tree/main/Ejemplos_LLM_ESP32/Ejemplo_Olbique_Strategies)

