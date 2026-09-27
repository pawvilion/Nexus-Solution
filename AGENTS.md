# Instrucciones para asistentes de código (Codex, Claude Code…)

Proyecto de hackatón: **Bárbara.IA**, una app Streamlit que ayuda a Bárbara (Terapias Dalmeet) a ganar alcance: convierte su inspiración en guiones, experiencias y propuestas de difusión con la API de OpenAI.

**Lee primero [docs/CONTEXTO.md](docs/CONTEXTO.md)** (quién es la clienta, qué construimos, nuestro diferenciador y las reglas que no se pueden romper) y [docs/ENTREGA.md](docs/ENTREGA.md) (qué evalúa el jurado).

- La plataforma se llama **Bárbara.IA** en todo lo que ve la usuaria o el jurado. "Nexus" es solo el nombre del equipo, del repositorio y de las carpetas de código (`nexus/`, `vistas/nexus.py`), que no se renombran.
- Responde y comenta el código en **español**.
- Nunca hagas commits en `main`: trabaja en la rama del compañero (ej. `pablo-...`) y los cambios entran por Pull Request.
- Respeta el reparto de archivos del README. Si tienes que tocar un archivo de otro rol, díselo al usuario.
- Nuestro diferenciador es la **cercanía**, no la complejidad técnica: prioriza que la app sea cálida y simple de usar antes que agregar funciones.
- **Bárbara la usa también desde el celular.** Todo debe verse bien a 375 px de ancho: nada que se salga de la pantalla, botones cortos en filas horizontales (`st.container(horizontal=True)`), gráficos con los nombres encima de las barras y no a un costado. Si agregas una página, súmala también al menú del celular en `app.py` (`menu_movil`).
- Los módulos se definen en `nexus/prompts.py` (`MODOS`); `app.py` los muestra automáticamente. Para agregar un módulo, agrega un modo ahí y su ejemplo en `nexus/demo.py`.
- La app debe seguir funcionando **sin API key** (modo demo con `nexus/demo.py`).
- Los prompts y los ejemplos nunca prometen curar ni usan la palabra "diagnóstico" (ver docs/CONTEXTO.md).
- Nunca escribas claves en el código ni subas `.streamlit/secrets.toml`. Las claves se leen con `st.secrets`.
- Mantén el código sencillo: somos un equipo que está aprendiendo.
- Para probar: `streamlit run app.py`.
