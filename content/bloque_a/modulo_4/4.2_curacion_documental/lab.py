"""
LAB 4.2 — Curación de Bases Documentales
==========================================
Objetivo: construir herramientas de auditoría, limpieza y
enriquecimiento de una base documental para RAG.

Ejercicios:
  1. Auditor de documentos — detecta problemas comunes
  2. Limpiador de texto — normaliza y sanitiza contenido
  3. Generador de metadatos con IA — enriquece documentos automáticamente

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


def llamar_api(prompt, temperatura=0.1, max_tokens=400):
    try:
        import anthropic
        client = anthropic.Anthropic()
        r = client.messages.create(model=MODELO, max_tokens=max_tokens,
            temperature=temperatura, messages=[{"role":"user","content":prompt}])
        return r.content[0].text.strip()
    except Exception as e:
        return f"Error: {e}"


# ─── PARTE 1: AUDITOR DE DOCUMENTOS ──────────────────────────────────────────

DOCUMENTOS_AUDITORIA = [
    {"id": "doc1", "titulo": "Política de devoluciones v1", "texto": "Devoluciones en 30 días.", "fecha": "2022-03-15", "estado": "vigente"},
    {"id": "doc2", "titulo": "Política de devoluciones v2", "texto": "Devoluciones en 30 días para productos estándar, 90 para defectuosos.", "fecha": "2025-01-10", "estado": "vigente"},
    {"id": "doc3", "titulo": "Procedimiento de compras", "texto": "", "fecha": "2023-06-01", "estado": "vigente"},
    {"id": "doc4", "titulo": "Datos empleados", "texto": "Juan García, DNI 12345678A, salario 35.000€. María López, 41.234€.", "fecha": "2024-01-01", "estado": "vigente"},
    {"id": "doc5", "titulo": "Manual de bienvenida", "texto": "Bienvenido a la empresa. " * 5, "fecha": "2021-09-01", "estado": "vigente"},
]

PATRONES_PII = [
    r"\b\d{8}[A-Z]\b",          # DNI español
    r"\b[A-Z]\d{7}[A-Z]\b",     # NIE
    r"\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b",  # tarjeta bancaria
    r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",  # email personal
    r"salario\s+\d[\d.]+",       # dato salarial
]

def auditar_documento(doc: dict) -> dict:
    alertas = []
    if not doc.get("texto", "").strip():
        alertas.append("VACÍO: documento sin contenido")
    if len(doc.get("texto","").split()) < 20:
        alertas.append("MUY_CORTO: menos de 20 palabras")
    for patron in PATRONES_PII:
        if re.search(patron, doc.get("texto",""), re.IGNORECASE):
            alertas.append(f"PII_DETECTADO: patrón sensible encontrado")
            break
    return {"id": doc["id"], "titulo": doc["titulo"], "alertas": alertas, "ok": len(alertas) == 0}

def auditar_coleccion(documentos: list) -> dict:
    # Detectar duplicados por similitud de título
    titulos = [d["titulo"].lower() for d in documentos]
    posibles_duplicados = []
    for i, t1 in enumerate(titulos):
        for j, t2 in enumerate(titulos):
            if i < j:
                palabras1 = set(re.sub(r'v\d+','',t1).split())
                palabras2 = set(re.sub(r'v\d+','',t2).split())
                if len(palabras1 & palabras2) / max(len(palabras1), 1) > 0.7:
                    posibles_duplicados.append((documentos[i]["id"], documentos[j]["id"]))

    resultados = [auditar_documento(d) for d in documentos]
    return {
        "total": len(documentos),
        "ok": sum(1 for r in resultados if r["ok"]),
        "con_alertas": [r for r in resultados if not r["ok"]],
        "posibles_duplicados": posibles_duplicados,
    }


# ─── PARTE 2: LIMPIADOR DE TEXTO ─────────────────────────────────────────────

def limpiar_texto(texto: str) -> dict:
    original = texto
    # Normalizar espacios
    texto = re.sub(r'\s+', ' ', texto).strip()
    # Eliminar caracteres de control
    texto = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', texto)
    # Redactar PII
    for patron in PATRONES_PII:
        texto = re.sub(patron, '[REDACTED]', texto, flags=re.IGNORECASE)

    return {
        "original_chars": len(original),
        "limpio_chars":   len(texto),
        "texto_limpio":   texto,
        "cambios":        original != texto,
    }


# ─── PARTE 3: GENERADOR DE METADATOS CON IA ──────────────────────────────────

PROMPT_METADATOS = """Analiza este documento y genera metadatos estructurados en JSON.

DOCUMENTO:
Título: {titulo}
Contenido: {texto}

Devuelve SOLO este JSON:
{{
  "tipo": "politica|procedimiento|manual|catalogo|normativa|otro",
  "departamento": "área responsable",
  "audiencia": ["lista", "de", "roles"],
  "palabras_clave": ["5", "palabras", "clave"],
  "resumen": "1 frase de qué trata",
  "necesita_actualizacion": true/false,
  "razon_actualizacion": "si aplica, por qué"
}}"""


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 64)
    print("LAB 4.2 — Curación de Bases Documentales")
    print("=" * 64)

    tiene_api = bool(os.getenv("ANTHROPIC_API_KEY"))

    print("\n[1] AUDITORÍA DE COLECCIÓN")
    print("-" * 64)
    auditoria = auditar_coleccion(DOCUMENTOS_AUDITORIA)
    print(f"\n  Total documentos: {auditoria['total']}")
    print(f"  Sin problemas: {auditoria['ok']}")
    print(f"  Con alertas: {len(auditoria['con_alertas'])}")
    for doc in auditoria['con_alertas']:
        print(f"\n  ⚠️  {doc['titulo']}")
        for alerta in doc['alertas']:
            print(f"      → {alerta}")
    if auditoria['posibles_duplicados']:
        print(f"\n  Posibles duplicados: {auditoria['posibles_duplicados']}")

    print("\n\n[2] LIMPIADOR DE TEXTO")
    print("-" * 64)
    for doc in DOCUMENTOS_AUDITORIA:
        if doc["texto"]:
            r = limpiar_texto(doc["texto"])
            if r["cambios"]:
                print(f"\n  {doc['titulo']}: {r['original_chars']} → {r['limpio_chars']} chars")
                print(f"  Texto limpio: {r['texto_limpio'][:120]}")

    print("\n\n[3] GENERADOR DE METADATOS CON IA")
    print("-" * 64)
    if tiene_api:
        doc_test = DOCUMENTOS_AUDITORIA[1]
        prompt = PROMPT_METADATOS.format(titulo=doc_test["titulo"], texto=doc_test["texto"])
        resultado = llamar_api(prompt, temperatura=0.1)
        print(f"\n  Documento: {doc_test['titulo']}")
        print(f"  Metadatos generados:\n  {resultado}")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY para generar metadatos con IA.")

    print("\n[FIN DEL LAB 4.2]")
