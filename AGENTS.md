# Instrucciones para asistentes de código (Codex, Claude Code…)

Proyecto de hackatón: **Nexus**, una app Streamlit que organiza la semana del usuario con la API de OpenAI.

- Responde y comenta el código en **español**.
- Nunca hagas commits en `main`: trabaja en la rama del compañero (ej. `pablo-...`) y los cambios entran por Pull Request.
- Respeta el reparto de archivos del README (Interfaz / IA / Lógica). Si tienes que tocar un archivo de otro rol, díselo al usuario.
- `nexus/modelos.py` es el contrato compartido entre todos; no cambies sus campos sin avisar.
- La app debe seguir funcionando **sin API key** (modo demo con `nexus/planificador_demo.py`).
- Nunca escribas claves en el código ni subas `.streamlit/secrets.toml`. Las claves se leen con `st.secrets`.
- Mantén el código sencillo: somos un equipo que está aprendiendo.
- Para probar: `streamlit run app.py`.
