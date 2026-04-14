"""
LAB 9.1 — AI Act Europeo y GDPR
==================================
Objetivo: aplicar los conceptos del AI Act y GDPR al análisis
de sistemas IA reales mediante ejercicios prácticos.

Ejercicios:
  1. Clasificador de riesgo AI Act para sistemas de una empresa
  2. Evaluación de cumplimiento GDPR en casos de uso con IA
  3. Generador de ficha de evaluación de impacto (EIPD simplificada)

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import json

MODELO = "claude-haiku-4-5-20251001"


def llamar_api(prompt, system="", max_tokens=700):
    try:
        import anthropic
        client = anthropic.Anthropic()
        kwargs = dict(
            model=MODELO,
            max_tokens=max_tokens,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}]
        )
        if system:
            kwargs["system"] = system
        r = client.messages.create(**kwargs)
        return r.content[0].text.strip()
    except Exception as e:
        return f"[Error API: {e}]"


# ─── EJERCICIO 1: CLASIFICADOR DE RIESGO AI ACT ───────────────────────────────

SISTEMAS_IA_EMPRESA = [
    {
        "nombre": "Chatbot de atención al cliente en la web",
        "descripcion": "Sistema conversacional que responde preguntas frecuentes, guía en el proceso de compra y transfiere a agente humano si es necesario. Interactúa directamente con clientes.",
        "usuarios_afectados": "clientes externos",
        "toma_decisiones_sobre_personas": False,
        "datos_personales": True,
        "sectores_regulados": [],
    },
    {
        "nombre": "Sistema de scoring para concesión de crédito",
        "descripcion": "Analiza datos financieros del solicitante y genera una puntuación que determina si se concede o deniega un préstamo y en qué condiciones.",
        "usuarios_afectados": "solicitantes de crédito",
        "toma_decisiones_sobre_personas": True,
        "datos_personales": True,
        "sectores_regulados": ["financiero"],
    },
    {
        "nombre": "Herramienta de resúmenes de emails internos",
        "descripcion": "Sistema interno que resume hilos de email largos para los empleados. Solo uso interno, no interactúa con clientes ni afecta a decisiones sobre personas.",
        "usuarios_afectados": "empleados internos",
        "toma_decisiones_sobre_personas": False,
        "datos_personales": False,
        "sectores_regulados": [],
    },
    {
        "nombre": "Sistema de análisis de CVs para selección de personal",
        "descripcion": "Clasifica y puntúa candidatos en base a sus CVs para filtrar los que pasan a entrevista. La decisión de entrevistar o rechazar se basa en gran parte en esta puntuación.",
        "usuarios_afectados": "candidatos a empleo",
        "toma_decisiones_sobre_personas": True,
        "datos_personales": True,
        "sectores_regulados": ["empleo"],
    },
    {
        "nombre": "Generador de contenido para redes sociales",
        "descripcion": "Genera borradores de posts para LinkedIn e Instagram que el equipo de marketing revisa y publica. El contenido no se publica directamente sin revisión humana.",
        "usuarios_afectados": "audiencia general",
        "toma_decisiones_sobre_personas": False,
        "datos_personales": False,
        "sectores_regulados": [],
    },
]

SECTORES_ALTO_RIESGO_AI_ACT = [
    "financiero", "crédito", "seguros", "empleo", "educación",
    "salud", "infraestructuras críticas", "administración de justicia",
    "gestión de fronteras", "servicios públicos esenciales"
]

SYSTEM_CLASIFICADOR = """Eres un experto en cumplimiento del AI Act europeo (Reglamento UE 2024/1689).
Clasifica sistemas de IA en las categorías del AI Act:
- INACEPTABLE: prácticas prohibidas (manipulación, puntuación social, etc.)
- ALTO_RIESGO: decisiones en sectores sensibles (empleo, crédito, salud, etc.)
- RIESGO_LIMITADO: sistemas que interactúan con personas o generan contenido IA
- MINIMO: herramientas internas o de baja interacción con personas

Basa tu clasificación en los artículos y anexos del AI Act."""

PROMPT_CLASIFICAR_RIESGO = """Clasifica este sistema de IA según el AI Act europeo:

Nombre: {nombre}
Descripción: {descripcion}
Usuarios afectados: {usuarios_afectados}
¿Toma decisiones con efectos sobre personas?: {toma_decisiones}
¿Usa datos personales?: {datos_personales}
¿Opera en sectores regulados?: {sectores}

