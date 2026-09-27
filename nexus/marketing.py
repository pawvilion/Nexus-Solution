"""Centro de marketing: convierte "Mi semana" en publicaciones listas para Instagram.

Responsable: Sofía.
Flujo: Bárbara.IA arma el plan de la semana (qué publicar cada día de "Publicar" y qué fotos o
videos necesita) → Bárbara sube sus fotos sin editar → la app las recorta, ajusta la luz y les pone
texto, y la IA escribe la descripción → Bárbara revisa, aprueba y lo programa en Meta Business Suite.
Nada se publica solo: la publicación automática por la API de Instagram queda como próximo paso.

Se guarda en data/marketing.json y las fotos en data/medios/ (fuera de GitHub).
"""

import io
import json
import zipfile
from datetime import date, timedelta
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageOps

from . import difusion, semana

CARPETA = Path(__file__).parent.parent / "data"
ARCHIVO = CARPETA / "marketing.json"
MEDIOS = CARPETA / "medios"

# Tamaños de Instagram: post vertical 4:5 e historia 9:16.
TAMANOS = {"post": (1080, 1350), "historia": (1080, 1920)}
ESTADOS = {
    "fotos": "📷 Faltan tus fotos",
    "revisar": "👀 Lista para que la revises",
    "aprobada": "✅ Aprobada: prográmala",
    "programada": "📅 Programada",
}

# Plan sin IA (modo demo): ideas que siguen su esencia, para rotar entre los días de publicar.
IDEAS = [
    {"tema": "Así nace un guatero de semillas", "formato": "Reel", "objetivo": "Mostrar tu trabajo artesanal",
     "tomas": ["Video de 10 s de tus manos llenando el guatero con semillas", "Foto de cerca de la tela y las semillas, con luz de ventana",
               "Foto del guatero terminado sobre una manta"]},
    {"tema": "Una pausa de 5 minutos para bajar el estrés", "formato": "Carrusel", "objetivo": "Educar: algo útil que la gente guarde",
     "tomas": ["Foto de tu espacio de terapia ordenado y con luz suave", "Foto de una taza de té o aromas junto a un guatero",
               "Foto tuya respirando tranquila (si te acomoda salir)"]},
    {"tema": "Conoce a Bárbara: 15 años acompañando el bienestar", "formato": "Foto", "objetivo": "Que te conozcan y confíen en ti",
     "tomas": ["Foto tuya en tu espacio de trabajo, mirando a la cámara", "Foto de tus manos preparando aceites o esencias"]},
    {"tema": "Qué pasa en una sesión de reflexología", "formato": "Carrusel", "objetivo": "Quitar el miedo a la primera sesión",
     "tomas": ["Foto de la camilla lista con mantas", "Foto de tus manos (sin la cara de la clienta)", "Foto de los aceites que usas"]},
]
HISTORIAS = [
    {"tema": "Detrás de escena: hoy estoy fabricando", "tomas": ["Video de 5 s de tu mesa de trabajo"]},
    {"tema": "Pregunta: ¿qué te ayuda a desconectarte?", "tomas": ["Foto tranquila de tu espacio o de la naturaleza"]},
]


# --- Guardar y cargar ---

def lunes_de(hoy: date) -> date:
    """Lunes de la semana que se planifica. El domingo ya se planifica la semana que empieza mañana."""
    mañana = hoy + timedelta(days=1)
    return mañana - timedelta(days=mañana.weekday())


