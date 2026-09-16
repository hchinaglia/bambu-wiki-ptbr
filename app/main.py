"""
Aplicação Web FastAPI para a Wiki Bambu Lab em Português (PT-BR).
"""

import os
from typing import Optional
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from crawler.build_db import (
    DB_FILE,
    get_article,
    get_articles_by_section,
    get_connection,
    get_sections_summary,
    init_db,
    search_articles,
)
from app.agent import ask_agent, stream_agent_response
from app.config import SUPPORTED_MODELS
from app.hms_data import HMS_DATABASE, search_hms_codes
from app.filament_data import FILAMENT_DATABASE, get_filaments

app = FastAPI(
    title="Wiki Bambu Lab PT-BR",
    description="Portal de Documentação da Bambu Lab em Português do Brasil.",
    version="1.0.0"
)

# Inicializa banco de dados apenas se não estiver no Vercel (onde o FS é read-only)
if os.environ.get("VERCEL") != "1":
    try:
        init_db(DB_FILE)
    except Exception:
        pass

# Configura arquivos estáticos e templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

try:
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(os.path.join(STATIC_DIR, "css"), exist_ok=True)
    os.makedirs(os.path.join(STATIC_DIR, "js"), exist_ok=True)
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
except Exception:
    pass

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": exc.__class__.__name__,
            "traceback": traceback.format_exc(),
            "db_file": str(DB_FILE),
            "db_exists": os.path.exists(DB_FILE) if DB_FILE else False,
        }
    )

# Mapeamento e taxonomia de seções com nomes em português e ícones
SECTION_CONFIG = {
    "x1": {"name": "Série X (X1 / X1-Carbon)", "icon": "bi-cpu", "group": "Hardware"},
    "x2d": {"name": "Série X2 (X2D)", "icon": "bi-cpu-fill", "group": "Hardware"},
    "p1": {"name": "Série P (P1P / P1S)", "icon": "bi-box-seam", "group": "Hardware"},
    "p2s": {"name": "Série P2 (P2S)", "icon": "bi-box-seam-fill", "group": "Hardware"},
    "a1": {"name": "Série A (A1)", "icon": "bi-printer", "group": "Hardware"},
    "a1-mini": {"name": "A1 Mini", "icon": "bi-printer-fill", "group": "Hardware"},
    "a2l": {"name": "Série A2 (A2L)", "icon": "bi-printer", "group": "Hardware"},
    "h2": {"name": "Série H (H2)", "icon": "bi-shield-check", "group": "Hardware"},
    "h2c": {"name": "Série H2C", "icon": "bi-shield", "group": "Hardware"},
    "h2s": {"name": "Série H2S", "icon": "bi-shield-shaded", "group": "Hardware"},
    "h2d": {"name": "Série H2D", "icon": "bi-shield-plus", "group": "Hardware"},
    "ams": {"name": "Sistema AMS Padrão", "icon": "bi-palette", "group": "AMS & Acessórios"},
    "ams-2-pro": {"name": "AMS 2 Pro", "icon": "bi-palette-fill", "group": "AMS & Acessórios"},
    "ams-ht": {"name": "AMS HT", "icon": "bi-palette2", "group": "AMS & Acessórios"},
    "ams-lite": {"name": "AMS Lite", "icon": "bi-vinyl", "group": "AMS & Acessórios"},
    "software": {"name": "Software & Apps", "icon": "bi-laptop", "group": "Software"},
    "bambu-studio": {"name": "Bambu Studio", "icon": "bi-window-stack", "group": "Software"},
    "filament-acc": {"name": "Filamentos & Acessórios", "icon": "bi-layers", "group": "Materiais & Consumíveis"},
    "makerworld": {"name": "MakerWorld & Modelos", "icon": "bi-globe", "group": "Ecossistema"},
    "cyberbrick": {"name": "CyberBrick", "icon": "bi-bricks", "group": "Ecossistema"},
    "general": {"name": "Geral & Manutenção", "icon": "bi-tools", "group": "Guias & Suporte"},
    "knowledge-sharing": {"name": "Base de Conhecimento", "icon": "bi-book", "group": "Guias & Suporte"},
}


