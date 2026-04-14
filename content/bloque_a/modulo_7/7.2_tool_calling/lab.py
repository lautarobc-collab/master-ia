"""
LAB 7.2 — Tool-Calling y Herramientas
=======================================
Objetivo: implementar tool-calling con la API de Anthropic y
diseñar herramientas corporativas reales.

Ejercicios:
  1. Agente con herramientas de CRM (consultar, registrar interacción)
  2. Asistente de calendario con tool-calling multi-step
  3. Análisis de calidad de definición de tools

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import json
from datetime import datetime, timedelta
import random

MODELO = "claude-haiku-4-5-20251001"

# ─── BASES DE DATOS SIMULADAS ─────────────────────────────────────────────────

CRM_CONTACTOS = {
    "ana.garcia@acmecorp.com": {
        "id": "CRM-001",
        "nombre": "Ana García",
        "empresa": "Acme Corp",
        "cargo": "Directora de Compras",
        "etapa_pipeline": "Propuesta enviada",
        "valor_oportunidad": 45000,
        "ultimo_contacto": "2025-03-15",
        "notas": "Interesada en módulo de análisis. Reunión pendiente para demo.",
        "interacciones": [
            {"tipo": "llamada", "fecha": "2025-03-15", "resumen": "Primer contacto, buena disposición"},
            {"tipo": "email", "fecha": "2025-03-18", "resumen": "Enviada propuesta comercial"},
        ],
    },
    "carlos.ruiz@betasolutions.es": {
        "id": "CRM-002",
        "nombre": "Carlos Ruiz",
        "empresa": "Beta Solutions",
        "cargo": "CEO",
        "etapa_pipeline": "Negociación",
        "valor_oportunidad": 120000,
        "ultimo_contacto": "2025-04-01",
        "notas": "Precio sensible. Pide descuento 15%. Decisión esta semana.",
        "interacciones": [
            {"tipo": "reunion", "fecha": "2025-04-01", "resumen": "Demo completada, muy positivo"},
        ],
    },
}

CALENDARIO = {
    "2025-05-06": [
        {"hora": "09:00", "titulo": "Stand-up equipo", "duracion": 30, "participantes": ["equipo ventas"]},
        {"hora": "11:00", "titulo": "Revisión presupuesto Q2", "duracion": 60, "participantes": ["Roberto", "CFO"]},
    ],
    "2025-05-07": [
        {"hora": "10:00", "titulo": "Demo cliente TechFlow", "duracion": 90, "participantes": ["Ana García"]},
        {"hora": "16:00", "titulo": "1:1 con manager", "duracion": 30, "participantes": ["Roberto"]},
    ],
    "2025-05-08": [],
}


# ─── IMPLEMENTACIÓN DE TOOLS ──────────────────────────────────────────────────

def buscar_contacto_crm(email: str) -> dict:
    contacto = CRM_CONTACTOS.get(email)
    if contacto:
        return {"encontrado": True, "contacto": contacto}
    return {"encontrado": False, "mensaje": f"No existe contacto con email {email}"}


def registrar_interaccion_crm(email: str, tipo: str, resumen: str) -> dict:
    if email not in CRM_CONTACTOS:
        return {"exito": False, "error": f"Contacto {email} no encontrado"}
    CRM_CONTACTOS[email]["interacciones"].append({
        "tipo": tipo,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "resumen": resumen,
    })
    CRM_CONTACTOS[email]["ultimo_contacto"] = datetime.now().strftime("%Y-%m-%d")
    return {"exito": True, "mensaje": f"Interacción '{tipo}' registrada para {email}"}


def actualizar_etapa_crm(email: str, nueva_etapa: str) -> dict:
    etapas_validas = ["Lead", "Contactado", "Demo programada", "Propuesta enviada",
                      "Negociación", "Cerrado ganado", "Cerrado perdido"]
    if email not in CRM_CONTACTOS:
        return {"exito": False, "error": "Contacto no encontrado"}
    if nueva_etapa not in etapas_validas:
        return {"exito": False, "error": f"Etapa inválida. Válidas: {etapas_validas}"}
    etapa_anterior = CRM_CONTACTOS[email]["etapa_pipeline"]
    CRM_CONTACTOS[email]["etapa_pipeline"] = nueva_etapa
    return {"exito": True, "etapa_anterior": etapa_anterior, "etapa_nueva": nueva_etapa}


def consultar_calendario(fecha: str, persona: str = "yo") -> dict:
    eventos = CALENDARIO.get(fecha, [])
    return {
        "fecha": fecha,
        "persona": persona,
        "eventos": eventos,
        "slots_libres": _calcular_slots_libres(eventos),
    }


def _calcular_slots_libres(eventos):
    horas_laborables = ["09:00", "10:00", "11:00", "12:00", "15:00", "16:00", "17:00"]
    horas_ocupadas = {e["hora"] for e in eventos}
    return [h for h in horas_laborables if h not in horas_ocupadas]


def crear_reunion(titulo: str, participantes: list, fecha: str, hora: str, duracion: int) -> dict:
    if fecha not in CALENDARIO:
        CALENDARIO[fecha] = []
    nuevo_evento = {
        "hora": hora,
        "titulo": titulo,
        "duracion": duracion,
        "participantes": participantes,
    }
    CALENDARIO[fecha].append(nuevo_evento)
    return {
        "exito": True,
        "evento_creado": nuevo_evento,
        "invitaciones_enviadas": participantes,
    }


# Dispatcher de tools
TOOLS_DISPONIBLES = {
    "buscar_contacto_crm": buscar_contacto_crm,
    "registrar_interaccion_crm": registrar_interaccion_crm,
    "actualizar_etapa_crm": actualizar_etapa_crm,
    "consultar_calendario": consultar_calendario,
    "crear_reunion": crear_reunion,
}

SCHEMAS_TOOLS = [
    {
        "name": "buscar_contacto_crm",
        "description": "Busca un contacto en el CRM por su email. Devuelve perfil completo: nombre, empresa, cargo, etapa en el pipeline de ventas, valor de oportunidad, último contacto y historial de interacciones.",
        "input_schema": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "Email corporativo del contacto"}
            },
            "required": ["email"],
        },
    },
    {
        "name": "registrar_interaccion_crm",
        "description": "Registra una nueva interacción (llamada, reunión, email) con un contacto en el CRM. Actualiza la fecha de último contacto.",
        "input_schema": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "Email del contacto"},
                "tipo": {"type": "string", "description": "Tipo de interacción: llamada, reunion, email, demo"},
                "resumen": {"type": "string", "description": "Resumen breve de la interacción (máx 200 caracteres)"},
            },
            "required": ["email", "tipo", "resumen"],
        },
    },
    {
        "name": "actualizar_etapa_crm",
        "description": "Actualiza la etapa del pipeline de ventas de un contacto. Etapas válidas: Lead, Contactado, Demo programada, Propuesta enviada, Negociación, Cerrado ganado, Cerrado perdido.",
        "input_schema": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "Email del contacto"},
                "nueva_etapa": {"type": "string", "description": "Nueva etapa del pipeline"},
            },
            "required": ["email", "nueva_etapa"],
        },
    },
    {
        "name": "consultar_calendario",
        "description": "Consulta los eventos de calendario de una fecha específica y devuelve los slots libres disponibles.",
        "input_schema": {
            "type": "object",
            "properties": {
                "fecha": {"type": "string", "description": "Fecha en formato YYYY-MM-DD"},
                "persona": {"type": "string", "description": "Persona a consultar. Por defecto 'yo'"},
            },
            "required": ["fecha"],
        },
    },
    {
        "name": "crear_reunion",
        "description": "Crea una reunión en el calendario y envía invitaciones a los participantes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "titulo": {"type": "string"},
                "participantes": {"type": "array", "items": {"type": "string"},
                                  "description": "Lista de emails o nombres"},
                "fecha": {"type": "string", "description": "Fecha YYYY-MM-DD"},
                "hora": {"type": "string", "description": "Hora en formato HH:MM"},
                "duracion": {"type": "integer", "description": "Duración en minutos"},
            },
            "required": ["titulo", "participantes", "fecha", "hora", "duracion"],
        },
    },
]


def ejecutar_tool(nombre: str, params: dict) -> str:
    fn = TOOLS_DISPONIBLES.get(nombre)
    if fn:
        try:
            resultado = fn(**params)
            return json.dumps(resultado, ensure_ascii=False, default=str)
        except Exception as e:
            return json.dumps({"error": str(e)})
    return json.dumps({"error": f"Tool '{nombre}' no disponible"})


# ─── AGENTE CON TOOL-CALLING ──────────────────────────────────────────────────

def ejecutar_agente(objetivo: str, tools_permitidas: list, tiene_api: bool,
                    system: str = "", max_ciclos: int = 8):
    """Ejecuta el bucle de agente con tool-calling."""
    if not tiene_api:
        return None

    try:
        import anthropic
        client = anthropic.Anthropic()
    except Exception as e:
        print(f"  Error cliente: {e}")
        return None

    schemas_filtrados = [s for s in SCHEMAS_TOOLS if s["name"] in tools_permitidas]
    mensajes = [{"role": "user", "content": objetivo}]

    system_completo = system or "Eres un asistente comercial con acceso al CRM y calendario corporativo. Usa las herramientas disponibles para completar la tarea del usuario."

    for ciclo in range(1, max_ciclos + 1):
        try:
            respuesta = client.messages.create(
                model=MODELO,
                max_tokens=800,
                system=system_completo,
                tools=schemas_filtrados,
                messages=mensajes,
            )
        except Exception as e:
            print(f"  Error API (ciclo {ciclo}): {e}")
            break

        if respuesta.stop_reason == "end_turn":
            for bloque in respuesta.content:
                if hasattr(bloque, "text") and bloque.text:
                    return bloque.text
            break

        if respuesta.stop_reason == "tool_use":
            mensajes.append({"role": "assistant", "content": respuesta.content})
            tool_results = []
            for bloque in respuesta.content:
                if bloque.type == "tool_use":
                    print(f"    [Tool] {bloque.name}({json.dumps(bloque.input, ensure_ascii=False)[:60]}...)")
                    resultado = ejecutar_tool(bloque.name, bloque.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": bloque.id,
                        "content": resultado,
                    })
            mensajes.append({"role": "user", "content": tool_results})
        else:
            break

    return None


# ─── EJERCICIO 1: AGENTE CRM ──────────────────────────────────────────────────

def ejercicio_1_agente_crm(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 1 — AGENTE CON HERRAMIENTAS DE CRM")
    print("=" * 64)

    tareas_crm = [
        "¿Cuál es el estado actual de la oportunidad con Ana García de Acme Corp? Su email es ana.garcia@acmecorp.com",
        "Registra que hoy tuve una llamada con Carlos Ruiz (carlos.ruiz@betasolutions.es). Le di un descuento del 10% y quedó en confirmar esta semana.",
    ]

    tools_crm = ["buscar_contacto_crm", "registrar_interaccion_crm", "actualizar_etapa_crm"]

    for tarea in tareas_crm:
        print(f"\n  Tarea: {tarea[:70]}...")
        if tiene_api:
            print("  Ejecutando agente...")
            resultado = ejecutar_agente(tarea, tools_crm, tiene_api)
            if resultado:
                print(f"  Respuesta: {resultado}")
            else:
                print("  [Sin respuesta del agente]")
        else:
            # Fallback manual
            if "ana.garcia" in tarea:
                contacto = buscar_contacto_crm("ana.garcia@acmecorp.com")["contacto"]
                print(f"  [Fallback] Contacto: {contacto['nombre']} — {contacto['etapa_pipeline']}")
                print(f"  Valor oportunidad: {contacto['valor_oportunidad']:,}€")
                print(f"  Notas: {contacto['notas']}")
            else:
                resultado = registrar_interaccion_crm(
                    "carlos.ruiz@betasolutions.es", "llamada",
                    "Ofrecido descuento 10%, pendiente confirmación"
                )
                print(f"  [Fallback] {resultado['mensaje']}")
            print("  [Configura ANTHROPIC_API_KEY para agente con razonamiento completo]")


# ─── EJERCICIO 2: ASISTENTE DE CALENDARIO ────────────────────────────────────

def ejercicio_2_asistente_calendario(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 2 — ASISTENTE DE CALENDARIO MULTI-STEP")
    print("=" * 64)

    tarea = (
        "Necesito programar una demo con Ana García (ana.garcia@acmecorp.com) "
        "de 60 minutos. Consulta mi disponibilidad el 6 y 7 de mayo de 2025 "
        "y crea la reunión en el primer slot libre que encuentres."
    )
    print(f"\n  Tarea: {tarea}")

    tools_calendario = ["consultar_calendario", "crear_reunion", "buscar_contacto_crm"]

    if tiene_api:
        print("  Ejecutando agente...")
        resultado = ejecutar_agente(tarea, tools_calendario, tiene_api)
        if resultado:
            print(f"\n  Resultado: {resultado}")
    else:
        # Simular el razonamiento paso a paso
        print("\n  [Simulación del agente — sin API]")
        print("\n  Paso 1: Consultar disponibilidad 6 mayo")
        cal_6 = consultar_calendario("2025-05-06")
        print(f"  Slots libres el 6/5: {cal_6['slots_libres']}")

        print("\n  Paso 2: Primer slot libre → 10:00")
        print("\n  Paso 3: Consultar datos del contacto")
        contacto_info = buscar_contacto_crm("ana.garcia@acmecorp.com")
        nombre = contacto_info["contacto"]["nombre"]
        print(f"  Contacto: {nombre}")

        print("\n  Paso 4: Crear reunión")
        reunion = crear_reunion(
            titulo=f"Demo con {nombre}",
            participantes=["ana.garcia@acmecorp.com"],
            fecha="2025-05-06",
            hora="10:00",
            duracion=60
        )
        print(f"  Reunión creada: {reunion['evento_creado']['titulo']} — {reunion['evento_creado']['hora']}")
        print(f"  Invitación enviada a: {reunion['invitaciones_enviadas']}")
        print("\n  [Configura ANTHROPIC_API_KEY para razonamiento IA completo]")


# ─── EJERCICIO 3: CALIDAD DE DEFINICIÓN DE TOOLS ─────────────────────────────

TOOLS_PARA_EVALUAR = [
    {
        "name": "do_thing",
        "description": "Does something with the data",
        "input_schema": {"type": "object", "properties": {"data": {"type": "string"}}},
    },
    {
        "name": "buscar_pedido",
        "description": "Busca un pedido en el sistema ERP por su número. Devuelve: número de pedido, fecha de creación, cliente, líneas de pedido (producto, cantidad, precio), estado (pendiente/enviado/entregado/cancelado) y fecha estimada de entrega.",
        "input_schema": {
            "type": "object",
            "properties": {
                "numero_pedido": {
                    "type": "string",
                    "description": "Número de pedido en formato PED-XXXXXX, ej: PED-002345"
                }
            },
            "required": ["numero_pedido"],
        },
    },
    {
        "name": "enviar_email",
        "description": "send email",
        "input_schema": {
            "type": "object",
            "properties": {
                "to": {"type": "string"},
                "body": {"type": "string"},
            },
        },
    },
]

PROMPT_EVALUACION_TOOL = """Eres un experto en diseño de APIs para agentes IA.
Evalúa la calidad de esta definición de tool según estos criterios:
1. Claridad del nombre (¿describe exactamente la acción?)
2. Descripción (¿explica cuándo usarla, qué devuelve, limitaciones?)
3. Parámetros (¿tienen tipo, descripción, formato esperado?)
4. Usabilidad (¿un LLM la usaría correctamente con esta definición?)