def cargar(hoy: date) -> dict:
    """El plan de la semana actual. Si el guardado es de otra semana, parte vacío."""
    try:
        plan = json.loads(ARCHIVO.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        plan = {}
    if plan.get("semana") != lunes_de(hoy).isoformat():
        return {"semana": lunes_de(hoy).isoformat(), "piezas": []}
    return plan


def guardar(plan: dict) -> None:
    CARPETA.mkdir(exist_ok=True)
    ARCHIVO.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")


def espacios_de_publicar(filas_semana: list[dict]) -> list[dict]:
    """Los días y horas marcados como "Publicar" en Mi semana."""
    return [{"dia": f["dia"], "hora": f["hora"]} for f in filas_semana if f["actividad"] == "Publicar"]


def fecha_de(plan: dict, dia: str) -> date:
    return date.fromisoformat(plan["semana"]) + timedelta(days=semana.DIAS.index(dia))


# --- Plan de la semana ---

def plan_por_reglas(espacios: list[dict], numero_semana: int) -> list[dict]:
    """Plan sin IA: una idea por cada día de publicar y dos historias."""
    piezas = []
    for i, espacio in enumerate(espacios):
        idea = IDEAS[(numero_semana + i) % len(IDEAS)]
        piezas.append({"tipo": "post", **espacio, **idea})
    dias_historia = [d for d in semana.DIAS if d not in {e["dia"] for e in espacios}][:2]
    for dia, historia in zip(dias_historia, HISTORIAS):
        piezas.append({"tipo": "historia", "dia": dia, "hora": "12:00", "formato": "Historia", "objetivo": "Estar presente entre posts", **historia})
    return piezas


def completar_piezas(piezas: list[dict]) -> list[dict]:
    """Deja cada pieza con todos sus campos y un identificador, venga de la IA o de las reglas."""
    completas = []
    for i, p in enumerate(piezas):
        if p.get("dia") not in semana.DIAS:
            continue
        tipo = "historia" if p.get("tipo") == "historia" else "post"
        completas.append({
            "id": f"p{i}",
            "tipo": tipo,
            "dia": p["dia"],
            "hora": str(p.get("hora") or ("12:00" if tipo == "historia" else "19:30")),
            "tema": str(p.get("tema", "")).strip() or "Publicación de la semana",
            "formato": str(p.get("formato") or ("Historia" if tipo == "historia" else "Foto")),
            "objetivo": str(p.get("objetivo", "")),
            "tomas": [str(t) for t in p.get("tomas", [])][:4],
            "estado": "fotos",
            "originales": [],  # fotos elegidas, tal como llegaron (para volver a editarlas)
            "fotos": [],       # rutas de las fotos ya editadas
            "videos": [],      # rutas de los videos tal como llegaron
            "texto_imagen": "",
            "descripcion": "",
            "consejo": "",
        })
    return sorted(completas, key=lambda p: (semana.DIAS.index(p["dia"]), p["hora"]))


# --- Edición de fotos ---

def editar_foto(datos: bytes, tipo: str, texto: str = "") -> Image.Image:
    """Endereza, recorta al tamaño de Instagram, mejora la luz y, si hay texto, lo pone abajo."""
    img = ImageOps.exif_transpose(Image.open(io.BytesIO(datos))).convert("RGB")
    ancho, alto = TAMANOS[tipo]
    img = ImageOps.fit(img, (ancho, alto), Image.LANCZOS, centering=(0.5, 0.45))
    # Corrige fotos oscuras o lavadas, pero a medias (mezclado con la original) para que se vea natural.
    img = Image.blend(img, ImageOps.autocontrast(img, cutoff=1, preserve_tone=True), 0.5)
    img = ImageEnhance.Brightness(img).enhance(1.04)
    img = ImageEnhance.Color(img).enhance(1.08)  # colores un poco más cálidos y vivos, sin exagerar
    img = ImageEnhance.Sharpness(img).enhance(1.15)
    if texto.strip():
        img = _poner_texto(img, texto, tipo)
    return img


def _poner_texto(img: Image.Image, texto: str, tipo: str) -> Image.Image:
    """Franja suave abajo con el texto en la letra de Terapias Dalmeet."""
    ancho, alto = img.size
    fuente = difusion._fuente("Lora", 64 if tipo == "historia" else 56, "Bold")
    firma = difusion._fuente("Nunito", 30, "SemiBold")
    lineas = difusion._lineas(difusion._sin_emojis(texto), fuente, ancho - 160)[:3]
    alto_franja = 90 * len(lineas) + 110
    base = alto - (320 if tipo == "historia" else 0)  # en historias se deja espacio para los botones de Instagram

    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.rectangle([0, base - alto_franja, ancho, base], fill=(63, 58, 52, 150))
    y = base - alto_franja + 40
    for linea in lineas:
        d.text((ancho / 2, y), linea, font=fuente, fill="#FFFFFF", anchor="mt")
        y += 90
    d.text((ancho / 2, base - 45), "Terapias Dalmeet", font=firma, fill="#FBF7F1", anchor="mm")
    return Image.alpha_composite(img.convert("RGBA"), capa).convert("RGB")


def guardar_original(datos: bytes, pieza_id: str, numero: int) -> str:
    """Guarda la foto como llegó (achicada a 2000 px), para poder volver a editarla si cambia el texto."""
    MEDIOS.mkdir(parents=True, exist_ok=True)
    img = ImageOps.exif_transpose(Image.open(io.BytesIO(datos))).convert("RGB")
    img.thumbnail((2000, 2000))
    ruta = MEDIOS / f"{pieza_id}_original{numero}.jpg"
    img.save(ruta, "JPEG", quality=92)
    return str(ruta)


def rehacer_fotos(pieza: dict) -> list[str]:
    """Edita las fotos originales de la pieza. El texto va solo en la primera (la portada)."""
    rutas = []
    for numero, original in enumerate(pieza.get("originales", [])):
        texto = pieza["texto_imagen"] if numero == 0 else ""
        img = editar_foto(Path(original).read_bytes(), pieza["tipo"], texto)
        ruta = MEDIOS / f"{pieza['id']}_{numero}.jpg"
        img.save(ruta, "JPEG", quality=90)
        rutas.append(str(ruta))
    return rutas


def guardar_video(datos: bytes, nombre: str, pieza_id: str, numero: int) -> str:
    MEDIOS.mkdir(parents=True, exist_ok=True)
    extension = Path(nombre).suffix.lower() or ".mp4"
    ruta = MEDIOS / f"{pieza_id}_video{numero}{extension}"
    ruta.write_bytes(datos)
    return str(ruta)


def miniatura(datos: bytes, lado: int = 768) -> bytes:
    """Versión liviana para mandarle a la IA (más rápido y gasta menos cupo)."""
    img = ImageOps.exif_transpose(Image.open(io.BytesIO(datos))).convert("RGB")
    img.thumbnail((lado, lado))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=80)
    return buf.getvalue()


