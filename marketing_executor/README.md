\
# Dalmeet Marketing Executor — MVP independiente

Aplicación separada de Nexus.

## Arquitectura

    NEXUS DALMEET
        ↓ propone estrategia/plan JSON
    MARKETING EXECUTOR
        ↓ valida y organiza
    BÁRBARA
        ↓ aprueba / modifica / rechaza
    EJECUTOR
        ↓ ejecuta (por ahora simulación)
    RESULTADOS
        ↓ métricas + embudo anónimo
    REPORTE PARA NEXUS
        ↓
    NEXUS genera el siguiente ciclo

## Lo que incluye este MVP

- Inicio / dashboard de supervisión.
- Importación del plan JSON generado por Nexus.
- Campañas separadas.
- Bandeja de aprobaciones.
- Edición antes de aprobar.
- Solicitud de cambios.
- Rechazo.
- Ejecución simulada.
- Calendario de acciones.
- Registro de métricas.
- Embudo de marketing anónimo.
- Conversión y CAC.
- Reporte de retroalimentación listo para Nexus.
- Descarga en TXT y JSON.
- SQLite para desarrollo.
- PostgreSQL listo para producción mediante `DATABASE_URL`.

## IMPORTANTE: Nexus NO se modifica

Puedes desplegar este proyecto como otra app Streamlit con otro repositorio y otra URL.

Ejemplo conceptual:

    nexus-dalmeet.streamlit.app
    dalmeet-marketing.streamlit.app

No comparten código ni base de datos en esta fase.

---

# INSTALACIÓN LOCAL

## 1. Descomprime la carpeta

Abre una terminal dentro de:

    dalmeet_marketing_executor_mvp/

## 2. Crea un entorno virtual (opcional, recomendado)

Windows:

    py -m venv .venv
    .venv\Scripts\activate

## 3. Instala dependencias

    pip install -r requirements.txt

## 4. Ejecuta

    streamlit run streamlit_app.py

---

# PRIMERA PRUEBA

1. Entra a `Plan actual`.
2. Selecciona `Importar desde Nexus`.
3. Pulsa `Cargar ejemplo`.
4. Pulsa `Validar e importar plan`.
5. Ve a `Aprobaciones`.
6. Revisa una acción.
7. Aprueba.
8. Ejecuta en simulación.
9. Ve a `Resultados`.
10. Registra alcance, gasto y algunas consultas/pacientes.
11. Ve a `Reporte para Nexus`.
12. Copia o descarga el reporte.

Con eso se prueba el ciclo completo sin tocar Nexus ni cuentas reales.

---

# CÓMO HACER QUE NEXUS GENERE PLANES COMPATIBLES

En `Plan actual > Formato para Nexus` está el contrato completo.

También está definido en:

    dalmeet_executor/brain_adapter.py

Variable:

    NEXUS_OUTPUT_INSTRUCTIONS

Pueden copiar ese texto al prompt/instrucciones de Nexus cuando estén listos.

No es necesario conectar técnicamente ambos programas todavía.

---

# DÓNDE SE CONECTA INSTAGRAM / META / WHATSAPP

Archivo:

    dalmeet_executor/executor.py

Hoy:

    execute_action(action_id, dry_run=True)

solo simula.

En la Fase 2 se reemplaza por conectores reales:

    publish_instagram(action)
    publish_facebook(action)
    create_meta_ad(action)
    send_whatsapp(action)

Mantener SIEMPRE la regla:

    acción externa
        → aprobación humana
        → ejecución

No dar acceso ilimitado al modelo para publicar, enviar mensajes o gastar dinero.

---

# BASE DE DATOS

## Desarrollo

Por defecto:

    sqlite:///dalmeet_marketing.db

No debes crear el archivo manualmente.

## Producción

Usa PostgreSQL.

Crea:

    .streamlit/secrets.toml

con:

    DATABASE_URL = "postgresql+psycopg://..."

No subas ese archivo a GitHub.

En Streamlit Community Cloud agrega el mismo secreto desde la configuración de la app.

---

# PRIVACIDAD

Este MVP evita intencionalmente registrar identidad de pacientes.

En `Resultados > Embudo anónimo` solo se guardan:

- fecha;
- origen;
- categoría general del servicio;
- resultado;
- cantidad.

NO guardar en esta app:

- nombre;
- RUT;
- teléfono;
- correo personal;
- diagnóstico;
- notas clínicas;
- motivo de consulta detallado.

Para marketing basta con información agregada y reduce riesgos innecesarios.

---

# ESTRUCTURA

    dalmeet_marketing_executor_mvp/
    ├── streamlit_app.py
    ├── requirements.txt
    ├── README.md
    ├── app_pages/
    │   ├── home.py
    │   ├── plan.py
    │   ├── approvals.py
    │   ├── calendar.py
    │   ├── results.py
    │   └── report.py
    ├── dalmeet_executor/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── db.py
    │   ├── schemas.py
    │   ├── brain_adapter.py
    │   ├── import_plan.py
    │   ├── executor.py
    │   ├── reporting.py
    │   └── ui.py
    └── .streamlit/
        ├── config.toml
        └── secrets.toml.example

---

# ORDEN DE DESARROLLO RECOMENDADO

## MVP actual
Plan → aprobación → simulación → resultados → reporte.

## Fase 2
PostgreSQL + publicación real en Meta/Instagram.

## Fase 3
Importación automática de métricas.

## Fase 4
Conexión API directa Nexus ↔ Executor.

No pasar a Fase 2 hasta que el flujo del MVP sea cómodo para Bárbara.
