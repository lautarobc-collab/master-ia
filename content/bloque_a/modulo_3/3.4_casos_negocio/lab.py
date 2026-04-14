"""
LAB 3.4 — Casos de Negocio: Automatización Documental a Escala
================================================================
Ejercicios prácticos para construir un pipeline de generación
y validación de documentos ejecutivos con Claude.

Requisito: ANTHROPIC_API_KEY en variables de entorno
  export ANTHROPIC_API_KEY="sk-ant-..."
"""

import os
import json
import re
from datetime import date

# ── Cliente Anthropic ────────────────────────────────────────────────────────
try:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    API_DISPONIBLE = True
except Exception:
    client = None
    API_DISPONIBLE = False

MODEL = "claude-haiku-4-5-20251001"

def llamar_claude(system: str, user: str, max_tokens: int = 1000, temperature: float = 0.3) -> str:
    if not API_DISPONIBLE:
        return "[DEMO] API no disponible — configura ANTHROPIC_API_KEY para ejecutar este ejercicio."
    msg = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system,
        messages=[{"role": "user", "content": user}]
    )
    return msg.content[0].text


# ════════════════════════════════════════════════════════════════════════════
# EJERCICIO 1 — Generador de resumen ejecutivo semanal
# ════════════════════════════════════════════════════════════════════════════

def ejercicio_1_resumen_ejecutivo():
    """
    Genera el resumen ejecutivo de un informe semanal a partir
    de datos de KPIs estructurados.
    Objetivo: salida JSON con resumen, desviaciones y acciones.
    """
    print("\n" + "═"*60)
    print("EJERCICIO 1 — Resumen ejecutivo semanal")
    print("═"*60)

    # Datos de ejemplo — en producción vendrían del ERP/CRM
    datos_kpis = {
        "semana": "14 abril 2026",
        "ventas": {"actual": 284000, "objetivo": 310000, "anterior": 295000, "unidad": "EUR"},
        "margen": {"actual": 38.2, "objetivo": 40.0, "anterior": 39.1, "unidad": "%"},
        "leads_nuevos": {"actual": 47, "objetivo": 50, "anterior": 41},
        "tasa_conversion": {"actual": 22.3, "objetivo": 25.0, "anterior": 24.1, "unidad": "%"},
        "incidencias_abiertas": {"actual": 12, "anterior": 8, "sla_maximo": 15},
        "nps": {"actual": 71, "anterior": 68},
    }

    system = """Eres un analista senior experto en comunicación ejecutiva.
Generas narrativa de negocio clara, directa y sin relleno.
Nunca repites todos los números — seleccionas y explicas los más relevantes.
Tono: profesional y directo. El resumen no puede superar 150 palabras."""

    user = f"""Analiza estos KPIs semanales y genera un informe ejecutivo estructurado.

DATOS:
{json.dumps(datos_kpis, ensure_ascii=False, indent=2)}

Genera un JSON con exactamente estas claves:
{{
  "resumen": "párrafo de máximo 150 palabras con los 3 datos más relevantes",
  "tendencia": "positiva | neutral | alerta",
  "desviaciones": [
    {{"kpi": "nombre", "valor_actual": X, "objetivo": Y, "variacion_pct": Z, "hipotesis": "..."}}
  ],
  "acciones": [
    {{"kpi": "nombre", "accion": "...", "responsable_sugerido": "..."}}
  ]
}}

Solo devuelve el JSON, sin texto adicional."""

    respuesta = llamar_claude(system, user, max_tokens=800)
    print(f"\nDatos de entrada:\n{json.dumps(datos_kpis, ensure_ascii=False, indent=2)}")
    print(f"\nInforme ejecutivo generado:\n{respuesta}")

    # Intento de parseo para demostrar uso programático
    try:
        informe = json.loads(respuesta)
        print(f"\n✓ JSON válido — Tendencia: {informe.get('tendencia', 'N/A')}")
        print(f"  Desviaciones detectadas: {len(informe.get('desviaciones', []))}")
        print(f"  Acciones propuestas: {len(informe.get('acciones', []))}")
    except json.JSONDecodeError:
        print("\n⚠ Respuesta no es JSON puro — revisar el prompt o parsear manualmente")


# ════════════════════════════════════════════════════════════════════════════
# EJERCICIO 2 — Generación de propuesta comercial personalizada
# ════════════════════════════════════════════════════════════════════════════

def ejercicio_2_propuesta_comercial():
    """
    Genera una propuesta comercial personalizada para un cliente
    a partir de sus datos en el CRM.
    Demuestra la generación a escala con datos variables.
    """
    print("\n" + "═"*60)
    print("EJERCICIO 2 — Propuesta comercial personalizada")
    print("═"*60)

    # Simula datos de CRM para 3 clientes distintos
    clientes = [
        {
            "nombre": "Carlos Martínez",
            "empresa": "Grupo Logística Sur S.L.",
            "sector": "logística y distribución",
            "empleados": 85,
            "dolor_principal": "gestión manual de albaranes y seguimiento de rutas",
            "presupuesto_estimado": "15.000-25.000 EUR/año",
            "contexto": "Reunión inicial positiva, CTO interesado en automatización",
        },
        {
            "nombre": "Ana Puig",
            "empresa": "Clínica Dental Puig & Asociados",
            "sector": "salud dental",
            "empleados": 22,
            "dolor_principal": "gestión de citas, recordatorios y comunicación con pacientes",
            "presupuesto_estimado": "5.000-8.000 EUR/año",
            "contexto": "Referida por cliente actual, busca solución rápida de implementar",
        },
    ]

    system = """Eres un consultor comercial experto en soluciones de IA empresarial.
Redactas propuestas personalizadas, directas y orientadas al valor para el cliente.
Nunca uses jerga técnica innecesaria. Habla el idioma del negocio del cliente.
Longitud máxima: 300 palabras por propuesta."""

    for cliente in clientes:
        print(f"\n{'─'*50}")
        print(f"Generando propuesta para: {cliente['empresa']}")
        print(f"{'─'*50}")

        user = f"""Genera una propuesta comercial personalizada para este cliente.

DATOS DEL CLIENTE:
{json.dumps(cliente, ensure_ascii=False, indent=2)}

La propuesta debe incluir:
1. Párrafo de apertura personalizado (menciona su empresa y dolor específico)
2. Solución propuesta (3 bullets concretos adaptados a su sector)
3. Beneficio esperado cuantificado (ahorro de tiempo o costes estimado)
4. Siguiente paso propuesto (llamada, demo, prueba piloto)

Tono: profesional pero cercano. Máximo 300 palabras."""

        propuesta = llamar_claude(system, user, max_tokens=500, temperature=0.4)
        print(propuesta)


