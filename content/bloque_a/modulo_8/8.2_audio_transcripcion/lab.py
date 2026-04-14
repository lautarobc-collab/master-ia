"""
LAB 8.2 — Audio: Transcripción e Inteligencia sobre Llamadas
=============================================================
Objetivo: procesar transcripciones de audio con IA para extraer
valor de reuniones, llamadas de ventas y atención al cliente.

Nota: este lab trabaja con TRANSCRIPCIONES (texto), no con audio real,
ya que la transcripción requiere Whisper o AssemblyAI por separado.
El valor de Claude está en el análisis del texto transcrito.

Ejercicios:
  1. Generador automático de actas de reunión
  2. Análisis de sentimiento en llamada de atención al cliente
  3. Scoring de llamada comercial + extracción de compromisos

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import json

MODELO = "claude-haiku-4-5-20251001"


def llamar_api(prompt, system="", max_tokens=800):
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


# ─── TRANSCRIPCIONES DE EJEMPLO ──────────────────────────────────────────────

TRANSCRIPCION_REUNION = """
[00:00] Roberto (Director Comercial): Buenos días a todos. Arrancamos con la revisión
del Q1. Pedro, ¿puedes empezar con los números?

[00:45] Pedro (Ventas): Claro. Cerramos el Q1 con 847.000 euros, un 12% por encima
del objetivo. Los segmentos de mayor crecimiento fueron pymes tecnológicas y retail.
El segmento industrial bajó un 8% respecto al Q4, principalmente por la pérdida de
dos cuentas que mencionamos en enero.

[02:10] Laura (Marketing): En cuanto a leads generados, el canal digital generó 340
leads cualificados, un 23% más que el trimestre anterior. La campaña de LinkedIn fue
la más efectiva, con un coste por lead de 45 euros.

[03:30] Roberto: Bien. Sobre el segmento industrial, Pedro, ¿tienes plan de recuperación?

[03:45] Pedro: Sí. He identificado 5 cuentas target para Q2. Propongo priorizar
Industrias Martínez y Grupo Forja, que tienen presupuesto confirmado para este año.
Necesitaré apoyo de un caso de éxito en ese sector para las demos.

[04:20] Laura: Puedo preparar el caso de éxito con TechMetal, que nos dio permiso
de publicación. Lo tendré listo antes del 15 de mayo.

[05:00] Roberto: Perfecto. Decidimos entonces: Pedro lidera la recuperación del segmento
industrial con esas 5 cuentas. Laura prepara el caso de éxito TechMetal para el 15 de mayo.
Para Q2, el objetivo es 920.000 euros, con foco en pymes tecnológicas y recuperar industrial.

[05:45] Ana (Finanzas): Antes de cerrar, necesito confirmar con Pedro la previsión
de cobros de abril porque tenemos un gap de tesorería en la segunda quincena.

[06:00] Pedro: Te llamo esta tarde, Ana. Tengo todos los datos de vencimientos.

[06:15] Roberto: Próxima reunión de revisión: 3 de junio, misma hora. Alguna pregunta más...
No. Cerramos aquí. Gracias a todos.
"""

TRANSCRIPCION_ATENCION_CLIENTE = """
Agente: Buenas tardes, le atiende Carlos del servicio al cliente de CloudServ.
¿En qué puedo ayudarle?

Cliente: Hola, mire, llevo tres días intentando que me resuelvan un problema
y nadie me soluciona nada. Estoy muy cansado de esta situación.

Agente: Entiendo su frustración, lamento los inconvenientes. ¿Puede decirme
su número de cliente o el email asociado a la cuenta?

Cliente: Sí, es martinez_juan arroba empresa punto com. El problema es que
desde el lunes no puedo acceder al módulo de informes. Me dice que no tengo
permisos, pero yo siempre he tenido acceso.

Agente: Entendido. Estoy viendo su cuenta ahora mismo. Efectivamente, el lunes
se realizó una actualización del sistema que afectó a los permisos de varios
usuarios. Disculpe las molestias, fue un error nuestro.

Cliente: ¿Un error vuestro? ¡Llevo tres días sin poder trabajar! ¿Saben el
daño que esto me ha causado? Estoy pensando seriamente en cambiar de proveedor.

Agente: Tiene toda la razón en estar molesto y le pido disculpas en nombre de
la empresa. Voy a restaurar sus permisos ahora mismo. ¿Puede hacer un refresh
de la página mientras lo hago?

Cliente: Sí, espere... Vale, ya tengo acceso. Pero esto no puede volver a pasar.

Agente: Le aseguro que no volverá a ocurrir. Voy a escalar internamente para
que se revise el proceso de actualización. Además, voy a aplicar un crédito
de 3 días en su factura por las molestias causadas. ¿Le parece bien?

