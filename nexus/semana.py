"""La semana de Bárbara: qué días publica, prepara contenido, atiende, fabrica y compra insumos.

Responsable: Sofía.
Se ve siempre en la barra lateral (la dibuja app.py en todas las páginas) y Bárbara la edita
cuando algo no le acomoda. La IA también la recibe, para sugerir publicar en sus días de publicar.
Se guarda en data/semana.json, igual que la memoria (fuera de GitHub).
"""

import json
from html import escape
from pathlib import Path

import streamlit as st

ARCHIVO = Path(__file__).parent.parent / "data" / "semana.json"

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# Qué puede anotar en su semana y el ícono con que se ve en la barra lateral.
ACTIVIDADES = {
    "Publicar": "📣",
    "Preparar contenido": "✍️",
    "Terapias": "💆",
    "Fabricar productos": "🧵",
    "Comprar insumos": "🛒",
    "Responder mensajes": "💬",
    "Difusión": "🤝",
    "Descanso": "🌿",
}

# Propuesta inicial: 3 días de publicar (martes y jueves en la noche, sábado en la mañana, cuando más
# se conecta su público de mujeres de 30 a 55 años) y el resto repartido entre su trabajo. Es una
# estimación: Bárbara la ajusta a su realidad y después según sus estadísticas de Instagram.
PROPUESTA = [
    {"dia": "Lunes", "hora": "10:00", "actividad": "Preparar contenido", "detalle": "Planificar los posts de la semana con Bárbara.IA"},
    {"dia": "Lunes", "hora": "16:00", "actividad": "Comprar insumos", "detalle": "Telas, semillas, hierbas y esencias"},
    {"dia": "Martes", "hora": "10:00", "actividad": "Fabricar productos", "detalle": "Guateros y sales de baño"},
    {"dia": "Martes", "hora": "15:00", "actividad": "Terapias", "detalle": ""},
    {"dia": "Martes", "hora": "19:30", "actividad": "Publicar", "detalle": "Primer post de la semana"},
    {"dia": "Miércoles", "hora": "10:00", "actividad": "Terapias", "detalle": ""},
    {"dia": "Miércoles", "hora": "16:00", "actividad": "Preparar contenido", "detalle": "Grabar o fotografiar para los próximos posts"},
    {"dia": "Jueves", "hora": "10:00", "actividad": "Fabricar productos", "detalle": ""},
    {"dia": "Jueves", "hora": "15:00", "actividad": "Terapias", "detalle": ""},
    {"dia": "Jueves", "hora": "20:00", "actividad": "Publicar", "detalle": "Segundo post de la semana"},
    {"dia": "Viernes", "hora": "10:00", "actividad": "Terapias", "detalle": ""},
    {"dia": "Viernes", "hora": "16:00", "actividad": "Difusión", "detalle": "Contactar una junta de vecinos, feria u organización"},
    {"dia": "Sábado", "hora": "10:30", "actividad": "Publicar", "detalle": "Tercer post de la semana"},
    {"dia": "Sábado", "hora": "11:30", "actividad": "Terapias", "detalle": "O feria, si hay una"},
    {"dia": "Domingo", "hora": "", "actividad": "Descanso", "detalle": "Tu autocuidado también cuenta"},
]