# ════════════════════════════════════════════════════════════════════════════
# EJERCICIO 3 — Validador automático de documentos generados
# ════════════════════════════════════════════════════════════════════════════

def ejercicio_3_validador_documentos():
    """
    Implementa el sistema de validación automática antes de distribuir
    un documento generado por IA.
    Detecta placeholders sin rellenar, datos incorrectos y alucinaciones.
    """
    print("\n" + "═"*60)
    print("EJERCICIO 3 — Validador automático de documentos")
    print("═"*60)

    # Documentos de ejemplo — uno válido y uno con errores
    documentos_test = [
        {
            "id": "DOC-001",
            "cliente": {"nombre": "María López", "empresa": "TechStart SL", "referencia": "TS-2026-04"},
            "contenido": """Estimada María López,

Adjuntamos la propuesta para TechStart SL con referencia TS-2026-04.
Hemos analizado vuestras necesidades en el sector tecnológico y proponemos
una solución que reduce el tiempo de procesamiento en un 60%.

El presupuesto para el primer año asciende a 18.000 EUR.
Quedamos a vuestra disposición para resolver cualquier duda.

Saludos cordiales,
Equipo Comercial""",
        },
        {
            "id": "DOC-002",
            "cliente": {"nombre": "Pedro Sanz", "empresa": "Constructora Sanz", "referencia": "CS-2026-11"},
            "contenido": """Estimado [NOMBRE_CLIENTE],

Adjuntamos la propuesta para {EMPRESA} con referencia PENDIENTE.
Hemos analizado vuestras necesidades en el sector INSERTAR_SECTOR.

El presupuesto para el primer año asciende a TBD EUR.
Podéis contactarnos en info@ejemplo.com o al 612 345 678.

Saludos,
Equipo""",
        },
    ]

    def validar_documento(doc: dict) -> dict:
        contenido = doc["contenido"]
        cliente   = doc["cliente"]
        errores   = []

        # Check 1: datos del cliente presentes
        for campo, valor in cliente.items():
            if valor not in contenido:
                errores.append(f"Dato ausente: '{valor}' ({campo}) no aparece en el documento")

        # Check 2: placeholders sin rellenar
        patrones_placeholder = [r'\[.{2,30}\]', r'\{.{2,30}\}', r'\bINSERTAR\b', r'\bPENDIENTE\b', r'\bTBD\b']
        for patron in patrones_placeholder:
            matches = re.findall(patron, contenido, re.IGNORECASE)
            if matches:
                errores.append(f"Placeholder sin rellenar: {matches}")

        # Check 3: longitud razonable
        palabras = len(contenido.split())
        if palabras < 30:
            errores.append(f"Documento demasiado corto: {palabras} palabras")
        elif palabras > 3000:
            errores.append(f"Documento demasiado largo: {palabras} palabras")

        return {
            "id": doc["id"],
            "valido": len(errores) == 0,
            "palabras": palabras,
            "errores": errores,
        }

    print("\nValidando documentos generados...\n")
    for doc in documentos_test:
        resultado = validar_documento(doc)
        estado = "✓ VÁLIDO" if resultado["valido"] else "✗ INVÁLIDO"
        print(f"{estado} — {resultado['id']} ({resultado['palabras']} palabras)")
        if resultado["errores"]:
            for error in resultado["errores"]:
                print(f"    → {error}")

    # Bonus: usar Claude para validación semántica
    print("\n" + "─"*50)
    print("Validación semántica con Claude (doc válido):")
    doc_valido = documentos_test[0]["contenido"]
    system = "Eres un revisor de calidad documental. Detectas inconsistencias, ambigüedades y problemas de tono."
    user = f"""Revisa este documento comercial y valora en JSON:
{{
  "tono_apropiado": true/false,
  "mensaje_claro": true/false,
  "problemas": ["lista de problemas si los hay"],
  "puntuacion": 1-10
}}

DOCUMENTO:
{doc_valido}

Solo devuelve el JSON."""

    validacion_semantica = llamar_claude(system, user, max_tokens=300)
    print(validacion_semantica)


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("LAB 3.4 — Automatización Documental a Escala")
    print(f"API disponible: {'Sí ✓' if API_DISPONIBLE else 'No — modo demo'}")
    print(f"Fecha: {date.today()}")

    ejercicio_1_resumen_ejecutivo()
    ejercicio_2_propuesta_comercial()
    ejercicio_3_validador_documentos()

    print("\n" + "═"*60)
    print("Lab completado.")
    print("Siguiente: Módulo 4 — Asistentes Corporativos y RAG")
    print("═"*60)
