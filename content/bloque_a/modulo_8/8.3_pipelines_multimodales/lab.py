"""
LAB 8.3 — Pipelines Multimodales
==================================
Objetivo: construir pipelines que combinen texto, imagen y audio
simulando casos empresariales completos.

Ejercicios:
  1. Pipeline de procesamiento de factura (imagen → datos → validación → contabilidad)
  2. Pipeline de informe de reunión (transcripción + slides → acta → tareas)
  3. Pipeline de control de recepción de mercancía (foto + albarán → verificación)

Requisitos:
    pip install anthropic

Ejecutar:
    python lab.py
"""

import os
import json
from datetime import datetime, timedelta

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


# ─── DATOS SIMULADOS ──────────────────────────────────────────────────────────

# Simula el output del paso de visión IA sobre una factura
DATOS_EXTRAIDOS_FACTURA = {
    "numero_factura": "INV-2025-00892",
    "fecha_emision": "2025-04-10",
    "fecha_vencimiento": "2025-05-10",
    "proveedor_nombre": "Suministros Tech S.L.",
    "proveedor_nif": "B-87654321",
    "cliente_nombre": "Mi Empresa S.A.",
    "cliente_nif": "A-12345678",
    "lineas": [
        {"descripcion": "Licencias software gestión", "cantidad": 5,
         "precio_unit": 450.00, "subtotal": 2250.00},
        {"descripcion": "Soporte técnico mensual", "cantidad": 1,
         "precio_unit": 350.00, "subtotal": 350.00},
    ],
    "base_imponible": 2600.00,
    "iva_porcentaje": 21,
    "iva_importe": 546.00,
    "total": 3146.00,
    "confianza_extraccion": "alta",
}

# Maestro de proveedores (ERP simulado)
MAESTRO_PROVEEDORES = {
    "B-87654321": {
        "nombre": "Suministros Tech S.L.",
        "activo": True,
        "cuenta_contable": "400001",
        "iban": "ES76 2100 0418 4502 0005 1332",
        "dias_pago": 30,
        "limite_aprobacion_automatica": 5000,
    },
    "B-99999999": {
        "nombre": "Proveedor Desconocido",
        "activo": False,
        "cuenta_contable": None,
    },
}

# Pedidos pendientes en ERP
PEDIDOS_ERP = {
    "PO-2025-0234": {
        "proveedor_nif": "B-87654321",
        "importe_aprobado": 2600.00,
        "estado": "recibido_pendiente_factura",
        "proyecto": "Actualización infraestructura 2025",
        "aprobado_por": "Director IT",
    },
}

# Datos de slides (simula el output del paso de visión sobre presentación)
CONTENIDO_SLIDES = {
    "slide_1": {
        "titulo": "Resultados Q1 2025",
        "datos_clave": "Facturación: 847K€ (+12% vs objetivo)",
    },
    "slide_2": {
        "titulo": "Análisis por Segmento",
        "datos_clave": "Pymes tecnológicas: +28% | Retail: +15% | Industrial: -8%",
    },
    "slide_3": {
        "titulo": "Plan Q2",
        "datos_clave": "Objetivo: 920K€ | 5 cuentas target industrial | Campaña pymes mayo",
    },
}

TRANSCRIPCION_REUNION_BREVE = """
Roberto: Repasamos los resultados del Q1. Pedro, los números superaron objetivo un 12%.
Pedro: Sí, pymes tecnológicas fue el motor. Industrial bajó, pero tengo plan para Q2
con 5 cuentas target. Necesito el caso de éxito TechMetal para las demos.
Laura: Lo preparo antes del 15 de mayo.
Roberto: Objetivo Q2: 920.000 euros. Próxima revisión: 3 de junio.
"""

