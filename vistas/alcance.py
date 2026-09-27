"""Tu alcance en números: cómo les va a las publicaciones de Bárbara, de dónde la encuentran
y cuántas consultas se convierten en clientas.

Responsable: Persona 3. El embudo de clientas viene del Marketing Executor de Benjamín.
Los números de publicaciones salen de las capturas que sube en "📊 Mis estadísticas" (o los escribe a mano).
"""

from datetime import datetime
from zoneinfo import ZoneInfo

import altair as alt
import pandas as pd
import streamlit as st

from nexus import actividad, embudo, estadisticas, resultados

# Colores de la marca con buen contraste sobre el fondo crema (barras 4,2:1; texto 10,5:1).
BARRA, TINTA, TINTA_SUAVE, GRILLA = "#5A7F60", "#3F3A34", "#6B645C", "#E8DFD3"


def miles(numero: float) -> str:
    return f"{numero:,.0f}".replace(",", ".")


st.title("📈 Tu alcance")
st.caption("Cómo les va a tus publicaciones y qué te está trayendo más gente.")

publicaciones = estadisticas.cargar()

if not publicaciones:
    st.info(
        "Todavía no hay números. Sube capturas de las estadísticas de tus publicaciones en "
        "**🌿 Bárbara.IA → 📊 Mis estadísticas** y aparecerán aquí solas. También puedes escribirlas en la tabla de abajo.",
        icon="📊",
    )
else:
    datos = pd.DataFrame(publicaciones)
    promedio_formato = datos.groupby("formato")["alcance"].mean().sort_values(ascending=False)
    mejor = datos.loc[datos["alcance"].idxmax()]

    # --- Números destacados ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Publicaciones registradas", len(datos))
    col2.metric("Alcance promedio", miles(datos["alcance"].mean()), help="Cuentas alcanzadas por publicación, en promedio")
    col3.metric("Tu mejor publicación", miles(mejor["alcance"]), help=f"{mejor['publicacion']} ({mejor['formato']})")
    st.caption(f"🏆 Tu mejor publicación: **{mejor['publicacion']}** ({mejor['formato'].lower()}), con {miles(mejor['alcance'])} cuentas alcanzadas.")

    if len(promedio_formato) >= 2 and promedio_formato.iloc[-1] > 0:
        primero, ultimo = promedio_formato.index[0], promedio_formato.index[-1]
        veces = f"{promedio_formato.iloc[0] / promedio_formato.iloc[-1]:.1f}".replace(".", ",")  # coma decimal chilena
        st.success(
            f"En promedio, tus publicaciones tipo **{primero.lower()}** llegan a {miles(promedio_formato.iloc[0])} cuentas "
            f"y las tipo **{ultimo.lower()}** a {miles(promedio_formato.iloc[-1])}: **{veces} veces más**. "
            "Úsalo para decidir qué formato priorizar.",
            icon="💡",
        )

    # --- Gráfico: alcance de cada publicación (una sola serie, un solo color) ---
    st.subheader("Cuentas alcanzadas por publicación")
    datos["etiqueta"] = datos["publicacion"] + " · " + datos["formato"]
    # Números con punto de miles, como se escriben en Chile (1.240 y no 1,240).
    for clave in estadisticas.METRICAS:
        datos[f"{clave}_txt"] = datos[clave].map(lambda n: "—" if pd.isna(n) else miles(n))
    # El nombre va ENCIMA de cada barra (no a la izquierda): así en el celular la barra usa todo el ancho.
    base = alt.Chart(datos).encode(
        y=alt.Y("etiqueta:N", sort=alt.EncodingSortField("alcance", order="descending"), axis=None),
        tooltip=[alt.Tooltip("publicacion:N", title="Publicación"), alt.Tooltip("fecha:N", title="Fecha"),
                 alt.Tooltip("formato:N", title="Formato")]
                + [alt.Tooltip(f"{clave}_txt:N", title=nombre) for clave, nombre in estadisticas.METRICAS.items()],
    )
    # Espacio a la derecha para que el número de la barra más larga no se corte.
    escala = alt.Scale(domain=[0, datos["alcance"].max() * 1.2])
    eje_x = alt.X("alcance:Q", axis=None, scale=escala)
    datos["cero"] = 0  # los nombres parten en el borde izquierdo
    barras = base.mark_bar(color=BARRA, cornerRadiusEnd=4, size=16, yOffset=9).encode(x=eje_x)
    nombres = base.mark_text(align="left", baseline="bottom", dy=-3, color=TINTA, fontSize=13, limit=330).encode(
        x=alt.X("cero:Q", axis=None, scale=escala), text="etiqueta:N")
    valores = base.mark_text(align="left", dx=6, dy=9, color=TINTA, fontSize=12, fontWeight="bold").encode(
        x=eje_x, text="alcance_txt:N")
    grafico = (barras + nombres + valores).properties(height=max(60 * len(datos), 120)).configure_view(strokeWidth=0)
    st.altair_chart(grafico, width="stretch")

