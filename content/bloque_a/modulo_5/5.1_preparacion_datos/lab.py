"""
LAB 5.1 — Preparación de Datos para Análisis con IA
=====================================================
Objetivo: aplicar el pipeline de preparación sobre un dataset
sucio realista y usar IA para las tareas que requieren semántica.

Ejercicios:
  1. Perfilador de dataset — diagnóstico automático de problemas
  2. Pipeline de limpieza — normalización, nulos, deduplicación
  3. Enriquecimiento con IA — categorización y extracción de entidades

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import re
import json
import time
from datetime import datetime

MODELO = "claude-haiku-4-5-20251001"

# ─── DATASET SUCIO DE EJEMPLO ─────────────────────────────────────────────────

DATASET_SUCIO = [
    {"id": 1,  "empresa": "ACME Solutions S.L.",    "fecha": "2025-01-15", "importe": "12.500",    "estado": "pagado",     "sector": "tecnología"},
    {"id": 2,  "empresa": "Acme solutions sl",      "fecha": "15/01/2025", "importe": "3200",      "estado": "Pagado",     "sector": "Tecnología"},
    {"id": 3,  "empresa": "Distribuciones Norte",   "fecha": "2025-02-03", "importe": "8.900,50",  "estado": "pendiente",  "sector": None},
    {"id": 4,  "empresa": "Dist. Norte S.A.",       "fecha": "03-02-2025", "importe": "N/A",       "estado": "PENDIENTE",  "sector": "logística"},
    {"id": 5,  "empresa": "Consultores Ibéricos",   "fecha": "2025-02-20", "importe": "45000",     "estado": "vencido",    "sector": "consultoría"},
    {"id": 6,  "empresa": "",                        "fecha": "2025-03-01", "importe": "-",         "estado": "cancelado",  "sector": "desconocido"},
    {"id": 7,  "empresa": "Tech Innovators SL",     "fecha": "01/03/2025", "importe": "7,500.00",  "estado": "pagado",     "sector": "tech"},
    {"id": 8,  "empresa": "Consultores Ibéricos",   "fecha": "2025-02-20", "importe": "45000",     "estado": "vencido",    "sector": "consultoría"},  # duplicado
]

ESTADOS_VALIDOS   = {"pagado", "pendiente", "vencido", "cancelado"}
SECTORES_VALIDOS  = {"tecnología", "logística", "consultoría", "industria", "servicios", "otro"}
MAPA_ESTADOS      = {"Pagado": "pagado", "PENDIENTE": "pendiente", "vencido": "vencido", "cancelado": "cancelado"}
MAPA_SECTORES     = {"tech": "tecnología", "tecnología": "tecnología", "logística": "logística",
                      "consultoría": "consultoría", "desconocido": "otro"}


# ─── PERFILADOR ───────────────────────────────────────────────────────────────

def perfilar_dataset(datos: list) -> dict:
    if not datos:
        return {}
    columnas = list(datos[0].keys())
    perfil = {}
    for col in columnas:
        valores = [r[col] for r in datos]
        nulos   = sum(1 for v in valores if v is None or str(v).strip() in ("", "N/A", "-", "desconocido"))
        unicos  = len(set(str(v) for v in valores))
        perfil[col] = {
            "nulos":    f"{nulos}/{len(datos)} ({nulos/len(datos)*100:.0f}%)",
            "únicos":   unicos,
            "ejemplos": list(set(str(v) for v in valores if v))[:3],
        }
    return perfil


# ─── PIPELINE DE LIMPIEZA ─────────────────────────────────────────────────────

def normalizar_fecha(fecha_str: str) -> str | None:
    if not fecha_str:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(fecha_str, fmt).strftime("%Y-%m-%d")
        except:
            pass
    return None

def normalizar_importe(importe_str: str) -> float | None:
    if not importe_str or str(importe_str).strip() in ("N/A", "-", ""):
        return None
    s = str(importe_str).strip()
    # Detectar si usa punto como miles y coma como decimal (europeo)
    if re.match(r'^\d{1,3}(\.\d{3})+(,\d+)?$', s):
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", "")
    try:
        return float(s)
    except:
        return None

def limpiar_registro(r: dict) -> dict:
    return {
        "id":      r["id"],
        "empresa": r["empresa"].strip() or None,
        "fecha":   normalizar_fecha(r.get("fecha")),
        "importe": normalizar_importe(r.get("importe")),
        "estado":  MAPA_ESTADOS.get(r.get("estado",""), r.get("estado","")).lower() if r.get("estado") else None,
        "sector":  MAPA_SECTORES.get((r.get("sector") or "").lower(), r.get("sector","").lower() or None),
    }

def deduplicar(datos: list) -> list:
    vistos = set()
    resultado = []
    for r in datos:
        clave = (r.get("empresa","").lower().strip(), r.get("fecha"), r.get("importe"))
        if clave not in vistos:
            vistos.add(clave)
            resultado.append(r)
    return resultado


# ─── ENRIQUECIMIENTO CON IA ───────────────────────────────────────────────────

def categorizar_empresas_con_ia(nombres: list) -> str:
    try:
        import anthropic
        client = anthropic.Anthropic()
        prompt = f"""Analiza estos nombres de empresa y agrúpalos si son la misma entidad.
