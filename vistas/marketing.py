"""Centro de marketing: el plan de Instagram de la semana, de las fotos sin editar a la publicación lista.

Responsable: Sofía.
Bárbara solo saca y sube las fotos o videos que le pide Bárbara.IA; la app las edita y escribe la
descripción. Ella revisa, aprueba y programa. La lógica está en nexus/marketing.py.
"""

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import streamlit as st

from nexus import marketing, memoria, revision, semana
from nexus.config import config_ia

api_key, base_url, modelo = config_ia()
hoy = datetime.now(ZoneInfo("America/Santiago")).date()
plan = marketing.cargar(hoy)
filas_semana = semana.cargar()


def crear_plan() -> None:
    espacios = marketing.espacios_de_publicar(filas_semana)
    if not espacios:
        st.session_state.aviso_mkt = "Tu semana no tiene días de Publicar. Agrégalos en la sección Calendario, en Editar mi semana."
        return
    piezas = None
    if api_key:
        from nexus.ia import planificar_marketing

        try:
            texto = ", ".join(f"{e['dia']} {e['hora']}".strip() for e in espacios)
            piezas = planificar_marketing(texto, memoria.como_texto(memoria.cargar()), api_key, modelo, base_url)
        except Exception:
            st.session_state.aviso_mkt = "No pude conectarme con la IA, así que te dejé un plan base. Puedes usarlo igual."
    if not piezas:
        piezas = marketing.plan_por_reglas(espacios, hoy.isocalendar().week)
    plan["piezas"] = marketing.completar_piezas(piezas)
    marketing.guardar(plan)


def preparar(pieza: dict, archivos: list) -> None:
    """Edita las fotos, guarda los videos y pide a la IA la descripción."""
    fotos = [a.getvalue() for a in archivos if a.type.startswith("image/")]
    videos = [a for a in archivos if a.type.startswith("video/")]
    resultado = None
    if api_key:
        from nexus.ia import preparar_publicacion

        try:
            miniaturas = [(marketing.miniatura(f), "image/jpeg") for f in fotos]
            resultado = preparar_publicacion(pieza, miniaturas, [v.name for v in videos],
                                             memoria.como_texto(memoria.cargar()), api_key, modelo, base_url)
        except Exception:
            st.session_state.aviso_mkt = "No pude conectarme con la IA: preparé la publicación con un texto base para que lo ajustes."
    resultado = resultado or marketing.descripcion_por_reglas(pieza)

    maximo = 5 if pieza["formato"] == "Carrusel" else 1
    elegidas = (resultado["orden"] or list(range(len(fotos))))[:maximo]
    pieza["originales"] = [marketing.guardar_original(fotos[i], pieza["id"], n) for n, i in enumerate(elegidas)]
    pieza["texto_imagen"] = resultado["texto_imagen"]
    pieza["fotos"] = marketing.rehacer_fotos(pieza)
    pieza["videos"] = [marketing.guardar_video(v.getvalue(), v.name, pieza["id"], n) for n, v in enumerate(videos)]
    pieza["descripcion"] = resultado["descripcion"]
    pieza["consejo"] = resultado["consejo"]
    pieza["estado"] = "revisar"
    marketing.guardar(plan)


def mostrar_revision(texto: str) -> bool:
    """Muestra las alertas del revisor. Devuelve True si hay alertas rojas (entonces no se puede aprobar)."""
    alertas = revision.revisar(texto)
    lineas = "\n".join(f"- **“{a.frase.replace('$', chr(92) + '$')}”**: {a.consejo}" for a in alertas)
    if revision.hay_rojas(alertas):
        st.error(f"Antes de aprobar, cambia esto:\n\n{lineas}", icon="✋")
        return True
    if alertas:
        st.warning(f"Revisa esto antes de aprobar:\n\n{lineas}", icon="👀")
    else:
        st.caption("✅ Revisado: sin promesas de salud ni datos por completar.")
    return False


st.title("📸 Centro de marketing")
st.caption("Tú solo sacas las fotos que te pido. Yo las edito, escribo la descripción y te digo cuándo publicar.")

with st.expander("¿Cómo funciona?", icon="💡"):
    st.markdown(
        "1. **Armo tu plan** con los días de 📣 Publicar de tu semana: qué publicar y qué fotos o videos necesito.\n"
        "2. **Me mandas tus fotos o videos tal cual**, sin editar.\n"
        "3. **Las edito** (tamaño de Instagram, luz y texto) y **escribo la descripción** con tu voz.\n"
        "4. **Tú revisas y apruebas.** Nada se publica sin que tú lo veas.\n"
        "5. **La programas** en Meta Business Suite o en Instagram para el día y la hora del plan, y sale sola."
    )

if aviso := st.session_state.pop("aviso_mkt", None):
    st.warning(aviso)
if not api_key:
    st.info("Modo demo: sin API key, el plan y las descripciones son de ejemplo. La edición de fotos funciona igual.")

if not plan["piezas"]:
    st.write("Aún no tienes plan para esta semana.")
    if st.button("Armar mi plan de la semana", icon="✨", type="primary"):
        with st.spinner("Pensando tu semana en Instagram..."):
            crear_plan()
        st.rerun()
    st.stop()

# --- Resumen de la semana ---
cuenta = {estado: sum(p["estado"] == estado for p in plan["piezas"]) for estado in marketing.ESTADOS}
st.markdown(f"**Semana del {marketing.fecha_de(plan, 'Lunes'):%d-%m}** · " +
            " · ".join(f"{texto}: {cuenta[estado]}" for estado, texto in marketing.ESTADOS.items() if cuenta[estado]))
