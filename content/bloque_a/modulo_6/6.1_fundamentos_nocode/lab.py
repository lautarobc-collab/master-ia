"""
LAB 6.1 — Fundamentos No-Code con IA
=======================================
Objetivo: simular y construir los flujos no-code más comunes
usando Python como motor, equivalente a lo que haría n8n/Make.

Ejercicios:
  1. Clasificador de emails — simula el flujo de enrutamiento
  2. Generador de actas — procesa transcripción → acta estructurada
  3. Enriquecedor de leads — genera perfil de empresa desde nombre

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import json
import time

MODELO = "claude-haiku-4-5-20251001"


def llamar_api(prompt, system="", temperatura=0.1, max_tokens=400):
    try:
        import anthropic
        client = anthropic.Anthropic()
        kwargs = dict(model=MODELO, max_tokens=max_tokens, temperature=temperatura,
                      messages=[{"role":"user","content":prompt}])
        if system:
            kwargs["system"] = system
        r = client.messages.create(**kwargs)
        return r.content[0].text.strip()
    except Exception as e:
        return f"Error: {e}"


# ─── FLUJO 1: CLASIFICADOR DE EMAILS ─────────────────────────────────────────

EMAILS_ENTRADA = [
    {"de": "cliente@empresa.com", "asunto": "Pedido 4521 - retraso", "cuerpo": "Llevo 3 semanas esperando mi pedido y nadie me responde. Esto es inaceptable."},
    {"de": "prospecto@startup.io", "asunto": "Consulta sobre precios para equipo de 20 personas", "cuerpo": "Hola, somos una startup de 20 personas y nos interesa vuestra solución. ¿Podríais enviarme tarifas?"},
    {"de": "proveedor@logistica.es", "asunto": "Factura 2025-0234", "cuerpo": "Adjunto la factura del mes de abril correspondiente a los servicios de transporte."},
]

PROMPT_CLASIFICAR = """Clasifica este email. Devuelve SOLO JSON válido.
{{
  "categoria": "reclamacion|consulta_comercial|factura|soporte|otro",
  "urgencia": "alta|media|baja",
  "departamento": "ventas|soporte|administracion|operaciones",
  "accion": "1 acción específica en infinitivo",
  "respuesta_automatica": "1 frase de confirmación para enviar al remitente"
}}

Email:
De: {de}
Asunto: {asunto}
Cuerpo: {cuerpo}"""


# ─── FLUJO 2: GENERADOR DE ACTAS ─────────────────────────────────────────────

TRANSCRIPCION_REUNION = """
[Reunión de seguimiento de proyecto IA — 14 de abril 2025]
[Asistentes: María (directora de operaciones), Carlos (IT), Ana (RRHH), Pedro (consultor externo)]

María: Bueno, empezamos. ¿Cómo va el piloto de clasificación de incidencias?
Carlos: Muy bien. Esta semana hemos procesado 847 tickets. La precisión está al 91%.
María: Perfecto. ¿Cuándo podemos pasar a producción?
Carlos: Si validamos los casos límite esta semana, podríamos estar en producción el día 28.
María: Bien. Carlos, ¿puedes preparar el plan de rollout para el jueves?
Carlos: Sí, sin problema.
Ana: Sobre formación del equipo, necesito que alguien del área técnica haga una sesión de 2 horas.
Pedro: Puedo hacerla yo. ¿La semana del 21?
Ana: Perfecto, coordinamos fechas por email.
María: Último punto: presupuesto para el siguiente módulo. Necesitamos aprobación de dirección.
María: Voy a preparar el caso de negocio para el comité del día 30. Pedro, ¿me mandas los números esta semana?
Pedro: Te los mando mañana por la mañana.
María: Perfecto. Cerramos aquí.
"""

PROMPT_ACTA = """Genera el acta de esta reunión en formato estructurado.

TRANSCRIPCIÓN:
{transcripcion}

Formato obligatorio:
## Acta de Reunión

**Fecha:** [extraer de la transcripción]
**Asistentes:** [lista]

### Temas tratados
[bullets con cada tema discutido]

### Decisiones tomadas
[bullets solo con decisiones concretas]

### Próximos pasos
| Acción | Responsable | Fecha límite |
|---|---|---|
[una fila por cada tarea asignada]

### Próxima reunión
[si se menciona, si no: "No definida"]"""


# ─── FLUJO 3: ENRIQUECEDOR DE LEADS ──────────────────────────────────────────

LEADS = [
    {"empresa": "Distribuciones Norte S.A.", "cargo": "Director de Operaciones", "email": "director@distnorte.es"},
    {"empresa": "Tech Innovators SL", "cargo": "CTO", "email": "cto@techinnovators.io"},
]

PROMPT_LEAD = """Eres un asistente de ventas. Basándote solo en el nombre de la empresa y el cargo,
genera un perfil de lead para ayudar al comercial a preparar la llamada.
Devuelve JSON.

{{
  "sector_probable": "sector más probable",
  "tamaño_probable": "startup|pyme|mediana|grande",
  "dolor_probable": "principal problema que probablemente tiene esta empresa",
  "propuesta_valor": "1 frase de cómo nuestro producto/servicio les ayudaría",
  "pregunta_apertura": "1 pregunta abierta para iniciar la conversación",
  "scoring": "frío|tibio|caliente"
}}

Empresa: {empresa}
Cargo del contacto: {cargo}"""


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 64)
    print("LAB 6.1 — Fundamentos No-Code con IA")
    print("=" * 64)

    tiene_api = bool(os.getenv("ANTHROPIC_API_KEY"))

    print("\n[1] FLUJO: CLASIFICADOR DE EMAILS")
    print("-" * 64)
    if tiene_api:
        for email in EMAILS_ENTRADA:
            prompt = PROMPT_CLASIFICAR.format(**email)
            resultado = llamar_api(prompt, temperatura=0.0, max_tokens=200)
            print(f"\n  Email: {email['asunto']}")
            print(f"  → {resultado}")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY.")

    print("\n\n[2] FLUJO: GENERADOR DE ACTAS")
    print("-" * 64)
    if tiene_api:
        prompt = PROMPT_ACTA.format(transcripcion=TRANSCRIPCION_REUNION)
        acta = llamar_api(prompt, temperatura=0.2, max_tokens=600)
        print(f"\n{acta}")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY.")

    print("\n\n[3] FLUJO: ENRIQUECEDOR DE LEADS")
    print("-" * 64)
    if tiene_api:
        for lead in LEADS:
            prompt = PROMPT_LEAD.format(**lead)
            perfil = llamar_api(prompt, temperatura=0.3, max_tokens=300)
            print(f"\n  Lead: {lead['empresa']} — {lead['cargo']}")
            print(f"  {perfil}")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY.")

    print("\n[FIN DEL LAB 6.1]")
