"""Kit de difusión: tarjeta digital, links de WhatsApp con origen y afiches con QR.

Responsable: Persona 3.
La idea es que la difusión salga del chat y circule en el mundo real (ferias, juntas de vecinos,
bio de Instagram) y que cada contacto diga de dónde llegó.
"""

import io
import textwrap
from pathlib import Path
from urllib.parse import quote, urlencode

import qrcode
from PIL import Image, ImageDraw, ImageFont

# Contenido de la tarjeta digital. Bárbara debe revisarlo: es lo que verán sus futuras clientas.
# Sin precios ni promesas de salud (ver docs/CONTEXTO.md).
TARJETA = {
    "nombre": "Terapias Dalmeet",
    "lema": "Terapias holísticas y productos hechos a mano, con cariño",
    "zona": "Puente Alto, Santiago · En mi espacio o a domicilio",
    "sobre_mi": (
        "Soy Bárbara, terapeuta holística transpersonal, con formación en psicología y 15 años de "
        "experiencia en Brasil. Creo que el bienestar no termina en la sesión: es algo del día a día. "
        "Por eso cada terapia es personalizada y cada producto lo hago a mano, a tu medida."
    ),
    "terapias": ["Masajes", "Reiki", "Reflexología", "Aromaterapia", "Flores de Bach"],
    "productos": [
        "Guateros terapéuticos de semillas, para frío o calor, para ti o para regalar",
        "Sales de baño para tu momento de autocuidado",
    ],
    "cierre": "Escríbeme y conversamos qué es lo que más te acomoda.",
}

# Afiche: tamaño vertical de Instagram (1080 x 1350), que también se imprime bien.
ANCHO, ALTO = 1080, 1350
CREMA, SALVIA, TINTA, TINTA_SUAVE, BLANCO = "#FBF7F1", "#5A7F60", "#3F3A34", "#6B645C", "#FFFFFF"
FUENTES = Path(__file__).parent / "fuentes"


def link_whatsapp(numero: str, origen: str | None) -> str:
    """Link que abre WhatsApp con un mensaje ya escrito que dice de dónde llegó la persona."""
    if origen:
        mensaje = f"Hola Bárbara, te encontré por {origen} y me gustaría saber más de tus terapias 🌿"
    else:
        mensaje = "Hola Bárbara, vi tu tarjeta y me gustaría saber más de tus terapias 🌿"
    return f"https://wa.me/{numero}?text={quote(mensaje)}"


def link_tarjeta(url_app: str, origen: str | None) -> str:
    parametros = {"p": "tarjeta"} | ({"origen": origen} if origen else {})
    return f"{url_app}/?{urlencode(parametros)}"


def _fuente(nombre: str, tamano: int, peso: str = "Regular") -> ImageFont.FreeTypeFont:
    fuente = ImageFont.truetype(str(FUENTES / f"{nombre}.ttf"), tamano)
    fuente.set_variation_by_name(peso)
    return fuente


def _lineas(texto: str, fuente: ImageFont.FreeTypeFont, ancho_max: int) -> list[str]:
    """Parte el texto en líneas que caben en ancho_max píxeles."""
    lineas = []
    for parrafo in texto.split("\n"):
        palabras, actual = parrafo.split(), ""
        for palabra in palabras:
            prueba = f"{actual} {palabra}".strip()
            if fuente.getlength(prueba) <= ancho_max:
                actual = prueba
            else:
                lineas.append(actual)
                actual = palabra
        lineas.append(actual)
    return lineas


def _sin_emojis(texto: str) -> str:
    """Las fuentes del afiche no tienen emojis: se quitan para que no salgan cuadrados vacíos."""
    return "".join(c for c in texto if ord(c) < 0x2600 or 0x2E80 <= ord(c) < 0x1F000).strip()


