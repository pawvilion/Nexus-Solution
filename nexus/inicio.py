"""Inicio proactivo: "Tu día con Nexus".

Responsable: Persona 1 (Interfaz).
Al abrir la app, Nexus saluda a Bárbara con lo que sabe de ella y le propone 3 acciones para hoy.
Con API key lo escribe la IA (nexus/ia.py); sin ella, se usan las reglas de este archivo.
"""

from datetime import datetime

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def saludo_hora(ahora: datetime) -> str:
    if 5 <= ahora.hour < 12:
        return "Buenos días"
    return "Buenas tardes" if 12 <= ahora.hour < 20 else "Buenas noches"


def contexto(recuerdos: list[dict], dias_sin_publicar: int | None, ahora: datetime) -> str:
    """Resumen de la situación de Bárbara para que la IA arme el inicio."""
    if dias_sin_publicar is None:
        publicacion = "Todavía no ha registrado ninguna publicación en Nexus."
    elif dias_sin_publicar == 0:
        publicacion = "Publicó hoy."
    else:
        publicacion = f"Su última publicación registrada fue hace {dias_sin_publicar} días."
    ultimos = [r["texto"] for r in recuerdos[-3:]]
    return (
        f"Hoy es {DIAS[ahora.weekday()]}, son las {ahora:%H:%M}.\n"
        f"{publicacion}\n"
        f"Lo último que te contó: {'; '.join(ultimos) if ultimos else 'nada todavía, es su primera vez.'}"
    )


def por_reglas(recuerdos: list[dict], dias_sin_publicar: int | None, ahora: datetime) -> dict:
    """Inicio sin IA: saludo y 3 acciones elegidas con reglas simples."""
    esencia = [r["texto"] for r in recuerdos if r["tipo"] == "esencia"]
    redes = [r for r in recuerdos if r["tipo"] == "redes"]

    lineas = [f"{saludo_hora(ahora)}, Bárbara 🌿"]
    if esencia:
        lineas.append(f"Tengo presente algo que me contaste: *\"{esencia[-1]}\"*.")
    if dias_sin_publicar is None or dias_sin_publicar >= 4:
        lineas.append("Hace un tiempo que no publicas. Hoy puede ser un buen día para mostrarte.")
    else:
        lineas.append("Vas muy bien con tus publicaciones, sigamos con ese ritmo.")

    acciones = []
    if dias_sin_publicar is None or dias_sin_publicar >= 2:
        tema = f"sobre esto que te conté: {esencia[-1]}" if esencia else "que muestre cómo trabajo con cariño"
        acciones.append({
            "titulo": "Preparar tu próximo post",
            "modo": "guion",
            "mensaje": f"Quiero hacer un post {tema}",
        })
    if len(esencia) < 3:
        acciones.append({
            "titulo": "Contarme un poco más de ti",
            "modo": "conversemos",
            "mensaje": "Quiero contarte por qué empecé con las terapias",
        })
    if not redes:
        acciones.append({
            "titulo": "Revisar qué te está funcionando en Instagram",
            "modo": "estadisticas",
            "mensaje": None,  # necesita que ella suba capturas, así que solo abre el módulo
        })
    acciones.append({
        "titulo": "Dar un paso hacia tu sueño de crear guateros junto a tus clientas",
        "modo": "experiencia",
        "mensaje": "Quiero que la gente cree su propio guatero conmigo",
    })
    acciones.append({
        "titulo": "Invitar a una junta de vecinos a una tarde de bienestar",
        "modo": "difusion",
        "mensaje": "Quiero repetir la feria de mi villa en otra villa de Puente Alto",
    })
    return {"saludo": " ".join(lineas), "acciones": acciones[:3]}