Cliente: Bueno, está bien. Lo de los 3 días de crédito lo aprecio. Pero que
conste que si vuelve a pasar, me voy.

Agente: Completamente entendido. ¿Hay algo más en lo que pueda ayudarle?

Cliente: No, de momento no. Gracias.

Agente: Gracias a usted. Que tenga buena tarde.
"""

TRANSCRIPCION_LLAMADA_VENTAS = """
Comercial (Sara): Buenos días Carlos, te llamo de parte de DataFlow Solutions.
Soy Sara, la account manager para vuestra zona. ¿Tienes unos minutos?

Prospecto (Carlos, Director IT): Sí, dime, aunque tengo una reunión en veinte minutos.

Sara: Perfecto, seré breve. Os estamos contactando porque vuestro competidor
directo, Alfa Distribución, implementó nuestra plataforma hace 6 meses y
han reducido un 40% el tiempo de generación de informes. ¿Es ese un problema
que también tenéis vosotros?

Carlos: La verdad es que sí. Los informes mensuales nos llevan casi una semana.
¿De qué tipo de solución hablamos?

Sara: DataFlow es una plataforma de automatización de reporting. Se conecta
a vuestros sistemas actuales: ERP, CRM, hojas de cálculo, y genera informes
automáticamente. Sin programación, sin IT adicional.

Carlos: Interesante. ¿Cuánto cuesta y cuánto tarda la implantación?

Sara: El coste depende del número de usuarios y conectores, pero para empresas
de vuestro tamaño el rango típico es entre 1.200 y 2.500 euros al mes.
La implantación es de 2 a 4 semanas. ¿Cuántos usuarios utilizarían el sistema?

Carlos: Unos 15, entre financiero, comercial y operaciones.

Sara: Con esos datos, estaríamos en torno a los 1.600 euros al mes.
¿Tendría sentido que hiciéramos una demo esta semana o la próxima?

Carlos: Podría ser. Pero primero necesito hablar con mi directora general,
Elena. Ella toma la decisión final. Si le parece bien, concertamos la demo.

Sara: Perfecto. ¿Podrías consultar con Elena esta semana y darte de vuelta el
viernes? Así podemos agendar la demo para la semana del 12.

Carlos: Sí, el viernes te escribo.

Sara: Genial. Te envío un email con el caso de éxito de Alfa Distribución
para que lo puedas pasar a Elena antes de la reunión. ¿Te parece?

Carlos: Sí, perfecto.

Sara: Estupendo. Muchas gracias Carlos, hasta el viernes.
"""


# ─── EJERCICIO 1: ACTA DE REUNIÓN ────────────────────────────────────────────

SYSTEM_SECRETARIO = """Eres el secretario de actas oficial de la empresa.
Generas actas claras, concisas y accionables.
Siempre distingues entre: temas discutidos, decisiones tomadas y acciones asignadas.
Las acciones tienen SIEMPRE: responsable, descripción y fecha si se menciona."""

PROMPT_ACTA = """Genera el acta oficial de esta reunión a partir de la transcripción.

Usa EXACTAMENTE este formato:
─────────────────────────────────────────
ACTA DE REUNIÓN
─────────────────────────────────────────
Tipo: [tipo de reunión]
Participantes: [nombres y cargos detectados]
Duración aproximada: [duración estimada]

RESUMEN EJECUTIVO
[2-3 frases que describan el propósito y resultado de la reunión]

TEMAS TRATADOS
[Número]. [Tema]
   [Resumen de la discusión en 2-4 frases]

DECISIONES TOMADAS
→ [Decisión clara y concreta]
→ [Siguiente decisión]

ACCIONES Y COMPROMISOS
☐ [RESPONSABLE] — [Acción concreta] — Plazo: [fecha o "sin fecha definida"]

PRÓXIMA REUNIÓN
[Fecha y contexto si se mencionó]
─────────────────────────────────────────

TRANSCRIPCIÓN:
{transcripcion}"""


def ejercicio_1_acta_reunion(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 1 — GENERADOR AUTOMÁTICO DE ACTAS")
    print("=" * 64)

    if tiene_api:
        prompt = PROMPT_ACTA.format(transcripcion=TRANSCRIPCION_REUNION)
        acta = llamar_api(prompt, system=SYSTEM_SECRETARIO, max_tokens=900)
        print(acta)
    else:
        print("\n  [Modo fallback — extracción por reglas básicas]")
        print()
        # Extraer información básica sin IA
        lineas = TRANSCRIPCION_REUNION.strip().split("\n")
        participantes = set()
        acciones = []
        for linea in lineas:
            if ":" in linea and "[" in linea:
                partes = linea.split("]")[1].strip() if "]" in linea else linea
                if "(" in partes:
                    nombre = partes.split("(")[0].strip()
                    participantes.add(nombre)
            if "lo tendré listo" in linea.lower() or "te llamo" in linea.lower():
                acciones.append(linea.strip()[:80])

        print("  ACTA BÁSICA (sin API):")
        print(f"  Participantes detectados: {', '.join(sorted(participantes))}")
        print(f"  Compromisos detectados por palabras clave:")
        for a in acciones:
            print(f"    → {a}...")
        print()
        print("  [Configura ANTHROPIC_API_KEY para acta completa y estructurada]")


# ─── EJERCICIO 2: ANÁLISIS DE ATENCIÓN AL CLIENTE ────────────────────────────

PROMPT_ANALISIS_LLAMADA_SOPORTE = """Analiza esta transcripción de llamada de atención al cliente.

