# Tomás de Camino Beck
# Proyecto: Botón que genera frase Oblique Strategy y la muestra en LCD

import time
import board
import busio
import keypad
import socketpool
import ssl
import wifi
import adafruit_requests as requests
from lcd import LCD, CursorMode
from i2c_pcf8574_interface import I2CPCF8574Interface
from secrets import secrets  # Este archivo debe tener 'ssid', 'password', 'api_key'

# ------------------------
# Inicializa conexión WiFi
# ------------------------
print("Conectando al WiFi...")
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Conectado a", secrets["ssid"])
print("IP:", wifi.radio.ipv4_address)

# ------------------------
# Configura sesión HTTPS
# ------------------------
socket = socketpool.SocketPool(wifi.radio)
https = requests.Session(socket, ssl.create_default_context())

# ------------------------
# Inicializa LCD
# ------------------------
i2c = board.I2C()
while not i2c.try_lock():
    pass

try:
    addresses = i2c.scan()
    if not addresses:
        print("No se encontraron dispositivos I2C.")
    else:
        print("Dispositivos I2C encontrados:", [hex(addr) for addr in addresses])
finally:
    i2c.unlock()

lcd_address = 0x27 if 0x27 in addresses else (0x3F if 0x3F in addresses else None)
if lcd_address is None:
    print("No se encontró un LCD compatible (0x27 o 0x3F).")
    lcd = None
else:
    interface = I2CPCF8574Interface(i2c, lcd_address)
    lcd = LCD(interface, num_rows=2, num_cols=16)
    lcd.clear()
    lcd.print("Esperando...")
    lcd.set_cursor_mode(CursorMode.HIDE)

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
        "generationConfig": {"maxOutputTokens": 60}
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

# ------------------------
# Detecta botón en GPIO0
# ------------------------
keys = keypad.Keys((board.IO0,), value_when_pressed=False, pull=True)

# ------------------------
# Loop principal
# ------------------------
while True:
    event = keys.events.get()
    if event and event.released:
        print("Botón presionado: generando frase...")
        if lcd:
            lcd.clear()
            lcd.print("Consultando...")

        frase = preguntar_gemini("Puedes generar una frase corta, estilo Oblique Strategies?")

        if lcd:
            lcd.clear()
            lcd.print(frase[:16])
            lcd.set_cursor_pos(1, 0)
            lcd.print(frase[16:32])
    time.sleep(0.1)
