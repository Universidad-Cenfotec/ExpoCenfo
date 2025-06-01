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
from secrets import secrets

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
