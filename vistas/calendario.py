"""Calendario: la semana de Bárbara ordenada por día, y la tabla para editarla.

Responsable: Sofía.
Los datos y la propuesta inicial están en nexus/semana.py. El Centro de marketing usa los días
marcados como "Publicar" para armar su plan.
"""

from datetime import datetime, timedelta
from html import escape
from zoneinfo import ZoneInfo

import streamlit as st

from nexus import semana

st.set_page_config(page_title="Calendario · Bárbara.IA", layout="wide")  # los 7 días necesitan todo el ancho

hoy = datetime.now(ZoneInfo("America/Santiago")).date()
lunes = hoy - timedelta(days=hoy.weekday())
filas = semana.cargar()

if aviso := st.session_state.pop("aviso_calendario", None):
    st.toast(aviso)

st.title("Calendario")
st.caption("Tu semana de trabajo: cuándo publicar, preparar contenido, atender, fabricar y comprar insumos. "
           "Si algo no te acomoda, cámbialo en la tabla de abajo.")

# Resumen de la semana y leyenda de colores.
conteo = {nombre: sum(f["actividad"] == nombre for f in filas) for nombre in semana.ACTIVIDADES}
st.markdown("  ".join(f":{color}-badge[{nombre}: {conteo[nombre]}]" for nombre, color in semana.ACTIVIDADES.items() if conteo[nombre]))

# --- La semana: un día por columna (en el celular quedan uno debajo del otro) ---
for columna, (i, dia) in zip(st.columns(7, gap="small", border=True), enumerate(semana.DIAS)):
    fecha = lunes + timedelta(days=i)
    with columna:
        st.markdown(f"**{dia}**  \n{fecha:%d-%m}" + ("  \n:primary-badge[Hoy]" if fecha == hoy else ""))
        del_dia = semana.del_dia(filas, dia)
        if not del_dia:
            st.caption("Libre")
        for fila in del_dia:
            color = semana.ACTIVIDADES.get(fila["actividad"], "gray")
            detalle = f"  \n<small>{escape(fila['detalle'])}</small>" if fila["detalle"] else ""
            # Texto en color y no etiqueta: así los nombres largos saltan de línea en vez de cortarse.
            st.markdown(f"**{fila['hora'] or 'Todo el día'}**  \n:{color}[**{fila['actividad']}**]{detalle}", unsafe_allow_html=True)

# --- Editar ---
st.subheader("Editar mi semana")
st.caption("Cambia el día, la hora o la actividad. Para agregar, usa la fila vacía del final; "
           "para borrar, marca la fila a la izquierda y toca el basurero.")
tabla = st.data_editor(
    filas,
    num_rows="dynamic",
    hide_index=True,
    width="stretch",
    column_order=["dia", "hora", "actividad", "detalle"],
    column_config={
        "dia": st.column_config.SelectboxColumn("Día", options=semana.DIAS, required=True),
        "hora": st.column_config.TextColumn("Hora", help="Ej.: 10:00. Puedes dejarla vacía.", max_chars=5),
        "actividad": st.column_config.SelectboxColumn("Actividad", options=list(semana.ACTIVIDADES), required=True),
        "detalle": st.column_config.TextColumn("Detalle", help="Opcional. Ej.: guateros de lavanda"),
    },
    key="editor_semana",
)
col_guardar, col_propuesta, _ = st.columns([1, 1, 2])
if col_guardar.button("Guardar cambios", icon=":material/check:", type="primary", width="stretch"):
    semana.guardar(tabla)
    st.session_state.pop("editor_semana", None)  # la tabla vuelve a leer lo guardado
    st.session_state.aviso_calendario = "Listo, guardé tu semana"
    st.rerun()
if col_propuesta.button("Volver a la propuesta inicial", icon=":material/restart_alt:", width="stretch"):
    semana.guardar(semana.PROPUESTA)
    st.session_state.pop("editor_semana", None)
    st.session_state.aviso_calendario = "Volví a la propuesta inicial"
    st.rerun()
