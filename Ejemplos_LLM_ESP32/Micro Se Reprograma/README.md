![rock](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/Ejemplos_LLM_ESP32/Micro%20Se%20Reprograma/RockPrompt.jpeg)
# Ejemplo de el ESP32 pidiendo a Gemini que lo reprograme

Tomás de Camino Beck, Ph.D.  
Universidad CENFOTEC

---

## ¿Puede un microcontrolador reprogramarse a sí mismo?

Hasta hace poco, los microcontroladores eran dispositivos que ejecutaban instrucciones fijas, programadas directamente por una persona. Una vez subido un programa, este simplemente repetía el mismo comportamiento, sin posibilidad de adaptarse o cambiar.

Pero con la llegada de los modelos de lenguaje como Gemini, esto cambia radicalmente. Ahora, un microcontrolador puede conectarse a internet, enviar una pregunta a un modelo de lenguaje, recibir un código generado en respuesta, y **ejecutarlo en tiempo real**. Esto significa que puede *reprogramarse a sí mismo* dinámicamente, según la situación o incluso de forma creativa.

Este tipo de arquitectura marca el inicio de una nueva etapa: la de sistemas ciberfísicos generativos, donde la inteligencia no está completamente dentro del microcontrolador, sino que proviene de una conversación con un modelo de lenguaje externo.

---

## ¿Qué hace este programa?

El programa está diseñado para ejecutarse en una **IdeaBoard con ESP32**, que se conecta a una red WiFi y se comunica con el modelo de lenguaje Gemini de Google. El microcontrolador:

1. Se conecta a internet.
2. Espera que el usuario presione un botón.
3. Al detectar el botón, envía una solicitud al modelo de lenguaje, pidiéndole que genere un patrón de luces RGB al estilo de una canción de rock.
4. Recibe ese patrón en forma de código Python.
5. Ejecuta ese código en el momento.

Este es un ejemplo simple, pero muestra con claridad el concepto de reprogramación dinámica asistida por inteligencia artificial.

[Pueden ver el progrma corirendo en este video](https://drive.google.com/file/d/1q_SMAtNqfTIBnznBlVCm2VLlt7Nw-OPF/view?usp=sharing)

---

## Organización de la información confidencial

Es importante no colocar directamente en el código principal información como:

* Nombre de la red WiFi (SSID)
* Contraseña de la red
* Clave API del modelo de lenguaje

Para eso se utiliza un archivo separado llamado `secrets.py`, que contiene un diccionario con esta información. Este archivo debe tener el siguiente formato:

```python
# secrets.py
secrets = {
    'ssid': 'NombreDeTuWiFi',
    'password': 'TuContraseñaWiFi',
    'api_key': 'TuClaveAPIdeGemini'
}
```

Este archivo debe guardarse en el mismo dispositivo que el archivo principal, pero **no debe compartirse ni subirse a internet**, ya que contiene información privada.

---

## Explicación del código paso a paso

### 1. Importación de librerías

El programa importa los módulos necesarios para controlar el hardware, manejar conexiones de red y trabajar con la API de Gemini.

```python
from ideaboard import IdeaBoard
import time, board, busio, keypad
import socketpool, ssl, wifi
import adafruit_requests as requests
from secrets import secrets
```

* `ideaboard`: biblioteca para controlar el hardware específico.
* `wifi`, `socketpool`, `ssl`: para manejar la conexión a internet.
* `requests`: permite hacer peticiones HTTPS al modelo de lenguaje.
* `secrets`: archivo con los datos privados.

### 2. Conexión a internet

El microcontrolador se conecta a la red WiFi utilizando los datos del archivo `secrets.py`.

```python
wifi.radio.connect(secrets["ssid"], secrets["password"])
```

Si la conexión es exitosa, el dispositivo enciende el LED verde por un momento para indicar que ya está conectado.

### 3. Preparación del acceso a Gemini

El endpoint de la API se arma con la clave que está guardada en el archivo de secretos.  [Pueden seguir este tutorial para ver como se genera la llave](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/Ejemplos_LLM_ESP32/Gemini_ESP32.md)

```python
api_key = secrets["api_key"]
endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
```

También se configura el sistema de red seguro con `socketpool` y `ssl`.

### 4. Función `preguntar_gemini(pregunta)`

Esta función toma una cadena de texto como pregunta, la envía al modelo de lenguaje y espera una respuesta.

```python
def preguntar_gemini(pregunta):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": pregunta}]}],
        "generationConfig": {"maxOutputTokens": 120}
    }
    response = https.post(endpoint, headers=headers, json=payload)
```

El resultado es el texto generado por el modelo, que en este caso será un fragmento de código Python.

### 5. Función `obtener_codigo_patron()`

Esta función define una pregunta específica para Gemini, pidiéndole que escriba una secuencia de colores RGB estilo `ib.pixel = (R,G,B)`, que represente una canción de rock.

```python
def obtener_codigo_patron():
    pregunta = "¿Podrías hacer una secuencia de colores como ib.pixel = (R,G,B) con tiempos, que represente una canción de rock?"
    return preguntar_gemini(pregunta)
```

### 6. Configuración del botón

Se usa la biblioteca `keypad` para monitorear si el botón (conectado al pin IO0) ha sido presionado.

```python
keys = keypad.Keys((board.IO0,), value_when_pressed=False, pull=True)
```

### 7. Bucle principal del programa

El código entra en un ciclo que se repite constantemente. En cada vuelta:

* Revisa si se ha soltado el botón.
* Si es así, imprime "Generando código", llama a `obtener_codigo_patron()`, y ejecuta el código que recibió de Gemini.

```python
while True:
    event = keys.events.get()
    if event and event.released:
        print("Generando código")
        ib.amarillo = True
        codigo = obtener_codigo_patron()
        ib.amarillo = False
        try:
            exec(codigo)
        except Exception as e:
            print("Error al ejecutar código:", e)
```

El LED amarillo se enciende mientras espera la respuesta y se apaga después.

---

## Consideraciones importantes

* **Seguridad**: el uso de `exec()` permite ejecutar cualquier código, por lo tanto se debe tener cuidado de no utilizar este tipo de sistemas en aplicaciones críticas o con conexiones públicas sin restricciones.
* **Uso educativo**: este programa está diseñado para exploración, prototipado y enseñanza. Permite a los estudiantes experimentar con la generación de comportamiento en tiempo real, entendiendo cómo un sistema puede combinar hardware, conectividad e inteligencia artificial.
* **Extensibilidad**: aunque en este caso el ejemplo se limita a luces RGB, el mismo principio puede usarse para generar sonidos, controlar motores, responder a sensores o incluso tomar decisiones de navegación en un robot.