listas = cuenta["aprobada"] + cuenta["programada"]
st.progress(listas / len(plan["piezas"]), text=f"{listas} de {len(plan['piezas'])} publicaciones listas")

# --- Una tarjeta por publicación ---
for pieza in plan["piezas"]:
    fecha = marketing.fecha_de(plan, pieza["dia"])
    icono = "⭕" if pieza["tipo"] == "historia" else "📸"
    with st.container(border=True):
        st.markdown(f"#### {icono} {pieza['dia']} {fecha:%d-%m} · {pieza['hora']}\n**{pieza['tema']}**")
        st.caption(f"{pieza['formato']} · {pieza['objetivo']} · {marketing.ESTADOS[pieza['estado']]}")

        if pieza["estado"] == "fotos":
            st.markdown("**Lo que necesito que me mandes:**\n" + "\n".join(f"- {t}" for t in pieza["tomas"]))
            archivos = st.file_uploader(
                "Sube tus fotos o videos tal cual, sin editar",
                type=["jpg", "jpeg", "png", "webp", "mp4", "mov"],
                accept_multiple_files=True,
                key=f"subir-{pieza['id']}",
            )
            if st.button("Preparar mi publicación", key=f"preparar-{pieza['id']}", icon="🪄", type="primary", disabled=not archivos):
                with st.spinner("Editando tus fotos y escribiendo la descripción..."):
                    preparar(pieza, archivos)
                st.rerun()
            continue

        # Ya tiene fotos: revisar, ajustar, aprobar y programar.
        if pieza["fotos"]:
            st.image(pieza["fotos"], width=220 if len(pieza["fotos"]) > 1 else 320)
        for video in pieza["videos"]:
            st.video(video)
        if pieza["videos"]:
            st.caption("🎬 El video va tal cual: recórtalo a 15 a 30 segundos en el editor de Instagram al publicarlo.")
        if pieza["consejo"]:
            st.info(pieza["consejo"], icon="💡")

        editable = pieza["estado"] == "revisar"
        if pieza["fotos"] and editable:
            nuevo_texto = st.text_input("Texto sobre la imagen (déjalo vacío para no poner texto)", pieza["texto_imagen"], key=f"texto-{pieza['id']}")
            if nuevo_texto != pieza["texto_imagen"] and st.button("Aplicar texto", key=f"aplicar-{pieza['id']}", icon="🔤"):
                pieza["texto_imagen"] = nuevo_texto
                pieza["fotos"] = marketing.rehacer_fotos(pieza)
                marketing.guardar(plan)
                st.rerun()

        descripcion = st.text_area("Descripción", pieza["descripcion"], height=220, key=f"desc-{pieza['id']}", disabled=not editable)
        if descripcion != pieza["descripcion"]:
            pieza["descripcion"] = descripcion
            marketing.guardar(plan)
        tiene_rojas = mostrar_revision(descripcion)

        if pieza["estado"] == "revisar":
            col_aprobar, col_cambiar = st.columns(2)
            if col_aprobar.button("Aprobar", key=f"aprobar-{pieza['id']}", icon="✅", type="primary", width="stretch", disabled=tiene_rojas):
                pieza["estado"] = "aprobada"
                marketing.guardar(plan)
                st.rerun()
            if col_cambiar.button("Cambiar las fotos", key=f"cambiar-{pieza['id']}", icon="🔄", width="stretch"):
                pieza.update(estado="fotos", fotos=[], videos=[], originales=[], descripcion="", consejo="")
                marketing.guardar(plan)
                st.rerun()
            continue

        # Aprobada o programada: descargar y programar.
        st.download_button("Descargar paquete (fotos + descripción)", marketing.zip_paquete(pieza, fecha),
                           f"{pieza['dia'].lower()}_{pieza['id']}.zip", "application/zip", key=f"zip-{pieza['id']}", icon="📦")
        for numero, ruta in enumerate(pieza["fotos"], start=1):
            nombre = f"{pieza['dia'].lower()}_{pieza['tipo']}_{numero}.jpg"
            st.download_button(f"Descargar foto {numero}", Path(ruta).read_bytes(), nombre, "image/jpeg",
                               key=f"foto-{pieza['id']}-{numero}", icon="🖼️")
        with st.expander("Cómo programarla para que salga sola", icon="📅"):
            st.markdown(
                f"**En Meta Business Suite** (app gratis de Meta):\n"
                f"1. Descarga las fotos a tu celular con los botones de arriba.\n"
                f"2. Abre Meta Business Suite → **Crear** → **{'Historia' if pieza['tipo'] == 'historia' else 'Publicación'}**.\n"
                f"3. Elige tu cuenta de Instagram, sube las fotos y pega la descripción (usa el ícono de copiar de abajo).\n"
                f"4. Toca **Programar** y elige **{pieza['dia'].lower()} {fecha:%d-%m} a las {pieza['hora']}**.\n\n"
                "**O en Instagram:** al crear el post, en *Configuración avanzada* activa **Programar esta publicación**."
            )
            st.code(pieza["descripcion"], language=None, wrap_lines=True)
        if pieza["estado"] == "aprobada":
            if st.button("Ya la programé", key=f"programada-{pieza['id']}", icon="📅"):
                pieza["estado"] = "programada"
                marketing.guardar(plan)
                st.rerun()

st.divider()
with st.expander("Rehacer el plan de la semana"):
    st.caption("Se borran las publicaciones de esta semana, también las aprobadas.")
    if st.button("Sí, armar un plan nuevo", icon="✨"):
        with st.spinner("Pensando tu semana en Instagram..."):
            crear_plan()
        st.rerun()
