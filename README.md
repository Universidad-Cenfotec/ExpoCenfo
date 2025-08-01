# ExpoCenfo 2025

La Universidad CENFOTEC se enorgullece en presentar una nueva edición de EXPOCENFO, la competencia universitaria que impulsa el ingenio, la innovación y la aplicación práctica del conocimiento en sistemas computacionales.

>**ExpoCenfo está abierto a todos y todas las etudiantes universitarias. [Información de inscripción en este link](https://ucenfotec.ac.cr/expocenfo/)**

Este año, el reto lleva a los participantes a la frontera del desarrollo tecnológico: la construcción de sistemas computacionales ejecutados en microcontroladores, potenciados por Modelos de Lenguaje de Gran Escala (LLMs).

El desafío consiste en diseñar y programar soluciones inteligentes capaces de percibir su entorno en tiempo real y generar respuestas dinámicas procesadas por un LLM, integrando sensores, procesamiento local y capacidades de lenguaje natural en el borde.

EXPOCENFO 2025 representa una oportunidad única para que los estudiantes universitarios desarrollen sistemas ciberfísicos avanzados, donde la creatividad, el pensamiento computacional y el dominio técnico convergen para dar forma al futuro de la computación embebida con inteligencia artificial.


Ver video de introducción:
[![ExpoCenfo](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/expoCenfo_Intro.jpg)](https://youtu.be/sKXtmYAvaPw?si=QJJzsI-w2-VWVzDZ)

**ExpoCenfo está abierto a todos y todas las etudiantes universitarias. [Información de inscripción en este link](https://ucenfotec.ac.cr/expocenfo/)**


## Kit ExpoCenfo

[EL kit ExpoCenfo consiste en una placa IdeaBoard (que es un ESP32) y un potenciómetro (para pruebas)](https://youtu.be/wZwcNW3o1u0?si=PoNOVPjaHQei806x), que se entrega de forma gratuita a todos y todas las participantes en el reto. Además en el Makerspace CENFOTEC, se cuentan con una colección de sensores y actuadores, que pueden ser utilizados por los participantes para sus proyectos.

¡Que comience el reto!

---
## Contenidos del repositorio

### Códigos y Ejemplos
- [Unpacking del Kit ExpoCenfo](https://youtu.be/wZwcNW3o1u0?si=PoNOVPjaHQei806x)
- [Video de como trabajar con el IdeaBoard y Circuit Python](https://youtu.be/GzA7peI1woc?si=t7AypJyVjUAOKnQ7)
- [Guía para configurar DeepSeek local y conectar con EPS32 (IdeaBoard)](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/Ejemplos_LLM_ESP32/ESP32_Ollama_Guide.md)
- [Guía de conexión de Google Gemini con el ESP32 (IdeaBoard)](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/Ejemplos_LLM_ESP32/Gemini_ESP32.md)
- [Ejemplo sencillo "Oblique Strategies", usa Gemini que comunica con ESP32](https://github.com/Universidad-Cenfotec/ExpoCenfo/tree/main/Ejemplos_LLM_ESP32/Ejemplo_Olbique_Strategies)
- [Ejemplo donde el ESP32 se "reprograma"a través de un código generado por Gemini](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/Ejemplos_LLM_ESP32/Micro%20Se%20Reprograma/README.md)
- [Ejemplo construyendo un servidor MCP para conectar con Gemini, y recibir peticiones de un ESP32](https://github.com/Universidad-Cenfotec/ExpoCenfo/tree/main/Ejemplos_LLM_ESP32/ESP32-MCPServer-Gemini)
- [Ejemplo de Google Gemini controlando un robot](https://github.com/Universidad-Cenfotec/Sumobot/blob/main/c%C3%B3digos_de_ejemplo/LLM_in_the_Loop_Robotics/README.md)

### Documentos
- [Reglas para proyectos ExpoCENFO](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/documentos/Juzgamiento%20de%20equipos-ExpoCenfo-2025.pdf)
- [Plantilla de entrega preliminar](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/documentos/Plantilla_Avance_Preliminar_CDIO.md)
- [Como crear un repositorio GitHub para el proyecto.](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/documentos/Guia_Documentacion_Proyectos_Borde_LLMs.md)

---

## Sistemas ciberfísicos Inteligentes

![arq_sis](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/documentos/Arq_Sist.png)

Este esquema representa un sistema ciberfísico inteligente en el que un microcontrolador (como el IdeaBoard basado en ESP32) actúa como puente entre el entorno físico y un modelo de lenguaje en la nube, como Gemini o ChatGPT. El sistema percibe el entorno mediante sensores que recogen información relevante (como temperatura, luz, sonido o movimiento), y esa información es procesada por el microcontrolador, el cual genera un **prompt** que describe el contexto o plantea una consulta. A través de una conexión WiFi y una clave de API, ese prompt se envía a un modelo de lenguaje avanzado alojado en la nube.

El modelo de lenguaje procesa el prompt y genera una respuesta inteligente que puede incluir un plan de acción, instrucciones, código o datos específicos. Esta respuesta regresa al microcontrolador, que la interpreta para tomar decisiones y actuar sobre el entorno mediante actuadores, como motores, luces u otros dispositivos. De esta forma, el sistema logra una interacción dinámica con el entorno, combinando percepción, razonamiento en la nube y acción local, lo cual permite construir soluciones adaptativas y autónomas aplicables a robótica, automatización, educación y más.

## Implicaciones de sistemas generativos conectados con microcontroladores

La naturaleza impredecible y generativa de los modelos de lenguaje tiene implicaciones profundas cuando se integran en sistemas físicos controlados por microcontroladores. Estos sistemas, tradicionalmente gobernados por lógica determinista, comienzan a comportarse de forma más dinámica, adaptable y contextual cuando se enlazan con una inteligencia generativa externa.

En primer lugar, la no repetibilidad exacta de las respuestas del modelo permite que un mismo sensor o estímulo pueda desencadenar distintas respuestas cada vez. Esto convierte a los microcontroladores en agentes más expresivos y flexibles. Por ejemplo, un robot educativo puede recibir una instrucción nueva o una sugerencia diferente de comportamiento ante la misma condición ambiental, lo que le permite evolucionar o improvisar dentro de límites definidos. Ya no está atado a scripts estáticos, sino que puede “conversar” con un modelo para redefinir su conducta.

Desde la perspectiva del diseño de sistemas, esto introduce un nuevo paradigma, la programación dinámica basada en lenguaje. El microcontrolador deja de ser únicamente un ejecutor de rutinas fijas y se convierte en un intérprete que colabora con un modelo generativo para actualizar su lógica, sus patrones de acción o incluso sus reglas de interacción en tiempo real. Esto abre la puerta a sistemas que pueden adaptarse a entornos cambiantes, personalizar respuestas para diferentes usuarios o explorar comportamientos creativos sin intervención humana directa.

Sin embargo, esta variabilidad también plantea desafíos importantes. La incertidumbre inherente a los modelos generativos puede ser un problema en entornos donde la precisión y la repetibilidad son críticas. Por esta razón, el diseño de estos sistemas híbridos requiere establecer límites de seguridad, mecanismos de verificación y estructuras de control que equilibren la creatividad del modelo con la estabilidad del sistema físico.

También surge un nuevo campo de exploración: el diseño de interfaces entre el lenguaje natural generado por modelos y las acciones codificadas que pueden ejecutar los microcontroladores. Esto requiere la creación de lenguajes intermedios, intérpretes simbólicos o sistemas de traducción que permitan convertir frases complejas en acciones concretas y seguras. A la vez, exige nuevas formas de depuración y pruebas, ya que los comportamientos no son totalmente predecibles y deben validarse en función del contexto.

En última instancia, al conectar microcontroladores con modelos generativos, se trasciende la noción de máquina programada y se entra en el terreno de sistemas *co-creativos*, capaces de colaborar con humanos y con su entorno para generar soluciones inéditas. Esta convergencia entre el mundo físico y la inteligencia lingüística generativa está abriendo nuevas posibilidades para la robótica, la automatización contextual, los entornos inteligentes y la interacción humano-máquina.


