# Guía para Documentar Proyectos de Inteligencia en el Borde con LLMs en GitHub
Tomás de Camino Beck, Ph.D.  
Universidad CENFOTEC


## 1. Estructura del Repositorio
```
/docs/                   # Documentación extendida (diagramas, notas técnicas, PDFs)
/hardware/               # Esquemas, diagramas de conexión, archivos CAD/PCB
/software/               # Código fuente (microcontrolador, backend, scripts)
/models/                 # Modelos, prompts y configuraciones de LLM
/tests/                  # Pruebas unitarias y de integración
/examples/               # Ejemplos simples de uso del sistema
README.md                # Descripción general del proyecto
ARCHITECTURE.md          # Documentación detallada de la arquitectura
SETUP.md                 # Guía de instalación y despliegue
CONTRIBUTING.md          # Normas para colaborar en el proyecto
LICENSE                  # Licencia del proyecto
CHANGELOG.md             # Registro de cambios
```

## 2. Documentar el Diseño del Sistema

### a) Diagramas
- **Diagrama de arquitectura**: Usa [Mermaid](https://mermaid-js.github.io/) o [Draw.io](https://app.diagrams.net/), o cualquier otro.
- **Diagrama de flujo de datos**: Explica cómo se envía información entre sensores, microcontrolador y LLM.
- **Esquemas eléctricos**: Diagramas de conexiones (pines, sensores, actuadores).

### b) Descripción de Componentes
En `README.md` o `/docs/`:
- Lista de **microcontroladores** usados.
- **Sensores/actuadores** conectados.
- **LLM** empleado (cloud/local).
- **Librerías** clave (con links a documentación oficial).

## 3. Documentar el Código
### a) README principal
Debe incluir:
- Descripción breve.
- Objetivo del sistema.
- Imagen/diagrama representativo.
- Ejemplo básico de funcionamiento.

### b) Comentarios y estilo
- Código comentado (PEP8 para Python, Arduino Style Guide para C++).
- Uso de docstrings para explicar funciones y clases.

### c) Ejemplos reproducibles
- Scripts simples en `/examples/` para probar partes individuales.

### d) Registro de cambios (CHANGELOG)
```
## [1.0.1] - 2025-08-01
- Optimización del consumo de energía del ESP32.
- Soporte para prompts dinámicos en el LLM.
```

## 4. Documentar la Arquitectura
En `ARCHITECTURE.md`:
- **Vista general**: Cómo interactúan los componentes.
- **Capas del sistema**:
  - Percepción (sensores y recolección de datos).
  - Procesamiento local (microcontrolador).
  - Comunicación con el LLM (API/librerías).
  - Toma de decisiones y acción.
- **Decisiones de diseño** y **posibles mejoras**.

## 5. Recomendaciones Generales
- **Licencia**: Usa una licencia abierta (MIT, Apache 2.0).
- **Etiquetas e Issues**: Organiza tareas en GitHub.
- **Wiki del proyecto**: Para documentación extendida.
- **Visualizaciones**: Diagramas e imágenes para comprensión.
- **Ramas (branches)**: `main`, `dev`, `feature/nueva-funcionalidad`.

## 6. Plantillas útiles
- **Pull Requests**: Qué hace el cambio y cómo probarlo.
- **Issues**: Formato para reportar errores o sugerencias.
