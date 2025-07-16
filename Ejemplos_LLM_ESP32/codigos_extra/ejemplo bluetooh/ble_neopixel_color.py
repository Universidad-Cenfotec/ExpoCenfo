# Tomás de Camino Beck
# Universidad CENFOTEC

import time
import random
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from ideaboard import IdeaBoard
# set up the radio hardware
ble = BLERadio()
ib = IdeaBoard()

# By default, your device will have some name like CIRCUITPYxxxx; let's make that more user friendly
ble.name = "IdeaBoard_BLE_1"

# set up the UART service. This virtual serial port lets you send text over BLE.
uart = UARTService()

# set up advertising, so your phone or PC will know that UART service is available on your device
advertisement = ProvideServicesAdvertisement(uart)

def text_to_tuple(t: str) -> tuple:
    # Elimina los paréntesis y espacios
    t = t.strip("()").replace(" ", "")
    # Convierte los valores a enteros y los empaqueta en una tupla
    return tuple(map(int, t.split(",")))


while True:
    print("Advertising BLE services")
    # start advertising
    ble.start_advertising(advertisement)
    # keep going until we get a connection
    while not ble.connected:
        pass

    # if we got here, we have a connection. Stop advertising!
    ble.stop_advertising()
    print("BLE connected")

    # do some work as long as we're connected
    while ble.connected:
        # try reading some text from the UART, e.g. typed into the app
        raw_bytes = uart.readline()
        if raw_bytes:
            text = raw_bytes.decode("utf-8")
            print(f"Got text from central: {text}")
            ib.pixel = text_to_tuple(text)
 

    # we no longer have a connection, so we'll go back to the top of the loop
    print("BLE disconnected")

