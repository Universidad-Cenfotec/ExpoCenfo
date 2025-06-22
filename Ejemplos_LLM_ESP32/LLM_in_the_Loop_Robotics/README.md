## Robótica LLM-in-the-Loop

Tomás de Camino Beck, Ph.D.  
Universidad CENFOTEC  

EL programa [`code_grid_gemini.py`](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/Ejemplos_LLM_ESP32/LLM_in_the_Loop_Robotics/code_grid_gemini.py) implementa un sistema robótico que combina navegación autónoma con generación de instrucciones usando inteligencia artificial generativa. Es un ejemplo práctico de:

* **AGVs (Automated Guided Vehicles)**: robots que se mueven en un entorno siguiendo rutas definidas.
* **LLM-in-the-Loop Robotics**: una arquitectura donde un modelo de lenguaje grande (LLM) como Gemini participa en tiempo real en la toma de decisiones del robot.

El robot se desplaza sobre una cuadrícula de líneas negras utilizando sensores infrarrojos para mantenerse en el camino y un giroscopio para girar con precisión. La secuencia de movimientos no está preprogramada; en cambio, se genera dinámicamente al enviar un "prompt" a Gemini, que devuelve una lista de comandos como `F, L, R` (Forward, Left, Right).

Para este ejercicio, se utiliza el [Sumobot de CENFOTEC](https://github.com/Universidad-Cenfotec/Sumobot) pero aplica en general para cualquier robot que cuente con giroscópio, y sensores IR seguidores de Línea

Detalles de como conectar el ESP32 a Gemini lo spueden ver en [este video](https://youtu.be/rFI_8TIMCNI?si=_rteSFMyBVmcoIL1). Este código utiliza ese ejemplo de base.

---

## Componentes clave del sistema

### Conexión a red y configuración

El bloque inicial configura el robot para conectarse a una red WiFi usando las credenciales definidas en el archivo `secrets.py`. Luego establece una sesión HTTPS con la API de Gemini.

### Botón de activación

Se configura el pin `IO0` (botón BOOT del ESP32) como entrada digital. Solo cuando este botón es presionado y soltado, el robot solicita instrucciones a Gemini y ejecuta la secuencia generada. Esto permite control manual sobre cuándo iniciar una navegación.

```python
keys = keypad.Keys((board.IO0,), value_when_pressed=False, pull=True)
```

---

## Interacción con Gemini (LLM-in-the-Loop)

### `obtener_movimientos(inicio, final)`

Genera un texto (prompt) como el siguiente:

> Necesito una secuencia de comandos c1,c2,c3,... donde cada comando c puede ser F, L o R, para que un robot se mueva del punto (0, 0) al punto (2, 3)...

Este prompt se envía a Gemini, y se espera una respuesta directa con una lista de comandos, por ejemplo:

```
F,F,L,F,F,R,F
```

### `preguntar_gemini(prompt)`

Hace la solicitud HTTP a Gemini usando el método POST. Si la respuesta es válida, extrae el texto generado por el modelo.

---

## Movimiento y navegación

### `forward_line_stop()`

Esta función hace que el robot avance sobre una línea negra, utilizando dos sensores delanteros y dos traseros. Se detiene cuando detecta una intersección (ambos sensores traseros detectan línea negra).

### `girar_grados(grados, drift)`

Usa el giroscopio para girar con precisión 90 grados a la izquierda o derecha, compensando el drift del sensor (deriva natural que se calibra previamente).

---

## Ejecución de la secuencia

### `execute(commandlist)`

Recorre la lista de comandos `['F', 'F', 'L', 'F']` y ejecuta la función correspondiente:

* `F` llama a `forward_line_stop()`
* `L` llama a `girar_grados(-90)`
* `R` llama a `girar_grados(90)`

Este mecanismo abstrae las acciones concretas del robot, permitiendo que las decisiones de alto nivel sean tomadas por el LLM.

---

## Loop principal

```python
while True:
    event = keys.events.get()
    if event and event.released:
        ...
```

Solo si se presiona y suelta el botón, el robot solicitará la ruta a Gemini, la interpretará y la ejecutará. Esto previene ejecuciones accidentales o en bucle.

te y adaptable. Representa una convergencia entre robótica física y modelos generativos, y puede considerarse una introducción experimental a las arquitecturas **LLM-in-the-Loop**, donde la lógica de comportamiento no es codificada directamente, sino generada en tiempo real mediante IA.

---

## EL "Prompt"

```
## Objetivo
Devuelve **solo** una lista CSV con los comandos mínimos que llevan al robot
desde {inicio} hasta {final} sobre una cuadrícula cartesiana.

## Comandos permitidos
F – Avanza 1 unidad en la dirección actual  
L – Gira 90° a la izquierda en su lugar  
R – Gira 90° a la derecha en su lugar  

## Restricciones de salida
- Sin texto adicional, títulos, comillas ni espacios.
- Usa mayúsculas.  
- Los comandos deben estar separados solo por comas
  (ej.: L,F,F,R,F).

## Parámetros de entrada
- `{inicio}`  ➜  tupla `(x₀, y₀)` donde el robot siempre mira al N  
- `{final}`   ➜  tupla `(x₁, y₁)`  
La orientación final siempre es al norte

**Ejemplo de salida válida**  
`L,F,F,F,R,F,F`
```

---

### Explicación de cada elemento

| Sección                      | Propósito                                                  | Detalles clave                                                                                                                     |
| ---------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Objetivo**                 | Define la tarea primaria para el LLM.                      | Pide la “lista CSV” y aclara el camino a generar (de `{inicio}` a `{final}`) en una cuadrícula.                                    |
| **Comandos permitidos**      | Especifica el vocabulario exacto que el modelo puede usar. | Se declaran F, L, R y se describe la semántica de cada uno; así se evita que el modelo invente acciones.                           |
| **Restricciones de salida**  | Impone el formato de respuesta y prohíbe texto redundante. | Al indicar “sin texto adicional” y “sin espacios” se garantiza que el resultado pueda pasarse directamente a tu función `execute`. |
| **Parámetros de entrada**    | Establece las variables que el sistema externo inyectará.  | `{inicio}` incluye orientación inicial θ₀ para que el LLM pueda planificar el primer giro; `{final}` solo necesita posición.       |
| **Ejemplo de salida válida** | Proporciona una referencia concreta que guía al modelo.    | El ejemplo muestra mayúsculas, comas y ausencia de espacios, reforzando las reglas de formato.                                     |

#### Por qué es adecuado para *LLM-in-the-Loop Robotics*

* **Claridad semántica**: el LLM recibe un dominio de comandos cerrado, lo que facilita validación automática y evita acciones ambiguas.
* **Formato estrictamente controlado**: permite que el software embarcado parsee la respuesta sin preprocesamiento complejo.
* **Variables inyectables**: `{inicio}` y `{final}` pueden sustituirse dinámicamente en cada iteración del bucle de control, integrando al modelo dentro del ciclo de decisión del robot.
* **Ejemplo orientativo**: reduce la entropía de la salida, algo crítico cuando la respuesta se usará directamente para ejecutar hardware.

