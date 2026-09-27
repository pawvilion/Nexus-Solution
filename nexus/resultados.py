"""Resumen de resultados que vuelve a la IA: así el siguiente plan aprende de lo que funcionó.

Responsable: Persona 3. Idea original: el "Reporte para Nexus" de Benjamín (Marketing Executor),
que aquí se hace solo: la IA lo recibe al armar el plan de marketing y "Tu día con Bárbara.IA".
"""

from collections import defaultdict

from . import actividad, embudo, estadisticas


def _alcance_por_formato(publicaciones: list[dict]) -> dict[str, float]:
    sumas, cuentas = defaultdict(float), defaultdict(int)
    for p in publicaciones:
        sumas[p["formato"]] += p["alcance"]
        cuentas[p["formato"]] += 1
    return dict(sorted(((f, sumas[f] / cuentas[f]) for f in sumas), key=lambda x: -x[1]))


def lineas() -> list[str]:
    """Los hallazgos principales, en frases cortas. Vacío si todavía no hay datos."""
    publicaciones, registros = estadisticas.cargar(), embudo.cargar()
    visitas = actividad.cargar().get("visitas", {})
    salida = []
    if publicaciones:
        mejor = max(publicaciones, key=lambda p: p["alcance"])
        salida.append(f"Mejor publicación: \"{mejor['publicacion']}\" ({mejor['formato']}), {mejor['alcance']} cuentas alcanzadas.")
        formatos = _alcance_por_formato(publicaciones)
        if len(formatos) >= 2:
            salida.append("Alcance promedio por formato: " + ", ".join(f"{f} {v:.0f}" for f, v in formatos.items()) + ".")
    if registros:
        conv = embudo.conversion(registros)
        salida.append(
            f"Embudo: {embudo.total(registros, 'consulta')} consultas, {embudo.total(registros, 'agendo')} agendaron o compraron, "
            f"{embudo.total(registros, 'volvio')} volvieron" + (f" (conversión {conv:.0f} %)." if conv is not None else ".")
        )
        mejor_origen = embudo.por_origen(registros)[0]
        if mejor_origen["agendo"]:
            salida.append(f"Origen que más clientas trae: {mejor_origen['origen']} ({mejor_origen['agendo']} agendaron o compraron).")
    if visitas:
        origen, n = max(visitas.items(), key=lambda x: x[1])
        salida.append(f"Visitas a su tarjeta digital: {sum(visitas.values())}, la mayoría desde {origen} ({n}).")
    return salida


def como_texto() -> str:
    """Para agregar al contexto de la IA."""
    hallazgos = lineas()
    if not hallazgos:
        return ""
    return ("## Sus resultados hasta ahora (úsalos para decidir qué repetir y qué cambiar)\n"
            + "\n".join(f"- {h}" for h in hallazgos))


def reporte(hoy: str) -> str:
    """Reporte en texto para descargar: sirve como evidencia y para compartir con el equipo."""
    hallazgos = lineas() or ["Todavía no hay resultados registrados."]
    return "\n".join([f"REPORTE DE RESULTADOS · Terapias Dalmeet · {hoy}", ""] + [f"- {h}" for h in hallazgos])