def crear_afiche(titulo: str, subtitulo: str, detalle: str, destino_qr: str, texto_qr: str) -> Image.Image:
    """Afiche con los colores de Terapias Dalmeet y un QR hacia destino_qr."""
    img = Image.new("RGB", (ANCHO, ALTO), CREMA)
    d = ImageDraw.Draw(img)
    margen = 90

    # Franja superior con el nombre.
    d.rectangle([0, 0, ANCHO, 170], fill=SALVIA)
    d.text((ANCHO / 2, 70), TARJETA["nombre"], font=_fuente("Lora", 64, "Bold"), fill=BLANCO, anchor="mm")
    d.text((ANCHO / 2, 128), "Terapias holísticas · Puente Alto", font=_fuente("Nunito", 32, "SemiBold"), fill=BLANCO, anchor="mm")

    # Primero se mide el texto, para dejarle espacio al QR sin que se monten.
    f_titulo, f_sub, f_det = _fuente("Lora", 76, "Bold"), _fuente("Nunito", 40, "SemiBold"), _fuente("Nunito", 34)
    lineas_titulo = _lineas(_sin_emojis(titulo), f_titulo, ANCHO - 2 * margen)[:2]
    lineas_sub = _lineas(_sin_emojis(subtitulo), f_sub, ANCHO - 2 * margen)[:2]
    items = [_lineas(l.strip(), f_det, ANCHO - 2 * margen - 40)[:2] for l in _sin_emojis(detalle).split("\n") if l.strip()][:4]

    inicio_detalle = 240 + 92 * len(lineas_titulo) + 14 + 54 * len(lineas_sub) + 26
    espacio_qr = lambda items: ALTO - 150 - 50 - (inicio_detalle + sum(46 * len(i) + 8 for i in items))
    while len(items) > 1 and espacio_qr(items) < 280:  # si no cabe, se quitan ideas del detalle desde el final
        items.pop()
    lado = max(220, min(390, espacio_qr(items)))

    # Título, subtítulo y detalle.
    y = 240
    for linea in lineas_titulo:
        d.text((ANCHO / 2, y), linea, font=f_titulo, fill=TINTA, anchor="mt")
        y += 92
    y += 14
    for linea in lineas_sub:
        d.text((ANCHO / 2, y), linea, font=f_sub, fill=SALVIA, anchor="mt")
        y += 54
    y += 26
    for item in items:
        for i, linea in enumerate(item):
            d.text((margen + 40, y), linea, font=f_det, fill=TINTA)
            if i == 0:
                d.ellipse([margen + 8, y + 16, margen + 22, y + 30], fill=SALVIA)
            y += 46
        y += 8

    # QR sobre una tarjeta blanca, abajo al centro (negro sobre blanco para que se lea bien).
    qr = qrcode.QRCode(border=2, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(destino_qr)
    imagen_qr = qr.make_image(fill_color=TINTA, back_color=BLANCO).convert("RGB").resize((lado, lado), Image.NEAREST)
    x_qr, y_qr = (ANCHO - lado) // 2, ALTO - lado - 150
    d.rounded_rectangle([x_qr - 20, y_qr - 20, x_qr + lado + 20, y_qr + lado + 20], radius=24, fill=BLANCO)
    img.paste(imagen_qr, (x_qr, y_qr))
    d.text((ANCHO / 2, ALTO - 95), _sin_emojis(texto_qr), font=_fuente("Nunito", 34, "Bold"), fill=TINTA, anchor="mm")
    d.text((ANCHO / 2, ALTO - 50), "Bárbara · Terapeuta holística transpersonal", font=_fuente("Nunito", 28), fill=TINTA_SUAVE, anchor="mm")
    return img


def como_png(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


def como_pdf(img: Image.Image) -> bytes:
    """PDF para imprimir: a 150 ppp el afiche queda de unos 18 x 23 cm."""
    buf = io.BytesIO()
    img.save(buf, "PDF", resolution=150)
    return buf.getvalue()