Responde SOLO JSON:
{{
  "categoria": "INACEPTABLE/ALTO_RIESGO/RIESGO_LIMITADO/MINIMO",
  "fundamento_legal": "artículo o anexo del AI Act que aplica",
  "obligaciones_principales": ["lista de 2-4 obligaciones concretas"],
  "plazo_cumplimiento": "fecha aproximada según el cronograma del AI Act",
  "prioridad_accion": "inmediata/alta/media/baja",
  "nota": "observación relevante para el equipo legal"
}}"""


def clasificar_riesgo_heuristico(sistema):
    """Clasificación básica sin IA."""
    if sistema["toma_decisiones_sobre_personas"]:
        sectores = [s.lower() for s in sistema.get("sectores_regulados", [])]
        if any(s in SECTORES_ALTO_RIESGO_AI_ACT for s in sectores):
            return "ALTO_RIESGO", "Decisiones en sector regulado por Anexo III AI Act"
    if "chatbot" in sistema["nombre"].lower() or "conversacional" in sistema["descripcion"].lower():
        return "RIESGO_LIMITADO", "Sistema conversacional — Art. 50 AI Act (transparencia)"
    if sistema["toma_decisiones_sobre_personas"] and sistema["datos_personales"]:
        return "ALTO_RIESGO", "Posible Anexo III — revisar con asesor legal"
    return "MINIMO", "Sin obligaciones específicas del AI Act"


def ejercicio_1_clasificador_riesgo(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 1 — CLASIFICADOR DE RIESGO AI ACT")
    print("=" * 64)

    for sistema in SISTEMAS_IA_EMPRESA:
        print(f"\n  Sistema: {sistema['nombre']}")
        print(f"  Descripción: {sistema['descripcion'][:70]}...")

        if tiene_api:
            prompt = PROMPT_CLASIFICAR_RIESGO.format(
                nombre=sistema["nombre"],
                descripcion=sistema["descripcion"],
                usuarios_afectados=sistema["usuarios_afectados"],
                toma_decisiones=sistema["toma_decisiones_sobre_personas"],
                datos_personales=sistema["datos_personales"],
                sectores=sistema["sectores_regulados"] or "ninguno"
            )
            resultado = llamar_api(prompt, system=SYSTEM_CLASIFICADOR, max_tokens=400)
            try:
                datos = json.loads(resultado)
                cat = datos["categoria"]
                iconos = {"INACEPTABLE": "🚫", "ALTO_RIESGO": "⚠", "RIESGO_LIMITADO": "ℹ", "MINIMO": "✓"}
                print(f"  Categoría: {iconos.get(cat, '?')} {cat}")
                print(f"  Base legal: {datos.get('fundamento_legal', 'N/A')}")
                print(f"  Prioridad: {datos.get('prioridad_accion', 'N/A').upper()}")
                print(f"  Obligaciones:")
                for ob in datos.get("obligaciones_principales", []):
                    print(f"    → {ob}")
            except json.JSONDecodeError:
                print(f"  {resultado[:200]}")
        else:
            categoria, motivo = clasificar_riesgo_heuristico(sistema)
            iconos = {"ALTO_RIESGO": "⚠", "RIESGO_LIMITADO": "ℹ", "MINIMO": "✓", "INACEPTABLE": "✗"}
            print(f"  Categoría (heurística): {iconos.get(categoria, '?')} {categoria}")
            print(f"  Motivo: {motivo}")


# ─── EJERCICIO 2: EVALUACIÓN GDPR ────────────────────────────────────────────

CASOS_GDPR = [
    {
        "id": "GDPR-01",
        "descripcion": "Enviamos transcripciones de llamadas de atención al cliente a la API de Claude para generar resúmenes automáticos. Las transcripciones incluyen nombres y datos de contacto de clientes.",
        "tipo_datos": "Nombre, teléfono, dirección, motivo de contacto",
        "base_legal_actual": "Interés legítimo",
        "informados_los_afectados": False,
        "datos_salen_ue": True,
        "pais_destino": "Estados Unidos (Anthropic)",
    },
    {
        "id": "GDPR-02",
        "descripcion": "Usamos IA para analizar CVs de candidatos. Los CVs se almacenan en nuestro servidor y el análisis se realiza con un modelo interno (on-premise).",
        "tipo_datos": "Nombre, edad, experiencia laboral, estudios",
        "base_legal_actual": "Ejecución de contrato (proceso de selección)",
        "informados_los_afectados": True,
        "datos_salen_ue": False,
        "pais_destino": None,
    },
    {
        "id": "GDPR-03",
        "descripcion": "Nuestro chatbot de soporte usa el histórico de compras del cliente para personalizar respuestas. El cliente no sabe que se usa su historial en el chatbot.",
        "tipo_datos": "Historial de compras, preferencias, incidencias previas",
        "base_legal_actual": "Interés legítimo",
        "informados_los_afectados": False,
        "datos_salen_ue": False,
        "pais_destino": None,
    },
]

PROMPT_EVALUAR_GDPR = """Eres un experto en GDPR (Reglamento UE 2016/679) aplicado a sistemas de IA.
Evalúa este caso de uso desde la perspectiva del GDPR:

Caso: {descripcion}
Tipos de datos: {tipo_datos}
Base legal actual: {base_legal_actual}
¿Informados los afectados?: {informados}
¿Datos salen de la UE?: {fuera_ue}
País destino (si aplica): {pais_destino}

Identifica riesgos y acciones necesarias. Responde SOLO JSON:
{{
  "cumplimiento_estimado": "alto/medio/bajo/critico",
  "riesgos_detectados": ["lista de riesgos concretos"],
  "base_legal_correcta": true/false,
  "base_legal_recomendada": "base legal correcta si la actual es incorrecta",
  "acciones_obligatorias": ["acciones requeridas por GDPR"],
  "plazo_recomendado": "inmediato/1 mes/3 meses",
  "articulos_aplicables": ["Art. X GDPR", "..."]
}}"""


def ejercicio_2_evaluacion_gdpr(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 2 — EVALUACIÓN DE CUMPLIMIENTO GDPR")
    print("=" * 64)

    for caso in CASOS_GDPR:
        print(f"\n  [{caso['id']}] {caso['descripcion'][:70]}...")
        print(f"  Datos: {caso['tipo_datos']}")
        print(f"  Base legal actual: {caso['base_legal_actual']} | Fuera UE: {caso['datos_salen_ue']}")

        if tiene_api:
            prompt = PROMPT_EVALUAR_GDPR.format(
                descripcion=caso["descripcion"],
                tipo_datos=caso["tipo_datos"],
                base_legal=caso["base_legal_actual"],
                informados=caso["informados_los_afectados"],
                fuera_ue=caso["datos_salen_ue"],
                pais_destino=caso.get("pais_destino") or "N/A",
                base_legal_actual=caso["base_legal_actual"],
            )
            resultado = llamar_api(prompt, max_tokens=400)
            try:
                datos = json.loads(resultado)
                niveles = {"critico": "🔴", "bajo": "🟠", "medio": "🟡", "alto": "🟢"}
                nivel = datos.get("cumplimiento_estimado", "?")
                print(f"  Cumplimiento: {niveles.get(nivel, '?')} {nivel.upper()}")
                print(f"  Base legal correcta: {'Sí' if datos.get('base_legal_correcta') else 'No — ' + datos.get('base_legal_recomendada', '')}")
                print(f"  Plazo: {datos.get('plazo_recomendado', '?')}")
                print(f"  Riesgos:")
                for r in datos.get("riesgos_detectados", [])[:3]:
                    print(f"    ⚠ {r}")
                print(f"  Acciones obligatorias:")
                for a in datos.get("acciones_obligatorias", [])[:3]:
                    print(f"    → {a}")
            except json.JSONDecodeError:
                print(f"  {resultado[:200]}")
        else:
            # Evaluación por reglas básicas
            riesgos = []
            if not caso["informados_los_afectados"]:
                riesgos.append("Falta de información al interesado (Art. 13/14 GDPR)")
            if caso["datos_salen_ue"] and caso.get("pais_destino") == "Estados Unidos (Anthropic)":
                riesgos.append("Transferencia a EE.UU. — verificar DPA y SCCs con Anthropic")
            if not riesgos:
                riesgos.append("Sin riesgos evidentes — revisión detallada recomendada")
            print(f"  Riesgos básicos detectados:")
            for r in riesgos:
                print(f"    ⚠ {r}")
            print("  [Configura ANTHROPIC_API_KEY para análisis jurídico completo]")


# ─── EJERCICIO 3: GENERADOR DE EIPD SIMPLIFICADA ─────────────────────────────

SISTEMA_PARA_EIPD = {
    "nombre": "Sistema de análisis predictivo de churn de clientes",
    "descripcion": "Usa historial de compras, interacciones de soporte y datos demográficos de clientes para predecir cuáles tienen más probabilidad de cancelar el servicio en los próximos 90 días. Los resultados se usan para activar campañas de retención dirigidas.",
    "datos_procesados": [
        "Historial de compras (últimos 24 meses)",
        "Número y tipo de interacciones con soporte",
        "Tiempo desde último acceso al servicio",
        "Segmento de cliente (pyme/enterprise/particular)",
        "Región geográfica",
    ],
    "numero_afectados_estimado": "~15.000 clientes activos",
    "responsable_tratamiento": "Mi Empresa S.A.",
    "proveedor_ia": "Anthropic (Claude API) — DPA firmado",
    "finalidad": "Reducir tasa de abandono activando retención proactiva",
    "base_legal_propuesta": "Interés legítimo (Art. 6.1.f GDPR)",
}

PROMPT_EIPD = """Eres el DPO (Delegado de Protección de Datos) de una empresa.
Genera una Evaluación de Impacto en la Protección de Datos (EIPD) simplificada
para este sistema de IA, siguiendo los requisitos del Art. 35 GDPR.