Tool a evaluar:
{tool_json}

Responde en JSON:
{{
  "puntuacion": 0-100,
  "nivel": "deficiente/aceptable/buena/excelente",
  "problemas": ["problema 1", "problema 2"],
  "mejoras_sugeridas": "versión mejorada de la definición en 2-3 frases",
  "veredicto": "1 frase resumen"
}}"""


def ejercicio_3_calidad_tools(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 3 — EVALUACIÓN DE CALIDAD DE TOOLS")
    print("=" * 64)

    for tool in TOOLS_PARA_EVALUAR:
        print(f"\n  Tool: {tool['name']}")
        print(f"  Descripción: {tool['description'][:60]}...")

        if tiene_api:
            try:
                import anthropic
                client = anthropic.Anthropic()
                prompt = PROMPT_EVALUACION_TOOL.format(
                    tool_json=json.dumps(tool, ensure_ascii=False, indent=2)
                )
                r = client.messages.create(
                    model=MODELO,
                    max_tokens=400,
                    messages=[{"role": "user", "content": prompt}]
                )
                respuesta = r.content[0].text.strip()
                try:
                    datos = json.loads(respuesta)
                    print(f"  Puntuación: {datos['puntuacion']}/100 — {datos['nivel'].upper()}")
                    if datos["problemas"]:
                        print(f"  Problemas: {'; '.join(datos['problemas'][:2])}")
                    print(f"  Mejora: {datos['mejoras_sugeridas'][:100]}...")
                except json.JSONDecodeError:
                    print(f"  Evaluación: {respuesta[:150]}")
            except Exception as e:
                print(f"  Error: {e}")
        else:
            # Heurísticas básicas
            score = 0
            problemas = []
            if len(tool["name"]) > 5 and "_" in tool["name"]:
                score += 25
            else:
                problemas.append("nombre poco descriptivo o sin guiones bajos")
            if len(tool["description"]) > 50:
                score += 35
            else:
                problemas.append("descripción muy corta")
            props = tool["input_schema"].get("properties", {})
            descripciones_ok = all("description" in v for v in props.values())
            if descripciones_ok and props:
                score += 40
            else:
                problemas.append("parámetros sin descripción")
            nivel = "excelente" if score >= 90 else "buena" if score >= 70 else "aceptable" if score >= 50 else "deficiente"
            print(f"  [Heurística] Puntuación: {score}/100 — {nivel.upper()}")
            if problemas:
                print(f"  Problemas: {'; '.join(problemas)}")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 64)
    print("LAB 7.2 — TOOL-CALLING Y HERRAMIENTAS")
    print("=" * 64)

    tiene_api = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if tiene_api:
        print(f"  Modelo: {MODELO}")
        print("  Modo: API activa — tool-calling real con Claude")
    else:
        print("  AVISO: ANTHROPIC_API_KEY no configurada.")
        print("  Modo: Fallback con ejecución directa de tools simuladas")

    ejercicio_1_agente_crm(tiene_api)
    ejercicio_2_asistente_calendario(tiene_api)
    ejercicio_3_calidad_tools(tiene_api)

    print("\n" + "=" * 64)
    print("RESUMEN DEL LAB")
    print("=" * 64)
    print("""
  Lo que hemos implementado:
  ✓ Tools de CRM (buscar, registrar, actualizar etapa)
  ✓ Tools de calendario (consultar, crear reunión)
  ✓ Bucle de tool-calling con Claude (ciclo percepción-acción)
  ✓ Evaluador de calidad de definiciones de tools

  Diseño de tools — reglas más importantes:
    1. Nombre descriptivo en snake_case
    2. Descripción: cuándo usarla + qué devuelve
    3. Parámetros con tipo, descripción y formato
    4. Una sola responsabilidad por tool
    5. Resultados JSON predecibles, incluso para errores
""")

    print("[FIN DEL LAB 7.2]")
