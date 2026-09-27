"""Inicio proactivo: "Tu día con Nexus".

Responsable: Persona 1 (Interfaz).
Al abrir la app, Nexus saluda a Bárbara con lo que sabe de ella y le propone 3 acciones para hoy.
Con API key lo escribe la IA (nexus/ia.py); sin ella, se usan las reglas de este archivo.
"""

from datetime import datetime

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

# Cómo diría Bárbara cada tema de su memoria en primera persona, para los mensajes de las acciones.
EN_PRIMERA_PERSONA = {"suenos": "mis sueños", "creencias": "lo que creo", "historia": "mi historia", "trabajo": "mi trabajo"}


def saludo_hora(ahora: datetime) -> str:
    if 5 <= ahora.hour < 12:
        return "Buenos días"
    return "Buenas tardes" if 12 <= ahora.hour < 20 else "Buenas noches"


def _por_fecha(memoria: dict, temas) -> list[str]:
    """Temas ordenados del más recientemente actualizado al más antiguo."""
    return sorted(temas, key=lambda t: memoria[t]["actualizado"], reverse=True)


def contexto(memoria: dict, dias_sin_publicar: int | None, ahora: datetime) -> str:
    """Resumen de la situación de Bárbara para que la IA arme el inicio."""
    if dias_sin_publicar is None:
        publicacion = "Todavía no ha registrado ninguna publicación en Nexus."
    elif dias_sin_publicar == 0:
        publicacion = "Publicó hoy."
    else:
        publicacion = f"Su última publicación registrada fue hace {dias_sin_publicar} días."
    recientes = _por_fecha(memoria, memoria)[:2]
    return (
        f"Hoy es {DIAS[ahora.weekday()]}, son las {ahora:%H:%M}.\n"
        f"{publicacion}\n"
        f"Temas de su memoria que se actualizaron hace poco: {', '.join(recientes) or 'ninguno, es su primera vez.'}"
    )


def por_reglas(memoria: dict, dias_sin_publicar: int | None, ahora: datetime) -> dict:
    """Inicio sin IA: saludo y 3 acciones elegidas con reglas simples."""
    esencia = _por_fecha(memoria, [t for t in memoria if t != "redes"])

    lineas = [f"{saludo_hora(ahora)}, Bárbara 🌿"]
    if esencia:
        primera_frase = memoria[esencia[0]]["texto"].split(". ")[0].rstrip(".")
        lineas.append(f"Tengo presente esto de ti: *\"{primera_frase}\"*.")
    if dias_sin_publicar is None or dias_sin_publicar >= 4:
        lineas.append("Hace un tiempo que no publicas. Hoy puede ser un buen día para mostrarte.")
    else:
        lineas.append("Vas muy bien con tus publicaciones, sigamos con ese ritmo.")

    acciones = []
    if dias_sin_publicar is None or dias_sin_publicar >= 2:
        tema = f"sobre {EN_PRIMERA_PERSONA[esencia[0]]}" if esencia else "que muestre cómo trabajo con cariño"
        acciones.append({"titulo": "Preparar tu próximo post", "modo": "guion", "mensaje": f"Quiero hacer un post {tema}"})
    if len(esencia) < 3:  # todavía sabe poco de ella
        # Sin mensaje: solo abre Conversemos, para que lo que se guarde lo escriba ella.
        acciones.append({"titulo": "Contarme un poco más de ti", "modo": "conversemos", "mensaje": None})
    if "redes" not in memoria:
        # Sin mensaje: necesita que ella suba capturas, así que solo abre el módulo.
        acciones.append({"titulo": "Revisar qué te está funcionando en Instagram", "modo": "estadisticas", "mensaje": None})
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
