# **Cómo conectar un ESP32 a un servidor local con Ollama — Guía paso a paso**

Jorge Ortega  
Coordinador MakerLab  
Universidad CENFOTEC

Con esta guía podrás conectar tu ESP32 a un servidor Flask que utiliza un modelo local de lenguaje con **Ollama**, como `deepseek-coder`, para generar respuestas a preguntas dinámicas. 

- [En este link el profesor Jorge Ortega, explica como hacerlo](https://youtu.be/d4747ZCveP4?si=nLi5QnsJbab93LWO)
- [Este es un video del profesor Tomás de Camino Beck, explicando Ollama](https://youtu.be/FgAk917ALwc?si=4PyimOd2cJuA8F2u)




![arq](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/documentos/Ollama_ESP32.png)

---

## **Materiales necesarios**

* Una placa **ESP32** (cualquier modelo compatible con Wi-Fi)
* Cable USB
* PC con **CircuitPython** o entorno compatible con `adafruit_requests`
* Conexión Wi-Fi disponible
* Un servidor con Python y **Ollama** instalado

---

## **Paso 1: Preparar el servidor con Flask y Ollama**

1. Asegúrate de tener instalado Python 3.8 o superior.
2. Instala Flask:
   ```bash
   pip install flask
   ```
3. Instala Ollama y el modelo que vas a usar:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull deepseek-coder
   ```
4. Crea un archivo `server.py` con el siguiente código:

```python
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    print(f"Datos recibidos: {data}")

    model = data.get("model")
    prompt = data.get("prompt")
    
    if not model or not prompt:
        return jsonify({"error": "Faltan 'model' o 'prompt' en la solicitud"}), 400

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return jsonify({"response": result.stdout.strip()})
        else:
            return jsonify({"error": "Error ejecutando Ollama", "details": result.stderr}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=11434)
```

5. Ejecuta el servidor:
   ```bash
   python server.py
   ```

---

## **Paso 2: Preparar el código del ESP32**

Asegúrate de que tu ESP32 tenga cargado CircuitPython y los paquetes necesarios como `wifi`, `socketpool` y `adafruit_requests`.

```python
import wifi
import socketpool
import adafruit_requests
from secrets import secrets

# Conectarse al WiFi
print("Conectando a WiFi...")
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("¡Conectado a WiFi!")
print("IP:", wifi.radio.ipv4_address)

# Crear el pool de sockets y la sesión de requests
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool)

# Definir la URL del servidor Flask
url = "http://192.168.100.49:11434/api/generate"

# Solicitar al usuario que ingrese el prompt dinámico
user_prompt = input("¿Qué te gustaría preguntar?\n")

# Datos del cuerpo de la solicitud, usando el prompt ingresado por el usuario
data = {
    "model": "deepseek-coder",
    "prompt": user_prompt
}

# Intentar hacer una solicitud HTTP POST
try:
    print("Intentando enviar solicitud POST al servidor Flask...")
    response = requests.post(url, json=data)
    print("¡Servidor alcanzado!")
    print("Código de estado:", response.status_code)
    print("Contenido:", response.text)
except Exception as e:
    print("No se pudo conectar al servidor:", e)
```

---

## **Paso 3: Crear el archivo de secretos**

Crea un archivo llamado `secrets.py` en tu ESP32 con este contenido (reemplaza con tus datos reales):

```python
secrets = {
    "ssid": "TU_SSID",
    "password": "TU_PASSWORD"
}
```

---

## **Paso 4: Probar todo**

1. Conecta el ESP32 a tu PC.
2. Usa un editor como Thonny o Mu para cargar el código.
3. Asegúrate de que el servidor Flask esté ejecutándose en la misma red local.
4. Corre el código del ESP32.
5. Ingresa un prompt cuando lo solicite, por ejemplo: `¿Qué hace un for loop en Python?`

👉 El servidor responderá con la salida generada por el modelo local.

---

## **Consejos adicionales**

* Asegúrate de que el firewall no bloquee el puerto 11434.
* Puedes modificar el modelo (por ejemplo, usar `llama3` o `codellama`) simplemente cambiando `"model": "..."` en el cuerpo del JSON.
* Para mayor seguridad, podrías restringir el acceso al servidor sólo a IPs locales.

---
