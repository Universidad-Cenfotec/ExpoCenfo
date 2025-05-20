# Interprete de Comandos

Tomás de Camino Beck, Ph.D.  
Universidad CENFOTEC

## ¿Qué es un intérprete de comandos?

Un **intérprete** es un programa que **lee instrucciones escritas en un lenguaje sencillo**, las **entiende** y luego **ejecuta acciones**. En este caso, estamos creando un intérprete que permite controlar un robot (o cualquier dispositivo) escribiendo comandos como:

```
mover 50
girar 90
parar
```

Este enfoque permite separar la **lógica del hardware** de la **interacción humana**, facilitando códigos dinámicos.

---

## Estructura del proyecto

Este intérprete está dividido en **dos archivos**:

---

### 1. `interprete.py`: la librería del intérprete

Este archivo contiene una **clase llamada `Interprete`**, que actúa como el "cerebro" que entiende los comandos. Tiene tres partes importantes:

#### `registrar(nombre, funcion)`

Sirve para **registrar comandos** que queremos usar. Por ejemplo, si queremos que el comando `mover` haga que el robot avance, escribimos:

```python
interprete.registrar("mover", mover)
```

Esto significa: *cuando alguien escriba `mover`, quiero que se ejecute la función `mover()`*.

#### `ejecutar(linea)`

Esta función **recibe una línea de texto**, como `"girar 90"`, la **separa en partes**, y llama a la función correspondiente con los **parámetros adecuados** (en este caso, `90`).

#### `_convertir(valor)`

Esta función ayuda al intérprete a **entender los parámetros**. Por ejemplo, si alguien escribe `"100"`, intenta convertirlo a número (`int` o `float`) automáticamente.

---

### 2. `Ejemplo_Interprete.py`: el programa principal

Este archivo es el que corre en el microcontrolador (por ejemplo, un ESP32 o un Circuit Playground).

#### ¿Qué hace?

1. **Define funciones reales** como `mover`, `girar`, `parar`, que simulan controlar un robot.
2. **Crea una instancia del intérprete** con `i = Interprete()`.
3. **Registra los comandos** con sus funciones.
4. **Espera a que el usuario escriba un comando** en la consola (por ejemplo por el USB serial).
5. **Ejecuta el comando** usando `i.ejecutar(linea)`.

---

## Ejemplo de uso en la práctica

Supongamos que conectamos nuestro ESP32 por USB y abrimos la consola serial (REPL). El usuario puede escribir:

```
>> mover 100
```

Y en pantalla aparecerá:

```
Moviendo 100 cm
```

Esto quiere decir que:

* El intérprete leyó el texto.
* Identificó que el comando es `mover`.
* Tomó el parámetro `100`, lo convirtió a número.
* Llamó a la función `mover(100)`.

---

## ¿Por qué es útil este proyecto?

* Permite **modificar el comportamiento del robot sin reprogramar todo**.
* Se pueden **agregar nuevos comandos fácilmente**, ideal para talleres o retos.
* Facilita la **comunicación con el robot en tiempo real**, útil para pruebas o educación.
* Se puede extender para recibir comandos desde **Bluetooth, UART, WiFi o archivos**.

---

## Posibles extensiones pedagógicas

* Implementar un comando `repetir 3 mover 10` para bucles simples.
* Leer comandos desde un archivo `.txt` y reproducirlos como una coreografía de movimiento.
* Agregar un sistema de variables y condiciones.
* Usar sensores para que el robot actúe con base en comandos más complejos (`si obstaculo mover 0`).

