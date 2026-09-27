# Nexus Solution

Nexus es la compañera de Bárbara, de **Terapias Dalmeet**, para ganar alcance. Ella cuenta una idea, un sueño o algo que le pasó, tal como le salga, y Nexus lo convierte en algo que puede usar hoy: un guion para redes, una experiencia para ofrecer o una propuesta para llegar a gente nueva. Todo con su voz.

Hecho con **Streamlit** y la **API de OpenAI (ChatGPT)** para la Hackatón FAE USACH 2026. El contexto completo del cliente está en [docs/CONTEXTO.md](docs/CONTEXTO.md) y lo que pide el jurado en [docs/ENTREGA.md](docs/ENTREGA.md).

## Módulos

| Módulo | Qué hace |
|--------|----------|
| ✍️ Guion para redes | Idea o anécdota → guion de reel o carrusel, texto, idea visual y cuándo publicar |
| 🌱 Laboratorio de experiencias | Inspiración → experiencia o servicio concreto (ej. "Crea tu guatero conmigo") |
| 🤝 Difusión fuera de redes | A quién quiere llegar → qué ofrecer y mensaje listo para enviar |

## Equipo y reparto

| Persona | Rol | Archivos de los que se encarga |
|---------|-----|-------------------------------|
| Pablo | **1 · Interfaz y esencia** | `app.py`, `nexus/esencia.md` (la voz y la visión de Bárbara) |
| (nombre) | **2 · IA y guiones** | `nexus/ia.py`, `nexus/prompts.py` (personalidad de Nexus, módulo de guiones) |
| (nombre) | **3 · Experiencias, difusión y despliegue** | Módulos 2 y 3 en `nexus/prompts.py`, `nexus/demo.py`, publicación en Streamlit Cloud |

`nexus/prompts.py` lo comparten las personas 2 y 3: avisad en el grupo antes de editarlo para no pisaros.

## Estructura

```
app.py               ← interfaz: conversación con Nexus y selector de módulo
nexus/esencia.md     ← quién es Bárbara, qué cree y qué sueña (la IA lo lee siempre)
nexus/prompts.py     ← personalidad de Nexus, límites y los 3 módulos
nexus/ia.py          ← conexión con ChatGPT
nexus/demo.py        ← respuestas de ejemplo cuando no hay API key
docs/                ← contexto del cliente y guía de la entrega
```

## Cómo ejecutarlo en tu ordenador

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

**Sin API key la app funciona en modo demo**, con respuestas de ejemplo. Cuando haya API key, copia `.streamlit/secrets.toml.example` como `.streamlit/secrets.toml` y pon la clave. Ese archivo **nunca se sube a GitHub** (ya está en `.gitignore`).

## Publicar en Streamlit Cloud

1. Entra en https://share.streamlit.io con la cuenta de GitHub.
2. `New app` → repositorio `Nexus-Solution`, rama `main`, archivo `app.py`.
3. En `Advanced settings → Secrets` pega el contenido de `secrets.toml` con la clave real.

## Trabajar en equipo

Lee [GUIA_EQUIPO.md](GUIA_EQUIPO.md) para saber cómo descargar el proyecto y trabajar sin pisarnos.
