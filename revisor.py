"""
REVISOR.PY — Revisión y mejora de módulos con Claude Opus
==========================================================
Envía el contenido de cualquier módulo a Claude Opus actuando
como co-autor experto crítico. Recibe un análisis estructurado
con puntos fuertes, lagunas y propuestas de mejora concretas.

Uso:
    python revisor.py                          # revisa el último módulo
    python revisor.py --modulo 1.3             # revisa un módulo concreto
    python revisor.py --modulo 1.2 --aplicar   # revisa y guarda revisión

Requisitos:
    pip install anthropic
    export ANTHROPIC_API_KEY='sk-ant-...'
"""

import os
import sys
import time
import argparse
from pathlib import Path

# ─── CONFIG ───────────────────────────────────────────────────────────────────

MODELO_REVISOR  = "claude-opus-4-6"      # el revisor usa Opus — máximo criterio
MODELO_EDITOR   = "claude-sonnet-4-6"    # el editor usa Sonnet — síntesis final

BASE_CONTENT = Path(__file__).parent / "content"

# Mapa id → ruta relativa al README
MODULOS = {
    "1.1": "bloque_a/modulo_1/1.1_panorama_ia/README.md",
    "1.2": "bloque_a/modulo_1/1.2_ia_palanca_estrategica/README.md",
    "1.3": "bloque_a/modulo_1/1.3_caso_negocio/README.md",
    "2.1": "bloque_a/modulo_2/2.1_arquitectura_llms/README.md",
    "2.2": "bloque_a/modulo_2/2.2_prompt_engineering/README.md",
    "2.3": "bloque_a/modulo_2/2.3_seleccion_modelos/README.md",
}


# ─── UTILIDADES ───────────────────────────────────────────────────────────────

def leer_modulo(id_modulo: str) -> tuple[str, Path]:
    """Lee el README del módulo y devuelve (contenido, ruta)."""
    if id_modulo not in MODULOS:
        print(f"Módulo '{id_modulo}' no encontrado. Disponibles: {', '.join(MODULOS)}")
        sys.exit(1)

    ruta = BASE_CONTENT / MODULOS[id_modulo]
    if not ruta.exists():
        print(f"Archivo no encontrado: {ruta}")
        sys.exit(1)

    return ruta.read_text(encoding="utf-8"), ruta


def ultimo_modulo() -> str:
    """Devuelve el id del último módulo con README disponible."""
    for mid in reversed(list(MODULOS.keys())):
        ruta = BASE_CONTENT / MODULOS[mid]
        if ruta.exists():
            return mid
    return "1.1"


# ─── PASO 1: ANÁLISIS CRÍTICO (OPUS) ─────────────────────────────────────────

def revisar_con_opus(contenido: str, id_modulo: str) -> str:
    """
    Claude Opus actúa como co-autor experto crítico.
    Analiza el módulo y devuelve un informe estructurado.

    PARÁMETROS CLAVE:
        temperature=0.7  → criterio propio, no solo eco del original
        max_tokens=2000  → análisis profundo con ejemplos concretos
        system prompt    → rol de experto independiente con licencia para criticar
    """
    import anthropic
    client = anthropic.Anthropic()

    system = """Eres un co-autor experto en formación de IA aplicada para directivos y managers.
Tu misión es revisar módulos de un Master en IA con criterio académico riguroso y visión práctica empresarial.

Tu rol es el de revisor crítico constructivo — NO un validador. Tienes licencia para:
- Señalar lo que falta aunque sea incómodo
- Proponer enfoques alternativos con argumentos
- Identificar ejemplos débiles y sugerir mejores
- Detectar lagunas conceptuales o didácticas

Formato de respuesta OBLIGATORIO (en markdown):

## ✅ Fortalezas del módulo
[3-5 puntos fuertes específicos con cita del texto]

## ⚠️ Lagunas y puntos débiles
[3-5 puntos con explicación de por qué es una laguna y su impacto en el aprendizaje]

## 💡 Propuestas de mejora concretas
[3-5 propuestas ACCIONABLES con el texto exacto sugerido o la estructura recomendada]

## 🔗 Conexiones que faltan
[Conceptos, casos reales o referencias que enriquecerían el módulo]

## 📊 Veredicto
[Puntuación 1-10 en: Rigor técnico / Claridad didáctica / Aplicabilidad práctica]
[Una frase de síntesis: qué haría de este módulo uno excelente]"""

    prompt = f"""Revisa en profundidad el siguiente módulo del Master IA (id: {id_modulo}):

---
{contenido}
---

Sé específico, directo y constructivo. El objetivo es hacer este módulo excelente, no solo bueno."""

    print(f"  Enviando a Claude Opus para revisión profunda...")
    inicio = time.time()

    resp = client.messages.create(
        model=MODELO_REVISOR,
        max_tokens=2000,
        temperature=0.7,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )

    latencia = round((time.time() - inicio) * 1000)
    tokens_info = f"\n\n---\n*Revisión generada por {MODELO_REVISOR} | {resp.usage.input_tokens}→{resp.usage.output_tokens} tokens | {latencia}ms*"

    return resp.content[0].text + tokens_info


