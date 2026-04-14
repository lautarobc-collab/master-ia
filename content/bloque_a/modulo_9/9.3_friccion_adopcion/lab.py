"""
LAB 9.3 — Fricción Tecnológica y Gestión del Cambio
=====================================================
Objetivo: construir herramientas para diagnosticar y gestionar
la adopción de IA en una organización.

Ejercicios:
  1. Diagnóstico de barreras — encuesta y análisis de actitudes
  2. Simulador de conversaciones difíciles sobre IA (AI Champion tool)
  3. Generador de plan de adopción personalizado por empresa

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
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )
        if system:
            kwargs["system"] = system
        r = client.messages.create(**kwargs)
        return r.content[0].text.strip()
    except Exception as e:
        return f"[Error API: {e}]"


# ─── EJERCICIO 1: DIAGNÓSTICO DE BARRERAS ────────────────────────────────────

# Resultados simulados de encuesta de actitud hacia IA
RESULTADOS_ENCUESTA = {
    "total_encuestados": 87,
    "departamentos": {
        "ventas": 22,
        "operaciones": 31,
        "administracion": 18,
        "marketing": 10,
        "it": 6,
    },
    "pregunta_1_actitud_general": {
        "pregunta": "¿Cómo describes tu actitud hacia el uso de IA en el trabajo?",
        "respuestas": {
            "muy_positiva": 12,
            "positiva": 28,
            "neutral": 24,
            "negativa": 16,
            "muy_negativa": 7,
        },
    },
    "pregunta_2_barreras": {
        "pregunta": "¿Cuál es tu principal barrera para usar IA? (múltiple)",
        "respuestas": {
            "miedo_perder_trabajo": 31,
            "falta_de_formacion": 42,
            "no_confio_en_resultados": 38,
            "demasiadas_herramientas": 27,
            "mi_jefe_no_la_usa": 19,
            "no_veo_el_beneficio": 15,
            "preocupacion_privacidad": 33,
        },
    },
    "pregunta_3_uso_actual": {
        "pregunta": "¿Usas actualmente alguna herramienta de IA en tu trabajo?",
        "respuestas": {
            "si_diariamente": 8,
            "si_semanalmente": 14,
            "si_ocasionalmente": 21,
            "no_nunca": 44,
        },
    },
    "pregunta_4_casos_uso_deseados": {
        "pregunta": "¿Para qué te gustaría usar IA? (múltiple)",
        "respuestas": {
            "redactar_emails": 67,
            "resumir_documentos": 58,
            "analizar_datos": 41,
            "preparar_presentaciones": 49,
            "automatizar_tareas_repetitivas": 72,
            "buscar_informacion": 55,
        },
    },
    "comentarios_abiertos": [
        "Me preocupa que los datos de clientes vayan a parar a empresas de fuera",
        "Quiero aprender pero nadie me enseña en horario de trabajo",
        "Mi jefe dice que hay que usarla pero él no la usa",
        "Probé ChatGPT y me dio datos incorrectos, desde entonces no me fío",
        "Creo que puede ayudar pero necesito ver casos prácticos de mi trabajo",
        "¿Quién es responsable si la IA comete un error en mi nombre?",
    ],
}

PROMPT_ANALIZAR_ENCUESTA = """Eres el responsable de gestión del cambio para la adopción de IA.
Analiza los resultados de esta encuesta y genera un diagnóstico ejecutivo.

Resultados de la encuesta:
{resultados}

Proporciona:
1. DIAGNÓSTICO: estado actual de la organización (3-4 frases)
2. TOP 3 BARRERAS PRIORITARIAS a abordar (con evidencia de los datos)
3. TOP 3 FORTALEZAS en las que apoyarse
4. SEGMENTOS DE RIESGO: qué departamentos o perfiles necesitan más atención
5. RECOMENDACIONES INMEDIATAS (primeras 4 semanas): 3 acciones concretas
6. MENSAJE CLAVE para la comunicación interna