# --- Descripción y paquete ---

def descripcion_por_reglas(pieza: dict) -> dict:
    """Texto sin IA (modo demo), con su voz y sin promesas de salud."""
    return {
        "orden": None,
        "texto_imagen": pieza["tema"] if pieza["tipo"] == "historia" else "",
        "descripcion": (
            f"{pieza['tema']} 🌿\n\n"
            "Cada cosa que hago la preparo con calma y con cariño, pensando en ese momento del día en que "
            "necesitas bajar el ritmo y conectar contigo.\n\n"
            "¿Y tú, cómo te regalas una pausa esta semana? Te leo en los comentarios 👇\n\n"
            "#TerapiasHolisticas #PuenteAlto #Autocuidado #HechoAMano #Bienestar"
        ),
        "consejo": "Modo demo: con la IA activa, Bárbara.IA elige tus mejores fotos y escribe un texto a tu medida.",
    }


def zip_paquete(pieza: dict, fecha: date) -> bytes:
    """Fotos editadas, videos y la descripción en un solo archivo, para pasarlo al celular o a Meta Business Suite."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for ruta in pieza["fotos"] + pieza["videos"]:
            if Path(ruta).exists():
                z.write(ruta, Path(ruta).name)
        z.writestr("descripcion.txt", f"{pieza['tema']}\nPublicar: {pieza['dia']} {fecha:%d-%m} a las {pieza['hora']}\n\n{pieza['descripcion']}")
    return buf.getvalue()
