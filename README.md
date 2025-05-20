# ExpoCenfo 2025

La Universidad CENFOTEC se enorgullece en presentar una nueva edición de EXPOCENFO, la competencia universitaria que impulsa el ingenio, la innovación y la aplicación práctica del conocimiento en sistemas computacionales.

Este año, el reto lleva a los participantes a la frontera del desarrollo tecnológico: la construcción de sistemas computacionales ejecutados en microcontroladores, potenciados por Modelos de Lenguaje de Gran Escala (LLMs).

El desafío consiste en diseñar y programar soluciones inteligentes capaces de percibir su entorno en tiempo real y generar respuestas dinámicas procesadas por un LLM, integrando sensores, procesamiento local y capacidades de lenguaje natural en el borde.

EXPOCENFO 2025 representa una oportunidad única para que los estudiantes universitarios desarrollen sistemas ciberfísicos avanzados, donde la creatividad, el pensamiento computacional y el dominio técnico convergen para dar forma al futuro de la computación embebida con inteligencia artificial.

## Kit ExpoCenfo

EL kit ExpoCenfo consiste en una placa IdeaBoard (que es un ESP32) y un potenciómetro (para pruebas), que se entrega de forma gratuita a todos y todas las participantes en el reto. Además en el Makerspace CENFOTEC, se cuentan con una colección de sensores y actuadores, que pueden ser utilizados por los participantes para sus proyectos.

¡Que comience el reto!

---
## Contenidos del repositorio

### Códigos y Ejemplos
- [Ejemplo de uso de DeepSeek local con EPS32 (IdeaBoard)](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/Ejemplos_LLM_ESP32/ESP32_Ollama_Guide.md)
- [Ejemplo de Google Gemini con el ESP32 (IdeaBoard)](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/Ejemplos_LLM_ESP32/Gemini_ESP32.md)
- [Ejemplo sencillo "Oblique Strategies", usa Gemini que comunica con ESP32](https://github.com/Universidad-Cenfotec/ExpoCenfo/tree/main/Ejemplos_LLM_ESP32/Ejemplo_Olbique_Strategies)

### Documentos
- [Reglas para proyectos ExpoCENFO](https://github.com/Universidad-Cenfotec/ExpoCenfo/blob/main/documentos/Juzgamiento%20de%20equipos-ExpoCenfo-2025.pdf)

---

## Sistemas ciberfísicos Inteligentes



Este esquema representa un sistema ciberfísico inteligente en el que un microcontrolador (como el IdeaBoard basado en ESP32) actúa como puente entre el entorno físico y un modelo de lenguaje en la nube, como Gemini o ChatGPT. El sistema percibe el entorno mediante sensores que recogen información relevante (como temperatura, luz, sonido o movimiento), y esa información es procesada por el microcontrolador, el cual genera un **prompt** que describe el contexto o plantea una consulta. A través de una conexión WiFi y una clave de API, ese prompt se envía a un modelo de lenguaje avanzado alojado en la nube.

El modelo de lenguaje procesa el prompt y genera una respuesta inteligente que puede incluir un plan de acción, instrucciones, código o datos específicos. Esta respuesta regresa al microcontrolador, que la interpreta para tomar decisiones y actuar sobre el entorno mediante actuadores, como motores, luces u otros dispositivos. De esta forma, el sistema logra una interacción dinámica con el entorno, combinando percepción, razonamiento en la nube y acción local, lo cual permite construir soluciones adaptativas y autónomas aplicables a robótica, automatización, educación y más.

