import socketpool
import ssl
import wifi
import adafruit_requests as requests

socket = socketpool.SocketPool(wifi.radio)
https = requests.Session(socket, ssl.create_default_context())

print("Connecting...")
wifi.radio.connect("ssid", "password")
print("Connected to Wifi!")

URL = "http://api.open-notify.org/iss-now.json"

data = https.get(URL).json()
print(data)
long = data["iss_position"]["longitude"]
lat = data["iss_position"]["latitude"]
print(f"The International Space Station is located at {lat}, {long}")