Sistema a evaluar:
{sistema}

Genera la EIPD en formato estructurado con:
1. ¿ES NECESARIA LA EIPD? (criterios del Art. 35)
2. DESCRIPCIÓN DEL TRATAMIENTO
3. EVALUACIÓN DE NECESIDAD Y PROPORCIONALIDAD
4. RIESGOS IDENTIFICADOS (con nivel: alto/medio/bajo)
5. MEDIDAS PARA MITIGAR RIESGOS
6. CONCLUSIÓN: ¿Puede procederse o necesita consulta previa a la AEPD?

Sé específico y práctico. Máximo 400 palabras."""


def ejercicio_3_eipd(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 3 — EVALUACIÓN DE IMPACTO (EIPD) SIMPLIFICADA")
    print("=" * 64)

    print(f"\n  Sistema: {SISTEMA_PARA_EIPD['nombre']}")
    print(f"  Descripción: {SISTEMA_PARA_EIPD['descripcion'][:80]}...")
    print(f"  Afectados: {SISTEMA_PARA_EIPD['numero_afectados_estimado']}")
    print(f"  Base legal propuesta: {SISTEMA_PARA_EIPD['base_legal_propuesta']}")

    if tiene_api:
        prompt = PROMPT_EIPD.format(
            sistema=json.dumps(SISTEMA_PARA_EIPD, ensure_ascii=False, indent=2)
        )
        eipd = llamar_api(prompt, max_tokens=700)
        print("\n  EVALUACIÓN DE IMPACTO (EIPD):")
        print("  " + "=" * 50)
        for linea in eipd.split("\n"):
            print(f"  {linea}")
    else:
        print("\n  EIPD BÁSICA (fallback):")
        print()
        print("  1. ¿ES NECESARIA LA EIPD?")
        print("     Sí. El sistema realiza evaluación sistemática de aspectos personales")
        print("     con efectos sobre las personas (Art. 35.3.a GDPR).")
        print()
        print("  2. RIESGOS PRINCIPALES:")
        print("     ⚠ MEDIO — Perfilado sin consentimiento explícito")
        print("     ⚠ MEDIO — Posibles sesgos en el modelo predictivo")
        print("     ⚠ BAJO  — Transferencia de datos a Anthropic (DPA firmado)")
        print()
        print("  3. MEDIDAS:")
        print("     → Informar a clientes en política de privacidad del uso de IA")
        print("     → Evaluación periódica de sesgos en el modelo")
        print("     → Derecho a no ser objeto de decisión automatizada garantizado")
        print()
        print("  4. CONCLUSIÓN: Puede procederse con las medidas indicadas.")
        print("     No requiere consulta previa si se implementan las medidas.")
        print()
        print("  [Configura ANTHROPIC_API_KEY para EIPD completa generada por IA]")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 64)
    print("LAB 9.1 — AI ACT EUROPEO Y GDPR")
    print("=" * 64)

    tiene_api = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if tiene_api:
        print(f"  Modelo: {MODELO}")
        print("  Modo: API activa — análisis legal con IA")
    else:
        print("  AVISO: ANTHROPIC_API_KEY no configurada.")
        print("  Modo: Análisis por reglas y heurísticas")
    print()
    print("  NOTA IMPORTANTE: Los resultados de este lab son orientativos.")
    print("  Para decisiones legales reales, consultar con asesor jurídico")
    print("  especializado en derecho digital.")

    ejercicio_1_clasificador_riesgo(tiene_api)
    ejercicio_2_evaluacion_gdpr(tiene_api)
    ejercicio_3_eipd(tiene_api)

    print("\n" + "=" * 64)
    print("RESUMEN DEL LAB")
    print("=" * 64)
    print("""
  Herramientas construidas:
  ✓ Clasificador de riesgo AI Act para sistemas empresariales
  ✓ Evaluador de cumplimiento GDPR para casos de uso con IA
  ✓ Generador de EIPD simplificada

  Recuerda:
    La mayoría de herramientas internas → RIESGO MÍNIMO
    Chatbots con clientes → RIESGO LIMITADO (transparencia)
    Decisiones sobre personas en sectores sensibles → ALTO RIESGO

  Próximos pasos para tu empresa:
    1. Inventariar todos los sistemas IA en uso
    2. Clasificar cada uno según el árbol de decisión
    3. Priorizar los de alto riesgo para actuación inmediata
    4. Actualizar avisos de privacidad para mencionar uso de IA
""")

    print("[FIN DEL LAB 9.1]")
