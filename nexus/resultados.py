"""Resumen de resultados que vuelve a la IA: así el siguiente plan aprende de lo que funcionó.

Responsable: Persona 3. Junta los números de Instagram (Tu alcance), las visitas a la tarjeta
y el embudo de la campaña activa del Marketing Executor de Benjamín (dalmeet_executor).
"""

from collections import defaultdict

from dalmeet_executor.db import get_active_campaign
from dalmeet_executor.reporting import build_campaign_summary

from . import actividad, estadisticas


def _alcance_por_formato(publicaciones: list[dict]) -> dict[str, float]:
    sumas, cuentas = defaultdict(float), defaultdict(int)
    for p in publicaciones:
        sumas[p["formato"]] += p["alcance"]
        cuentas[p["formato"]] += 1
    return dict(sorted(((f, sumas[f] / cuentas[f]) for f in sumas), key=lambda x: -x[1]))


def lineas() -> list[str]:
    """Los hallazgos principales, en frases cortas. Vacío si todavía no hay datos."""
    publicaciones = estadisticas.cargar()
    visitas = actividad.cargar().get("visitas", {})
    salida = []
    if publicaciones:
        mejor = max(publicaciones, key=lambda p: p["alcance"])
        salida.append(f"Mejor publicación: \"{mejor['publicacion']}\" ({mejor['formato']}), {mejor['alcance']} cuentas alcanzadas.")
        formatos = _alcance_por_formato(publicaciones)
        if len(formatos) >= 2:
            salida.append("Alcance promedio por formato: " + ", ".join(f"{f} {v:.0f}" for f, v in formatos.items()) + ".")
    campana = get_active_campaign()
    if campana:
        r = build_campaign_summary(campana.id)["results"]
        if r["consultations"] or r["patients"]:
            salida.append(f"Campaña \"{campana.name}\": {r['consultations']} consultas, {r['patients']} nuevas clientas "
                          f"(conversión {r['conversion_consultation_to_patient_pct']:.0f} %).")
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