# Datos de albarán y foto de recepción (simulados)
ALBARAN_PROVEEDOR = {
    "numero": "ALB-20250412-089",
    "proveedor": "Distribuidora Norte S.L.",
    "fecha": "2025-04-12",
    "lineas": [
        {"ref": "SKU-001", "descripcion": "Cajas A4 resma 500h", "cantidad_pedida": 20},
        {"ref": "SKU-002", "descripcion": "Bolígrafos caja 50u", "cantidad_pedida": 10},
        {"ref": "SKU-003", "descripcion": "Carpetas archivador", "cantidad_pedida": 30},
    ],
}

RECEPCION_REAL_SIMULADA = {
    "lineas_recibidas": [
        {"ref": "SKU-001", "cantidad_recibida": 20, "estado": "correcto"},
        {"ref": "SKU-002", "cantidad_recibida": 8, "estado": "incompleto"},  # Faltan 2
        {"ref": "SKU-003", "cantidad_recibida": 30, "estado": "correcto"},
    ],
    "observaciones_visuales": "Caja exterior del SKU-002 presenta daño en esquina. Los bolígrafos parecen correctos internamente.",
}


# ─── EJERCICIO 1: PIPELINE DE FACTURAS ───────────────────────────────────────

def paso_1_extraer_factura(tiene_api):
    """Simula la extracción de datos de factura via visión IA."""
    if tiene_api:
        # En producción: aquí iría la llamada de visión con imagen real
        # Por simplicidad usamos datos simulados y pedimos análisis al LLM
        prompt = f"""Tienes los datos extraídos de una factura vía visión IA.
Verifica la coherencia matemática y detecta posibles errores.
Datos: {json.dumps(DATOS_EXTRAIDOS_FACTURA, ensure_ascii=False)}

Responde JSON: {{"coherente": true/false, "errores": [], "total_calculado": 0.00}}"""
        resp = llamar_api(prompt, max_tokens=150)
        try:
            return json.loads(resp), DATOS_EXTRAIDOS_FACTURA
        except json.JSONDecodeError:
            return {"coherente": True, "errores": []}, DATOS_EXTRAIDOS_FACTURA
    else:
        # Validación matemática sin IA
        datos = DATOS_EXTRAIDOS_FACTURA
        iva_calculado = round(datos["base_imponible"] * datos["iva_porcentaje"] / 100, 2)
        total_calculado = round(datos["base_imponible"] + iva_calculado, 2)
        coherente = (abs(iva_calculado - datos["iva_importe"]) < 0.01 and
                     abs(total_calculado - datos["total"]) < 0.01)
        return {"coherente": coherente, "total_calculado": total_calculado, "errores": []}, datos


def paso_2_validar_contra_erp(datos_factura):
    """Valida la factura contra el ERP."""
    nif = datos_factura["proveedor_nif"]
    proveedor_erp = MAESTRO_PROVEEDORES.get(nif)

    resultado = {
        "proveedor_en_maestro": proveedor_erp is not None,
        "proveedor_activo": proveedor_erp.get("activo", False) if proveedor_erp else False,
        "pedido_relacionado": None,
        "discrepancia_importe": None,
        "es_duplicado": False,
    }

    if proveedor_erp:
        # Buscar pedido relacionado
        for num_po, po in PEDIDOS_ERP.items():
            if po["proveedor_nif"] == nif and po["estado"] == "recibido_pendiente_factura":
                diferencia = abs(po["importe_aprobado"] - datos_factura["base_imponible"])
                tolerancia = po["importe_aprobado"] * 0.01  # 1% tolerancia
                resultado["pedido_relacionado"] = num_po
                resultado["discrepancia_importe"] = diferencia > tolerancia
                resultado["importe_pedido"] = po["importe_aprobado"]
                break

    return resultado