def cargar() -> list[dict]:
    try:
        return json.loads(ARCHIVO.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return [dict(fila) for fila in PROPUESTA]


def guardar(filas) -> None:
    """Guarda la semana. Descarta las filas sin día o sin actividad y ordena por día y hora."""
    if hasattr(filas, "to_dict"):  # st.data_editor puede devolver una tabla de pandas
        filas = filas.to_dict("records")
    limpias = []
    for fila in filas:
        texto = {campo: fila.get(campo) if isinstance(fila.get(campo), str) else "" for campo in ("dia", "hora", "actividad", "detalle")}
        texto = {campo: valor.strip() for campo, valor in texto.items()}
        if texto["dia"] in DIAS and texto["actividad"] in ACTIVIDADES:
            limpias.append(texto)
    limpias.sort(key=lambda f: (DIAS.index(f["dia"]), f["hora"] or "99"))
    ARCHIVO.parent.mkdir(exist_ok=True)
    ARCHIVO.write_text(json.dumps(limpias, ensure_ascii=False, indent=2), encoding="utf-8")


def del_dia(filas: list[dict], dia: str) -> list[dict]:
    return sorted((f for f in filas if f["dia"] == dia), key=lambda f: f["hora"] or "99")


def _corta(fila: dict) -> str:
    """Ej.: "💆 15:00 Terapias"."""
    return " ".join(parte for parte in (ACTIVIDADES.get(fila["actividad"], "•"), fila["hora"], fila["actividad"]) if parte)


def resumen_hoy(filas: list[dict], dia_semana: int) -> str:
    """Una línea con lo de hoy, para verla arriba del chat (en el celular la barra lateral se esconde)."""
    hoy = del_dia(filas, DIAS[dia_semana])
    return " · ".join(_corta(f) for f in hoy) or "nada anotado"


def como_texto(filas: list[dict]) -> str:
    """La semana en texto, para que la IA la tenga en cuenta."""
    lineas = []
    for dia in DIAS:
        del_d = del_dia(filas, dia)
        if del_d:
            lineas.append(f"- {dia}: " + ", ".join(f"{f['actividad'].lower()}" + (f" a las {f['hora']}" if f["hora"] else "") for f in del_d))
    if not lineas:
        return ""
    return ("## Su semana (la organiza ella misma)\n"
            "Si sugieres cuándo publicar, usa uno de sus días de publicar.\n" + "\n".join(lineas))


@st.dialog("Editar mi semana", width="large")
def _editar() -> None:
    st.caption("Cambia lo que no te acomode. Para agregar, usa la fila vacía del final. "
               "Para borrar, marca la fila a la izquierda y toca el basurero 🗑️.")
    tabla = st.data_editor(
        cargar(),
        num_rows="dynamic",
        hide_index=True,
        column_order=["dia", "hora", "actividad", "detalle"],
        column_config={
            "dia": st.column_config.SelectboxColumn("Día", options=DIAS, required=True),
            "hora": st.column_config.TextColumn("Hora", help="Ej.: 10:00. Puedes dejarla vacía.", max_chars=5),
            "actividad": st.column_config.SelectboxColumn("Qué hago", options=list(ACTIVIDADES), required=True),
            "detalle": st.column_config.TextColumn("Detalle", help="Opcional. Ej.: guateros de lavanda"),
        },
        key="editor_semana",
    )
    col_guardar, col_propuesta = st.columns(2)
    if col_guardar.button("Guardar mi semana", icon=":material/check:", type="primary", width="stretch"):
        guardar(tabla)
        st.rerun()
    if col_propuesta.button("Volver a la propuesta inicial", icon=":material/restart_alt:", width="stretch"):
        guardar(PROPUESTA)
        st.rerun()


def mostrar_en_barra(dia_semana: int) -> None:
    """Hoy con detalle y el resto de la semana en una línea por día, más el botón para editarla."""
    filas = cargar()
    hoy = DIAS[dia_semana]
    st.subheader("🗓️ Mi semana")

    with st.container(border=True):
        st.markdown(f"**Hoy, {hoy.lower()}**")
        de_hoy = del_dia(filas, hoy)
        for fila in de_hoy:
            detalle = f"  \n<small>{escape(fila['detalle'])}</small>" if fila["detalle"] else ""
            st.markdown(_corta(fila) + detalle, unsafe_allow_html=True)
        if not de_hoy:
            st.caption("Nada anotado para hoy.")

    # El resto de la semana a partir de mañana, una línea por día.
    siguientes = DIAS[dia_semana + 1:] + DIAS[:dia_semana]
    lineas = []
    for dia in siguientes:
        iconos = " · ".join(f"{ACTIVIDADES.get(f['actividad'], '•')} {f['hora']}".strip() for f in del_dia(filas, dia))
        lineas.append(f"**{dia[:3]}** {iconos or '—'}")
    st.markdown("  \n".join(lineas))
    st.caption(" · ".join(f"{icono} {nombre.lower()}" for nombre, icono in ACTIVIDADES.items()))

    if st.button("Editar mi semana", icon="✏️", width="stretch"):
        _editar()