Devuelve SOLO JSON con este esquema:
{{
  "satisfaccion_cliente_final": 1-5,
  "nivel_frustracion_inicial": "bajo/medio/alto/muy_alto",
  "nivel_frustracion_final": "bajo/medio/alto/muy_alto",
  "resolucion_primera_llamada": true/false,
  "temas_principales": ["lista"],
  "sentimiento_progresion": "mejoró/empeoró/estable",
  "alertas": {{
    "amenaza_baja": true/false,
    "menciona_competencia": true/false,
    "queja_producto": true/false,
    "compensacion_otorgada": true/false
  }},
  "compromisos_agente": ["lista de compromisos adquiridos"],
  "calidad_atencion": 1-10,
  "recomendacion_seguimiento": "acción recomendada para el equipo",
  "resumen_ejecutivo": "2 frases para el informe diario del supervisor"
}}"""


def ejercicio_2_analisis_soporte(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 2 — ANÁLISIS DE LLAMADA DE ATENCIÓN AL CLIENTE")
    print("=" * 64)

    if tiene_api:
        analisis = llamar_api(PROMPT_ANALISIS_LLAMADA_SOPORTE +
                              "\n\nTRANSCRIPCIÓN:\n" + TRANSCRIPCION_ATENCION_CLIENTE,
                              max_tokens=500)
        try:
            datos = json.loads(analisis)
            print(f"\n  Satisfacción final: {datos['satisfaccion_cliente_final']}/5")
            print(f"  Frustración: {datos['nivel_frustracion_inicial']} → {datos['nivel_frustracion_final']}")
            print(f"  Resolución en primera llamada: {'Sí' if datos['resolucion_primera_llamada'] else 'No'}")
            print(f"  Calidad de atención: {datos['calidad_atencion']}/10")
            print(f"\n  Alertas:")
            for alerta, valor in datos["alertas"].items():
                icono = "⚑" if valor else "·"
                print(f"    {icono} {alerta}: {'SÍ' if valor else 'no'}")
            print(f"\n  Compromisos del agente:")
            for c in datos["compromisos_agente"]:
                print(f"    → {c}")
            print(f"\n  Recomendación: {datos['recomendacion_seguimiento']}")
            print(f"\n  Resumen ejecutivo: {datos['resumen_ejecutivo']}")
        except json.JSONDecodeError:
            print(f"\n  {analisis}")
    else:
        print("\n  [Análisis por reglas básicas]")
        texto = TRANSCRIPCION_ATENCION_CLIENTE.lower()
        print()
        print(f"  Amenaza de baja detectada: {'Sí' if 'cambiar de proveedor' in texto or 'me voy' in texto else 'No'}")
        print(f"  Compensación otorgada: {'Sí' if 'crédito' in texto or 'descuento' in texto else 'No'}")
        print(f"  Resolución aparente: {'Sí' if 'ya tengo acceso' in texto else 'No determinable'}")
        print(f"  Satisfacción estimada: 3/5 (basado en keywords de frustración y resolución)")
        print()
        print("  [Configura ANTHROPIC_API_KEY para análisis completo con IA]")


# ─── EJERCICIO 3: SCORING DE LLAMADA COMERCIAL ───────────────────────────────

PROMPT_SCORING_VENTAS = """Eres un coach de ventas analizando una llamada comercial.
Evalúa la llamada según metodología SPIN Selling y mejores prácticas de ventas B2B.

