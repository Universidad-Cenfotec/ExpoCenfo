# Tomás de Camino Beck
# Proyecto: Botón que genera frase Oblique Strategy y la muestra en LCD

from ideaboard import IdeaBoard
import time
import board
import busio
import keypad
import socketpool
import ssl
import wifi
import adafruit_requests as requests
from secrets import secrets  # Este archivo debe tener 'ssid', 'password', 'api_key'

ib = IdeaBoard()

# ------------------------
# Inicializa conexión WiFi
# ------------------------
ib.pixel = (0,0,0)
print("Conectando al WiFi...")
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Conectado a", secrets["ssid"])
print("IP:", wifi.radio.ipv4_address)
ib.pixel = (0,200,0)
time.sleep(0.5)
ib.pixel = (0,0,0)

# ------------------------
# Configura sesión HTTPS
# ------------------------
socket = socketpool.SocketPool(wifi.radio)
https = requests.Session(socket, ssl.create_default_context())

# ------------------------
# Configura Gemini
# ------------------------
api_key = secrets["api_key"]
endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

def preguntar_gemini(pregunta):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": pregunta}]
        }],
        "generationConfig": {"maxOutputTokens": 500}
    }

    print("Enviando pregunta a Gemini...")
    response = https.post(endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        texto = data["candidates"][0]["content"]["parts"][0]["text"]
        print("Gemini dice:", texto)
        return texto
    else:
        print("Error:", response.status_code)
        return "Error"

def obtener_codigo_patron():
    pregunta = (
        "Podrìas hacer con secuencia de colores, escritas como comandos ib.pixel = (R,G,B), separados por time.sleep(s), donde s son segundos, de un ritmo de una, solo una, canción de rock. Sin comentarios antes ni después."
    )
    codigo = preguntar_gemini(pregunta)
    return codigo


# ------------------------
# Detecta botón en GPIO0
# ------------------------
keys = keypad.Keys((board.IO0,), value_when_pressed=False, pull=True)

# ------------------------
# Loop principal
# ------------------------
while True:
    ib.pixel = (0,255,0)
    event = keys.events.get()
    if event and event.released:
        ib.pixel = (0,0,0)
        ib.pixel = (255,0,0)
        codigo = obtener_codigo_patron()
        try:
            exec(codigo)
        except Exception as e:
            print("Error al ejecutar código:", e)
    time.sleep(0.5)