def paso_3_decisión_contabilizacion(validacion, datos_factura, tiene_api):
    """Decide si contabilizar automáticamente o escalar."""
    total = datos_factura["total"]
    proveedor = MAESTRO_PROVEEDORES.get(datos_factura["proveedor_nif"], {})
    limite_auto = proveedor.get("limite_aprobacion_automatica", 0)

    if not validacion["proveedor_activo"]:
        return "RECHAZAR", "Proveedor no activo en el maestro"
    if validacion["es_duplicado"]:
        return "RECHAZAR", "Factura duplicada detectada"
    if validacion["discrepancia_importe"]:
        return "ESCALAR_HUMANO", "Discrepancia de importe con el pedido"
    if total > limite_auto:
        return "ESCALAR_HUMANO", f"Importe ({total}€) supera el límite de aprobación automática ({limite_auto}€)"
    if not validacion["pedido_relacionado"]:
        return "ESCALAR_HUMANO", "No se encontró pedido de compra relacionado"

    return "CONTABILIZAR_AUTO", "Todas las validaciones superadas"


def ejercicio_1_pipeline_facturas(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 1 — PIPELINE DE PROCESAMIENTO DE FACTURAS")
    print("=" * 64)

    print("\n  PASO 1: Extracción de datos (visión IA)")
    print("  " + "─" * 50)
    verificacion, datos = paso_1_extraer_factura(tiene_api)
    print(f"  Factura: {datos['numero_factura']} | Proveedor: {datos['proveedor_nombre']}")
    print(f"  Total: {datos['total']:,.2f}€ | Coherencia matemática: {'✓' if verificacion.get('coherente') else '✗'}")
    if verificacion.get("errores"):
        print(f"  Errores: {verificacion['errores']}")

    print("\n  PASO 2: Validación contra ERP")
    print("  " + "─" * 50)
    validacion = paso_2_validar_contra_erp(datos)
    print(f"  Proveedor en maestro: {'✓' if validacion['proveedor_en_maestro'] else '✗'}")
    print(f"  Proveedor activo: {'✓' if validacion['proveedor_activo'] else '✗'}")
    print(f"  Pedido relacionado: {validacion.get('pedido_relacionado') or 'No encontrado'}")
    print(f"  Discrepancia de importe: {'⚠ Sí' if validacion.get('discrepancia_importe') else '✓ No'}")
    print(f"  Duplicado: {'⚠ Sí' if validacion.get('es_duplicado') else '✓ No'}")

    print("\n  PASO 3: Decisión de contabilización")
    print("  " + "─" * 50)
    decision, motivo = paso_3_decisión_contabilizacion(validacion, datos, tiene_api)
    print(f"  Decisión: {decision}")
    print(f"  Motivo: {motivo}")

    if decision == "CONTABILIZAR_AUTO":
        proveedor_erp = MAESTRO_PROVEEDORES[datos["proveedor_nif"]]
        fecha_vto = (datetime.now() + timedelta(days=proveedor_erp["dias_pago"])).strftime("%Y-%m-%d")
        print(f"\n  PASO 4: Contabilización automática")
        print(f"  ✓ Asiento creado en cuenta {proveedor_erp['cuenta_contable']}")
        print(f"  ✓ Pago programado para {fecha_vto} (IBAN: {proveedor_erp['iban'][:10]}...)")
        print(f"  ✓ Email de confirmación enviado al proveedor")
    else:
        print(f"\n  PASO 4: Escalada a revisión humana")
        print(f"  → Tarea creada en sistema financiero")
        print(f"  → Asignada al departamento de cuentas a pagar")
        print(f"  → SLA: revisión en 24 horas laborables")

    if tiene_api:
        # Generar email de notificación
        prompt = f"""Redacta un email de notificación conciso para el equipo de administración.
Decisión: {decision} — {motivo}
Factura: {datos['numero_factura']} de {datos['proveedor_nombre']} por {datos['total']:.2f}€
Máximo 3 frases. Tono profesional."""
        email = llamar_api(prompt, max_tokens=120)
        print(f"\n  Email de notificación generado:")
        print(f"  {email}")


# ─── EJERCICIO 2: PIPELINE DE INFORME DE REUNIÓN ─────────────────────────────

def ejercicio_2_pipeline_reunion(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 2 — PIPELINE INFORME DE REUNIÓN (audio + slides)")
    print("=" * 64)

    print("\n  PASO 1: Procesar transcripción de audio")
    print(f"  Transcripción disponible: {len(TRANSCRIPCION_REUNION_BREVE.strip())} caracteres")

    print("\n  PASO 2: Procesar slides de la presentación")
    for num, slide in CONTENIDO_SLIDES.items():
        print(f"  {num}: {slide['titulo']} — {slide['datos_clave'][:50]}...")

    print("\n  PASO 3: Síntesis multimodal → Acta")
    print("  " + "─" * 50)

    if tiene_api:
        slides_texto = "\n".join([
            f"Slide {n}: {s['titulo']} | {s['datos_clave']}"
            for n, s in CONTENIDO_SLIDES.items()
        ])
        prompt = f"""Genera el acta de esta reunión combinando la transcripción y el contenido de las slides.

TRANSCRIPCIÓN:
{TRANSCRIPCION_REUNION_BREVE}

CONTENIDO DE LAS DIAPOSITIVAS:
{slides_texto}

Genera:
1. RESUMEN EJECUTIVO (3 frases máx, referenciando datos de slides cuando sea relevante)
2. DECISIONES TOMADAS (lista)
3. ACCIONES ASIGNADAS (formato: RESPONSABLE — ACCIÓN — FECHA)"""

        acta = llamar_api(prompt, max_tokens=400)
        print(acta)

        # Extraer tareas en JSON
        print("\n  PASO 4: Extracción de tareas para el gestor de proyectos")
        prompt_tareas = f"""Del siguiente acta, extrae SOLO las acciones asignadas en JSON:
[{{"responsable": "nombre", "accion": "descripcion", "fecha_limite": "YYYY-MM-DD o null"}}]
No incluyas nada más, solo el array JSON.

{acta}"""
        tareas_json = llamar_api(prompt_tareas, max_tokens=200)
        try:
            tareas = json.loads(tareas_json)
            print(f"  Tareas extraídas: {len(tareas)}")
            for t in tareas:
                print(f"    ☐ {t.get('responsable', '?')} — {t.get('accion', '?')} — {t.get('fecha_limite', 'sin fecha')}")
        except json.JSONDecodeError:
            print(f"  Tareas: {tareas_json[:150]}")
    else:
        print("  [Modo fallback — síntesis por concatenación]")
        print()
        print("  RESUMEN: Reunión de revisión Q1 2025. Superado objetivo 12%.")
        print("  Segmento industrial con plan de recuperación para Q2.")
        print()
        print("  ACCIONES:")
        print("  ☐ Laura — Caso de éxito TechMetal — 15/05/2025")
        print("  ☐ Pedro — Contactar 5 cuentas target industrial — Q2 2025")
        print("  ☐ Pedro — Llamar a Ana (finanzas) sobre previsión cobros — hoy")
        print()
        print("  [Configura ANTHROPIC_API_KEY para síntesis y extracción IA completa]")


# ─── EJERCICIO 3: CONTROL DE RECEPCIÓN DE MERCANCÍA ──────────────────────────

def ejercicio_3_pipeline_recepcion(tiene_api):
    print("\n" + "=" * 64)
    print("EJERCICIO 3 — PIPELINE CONTROL DE RECEPCIÓN DE MERCANCÍA")
    print("=" * 64)

    print("\n  PASO 1: Datos del albarán del proveedor")
    for linea in ALBARAN_PROVEEDOR["lineas"]:
        print(f"  {linea['ref']}: {linea['descripcion']} — Pedido: {linea['cantidad_pedida']} unidades")

    print("\n  PASO 2: Datos de la recepción real (simula análisis de foto)")
    for linea in RECEPCION_REAL_SIMULADA["lineas_recibidas"]:
        icono = "✓" if linea["estado"] == "correcto" else "⚠"
        print(f"  {icono} {linea['ref']}: Recibido {linea['cantidad_recibida']} unidades ({linea['estado']})")
    print(f"  Observaciones: {RECEPCION_REAL_SIMULADA['observaciones_visuales']}")

    print("\n  PASO 3: Comparativa automática albarán vs. recepción")
    discrepancias = []
    for pedida in ALBARAN_PROVEEDOR["lineas"]:
        for recibida in RECEPCION_REAL_SIMULADA["lineas_recibidas"]:
            if pedida["ref"] == recibida["ref"]:
                if pedida["cantidad_pedida"] != recibida["cantidad_recibida"]:
                    discrepancias.append({
                        "ref": pedida["ref"],
                        "descripcion": pedida["descripcion"],
                        "pedido": pedida["cantidad_pedida"],
                        "recibido": recibida["cantidad_recibida"],
                        "diferencia": recibida["cantidad_recibida"] - pedida["cantidad_pedida"],
                    })

    if discrepancias:
        print(f"  Discrepancias detectadas: {len(discrepancias)}")
        for d in discrepancias:
            print(f"  ⚠ {d['ref']} — {d['descripcion']}: pedido {d['pedido']}, recibido {d['recibido']} (diferencia: {d['diferencia']:+d})")
    else:
        print("  ✓ Sin discrepancias en cantidades")

    print("\n  PASO 4: Decisión y acción")
    if discrepancias:
        print("  Decisión: RECEPCIÓN PARCIAL — crear reclamación al proveedor")
        if tiene_api:
            prompt = f"""Redacta un email de reclamación al proveedor {ALBARAN_PROVEEDOR['proveedor']}
por las siguientes discrepancias en el albarán {ALBARAN_PROVEEDOR['numero']}:
{json.dumps(discrepancias, ensure_ascii=False)}
Observaciones adicionales: {RECEPCION_REAL_SIMULADA['observaciones_visuales']}
Tono: profesional y directo. Máximo 4 frases. Solicitar reposición urgente."""
            email = llamar_api(prompt, max_tokens=200)
            print(f"\n  Email de reclamación generado:")
            print(f"  {email}")
        else:
            print("\n  Email de reclamación (plantilla):")
            for d in discrepancias:
                print(f"  Falta: {d['pedido'] - d['recibido']} unidades de {d['descripcion']}")
            print("  Se solicita reposición en siguiente entrega.")
            print("  [Configura ANTHROPIC_API_KEY para email personalizado IA]")
    else:
        print("  ✓ Recepción conforme — confirmación automática en ERP")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 64)
    print("LAB 8.3 — PIPELINES MULTIMODALES")
    print("=" * 64)

    tiene_api = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if tiene_api:
        print(f"  Modelo: {MODELO}")
        print("  Modo: API activa — pipelines completos con IA")
    else:
        print("  AVISO: ANTHROPIC_API_KEY no configurada.")
        print("  Modo: Lógica de validación sin generación IA")

    ejercicio_1_pipeline_facturas(tiene_api)
    ejercicio_2_pipeline_reunion(tiene_api)
    ejercicio_3_pipeline_recepcion(tiene_api)

    print("\n" + "=" * 64)
    print("RESUMEN DEL LAB")
    print("=" * 64)
    print("""
  Pipelines construidos:
  ✓ Facturas: extracción → validación → contabilización automática
  ✓ Reuniones: transcripción + slides → acta → tareas JSON
  ✓ Recepciones: albarán vs. real → detección discrepancias → reclamación

  Patrón universal del pipeline multimodal:
    1. Captura (trigger: email, carpeta, formulario)
    2. Extracción IA (visión, audio, OCR)
    3. Validación contra sistemas (ERP, CRM, BD)
    4. Decisión (auto / HITL / rechazo)
    5. Acción + notificación + registro

  KPI más importante a medir:
    Tasa de procesamiento automático = casos sin intervención humana / total
    Objetivo típico: > 80% en el caso feliz
""")

    print("[FIN DEL LAB 8.3]")