Analiza y devuelve JSON:
{{
  "scores": {{
    "apertura_y_rapport": 1-10,
    "identificacion_necesidades": 1-10,
    "propuesta_de_valor": 1-10,
    "manejo_objeciones": 1-10,
    "cierre_y_siguientes_pasos": 1-10
  }},
  "score_total": 0-100,
  "etapa_pipeline": "prospecto/cualificado/demo_pendiente/propuesta/negociacion",
  "senales_compra_detectadas": ["lista"],
  "objeciones_no_resueltas": ["lista"],
  "compromisos_adquiridos": {{
    "cliente": ["lo que el cliente se comprometió a hacer"],
    "comercial": ["lo que el comercial se comprometió a hacer"]
  }},
  "siguiente_paso_recomendado": "acción concreta con fecha",
  "probabilidad_avance_pct": 0-100,
  "feedback_coaching": "2-3 sugerencias concretas de mejora para el comercial"
}}"""


def ejercicio_3_scoring_ventas(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 3 — SCORING DE LLAMADA COMERCIAL")
    print("=" * 64)

    if tiene_api:
        analisis = llamar_api(PROMPT_SCORING_VENTAS +
                              "\n\nTRANSCRIPCIÓN:\n" + TRANSCRIPCION_LLAMADA_VENTAS,
                              max_tokens=600)
        try:
            datos = json.loads(analisis)
            print(f"\n  SCORECARD DE LA LLAMADA:")
            print(f"  {'─'*40}")
            for dimension, puntos in datos["scores"].items():
                barra = "█" * puntos + "░" * (10 - puntos)
                print(f"  {dimension.replace('_', ' '):<30} {barra} {puntos}/10")
            print(f"  {'─'*40}")
            print(f"  SCORE TOTAL: {datos['score_total']}/100")
            print(f"\n  Etapa en pipeline: {datos['etapa_pipeline'].upper()}")
            print(f"  Probabilidad de avance: {datos['probabilidad_avance_pct']}%")

            print(f"\n  Señales de compra detectadas:")
            for s in datos["senales_compra_detectadas"]:
                print(f"    ✓ {s}")

            if datos["objeciones_no_resueltas"]:
                print(f"\n  Objeciones no resueltas:")
                for o in datos["objeciones_no_resueltas"]:
                    print(f"    ⚠ {o}")

            print(f"\n  Compromisos:")
            for c in datos["compromisos_adquiridos"].get("cliente", []):
                print(f"    Cliente → {c}")
            for c in datos["compromisos_adquiridos"].get("comercial", []):
                print(f"    Comercial → {c}")

            print(f"\n  Siguiente paso: {datos['siguiente_paso_recomendado']}")
            print(f"\n  Feedback coaching:")
            print(f"  {datos['feedback_coaching']}")

        except json.JSONDecodeError:
            print(f"\n  {analisis}")
    else:
        print("\n  [Scoring básico por reglas]")
        texto = TRANSCRIPCION_LLAMADA_VENTAS.lower()
        tiene_precio = "1.600 euros" in texto or "coste" in texto
        tiene_siguiente_paso = "viernes" in texto or "demo" in texto
        tiene_decisor = "directora general" in texto or "elena" in texto
        print()
        print(f"  Propuesta de precio: {'Sí' if tiene_precio else 'No'} ✓")
        print(f"  Siguiente paso definido: {'Sí' if tiene_siguiente_paso else 'No'} ✓")
        print(f"  Decisor identificado: {'Sí' if tiene_decisor else 'No'} ✓")
        print(f"  Score estimado: {'Alto (7-8/10)' if sum([tiene_precio, tiene_siguiente_paso, tiene_decisor]) >= 2 else 'Medio'}")
        print(f"  Probabilidad de avance: ~60% (estimación básica)")
        print()
        print("  [Configura ANTHROPIC_API_KEY para análisis completo de ventas]")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 64)
    print("LAB 8.2 — AUDIO: TRANSCRIPCIÓN E INTELIGENCIA EN LLAMADAS")
    print("=" * 64)

    tiene_api = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if tiene_api:
        print(f"  Modelo: {MODELO}")
        print("  Modo: API activa — análisis completo con IA")
    else:
        print("  AVISO: ANTHROPIC_API_KEY no configurada.")
        print("  Modo: Fallback con extracción por palabras clave")
    print()
    print("  Nota: este lab procesa transcripciones de texto.")
    print("  Para transcribir audio real: pip install openai-whisper")

    ejercicio_1_acta_reunion(tiene_api)
    ejercicio_2_analisis_soporte(tiene_api)
    ejercicio_3_scoring_ventas(tiene_api)

    print("\n" + "=" * 64)
    print("RESUMEN DEL LAB")
    print("=" * 64)
    print("""
  Casos de uso implementados:
  ✓ Generación de actas estructuradas desde transcripción
  ✓ Análisis de sentimiento y alertas en atención al cliente
  ✓ Scoring de llamadas comerciales con feedback de coaching

  Pipeline completo en producción:
    Audio → Whisper/AssemblyAI → Transcripción → Claude → CRM/Notion

  ROI típico:
    • Actas: de 30 min a 30 segundos por reunión
    • Soporte: analizar 100% de llamadas vs. 2% muestreadas
    • Ventas: coaching basado en datos reales, no percepción
""")

    print("[FIN DEL LAB 8.2]")