Sé específico y usa los datos de la encuesta."""


def calcular_metricas_basicas(encuesta):
    """Calcula métricas clave sin IA."""
    total = encuesta["total_encuestados"]
    uso = encuesta["pregunta_3_uso_actual"]["respuestas"]
    actitud = encuesta["pregunta_1_actitud_general"]["respuestas"]

    pct_usuarios_activos = round((uso["si_diariamente"] + uso["si_semanalmente"]) / total * 100, 1)
    pct_alguna_vez = round((uso["si_diariamente"] + uso["si_semanalmente"] + uso["si_ocasionalmente"]) / total * 100, 1)
    pct_nunca = round(uso["no_nunca"] / total * 100, 1)
    pct_positivos = round((actitud["muy_positiva"] + actitud["positiva"]) / total * 100, 1)
    pct_negativos = round((actitud["negativa"] + actitud["muy_negativa"]) / total * 100, 1)

    barreras = encuesta["pregunta_2_barreras"]["respuestas"]
    top_barrera = max(barreras, key=lambda x: barreras[x])

    return {
        "usuarios_activos_pct": pct_usuarios_activos,
        "alguna_vez_pct": pct_alguna_vez,
        "nunca_pct": pct_nunca,
        "actitud_positiva_pct": pct_positivos,
        "actitud_negativa_pct": pct_negativos,
        "principal_barrera": top_barrera,
    }


def ejercicio_1_diagnostico(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 1 — DIAGNÓSTICO DE BARRERAS DE ADOPCIÓN")
    print("=" * 64)

    metricas = calcular_metricas_basicas(RESULTADOS_ENCUESTA)

    print(f"\n  Total encuestados: {RESULTADOS_ENCUESTA['total_encuestados']}")
    print(f"\n  MÉTRICAS CLAVE:")
    print(f"  Usuarios activos (diario+semanal):  {metricas['usuarios_activos_pct']}%")
    print(f"  Han usado alguna vez:               {metricas['alguna_vez_pct']}%")
    print(f"  Nunca han usado IA:                 {metricas['nunca_pct']}%")
    print(f"  Actitud positiva/muy positiva:      {metricas['actitud_positiva_pct']}%")
    print(f"  Actitud negativa/muy negativa:      {metricas['actitud_negativa_pct']}%")
    print(f"  Principal barrera: {metricas['principal_barrera'].replace('_', ' ')}")

    print(f"\n  TOP CASOS DE USO DESEADOS:")
    casos = RESULTADOS_ENCUESTA["pregunta_4_casos_uso_deseados"]["respuestas"]
    for caso, votos in sorted(casos.items(), key=lambda x: -x[1])[:4]:
        barra = "█" * (votos // 10) + "░" * (8 - votos // 10)
        print(f"  {caso.replace('_', ' '):<30} {barra} {votos}/{RESULTADOS_ENCUESTA['total_encuestados']}")

    if tiene_api:
        prompt = PROMPT_ANALIZAR_ENCUESTA.format(
            resultados=json.dumps(RESULTADOS_ENCUESTA, ensure_ascii=False, indent=2)
        )
        diagnostico = llamar_api(prompt, max_tokens=700)
        print("\n  DIAGNÓSTICO EJECUTIVO (IA):")
        print("  " + "─" * 50)
        for linea in diagnostico.split("\n"):
            print(f"  {linea}")
    else:
        print("\n  DIAGNÓSTICO BÁSICO (reglas):")
        print()
        if metricas["nunca_pct"] > 40:
            print("  ⚠ ALERTA: Más del 40% nunca ha usado IA — adopción crítica")
        if metricas["actitud_negativa_pct"] > 20:
            print("  ⚠ Resistencia significativa — comunicación prioritaria")
        print()
        print("  RECOMENDACIONES INMEDIATAS:")
        print("  1. Formación práctica urgente — la falta de formación es la barrera #1")
        print("  2. Comunicar política de privacidad para reducir preocupación sobre datos")
        print("  3. El manager debe usar IA públicamente para modelar el comportamiento")
        print()
        print("  [Configura ANTHROPIC_API_KEY para diagnóstico completo con IA]")


# ─── EJERCICIO 2: SIMULADOR DE CONVERSACIONES DIFÍCILES ──────────────────────

ESCENARIOS_DIFICILES = [
    {
        "id": "E-01",
        "perfil_empleado": "Operario de almacén, 52 años, 20 años en la empresa",
        "objecion": "Con esto de la IA, ¿cuánto tiempo nos queda aquí? He leído que van a automatizar todos los almacenes.",
        "contexto": "En una sesión de formación grupal, delante de 15 compañeros",
    },
    {
        "id": "E-02",
        "perfil_empleado": "Administrativo contable, 38 años, perfil analítico",
        "objecion": "Probé el sistema de IA para generar el informe financiero y cometió 3 errores graves. No me fío para nada de esta tecnología.",
        "contexto": "Reunión 1:1 con el AI Champion del departamento",
    },
    {
        "id": "E-03",
        "perfil_empleado": "Directora de RRHH, 45 años, muy respetada en la empresa",
        "objecion": "Me preocupa que si usamos IA para selección de candidatos, estemos discriminando sin darnos cuenta. He leído casos muy preocupantes.",
        "contexto": "Reunión con el equipo directivo",
    },
]

SYSTEM_AI_CHAMPION = """Eres un AI Champion experto en gestión del cambio tecnológico.
Tu rol es responder a objeciones y miedos sobre IA de forma empática, honesta y práctica.