# ─── PASO 2: SÍNTESIS Y VERSIÓN MEJORADA (SONNET) ────────────────────────────

def sintetizar_mejoras(contenido_original: str, revision: str, id_modulo: str) -> str:
    """
    Claude Sonnet recibe el original + la revisión de Opus y
    genera una versión mejorada del módulo incorporando las sugerencias.

    PARÁMETROS CLAVE:
        temperature=0.3  → fiel al original, mejoras controladas
        max_tokens=4000  → suficiente para un README completo mejorado
    """
    import anthropic
    client = anthropic.Anthropic()

    prompt = f"""Tienes el módulo original de un Master IA y la revisión crítica de un experto.

## MÓDULO ORIGINAL (id: {id_modulo})
{contenido_original}

## REVISIÓN DEL EXPERTO
{revision}

Tu tarea: genera una versión MEJORADA del módulo que:
1. Mantiene toda la estructura y los puntos fuertes del original
2. Incorpora las mejoras concretas sugeridas por el revisor
3. Corrige las lagunas identificadas
4. Añade las conexiones y ejemplos propuestos donde aporten valor

REGLAS:
- Respeta el estilo y el tono del original
- No elimines secciones existentes, expándelas o mejóralas
- Si el revisor propone texto exacto, úsalo
- El resultado debe ser un README.md completo y listo para publicar

Devuelve únicamente el contenido del README mejorado, sin comentarios adicionales."""

    print(f"  Sintetizando versión mejorada con Claude Sonnet...")
    inicio = time.time()

    resp = client.messages.create(
        model=MODELO_EDITOR,
        max_tokens=4000,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )

    latencia = round((time.time() - inicio) * 1000)
    print(f"  Síntesis completada en {latencia}ms ({resp.usage.output_tokens} tokens)")

    return resp.content[0].text


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Revisor de módulos Master IA con Claude Opus")
    parser.add_argument("--modulo", "-m", default=None,
                        help="ID del módulo a revisar (ej: 1.3). Por defecto el último disponible.")
    parser.add_argument("--aplicar", "-a", action="store_true",
                        help="Guarda la versión mejorada como README_v2.md junto al original.")
    args = parser.parse_args()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: configura ANTHROPIC_API_KEY antes de ejecutar.")
        print("  export ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)

    try:
        import anthropic  # noqa
    except ImportError:
        print("Error: instala el SDK → pip install anthropic")
        sys.exit(1)

    id_modulo = args.modulo or ultimo_modulo()
    contenido, ruta = leer_modulo(id_modulo)

    print("=" * 64)
    print(f"REVISOR — Módulo {id_modulo}")
    print(f"Archivo: {ruta.relative_to(Path(__file__).parent)}")
    print("=" * 64)

    # ── PASO 1: Revisión crítica con Opus ──────────────────────────────────
    print("\n[1/2] ANÁLISIS CRÍTICO (Claude Opus)\n")
    revision = revisar_con_opus(contenido, id_modulo)
    print(revision)

    # ── PASO 2: Versión mejorada (opcional) ────────────────────────────────
    if args.aplicar:
        print("\n" + "=" * 64)
        print("[2/2] VERSIÓN MEJORADA (Claude Sonnet)\n")
        version_mejorada = sintetizar_mejoras(contenido, revision, id_modulo)

        ruta_v2 = ruta.parent / "README_v2.md"
        ruta_v2.write_text(version_mejorada, encoding="utf-8")
        print(f"\n  ✓ Versión mejorada guardada en: {ruta_v2.relative_to(Path(__file__).parent)}")
        print("  → Revisa README_v2.md, y si te convence reemplaza el README.md original.")
    else:
        print("\n" + "─" * 64)
        print("TIP: Ejecuta con --aplicar para generar README_v2.md con las mejoras incorporadas.")
        print(f"     python revisor.py --modulo {id_modulo} --aplicar")

    print("\n[FIN DE REVISIÓN]")


if __name__ == "__main__":
    main()