# --- Tabla editable ---
with st.expander("Ver y corregir los números", icon="✏️", expanded=not publicaciones):
    st.caption("Si algún número quedó mal leído, corrígelo aquí. También puedes agregar publicaciones a mano.")
    tabla = pd.DataFrame(publicaciones, columns=list(estadisticas.COLUMNAS))
    editada = st.data_editor(
        tabla,
        num_rows="dynamic",
        hide_index=True,
        width="stretch",
        column_config={
            "publicacion": st.column_config.TextColumn("Publicación", required=True),
            "fecha": st.column_config.TextColumn("Fecha"),
            "formato": st.column_config.SelectboxColumn("Formato", options=estadisticas.FORMATOS, required=True),
        }
        | {clave: st.column_config.NumberColumn(nombre, min_value=0, step=1, format="%d") for clave, nombre in estadisticas.METRICAS.items()},
    )
    if st.button("Guardar cambios", icon=":material/check:", type="primary"):
        filas = editada.astype(object).where(editada.notna(), None).to_dict("records")
        estadisticas.reemplazar(filas)
        st.toast("Listo, guardé tus números", icon="🌿")
        st.rerun()

# --- De dónde te encuentran (visitas a la tarjeta por QR o link) ---
visitas = actividad.cargar().get("visitas", {})
if visitas:
    st.subheader("¿De dónde llegan a tu tarjeta?")
    st.caption("Visitas a tu tarjeta digital según el QR o link que usaron.")
    st.dataframe(
        pd.DataFrame(sorted(visitas.items(), key=lambda x: -x[1]), columns=["Origen", "Visitas"]),
        hide_index=True, width="stretch",
    )

# --- Embudo: de consulta a clienta (solo cantidades, sin datos personales) ---
st.divider()
st.subheader("🧲 De consulta a clienta")
st.caption("Anota cuántas personas te escriben y cuántas agendan o compran, según de dónde llegaron. "
           "Así sabrás qué difusión te trae clientas de verdad. Solo cantidades: nunca nombres ni datos de salud.")

registros = embudo.cargar()
hoy = datetime.now(ZoneInfo("America/Santiago")).date()

with st.form("embudo", clear_on_submit=True, border=True):
    col_origen, col_servicio = st.columns(2)
    # Los lugares de sus afiches con QR también aparecen como opción, y puede escribir uno nuevo.
    opciones = embudo.ORIGENES + sorted(set(visitas) - set(embudo.ORIGENES) - {"Link directo"})
    origen = col_origen.selectbox("¿De dónde llegó?", opciones, accept_new_options=True)
    servicio = col_servicio.selectbox("¿Qué le interesó?", embudo.SERVICIOS)
    col_etapa, col_cantidad, col_fecha = st.columns([2, 1, 1])
    etapa = col_etapa.radio("¿Qué pasó?", list(embudo.ETAPAS), format_func=embudo.ETAPAS.get, horizontal=True)
    cantidad = col_cantidad.number_input("Cuántas", min_value=1, value=1, step=1)
    fecha = col_fecha.date_input("Fecha", value=hoy, format="DD-MM-YYYY")
    if st.form_submit_button("Anotar", icon=":material/add:", type="primary"):
        embudo.agregar(registros, fecha.isoformat(), origen or "Otro", servicio, etapa, cantidad)
        st.toast("Anotado", icon="🌿")
        st.rerun()

if registros:
    conv = embudo.conversion(registros)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Me escribieron", embudo.total(registros, "consulta"))
    col2.metric("Agendaron o compraron", embudo.total(registros, "agendo"))
    col3.metric("Volvieron otra vez", embudo.total(registros, "volvio"))
    col4.metric("Conversión", "—" if conv is None else f"{conv:.0f} %".replace(".", ","),
                help="De cada 100 personas que te escriben, cuántas agendan o compran")

    tabla_origen = pd.DataFrame(embudo.por_origen(registros))
    tabla_origen["conversion"] = tabla_origen["conversion"].map(lambda c: "—" if pd.isna(c) else f"{c:.0f} %")
    st.dataframe(
        tabla_origen.rename(columns={"origen": "Origen", **embudo.ETAPAS, "conversion": "Conversión"}),
        hide_index=True, width="stretch",
    )
    mejor = embudo.por_origen(registros)[0]
    if mejor["agendo"]:
        st.success(f"Lo que más clientas te trae: **{mejor['origen']}**. Vale la pena repetirlo.", icon="💡")

# --- Reporte: resume todo y es lo que la IA usa para el siguiente plan ---
st.divider()
st.subheader("📝 Tu reporte")
st.caption("Bárbara.IA tiene en cuenta estos resultados al armar tu plan de marketing y tu día, "
           "para repetir lo que funciona y cambiar lo que no.")
texto_reporte = resultados.reporte(hoy.strftime("%d-%m-%Y"))
st.code(texto_reporte, language=None, wrap_lines=True)
st.download_button("Descargar reporte", texto_reporte, f"reporte_dalmeet_{hoy.isoformat()}.txt", icon="⬇️")
