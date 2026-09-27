"""Revisa lo que escribe la IA antes de que Bárbara lo publique o lo envíe.

Responsable: Sofía (aporte a la entrega).
Los prompts le piden a la IA que no prometa curas ni hable de diagnósticos (ver docs/CONTEXTO.md),
pero la IA a veces se equivoca. Este módulo lo comprueba con reglas simples, sin IA y sin internet,
y le dice a Bárbara qué frase cambiar. No reemplaza su lectura: solo le ayuda a no pasar algo por alto.

Para probar las reglas sin abrir la app:  py -m nexus.revision
"""

import re
from dataclasses import dataclass

ROJO = "rojo"          # hay que cambiarlo antes de publicar
AMARILLO = "amarillo"  # revisarlo con atención


@dataclass
class Alerta:
    nivel: str
    frase: str    # lo que encontró en el texto
    consejo: str  # qué hacer


# (nivel, patrón, consejo). El orden no importa: se revisan todas.
REGLAS = [
    (ROJO, r"\bcur(?:ar|ará|an|as|a|o|aci[oó]n|ativ[oa]s?)\b",
     'Suena a promesa de cura. Prueba con "te ayuda a relajarte" o "acompaña tu bienestar".'),
    (ROJO, r"\bsan(?:ar|ará|an|aci[oó]n|adora?)\b",
     'Suena a promesa de sanación. Prueba con "un espacio para tu bienestar".'),
    (ROJO, r"diagn[oó]stic\w*",
     'No uses "diagnóstico". Di "conversación inicial" o "escucha".'),
    (ROJO, r"garantiz\w*|\b100\s?%|resultados? asegurad\w*|te aseguro",
     "Promete resultados. Cada persona vive la sesión distinto: habla de lo que ofreces, no de lo que va a lograr."),
    (ROJO, r"milagr\w*",
     'Evita "milagro" o "milagroso".'),
    (ROJO, r"reemplaz\w*\s+(?:a\s+|al\s+|el\s+|la\s+|tu\s+|tus\s+)?(?:m[eé]dic|medicament|tratamient|psic[oó]log)\w*"
           r"|dej(?:a|ar|es)\s+(?:de\s+tomar\s+)?(?:tu|tus|el|los|la)\s+(?:medicament|tratamient|remedio)\w*",
     "Sugiere dejar la atención médica. Aclara que las terapias son un complemento."),
    (AMARILLO, r"\btratamientos?\b|\btrat(?:a|ar|o|amos)\s+(?:la|el|tu|tus|los|las)\b",
     "Presenta la terapia como tratamiento. Mejor: sesión, acompañamiento, espacio de autocuidado."),
    (AMARILLO, r"\bpacientes?\b|atenci[oó]n cl[ií]nica|psicoterapia|terapia psicol[oó]gica",
     'Suena a atención clínica. Di "clienta" o "persona" y no presentes la sesión como psicología clínica.'),
    (AMARILLO, r"\belimin(?:a|ar|ará|as|an)\b",
     '"Elimina" suena a promesa. Prueba con "ayuda a soltar" o "alivia la tensión".'),
    (AMARILLO, r"alivi\w*\s+(?:el|tu|los|tus)\s+dolor",
     'Habla de "tensión" o "cansancio" en vez de prometer quitar el dolor.'),
    (AMARILLO, r"\b(?:depresi[oó]n|ansiedad|tdah|c[aá]ncer|diabetes|fibromialgia|hipertensi[oó]n|insomnio"
               r"|dolor cr[oó]nico|trastornos?|enfermedad(?:es)?)\b",
     "Menciona una condición de salud. No prometas ningún efecto sobre ella."),
    (AMARILLO, r"\$\s?\d[\d.]*|\b\d+\s?(?:mil|lucas)\b",
     "Tiene un precio. Confirma que sea el tuyo y esté vigente (la IA no conoce tus precios)."),
    (AMARILLO, r"(?:\+?56\s?)?\b9[\s-]?\d{4}[\s-]?\d{4}\b",
     "Tiene un número de teléfono. Verifica que sea el del negocio."),
    (ROJO, r"\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b",
     "Parece un RUT. Nunca publiques datos personales."),
    (AMARILLO, r"\[[^\]\n]{1,80}\]",
     "Hay algo entre corchetes por completar. Llénalo antes de publicar o enviar."),
]

_REGLAS = [(nivel, re.compile(patron, re.IGNORECASE), consejo) for nivel, patron, consejo in REGLAS]


def revisar(texto: str) -> list[Alerta]:
    """Devuelve las alertas del texto, primero las rojas. Lista vacía si no encontró nada."""
    alertas = []
    for nivel, patron, consejo in _REGLAS:
        encontrado = patron.search(texto or "")
        if encontrado:
            alertas.append(Alerta(nivel, encontrado.group(0).strip(), consejo))
    if len(texto or "") > 2200:
        alertas.append(Alerta(ROJO, f"{len(texto)} caracteres", "Instagram acepta hasta 2.200 caracteres: acórtalo."))
    return sorted(alertas, key=lambda a: a.nivel != ROJO)


def hay_rojas(alertas: list[Alerta]) -> bool:
    return any(a.nivel == ROJO for a in alertas)


if __name__ == "__main__":
    # Pruebas rápidas de las reglas: py -m nexus.revision
    from nexus import demo

    casos = {
        "Esta terapia cura la ansiedad, resultados garantizados": 3,
        "Te hago un diagnóstico energético en la primera sesión": 1,
        "El reiki reemplaza tu medicamento para dormir": 1,
        "Sesión de reiki por $15.000, escríbeme": 1,
        "Precio: [a completar por Bárbara]": 1,
        "Un espacio para relajarte y soltar la tensión de la semana 🌿": 0,
        "Se trata de un momento para ti": 0,
    }
    fallas = 0
    for texto, esperadas in casos.items():
        obtenidas = len(revisar(texto))
        if obtenidas != esperadas:
            fallas += 1
            print(f"FALLA ({obtenidas} alertas, se esperaban {esperadas}): {texto}")
    for modo, respuesta in demo.RESPUESTAS.items():
        if hay_rojas(revisar(respuesta)):
            fallas += 1
            print(f"FALLA: la respuesta demo de '{modo}' tiene alertas rojas")
    print("Todo bien ✔" if not fallas else f"{fallas} prueba(s) fallaron")
