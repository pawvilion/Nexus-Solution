# Nexus Solution

Asistente con IA que organiza tu semana: escribes tus tareas (duración, prioridad, día fijo) y tus preferencias, y Nexus te devuelve un horario semanal. Hecho con **Streamlit** y la **API de OpenAI (ChatGPT)**.

## Equipo y reparto

| Persona | Rol | Archivos de los que se encarga |
|---------|-----|-------------------------------|
| Pablo | **1 · Interfaz** | `app.py` (pantallas, formulario, vista de la semana) |
| (nombre) | **2 · IA** | `nexus/ia.py`, `nexus/prompts.py` (conexión con ChatGPT y los prompts) |
| (nombre) | **3 · Lógica, datos y despliegue** | `nexus/modelos.py`, `nexus/planificador_demo.py`, `requirements.txt`, publicación en Streamlit Cloud |

Cada uno trabaja sobre todo en sus archivos, así casi no habrá conflictos. `nexus/modelos.py` es el "contrato" entre todos: si cambias un campo, avisa al grupo antes.

### Ideas de tareas por rol

- **Interfaz:** editar/borrar tareas sueltas, vista de calendario más bonita, botón para descargar el horario.
- **IA:** mejorar el prompt, que la IA explique el plan, permitir escribir las tareas en lenguaje natural ("tengo examen el jueves y quiero ir al gimnasio 3 veces").
- **Lógica y despliegue:** mejorar el planificador demo (descansos, repartir tareas largas), exportar a Google Calendar (`.ics`), publicar en Streamlit Cloud.

## Cómo ejecutarlo en tu ordenador

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

**Sin API key la app funciona en "modo demo"** con un planificador simple sin IA, así podemos avanzar aunque todavía no tengamos créditos.

Cuando haya API key: copia `.streamlit/secrets.toml.example` como `.streamlit/secrets.toml` y pon la clave. Ese archivo **nunca se sube a GitHub** (ya está en `.gitignore`).

## Publicar en Streamlit Cloud

1. Entra en https://share.streamlit.io con la cuenta de GitHub.
2. `New app` → repositorio `Nexus-Solution`, rama `main`, archivo `app.py`.
3. En `Advanced settings → Secrets` pega el contenido de `secrets.toml` con la clave real.

## Trabajar en equipo

Lee [GUIA_EQUIPO.md](GUIA_EQUIPO.md) para saber cómo descargar el proyecto y trabajar sin pisarnos.
