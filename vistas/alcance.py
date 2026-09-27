"""Tu alcance en números: cómo les va a las publicaciones de Bárbara y de dónde la encuentran.

Responsable: Persona 3.
Los números salen de las capturas que sube en "📊 Mis estadísticas" (o los escribe a mano en la tabla).
"""

import altair as alt
import pandas as pd
import streamlit as st

from nexus import actividad, estadisticas

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
    base = alt.Chart(datos).encode(
        y=alt.Y("etiqueta:N", sort="-x", title=None,
                axis=alt.Axis(labelColor=TINTA, labelLimit=280, labelOverlap=False, labelFontSize=12, ticks=False, domain=False)),
        x=alt.X("alcance:Q", title="Cuentas alcanzadas",
                axis=alt.Axis(labelColor=TINTA_SUAVE, titleColor=TINTA_SUAVE, gridColor=GRILLA, domain=False, ticks=False,
                              labelExpr="replace(format(datum.value, ',.0f'), ',', '.')")),
        tooltip=[alt.Tooltip("publicacion:N", title="Publicación"), alt.Tooltip("fecha:N", title="Fecha"),
                 alt.Tooltip("formato:N", title="Formato")]
                + [alt.Tooltip(f"{clave}_txt:N", title=nombre) for clave, nombre in estadisticas.METRICAS.items()],
    )
    barras = base.mark_bar(color=BARRA, cornerRadiusEnd=4, size=20)
    etiquetas = base.mark_text(align="left", dx=6, color=TINTA, fontSize=12).encode(text="alcance_txt:N")
    grafico = (barras + etiquetas).properties(height=max(52 * len(datos), 120)).configure_view(strokeWidth=0)
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
