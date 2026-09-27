"""Marketing Executor: el ciclo de marketing de Terapias Dalmeet.

Idea, diseño y lógica: Benjamín (paquete dalmeet_executor). Aquí se integra dentro de Bárbara.IA:
Bárbara.IA analiza y crea el plan → el Executor lo valida y organiza → Bárbara aprueba, modifica o
rechaza → se ejecuta → se guardan resultados → el reporte vuelve a Bárbara.IA → nuevo plan ajustado.
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

from dalmeet_executor.brain_adapter import NEXUS_OUTPUT_INSTRUCTIONS, example_plan
from dalmeet_executor.db import (
    add_action, add_lead_event, add_metric, create_campaign, get_active_campaign, init_db, lead_total,
    list_actions, list_campaigns, list_lead_events, set_action_status, set_active_campaign, update_action,
)
from dalmeet_executor.executor import approve_action, execute_action, reject_action
from dalmeet_executor.import_plan import save_nexus_plan
from dalmeet_executor.reporting import build_campaign_summary, build_nexus_json, build_nexus_report
from dalmeet_executor.ui import status_badge
from nexus import memoria, resultados, revision, semana
from nexus.config import config_ia
from nexus.difusion import TARJETA

init_db()
api_key, base_url, modelo = config_ia()
hoy = datetime.now(ZoneInfo("America/Santiago")).date()

# Nombres cercanos para lo que el Executor guarda con claves técnicas.
TIPOS = {"social_post": "Publicación", "story": "Historia", "reel": "Reel", "ad_campaign": "Anuncio pagado",
         "follow_up": "Seguimiento", "analysis": "Análisis", "email": "Correo"}
CANALES = {"instagram": "Instagram", "facebook": "Facebook", "whatsapp": "WhatsApp", "email": "Correo", "internal": "Interno"}
RESULTADOS = {"consulta": "Me escribió", "agendado": "Agendó", "paciente": "Nueva clienta", "no_convirtió": "No siguió"}
ORIGENES = ["Instagram", "WhatsApp", "Facebook / Marketplace", "Recomendación", "Feria o afiche (QR)", "Otro"]


def fecha_bonita(texto: str | None) -> str:
    if not texto:
        return "sin fecha"
    try:
        return datetime.fromisoformat(texto).strftime("%d-%m · %H:%M")
    except ValueError:
        return texto


def crear_plan(con_reporte: bool) -> None:
    """Bárbara.IA analiza la situación y crea el plan; el Executor lo valida y lo guarda como campaña activa."""
    from nexus.ia import IASaturada, normalizar_plan, planificar_campana

    partes = [memoria.como_texto(memoria.cargar()), semana.como_texto(semana.cargar()), resultados.como_texto()]
    activa = get_active_campaign()
    if con_reporte and activa:  # el reporte del ciclo anterior vuelve a Bárbara.IA
        partes.append("## Reporte del ciclo anterior\n" + build_nexus_report(activa.id))
    try:
        crudo = planificar_campana("\n\n".join(p for p in partes if p), hoy.isoformat(), (hoy + timedelta(days=1)).isoformat(),
                                   (hoy + timedelta(days=14)).isoformat(), NEXUS_OUTPUT_INSTRUCTIONS, api_key, modelo, base_url)
        campana_id = save_nexus_plan(normalizar_plan(crudo), make_active=True)  # aquí el Executor valida el formato
        st.session_state.aviso_exe = ("success", f"Listo: creé la campaña #{campana_id}. Revisa sus acciones en ✅ Aprobar.")
    except IASaturada:
        st.session_state.aviso_exe = ("warning", "La IA está con muchas consultas. Espera un minuto y vuelve a intentarlo.")
    except Exception as error:
        st.session_state.aviso_exe = ("error", f"No pude crear un plan válido ({error}). Inténtalo de nuevo.")


def ajustar_con_ia(accion, nota: str) -> None:
    """MODIFICAR: Bárbara.IA reescribe la acción según la nota y la acción vuelve a revisión."""
    from nexus.ia import ajustar_accion

    nuevo = ajustar_accion(accion.action_type, accion.channel, accion.title, accion.content, nota, api_key, modelo, base_url)
    update_action(accion.id, title=nuevo["title"], content=nuevo["content"], reviewer_note=nota, status="propuesta")
    # Los cuadros de texto recuerdan lo que tenían: se borran para que muestren la versión nueva
    # (si no, al aprobar se guardaría encima el texto antiguo).
    for campo in ("t", "c"):
        st.session_state.pop(f"{campo}-{accion.id}", None)


def ejecutar_internas(acciones) -> None:
    """Las acciones internas que no requieren aprobación pasan solas a ejecución cuando llega su fecha."""
    for a in acciones:
        if a.channel == "internal" and not a.requires_approval and a.status == "aprobada" \
                and a.scheduled_for and a.scheduled_for[:10] <= hoy.isoformat():
            execute_action(a.id, dry_run=True)
            set_action_status(a.id, "ejecutada", result="Análisis automático: " + (resultados.como_texto() or "todavía sin resultados registrados."))


# --- Encabezado ---
st.title("⚙️ Marketing Executor")
st.caption("Bárbara.IA piensa el plan · tú lo apruebas · el Executor lo ejecuta y mide · y el ciclo vuelve a empezar.")

if aviso := st.session_state.pop("aviso_exe", None):
    getattr(st, aviso[0])(aviso[1])

campana = get_active_campaign()
acciones = list_actions(campana.id) if campana else []
ejecutar_internas(acciones)
acciones = list_actions(campana.id) if campana else []

with st.expander("¿Cómo funciona el ciclo?", icon="🔁"):
    st.markdown(
        "1. **Bárbara.IA analiza** tu situación (memoria, semana, resultados) y **crea el plan** de la campaña.\n"
        "2. **El Executor lo valida y organiza**, y clasifica cada acción: ¿necesita tu aprobación?\n"
        "3. **Tú revisas** cada acción: **apruebas**, **pides cambios** (vuelve a revisión) o **rechazas**.\n"
        "4. Lo aprobado **se ejecuta**: lo publicas o programas tú (la publicación automática es la fase 2).\n"
        "5. **Anotas resultados**: alcance, consultas y nuevas clientas.\n"
        "6. **El reporte vuelve a Bárbara.IA**, que evalúa qué funcionó y **crea el siguiente plan ajustado**."
    )

tab_resumen, tab_plan, tab_aprobar, tab_agenda, tab_resultados, tab_reporte = st.tabs(
    ["🏠 Resumen", "🧠 Plan", "✅ Aprobar", "📅 Agenda", "📊 Resultados", "🔁 Reporte"]
)

# ---------------- RESUMEN ----------------
with tab_resumen:
    if not campana:
        st.info("Todavía no hay una campaña activa. Crea la primera en **🧠 Plan**.", icon="🧠")
    else:
        st.subheader(campana.name)
        st.write(campana.objective)
        pendientes = [a for a in acciones if a.status in ("propuesta", "cambios_solicitados")]
        listas = [a for a in acciones if a.status == "aprobada"]
        consultas, clientas = lead_total(campana.id, "consulta"), lead_total(campana.id, "paciente")
        with st.container(horizontal=True):
            st.metric("Por aprobar", len(pendientes))
            st.metric("Listas para ejecutar", len(listas))
            st.metric("Ejecutadas", sum(a.status == "ejecutada" for a in acciones))
        with st.container(horizontal=True):
            st.metric("Consultas", f"{consultas} / {campana.target_leads or '—'}")
            st.metric("Nuevas clientas", f"{clientas} / {campana.target_patients or '—'}")
        if campana.target_patients:
            avance = min(clientas / campana.target_patients, 1.0)
            st.progress(avance, text=f"Meta de nuevas clientas: {avance * 100:.0f} %")
        if pendientes:
            st.warning(f"Tienes {len(pendientes)} acción(es) esperando tu aprobación en **✅ Aprobar**.", icon="✋")

# ---------------- PLAN ----------------
with tab_plan:
    st.write("Bárbara.IA analiza tu situación (lo que sabe de ti, tu semana y tus resultados) y arma una campaña de 2 semanas.")
    if api_key:
        if st.button("Crear un plan nuevo con Bárbara.IA", icon="✨", type="primary"):
            with st.spinner("Analizando tu situación y armando la estrategia..."):
                crear_plan(con_reporte=False)
            st.rerun()
    else:
        st.info("Modo demo: sin API key, usa **Cargar ejemplo** más abajo para ver cómo funciona.")

    campanas = list_campaigns()
    if campanas:
        st.subheader("Tus campañas")
        for c in campanas:
            with st.container(border=True):
                activa_txt = " · **ACTIVA**" if campana and c.id == campana.id else ""
                st.markdown(f"**#{c.id} · {c.name}**{activa_txt}")
                st.caption(f"{c.start_date or '—'} → {c.end_date or '—'} · {len(list_actions(c.id))} acciones")
                if not (campana and c.id == campana.id) and st.button("Activar", key=f"activar-{c.id}"):
                    set_active_campaign(c.id)
                    st.rerun()

    with st.expander("Importar un plan en formato JSON", icon="📥"):
        st.caption("Para pegar un plan hecho en otro lado. El Executor lo valida antes de crear cualquier acción.")
        if st.button("Cargar ejemplo"):
            import json
            st.session_state.plan_json = json.dumps(example_plan(), ensure_ascii=False, indent=2)
        texto_json = st.text_area("Plan JSON", key="plan_json", height=220)
        if st.button("Validar e importar", type="primary"):
            try:
                st.success(f"Campaña #{save_nexus_plan(texto_json, make_active=True)} creada.")
                st.rerun()
            except Exception as error:
                st.error(str(error))
        st.caption("Formato que entiende el Executor:")
        st.code(NEXUS_OUTPUT_INSTRUCTIONS, language=None, wrap_lines=True)

    with st.expander("Crear una campaña a mano", icon="✍️"):
        with st.form("campana_manual"):
            nombre = st.text_input("Nombre de la campaña")
            objetivo = st.text_area("Objetivo")
            meta_consultas = st.number_input("Meta de consultas", min_value=0, step=1)
            meta_clientas = st.number_input("Meta de nuevas clientas", min_value=0, step=1)
            if st.form_submit_button("Crear campaña"):
                if nombre.strip() and objetivo.strip():
                    c = create_campaign(nombre.strip(), objetivo.strip(), 0, int(meta_consultas), int(meta_clientas),
                                        hoy.isoformat(), (hoy + timedelta(days=14)).isoformat(), make_active=True)
                    st.success(f"Campaña #{c.id} creada. Agrega acciones en 📅 Agenda.")
                else:
                    st.error("Completa nombre y objetivo.")

# ---------------- APROBAR ----------------
with tab_aprobar:
    if not campana:
        st.info("Primero crea una campaña en **🧠 Plan**.")
    else:
        st.caption("Nada que salga hacia afuera se ejecuta sin tu aprobación. Tú tienes la última palabra.")
        por_revisar = sorted((a for a in acciones if a.status in ("propuesta", "cambios_solicitados")),
                             key=lambda a: a.scheduled_for or "9999")
        if not por_revisar:
            st.success("No tienes acciones pendientes de aprobación.", icon="✅")
        for a in por_revisar:
            with st.container(border=True):
                st.markdown(f"**{a.title}**")
                st.caption(f"{TIPOS.get(a.action_type, a.action_type)} · {CANALES.get(a.channel, a.channel)} · "
                           f"{fecha_bonita(a.scheduled_for)} · prioridad {a.priority}")
                titulo = st.text_input("Título", a.title, key=f"t-{a.id}")
                contenido = st.text_area("Contenido", a.content, height=180, key=f"c-{a.id}")
                alertas = revision.revisar(f"{titulo}\n{contenido}")  # revisor de Sofía: promesas de salud, precios
                if alertas:
                    lista = "\n".join(f"- **“{x.frase}”**: {x.consejo}" for x in alertas)
                    (st.error if revision.hay_rojas(alertas) else st.warning)(f"Revisa esto antes de aprobar:\n\n{lista}")
                nota = st.text_input("¿Qué cambiarías? (para pedir cambios o dejar una nota)", a.reviewer_note or "", key=f"n-{a.id}",
                                     placeholder="Ej.: más corto, menciona que sirve para regalar")
                with st.container(horizontal=True):
                    if st.button("Aprobar", key=f"ok-{a.id}", icon="✅", type="primary", disabled=revision.hay_rojas(alertas)):
                        update_action(a.id, title=titulo.strip(), content=contenido)
                        approve_action(a.id, nota or None)
                        st.rerun()
                    # Siempre activo: Streamlit recibe la nota junto con el clic, así no se pierde el primer clic.
                    if api_key and st.button("Modificar con IA", key=f"mod-{a.id}", icon="✏️"):
                        if not nota.strip():
                            st.warning("Escribe arriba qué cambiarías y vuelve a tocar el botón.")
                        else:
                            with st.spinner("Reescribiendo según tu nota..."):
                                ajustar_con_ia(a, nota.strip())
                            st.rerun()
                    if st.button("Guardar mis cambios", key=f"g-{a.id}", icon="💾"):
                        update_action(a.id, title=titulo.strip(), content=contenido, reviewer_note=nota)
                        st.rerun()
                    if st.button("Rechazar", key=f"no-{a.id}", icon="🚫"):
                        reject_action(a.id, nota or None)
                        st.rerun()

        aprobadas = [a for a in acciones if a.status == "aprobada"]
        if aprobadas:
            st.subheader("Aprobadas: listas para ejecutar")
            for a in sorted(aprobadas, key=lambda a: a.scheduled_for or "9999"):
                with st.container(border=True):
                    st.markdown(f"**{a.title}** · {fecha_bonita(a.scheduled_for)}")
                    st.code(a.content, language=None, wrap_lines=True)
                    if st.button("Ejecutar", key=f"ej-{a.id}", icon="🚀"):
                        st.session_state.aviso_exe = ("success", execute_action(a.id, dry_run=True))
                        st.rerun()

# ---------------- AGENDA ----------------
with tab_agenda:
    if not campana:
        st.info("Primero crea una campaña en **🧠 Plan**.")
    else:
        for a in sorted(acciones, key=lambda a: a.scheduled_for or "9999"):
            st.markdown(f"**{fecha_bonita(a.scheduled_for)}** · {a.title}  \n"
                        f":gray[{TIPOS.get(a.action_type, a.action_type)} · {CANALES.get(a.channel, a.channel)} · "
                        f"{status_badge(a.status)}]")
            if a.execution_result:
                st.caption(a.execution_result)
        with st.expander("Agregar una acción a mano", icon="➕"):
            with st.form("accion_manual", clear_on_submit=True):
                titulo = st.text_input("Título")
                tipo = st.selectbox("Tipo", list(TIPOS), format_func=TIPOS.get)
                canal = st.selectbox("Canal", list(CANALES), format_func=CANALES.get)
                contenido = st.text_area("Contenido o instrucciones")
                dia = st.date_input("Fecha", value=hoy, format="DD-MM-YYYY")
                hora = st.time_input("Hora", value=None)
                if st.form_submit_button("Agregar"):
                    if titulo.strip():
                        cuando = f"{dia.isoformat()}T{(hora.strftime('%H:%M:%S') if hora else '10:00:00')}"
                        # Regla del Executor: todo lo que sale hacia afuera requiere aprobación.
                        add_action(campana.id, tipo, canal, titulo.strip(), contenido, cuando, "media", canal != "internal")
                        st.rerun()
                    else:
                        st.error("Escribe un título.")

# ---------------- RESULTADOS ----------------
with tab_resultados:
    if not campana:
        st.info("Primero crea una campaña en **🧠 Plan**.")
    else:
        r = build_campaign_summary(campana.id)["results"]
        with st.container(horizontal=True):
            st.metric("Alcance", f"{r['reach']:,.0f}".replace(",", "."))
            st.metric("Consultas", r["consultations"])
            st.metric("Nuevas clientas", r["patients"])
            st.metric("Conversión", f"{r['conversion_consultation_to_patient_pct']:.0f} %")

        st.subheader("Anota quién llegó")
        st.caption("Solo cantidades: nunca nombres, teléfonos, RUT ni datos de salud.")
        with st.form("embudo", clear_on_submit=True):
            origen = st.selectbox("¿De dónde llegó?", ORIGENES, accept_new_options=True)
            servicio = st.selectbox("¿Qué le interesó?", TARJETA["terapias"] + ["Guateros y productos", "Otro"])
            resultado = st.radio("¿Qué pasó?", list(RESULTADOS), format_func=RESULTADOS.get, horizontal=True)
            cantidad = st.number_input("Cuántas", min_value=1, value=1, step=1)
            if st.form_submit_button("Anotar", icon=":material/add:", type="primary"):
                add_lead_event(campana.id, origen or "Otro", servicio, resultado, int(cantidad), hoy.isoformat())
                st.rerun()

        st.subheader("Anota cómo le fue a una acción")
        ejecutadas = {f"{a.title} ({fecha_bonita(a.scheduled_for)})": a.id for a in acciones if a.status == "ejecutada"}
        with st.form("metrica", clear_on_submit=True):
            accion = st.selectbox("Acción", ["General / campaña"] + list(ejecutadas))
            metrica = st.selectbox("Métrica", ["alcance", "interacciones", "clics", "impresiones", "gasto"])
            valor = st.number_input("Valor", min_value=0.0, step=1.0)
            if st.form_submit_button("Guardar"):
                add_metric(campana.id, ejecutadas.get(accion), metrica, valor, hoy.isoformat())
                st.rerun()

        eventos = list_lead_events(campana.id)
        if eventos:
            tabla = pd.DataFrame([{"Origen": e.source, "Resultado": RESULTADOS.get(e.outcome, e.outcome), "Cantidad": e.quantity}
                                  for e in eventos])
            st.dataframe(tabla.groupby(["Origen", "Resultado"], as_index=False)["Cantidad"].sum(), hide_index=True, width="stretch")

# ---------------- REPORTE ----------------
with tab_reporte:
    if not campana:
        st.info("Primero crea una campaña en **🧠 Plan**.")
    else:
        st.caption("Cierra el ciclo: este reporte vuelve a Bárbara.IA para que diseñe el siguiente plan.")
        reporte = build_nexus_report(campana.id)
        st.code(reporte, language=None, wrap_lines=True)
        if api_key and st.button("Crear el siguiente plan con estos resultados", icon="🔁", type="primary"):
            with st.spinner("Evaluando qué funcionó y armando el nuevo plan..."):
                crear_plan(con_reporte=True)
            st.rerun()
        with st.container(horizontal=True):
            st.download_button("Reporte (.txt)", reporte, f"reporte_campana_{campana.id}.txt", icon="⬇️")
            st.download_button("Datos (.json)", build_nexus_json(campana.id), f"reporte_campana_{campana.id}.json",
                               "application/json", icon="⬇️")