Principios de respuesta:
- Primero valida el sentimiento, no lo desestimes
- Sé honesto sobre las limitaciones reales de la IA
- Usa ejemplos concretos y locales (del sector, de la empresa)
- No hagas promesas que no puedes garantizar
- Propón siempre un siguiente paso concreto

Nunca digas:
- "La IA nunca quita trabajos" (es impreciso y los empleados no lo creen)
- "No te preocupes" sin dar razones concretas
- "Es muy fácil de usar" (minimiza la experiencia del empleado)"""

PROMPT_RESPUESTA_AI_CHAMPION = """Escenario de conversación para AI Champion:

Perfil del empleado: {perfil}
Contexto: {contexto}
Objeción o comentario: "{objecion}"

Genera la respuesta ideal del AI Champion. Incluye:
1. VALIDACIÓN (1-2 frases de reconocimiento genuino)
2. RESPUESTA HONESTA (aborda el fondo de la preocupación con honestidad)
3. REDIRECCION POSITIVA (muestra el camino posible)
4. SIGUIENTE PASO (1 acción concreta propuesta)

Extensión: 150-200 palabras. Tono: cercano, profesional, honesto."""


def ejercicio_2_simulador_conversaciones(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 2 — SIMULADOR DE CONVERSACIONES DIFÍCILES (AI Champion)")
    print("=" * 64)

    for escenario in ESCENARIOS_DIFICILES:
        print(f"\n  [{escenario['id']}] {escenario['perfil_empleado']}")
        print(f"  Contexto: {escenario['contexto']}")
        print(f"  Objeción: \"{escenario['objecion'][:70]}...\"")

        if tiene_api:
            prompt = PROMPT_RESPUESTA_AI_CHAMPION.format(**escenario)
            respuesta = llamar_api(prompt, system=SYSTEM_AI_CHAMPION, max_tokens=350)
            print(f"\n  RESPUESTA DEL AI CHAMPION:")
            print("  " + "─" * 45)
            for linea in respuesta.split("\n"):
                print(f"  {linea}")
        else:
            # Fallback: respuestas plantilla por tipo de objeción
            objecion = escenario["objecion"].lower()
            if "quita" in objecion or "automati" in objecion or "queda" in objecion:
                print("\n  RESPUESTA (plantilla):")
                print("  Entiendo perfectamente ese miedo — es una preocupación legítima que")
                print("  muchos compañeros comparten. Lo que hemos visto en nuestra empresa")
                print("  es que la IA libera tiempo de las tareas más repetitivas para que")
                print("  nos centremos en lo que realmente requiere nuestra experiencia.")
                print("  → Siguiente paso: ¿Te apetece que veamos juntos qué partes de tu")
                print("    trabajo podrías automatizar y cuáles no?")
            elif "error" in objecion or "fío" in objecion:
                print("\n  RESPUESTA (plantilla):")
                print("  Tienes toda la razón — esos errores son reales y es importante que")
                print("  los hayas detectado. La IA comete errores, como cualquier herramienta.")
                print("  El cambio está en saber cuándo verificar y cómo. Con un buen prompt")
                print("  y el proceso de validación correcto, los errores se reducen mucho.")
                print("  → Siguiente paso: ¿Me enseñas el caso concreto? Aprendemos juntos.")
            else:
                print("\n  RESPUESTA (plantilla):")
                print("  Es una preocupación muy válida y es importante abordarla antes de seguir.")
                print("  Las mejores decisiones sobre IA se toman con información real, no solo")
                print("  con lo que leemos en prensa. Propongo que revisemos el caso concreto.")
                print("  → Siguiente paso: Organizar una sesión de análisis de riesgo real.")
            print("  [Configura ANTHROPIC_API_KEY para respuestas personalizadas con IA]")


# ─── EJERCICIO 3: GENERADOR DE PLAN DE ADOPCIÓN ──────────────────────────────

PERFIL_EMPRESA_ADOPCION = {
    "nombre": "Logística Express S.L.",
    "sector": "Transporte y logística",
    "empleados": 180,
    "estructura": "60% operarios de almacén, 25% administrativos, 10% comerciales, 5% dirección",
    "nivel_digital_actual": "Medio-bajo — usan ERP básico y Office. Poca cultura digital.",
    "resistencia_detectada": "Alta en operarios (miedo a automatización). Media en administración.",
    "budget_formacion": "Limitado — máx 15h de formación remunerada por empleado este año",
    "casos_uso_prioritarios": [
        "Automatización de emails de seguimiento de envíos",
        "Generación de documentación de entrega",
        "Análisis de incidencias recurrentes",
    ],
    "plazo_objetivo": "Adopción activa del 60% en 6 meses",
    "restricciones": [
        "No se puede contratar personal adicional de IT",
        "Las operaciones no pueden parar para formación larga",
        "Alta rotación en operarios (30% anual)",
    ],
}

PROMPT_PLAN_ADOPCION = """Eres un consultor de gestión del cambio especializado en adopción de IA en pymes.
Genera un plan de adopción de IA personalizado y realista para esta empresa.

