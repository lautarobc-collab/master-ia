"""
LAB 4.1 — Fundamentos de RAG
==============================
Objetivo: construir un sistema RAG mínimo funcional — desde
el chunking de documentos hasta la generación de respuestas
citando fuentes — usando solo Chroma y Claude.

Ejercicios:
  1. Chunker — divide documentos en fragmentos con solapamiento
  2. RAG manual — simula búsqueda semántica con similitud de palabras
  3. RAG real con Chroma (requiere: pip install chromadb anthropic)

Requisitos:
    pip install anthropic chromadb

Ejecutar:
    python lab.py
"""

import os
import re
import time

MODELO = "claude-haiku-4-5-20251001"

# ─── BASE DOCUMENTAL DE EJEMPLO ───────────────────────────────────────────────

DOCUMENTOS = [
    {
        "id": "politica_devoluciones",
        "titulo": "Política de Devoluciones — actualizada enero 2025",
        "texto": """Los clientes pueden solicitar la devolución de cualquier producto en los primeros 30 días
desde la fecha de recepción. Para productos defectuosos el plazo es de 90 días.
El proceso de devolución se inicia contactando con atención al cliente por email a devoluciones@empresa.com
o llamando al 900 123 456. El reembolso se tramita en un plazo máximo de 5 días hábiles.
Los productos personalizados no admiten devolución salvo defecto de fabricación.
Los gastos de envío de la devolución corren a cargo del cliente, excepto en casos de error del proveedor."""
    },
    {
        "id": "politica_privacidad",
        "titulo": "Política de Privacidad y Protección de Datos",
        "texto": """Tratamos los datos personales conforme al Reglamento General de Protección de Datos (RGPD).
Los datos recogidos se usan exclusivamente para gestionar la relación comercial.
No cedemos datos a terceros sin consentimiento expreso, salvo obligación legal.
Los datos se conservan durante la vigencia del contrato y 5 años adicionales por obligaciones fiscales.
El responsable del tratamiento es Empresa S.L., con domicilio en Calle Mayor 1, Madrid.
Para ejercer derechos ARCO contactar con privacidad@empresa.com."""
    },
    {
        "id": "catalogo_productos",
        "titulo": "Catálogo de Productos — Línea Profesional 2025",
        "texto": """La línea profesional incluye: sillas ergonómicas (299-599€), mesas de trabajo (199-899€)
y accesorios de escritorio. Todos los productos incluyen 2 años de garantía.
Los pedidos superiores a 500€ tienen envío gratuito en península.
Plazo de entrega estándar: 3-5 días hábiles. Plazo exprés (24h): disponible con suplemento de 15€.
Descuentos para empresa: 10% a partir de 10 unidades, 18% a partir de 25 unidades.
Los pedidos se realizan a través de nuestra tienda online o por teléfono."""
    },
]


# ─── PARTE 1: CHUNKER ─────────────────────────────────────────────────────────

def chunker(texto: str, chunk_size: int = 200, overlap: int = 40) -> list:
    """
    Divide texto en chunks por palabras con solapamiento.
    Intenta no cortar en medio de frases usando puntuación como guía.
    """
    palabras = texto.split()
    chunks = []
    inicio = 0

    while inicio < len(palabras):
        fin = min(inicio + chunk_size, len(palabras))
        chunk = " ".join(palabras[inicio:fin])
        chunks.append(chunk)
        inicio += chunk_size - overlap

    return chunks


# ─── PARTE 2: RAG MANUAL (sin vectores, búsqueda por palabras clave) ──────────

def similitud_palabras(query: str, texto: str) -> float:
    """Similitud simple basada en palabras compartidas (tf-idf simplificado)."""
    stop = {"de", "la", "el", "en", "y", "a", "los", "las", "por", "con", "se", "su", "que"}
    q_words = set(query.lower().split()) - stop
    t_words = set(texto.lower().split()) - stop
    if not q_words:
        return 0.0
    return len(q_words & t_words) / len(q_words)


def recuperar_chunks(query: str, documentos: list, top_k: int = 3) -> list:
    """Recupera los chunks más relevantes para la query."""
    candidatos = []
    for doc in documentos:
        chunks = chunker(doc["texto"])
        for i, chunk in enumerate(chunks):
            score = similitud_palabras(query, chunk)
            candidatos.append({
                "doc_id":   doc["id"],
                "titulo":   doc["titulo"],
                "chunk_id": i,
                "texto":    chunk,
                "score":    score,
            })

    return sorted(candidatos, key=lambda x: x["score"], reverse=True)[:top_k]


def rag_responder(query: str, documentos: list) -> dict:
    """Pipeline RAG completo: recupera chunks y genera respuesta citando fuentes."""
    chunks = recuperar_chunks(query, documentos, top_k=3)
    contexto = "\n\n".join([
        f"[Fuente: {c['titulo']}]\n{c['texto']}"
        for c in chunks if c["score"] > 0
    ])

    if not contexto:
        return {"respuesta": "No encontré información relevante en la base documental.", "chunks": []}

    try:
        import anthropic
        client = anthropic.Anthropic()
        prompt = f"""Responde la siguiente pregunta ÚNICAMENTE basándote en el contexto proporcionado.
Si la respuesta no está en el contexto, di "No dispongo de esa información en la base documental".
Cita la fuente al final de la respuesta entre corchetes.

CONTEXTO:
{contexto}

PREGUNTA: {query}"""

        resp = client.messages.create(
            model=MODELO, max_tokens=300, temperature=0.0,
            messages=[{"role": "user", "content": prompt}]
        )
        return {
            "respuesta": resp.content[0].text.strip(),
            "chunks_usados": [c["titulo"] for c in chunks if c["score"] > 0],
            "scores": [(c["titulo"][:40], round(c["score"], 3)) for c in chunks],
        }
    except Exception as e:
        return {"respuesta": f"Error: {e}", "chunks": []}


