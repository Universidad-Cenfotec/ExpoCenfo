"""
Ejemplo de leer un registro de un tag RFID y realizar una tarea

Conexiones:
RC-522 --> IdeaBoard
GND --> GND
3.3v --> 3.3v
SDA --> IO5
SCL --> IO18
MOSI --> IO23
MISO --> IO19
RST --> IO4
"""

import time
import board
from ideaboard import IdeaBoard
import mfrc522

ib = IdeaBoard()

reader = mfrc522.MFRC522(board.SCK, board.MOSI, board.MISO, board.IO4, board.IO5)

def leer_tag(rdr):

    rdr.set_antenna_gain(0x07 << 4)

    print("leyendo...")

    while True:
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                print(f"Tipo de tag: {tag_type:#x}")
                print(f"UID: {raw_uid[0]:#x}{raw_uid[1]:x}{raw_uid[2]:x}{raw_uid[3]:x}")
                if rdr.select_tag(raw_uid) == rdr.OK:
                    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                    if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                        data = rdr.read(8)
                        rdr.stop_crypto1()
                        return data
                    else:
                        print("Error de autenticacion")
                else:
                    print("Tag no seleccionado")


while True:
    data = leer_tag(reader)
    print(f"Data: {data[0]}")
    if data[0] == 255:
        ib.pixel = (255,0,0)
    elif data[0] == 0:
        ib.pixel = (0,255,0)
        