Devuelve JSON: lista de grupos, donde cada grupo tiene "nombre_canonico" y "variantes".

Nombres: {json.dumps(nombres, ensure_ascii=False)}"""
        r = client.messages.create(model=MODELO, max_tokens=300, temperature=0.0,
            messages=[{"role":"user","content":prompt}])
        return r.content[0].text.strip()
    except Exception as e:
        return f"Error: {e}"


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 64)
    print("LAB 5.1 — Preparación de Datos para Análisis con IA")
    print("=" * 64)

    print("\n[1] PERFILADO DEL DATASET SUCIO")
    print("-" * 64)
    perfil = perfilar_dataset(DATASET_SUCIO)
    for col, stats in perfil.items():
        print(f"\n  {col}: {stats['nulos']} nulos | {stats['únicos']} únicos")
        print(f"    Ejemplos: {stats['ejemplos']}")

    print("\n\n[2] PIPELINE DE LIMPIEZA")
    print("-" * 64)
    datos_limpios = [limpiar_registro(r) for r in DATASET_SUCIO]
    datos_limpios = deduplicar(datos_limpios)
    datos_limpios = [r for r in datos_limpios if r["empresa"]]  # eliminar sin empresa

    print(f"\n  Registros originales: {len(DATASET_SUCIO)}")
    print(f"  Registros limpios: {len(datos_limpios)}")
    print(f"\n  {'ID':<4} {'Empresa':<30} {'Fecha':<12} {'Importe':>10} {'Estado':<12} {'Sector'}")
    print("  " + "-" * 76)
    for r in datos_limpios:
        print(f"  {r['id']:<4} {str(r['empresa']):<30} {str(r['fecha']):<12} "
              f"{str(r['importe'] or 'nulo'):>10} {str(r['estado']):<12} {r['sector']}")

    print("\n\n[3] ENRIQUECIMIENTO CON IA — Deduplicación semántica de empresas")
    print("-" * 64)
    nombres = list(set(r["empresa"] for r in DATASET_SUCIO if r["empresa"]))
    if os.getenv("ANTHROPIC_API_KEY"):
        resultado = categorizar_empresas_con_ia(nombres)
        print(f"\n  Nombres analizados: {nombres}")
        print(f"\n  Grupos detectados:\n  {resultado}")
    else:
        print(f"\n  Nombres para analizar: {nombres}")
        print("  NOTA: Configura ANTHROPIC_API_KEY para agrupar con IA.")
        print("  Resultado esperado: 'ACME Solutions S.L.' y 'Acme solutions sl' → mismo grupo")

    print("\n[FIN DEL LAB 5.1]")
