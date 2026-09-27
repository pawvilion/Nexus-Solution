"""La semana de Bárbara: qué días publica, prepara contenido, atiende, fabrica y compra insumos.

Responsable: Sofía.
Se ve y se edita en la página Calendario (vistas/calendario.py). La IA también la recibe, para
sugerir publicar en sus días de publicar y armar el plan del Centro de marketing.
Se guarda en data/semana.json, igual que la memoria (fuera de GitHub).
"""

import json
from pathlib import Path

ARCHIVO = Path(__file__).parent.parent / "data" / "semana.json"

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# Qué puede anotar en su semana y el color de su etiqueta en el calendario (colores de st.badge).
ACTIVIDADES = {
    "Publicar": "red",
    "Preparar contenido": "violet",
    "Terapias": "green",
    "Fabricar productos": "orange",
    "Comprar insumos": "blue",
    "Responder mensajes": "blue",
    "Difusión": "primary",
    "Descanso": "gray",
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


def resumen_hoy(filas: list[dict], dia_semana: int) -> str:
    """Lo de hoy en una línea, ej.: "10:00 Fabricar productos, 15:00 Terapias"."""
    hoy = del_dia(filas, DIAS[dia_semana])
    return ", ".join(f"{f['hora']} {f['actividad']}".strip() for f in hoy) or "nada anotado"


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