def get_navigation_tree():
    """Gera a árvore de navegação para a barra lateral esquerda."""
    sections_summary = get_sections_summary(DB_FILE)
    counts = {s["section"]: s["count"] for s in sections_summary}

    groups = {}
    configured_ids = set()

    for sec_id, info in SECTION_CONFIG.items():
        configured_ids.add(sec_id)
        group_name = info["group"]
        if group_name not in groups:
            groups[group_name] = []
        groups[group_name].append({
            "id": sec_id,
            "name": info["name"],
            "icon": info["icon"],
            "count": counts.get(sec_id, 0),
            "url": f"/wiki/{sec_id}"
        })

    # Adiciona seções adicionais encontradas no banco
    other_sections = []
    for s in sections_summary:
        sec_id = s["section"]
        if sec_id not in configured_ids and s["count"] > 1:
            other_sections.append({
                "id": sec_id,
                "name": sec_id.replace("-", " ").title(),
                "icon": "bi-folder",
                "count": s["count"],
                "url": f"/wiki/{sec_id}"
            })

    if other_sections:
        groups["Outros Guias"] = other_sections

    return groups


@app.get("/", response_class=HTMLResponse)
@app.get("/api/index.py", response_class=HTMLResponse)
@app.get("/api/index", response_class=HTMLResponse)
@app.get("/api", response_class=HTMLResponse)
async def home(request: Request):
    """Página inicial no mesmo estilo da Home da Bambu Lab."""
    with get_connection(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM articles")
        total_articles = cursor.fetchone()[0]

        cursor.execute("""
            SELECT path, section, subsection, title, description, updated_at 
            FROM articles 
            ORDER BY id DESC 
            LIMIT 6
        """)
        recent_articles = [dict(r) for r in cursor.fetchall()]

    nav_tree = get_navigation_tree()

    return templates.TemplateResponse("home.html", {
        "request": request,
        "total_articles": total_articles,
        "recent_articles": recent_articles,
        "nav_tree": nav_tree,
        "section_config": SECTION_CONFIG,
    })


@app.get("/wiki/{path:path}", response_class=HTMLResponse)
async def read_article(request: Request, path: str):
    """Visualizador de artigo da documentação."""
    clean_path = path.strip("/")
    article = get_article(clean_path, DB_FILE)

    # Se o caminho for apenas o nome de uma seção (ex: /wiki/x1), mostra o índice da seção
    if not article and clean_path in SECTION_CONFIG:
        section_articles = get_articles_by_section(clean_path, DB_FILE)
        section_info = SECTION_CONFIG.get(clean_path, {"name": clean_path.upper(), "icon": "bi-folder"})
        return templates.TemplateResponse("section.html", {
            "request": request,
            "section_id": clean_path,
            "section_info": section_info,
            "articles": section_articles,
            "nav_tree": get_navigation_tree(),
            "active_path": clean_path
        })

    if not article:
        # Tenta buscar por slug aproximado
        with get_connection(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE slug = ? OR path LIKE ?", (clean_path, f"%{clean_path}%"))
            row = cursor.fetchone()
            if row:
                article = get_article(row["path"], DB_FILE)

    if not article:
        raise HTTPException(status_code=404, detail="Artigo não encontrado na Wiki")

    nav_tree = get_navigation_tree()

    # Breadcrumbs
    path_parts = article["path"].split("/")
    breadcrumbs = [{"name": "Início", "url": "/"}]
    accumulated = ""
    for part in path_parts[:-1]:
        accumulated = f"{accumulated}/{part}" if accumulated else part
        section_title = SECTION_CONFIG.get(part, {}).get("name", part.capitalize())
        breadcrumbs.append({"name": section_title, "url": f"/wiki/{accumulated}"})
    breadcrumbs.append({"name": article["title"], "url": None})

    return templates.TemplateResponse("article.html", {
        "request": request,
        "article": article,
        "breadcrumbs": breadcrumbs,
        "nav_tree": nav_tree,
        "active_path": article["path"],
        "section_info": SECTION_CONFIG.get(article["section"], {"name": article["section"].upper(), "icon": "bi-file-text"}),
    })


@app.get("/search", response_class=HTMLResponse)
async def search_page(request: Request, q: str = Query("", alias="q"), series: Optional[str] = Query(None)):
    """Página com resultados detalhados de busca e filtro opcional por série."""
    raw_results = search_articles(q, limit=60, db_path=DB_FILE) if q else []
    
    # Filtro opcional por modelo/série de impressora
    if series and series.lower() != "todas":
        s_clean = series.lower()
        results = [r for r in raw_results if s_clean in r["section"].lower() or (r.get("subsection") and s_clean in r["subsection"].lower())]
    else:
        results = raw_results

    return templates.TemplateResponse("search.html", {
        "request": request,
        "query": q,
        "selected_series": series or "todas",
        "results": results,
        "total_results": len(results),
        "nav_tree": get_navigation_tree(),
        "active_path": ""
    })


@app.get("/hms", response_class=HTMLResponse)
async def hms_page(request: Request, q: str = Query("", alias="q")):
    """Página de decodificação de códigos de erro HMS da Bambu Lab."""
    codes = search_hms_codes(q)
    return templates.TemplateResponse("hms.html", {
        "request": request,
        "query": q,
        "hms_codes": codes,
        "nav_tree": get_navigation_tree(),
        "active_path": "hms"
    })


@app.get("/api/hms")
async def api_hms(q: str = Query("")):
    """Endpoint JSON para consulta de códigos HMS."""
    return JSONResponse(search_hms_codes(q))


@app.get("/filamentos", response_class=HTMLResponse)
async def filaments_page(request: Request, printer: Optional[str] = None, category: Optional[str] = None):
    """Página do Guia Interativo de Filamentos e Temperaturas."""
    filaments = get_filaments(printer=printer, category=category)
    return templates.TemplateResponse("filaments.html", {
        "request": request,
        "filaments": filaments,
        "selected_printer": printer or "Todos",
        "selected_category": category or "Todos",
        "nav_tree": get_navigation_tree(),
        "active_path": "filamentos"
    })


@app.get("/api/filamentos")
async def api_filaments(printer: Optional[str] = None, category: Optional[str] = None):
    """Endpoint JSON da tabela de filamentos."""
    return JSONResponse(get_filaments(printer=printer, category=category))


@app.get("/api/search")
async def api_search(q: str = Query(..., min_length=1)):
    """Endpoint JSON de busca rápida para autocomplete na barra superior."""
    results = search_articles(q, limit=10, db_path=DB_FILE)
    return JSONResponse({
        "query": q,
        "total": len(results),
        "results": [
            {
                "title": r["title"],
                "path": f"/wiki/{r['path']}",
                "section": SECTION_CONFIG.get(r["section"], {}).get("name", r["section"]),
                "snippet": r.get("snippet", "")
            }
            for r in results
        ]
    })


@app.get("/api/stats")
async def api_stats():
    """Retorna estatísticas do banco de dados."""
    sections = get_sections_summary(DB_FILE)
    total = sum(s["count"] for s in sections)
    return JSONResponse({
        "total_articles": total,
        "sections": sections
    })


@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Página dedicada do assistente de inteligência artificial da Wiki."""
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "supported_models": SUPPORTED_MODELS,
        "nav_tree": get_navigation_tree(),
        "active_path": "chat"
    })


@app.post("/api/chat")
async def api_chat(request: Request):
    """Endpoint da API para responder perguntas com suporte a texto, imagem (Gemini Vision) e histórico."""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Formato JSON inválido")

    query = (body.get("query") or body.get("question") or "").strip()
    selected_model = body.get("model", "auto")
    history = body.get("history", [])
    image_b64 = body.get("image_b64")
    mime_type = body.get("mime_type")
    current_path = body.get("current_path")

    result = ask_agent(
        query,
        selected_model=selected_model,
        history=history,
        image_b64=image_b64,
        mime_type=mime_type,
        current_path=current_path
    )
    return JSONResponse(result)


@app.post("/api/chat/stream")
async def api_chat_stream(request: Request):
    """Endpoint Server-Sent Events (SSE) para transmissão token a token em tempo real."""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Formato JSON inválido")

    query = (body.get("query") or body.get("question") or "").strip()
    selected_model = body.get("model", "auto")
    history = body.get("history", [])
    image_b64 = body.get("image_b64")
    mime_type = body.get("mime_type")
    current_path = body.get("current_path")

    return StreamingResponse(
        stream_agent_response(
            query,
            selected_model=selected_model,
            history=history,
            image_b64=image_b64,
            mime_type=mime_type,
            current_path=current_path
        ),
        media_type="text/event-stream"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