# ─── PARTE 3: RAG CON CHROMA (vectores reales) ───────────────────────────────

def rag_con_chroma(query: str, documentos: list) -> dict:
    """RAG real usando Chroma para almacenamiento vectorial."""
    try:
        import chromadb
        client_chroma = chromadb.Client()

        # Crear/obtener colección
        try:
            coleccion = client_chroma.get_collection("base_documental")
        except:
            coleccion = client_chroma.create_collection("base_documental")

            # Indexar documentos
            ids, textos, metadatos = [], [], []
            for doc in documentos:
                chunks = chunker(doc["texto"])
                for i, chunk in enumerate(chunks):
                    ids.append(f"{doc['id']}_{i}")
                    textos.append(chunk)
                    metadatos.append({"titulo": doc["titulo"], "doc_id": doc["id"]})

            coleccion.add(documents=textos, ids=ids, metadatas=metadatos)

        # Buscar
        resultados = coleccion.query(query_texts=[query], n_results=3)
        chunks_texto = resultados["documents"][0]
        chunks_meta  = resultados["metadatas"][0]

        return {
            "chunks_recuperados": [
                {"titulo": m["titulo"], "texto": t[:150] + "..."}
                for t, m in zip(chunks_texto, chunks_meta)
            ],
            "nota": "Chroma usa embeddings locales por defecto (sin API key)"
        }
    except ImportError:
        return {"error": "pip install chromadb"}
    except Exception as e:
        return {"error": str(e)}


# ─── MAIN ─────────────────────────────────────────────────────────────────────

PREGUNTAS_TEST = [
    "¿Cuánto tiempo tengo para devolver un producto?",
    "¿Hay descuentos para pedidos grandes de empresa?",
    "¿Cómo puedo ejercer mis derechos de privacidad?",
    "¿Cuál es el plazo de entrega estándar?",
]

if __name__ == "__main__":

    print("=" * 64)
    print("LAB 4.1 — Fundamentos de RAG")
    print("=" * 64)

    # ── EJERCICIO 1: Chunker ─────────────────────────────────────────────────
    print("\n[1] CHUNKER — División de documentos")
    print("-" * 64)
    doc_ejemplo = DOCUMENTOS[0]
    chunks = chunker(doc_ejemplo["texto"], chunk_size=50, overlap=10)
    print(f"\n  Documento: {doc_ejemplo['titulo']}")
    print(f"  Palabras totales: {len(doc_ejemplo['texto'].split())}")
    print(f"  Chunks generados: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"\n  [Chunk {i+1}] ({len(chunk.split())} palabras)")
        print(f"  {chunk[:150]}...")

    # ── EJERCICIO 2: RAG manual ──────────────────────────────────────────────
    print("\n\n[2] RAG MANUAL — Recuperación por palabras clave")
    print("-" * 64)

    for pregunta in PREGUNTAS_TEST[:2]:
        chunks_r = recuperar_chunks(pregunta, DOCUMENTOS, top_k=2)
        print(f"\n  Pregunta: {pregunta}")
        for c in chunks_r:
            print(f"  Score {c['score']:.2f} | {c['titulo'][:50]}")
            print(f"    {c['texto'][:100]}...")

    # ── EJERCICIO 3: RAG completo con generación ─────────────────────────────
    print("\n\n[3] RAG COMPLETO — Recuperación + Generación")
    print("-" * 64)

    tiene_api = bool(os.getenv("ANTHROPIC_API_KEY"))

    if tiene_api:
        for pregunta in PREGUNTAS_TEST:
            print(f"\n  Q: {pregunta}")
            r = rag_responder(pregunta, DOCUMENTOS)
            print(f"  A: {r['respuesta']}")
            print(f"  Fuentes: {r.get('chunks_usados', [])}")
    else:
        print("\n  NOTA: Configura ANTHROPIC_API_KEY para la generación de respuestas.")
        print("  La recuperación funciona sin API. El generador necesita Claude.")

    # ── EJERCICIO 4: RAG con Chroma ──────────────────────────────────────────
    print("\n\n[4] RAG CON CHROMA (embeddings reales)")
    print("-" * 64)
    r_chroma = rag_con_chroma(PREGUNTAS_TEST[0], DOCUMENTOS)
    if "error" in r_chroma:
        print(f"\n  {r_chroma['error']}")
    else:
        print(f"\n  Pregunta: {PREGUNTAS_TEST[0]}")
        for c in r_chroma.get("chunks_recuperados", []):
            print(f"  [{c['titulo'][:50]}] {c['texto']}")
        print(f"\n  {r_chroma.get('nota','')}")

    print("\n[FIN DEL LAB 4.1]")