Perfil de la empresa:
{perfil}

El plan debe incluir:
1. EVALUACIÓN DE PUNTO DE PARTIDA (1 párrafo)
2. ESTRATEGIA GENERAL (enfoque recomendado dado el contexto)
3. PLAN POR FASES (4 fases con duración, objetivos y actividades clave)
4. PROGRAMA DE AI CHAMPIONS (cómo seleccionarlos en este contexto)
5. MÉTRICAS DE SEGUIMIENTO (3-4 KPIs específicos para este sector)
6. RIESGOS PRINCIPALES Y MITIGACIÓN
7. QUICK WINS (2-3 victorias rápidas en las primeras 4 semanas)

Sé realista con las restricciones indicadas. Extensión máxima: 500 palabras."""


def ejercicio_3_plan_adopcion(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 3 — GENERADOR DE PLAN DE ADOPCIÓN IA")
    print("=" * 64)

    print(f"\n  Empresa: {PERFIL_EMPRESA_ADOPCION['nombre']}")
    print(f"  Sector: {PERFIL_EMPRESA_ADOPCION['sector']}")
    print(f"  Empleados: {PERFIL_EMPRESA_ADOPCION['empleados']}")
    print(f"  Objetivo: {PERFIL_EMPRESA_ADOPCION['plazo_objetivo']}")
    print(f"  Restricciones: {'; '.join(PERFIL_EMPRESA_ADOPCION['restricciones'][:2])}")

    if tiene_api:
        prompt = PROMPT_PLAN_ADOPCION.format(
            perfil=json.dumps(PERFIL_EMPRESA_ADOPCION, ensure_ascii=False, indent=2)
        )
        plan = llamar_api(prompt, max_tokens=800)
        print("\n  PLAN DE ADOPCIÓN PERSONALIZADO:")
        print("  " + "=" * 55)
        for linea in plan.split("\n"):
            print(f"  {linea}")
    else:
        print("\n  PLAN DE ADOPCIÓN (plantilla sector logística):")
        print("  " + "=" * 55)
        print("""
  ESTRATEGIA: Adopción por capas — empezar por administrativos
  (más fácil, mayor impacto visible) y expandir a operarios con
  casos de uso muy específicos (documentación, no decisiones).

  FASE 1 — QUICK WINS (semanas 1-4):
    → Automatizar emails de confirmación de entrega (1 semana)
    → Nominar 2 AI Champions: 1 en admin, 1 en comercial
    → Comunicación del CEO: "la IA nos ayuda a ser más competitivos"

  FASE 2 — PILOTO (semanas 5-12):
    → 15-20 voluntarios: admin + comerciales
    → Formación en bloques de 2h (adaptar a turnos de operarios)
    → Medir: tiempo ahorrado en documentación de entrega

  FASE 3 — EXPANSIÓN (meses 3-6):
    → Champions forman a sus equipos en formato "café de 30 min"
    → Integrar IA en el flujo de registro de incidencias
    → Dashboard de uso visible en pantallas del almacén

  KPIs CLAVE:
    → % empleados que usan IA mínimo 1x/semana
    → Tiempo medio de generación de documentación (antes vs. después)
    → Incidencias de envío mal documentadas (objetivo -20%)

  RIESGO PRINCIPAL: Alta rotación de operarios — solución: crear
  material de onboarding de IA de 30 minutos para nuevos empleados.""")
        print()
        print("  [Configura ANTHROPIC_API_KEY para plan personalizado con IA]")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 64)
    print("LAB 9.3 — FRICCIÓN TECNOLÓGICA Y GESTIÓN DEL CAMBIO")
    print("=" * 64)

    tiene_api = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if tiene_api:
        print(f"  Modelo: {MODELO}")
        print("  Modo: API activa")
    else:
        print("  AVISO: ANTHROPIC_API_KEY no configurada.")
        print("  Modo: Análisis con reglas y plantillas de referencia")

    ejercicio_1_diagnostico(tiene_api)
    ejercicio_2_simulador_conversaciones(tiene_api)
    ejercicio_3_plan_adopcion(tiene_api)

    print("\n" + "=" * 64)
    print("RESUMEN DEL LAB")
    print("=" * 64)
    print("""
  Herramientas construidas:
  ✓ Diagnóstico de actitud y barreras de adopción
  ✓ Simulador de respuestas para AI Champions
  ✓ Generador de plan de adopción adaptado a la empresa

  Los 3 factores que más predicen el éxito de adopción:
    1. El manager directo usa la IA (modelado del comportamiento)
    2. La formación es práctica y en el contexto real del trabajo
    3. Hay una victoria rápida visible en las primeras 2-3 semanas

  El mayor error en gestión del cambio IA:
    Tratar la resistencia como un problema de comunicación
    cuando en realidad es un problema de experiencia.
    La gente adopta cuando lo intenta y funciona,
    no cuando les convencemos con argumentos.
""")

    print("[FIN DEL LAB 9.3]")
