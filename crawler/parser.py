"""
Módulo de parsing e limpeza de conteúdo HTML da Wiki Bambu Lab.
Extrai metadados, estrutura de navegação (sidebar), sumário (TOC) e conteúdo HTML.
"""

import base64
import json
import re
from typing import Any, Dict, List, Optional, Tuple
from bs4 import BeautifulSoup

BAMBU_BASE_URL = "https://wiki.bambulab.com"


def parse_wiki_page(html: str, target_lang: str = "pt-br") -> Optional[Dict[str, Any]]:
    """
    Faz o parsing de uma página HTML da Wiki Bambu Lab (Wiki.js).
    Retorna um dicionário com metadados estruturados e HTML limpo.
    """
    if not html:
        return None

    # 1. Extrair atributos da tag <page>
    page_match = re.search(r"<page\s+([^>]+)>", html)
    attrs: Dict[str, str] = {}
    if page_match:
        raw_attrs = page_match.group(1)
        for k, v in re.findall(r'([\w\-:]+)=\"([^\"]*)\"', raw_attrs):
            attrs[k] = v

    # Fallback para título se <page> não tiver
    title = attrs.get("title")
    if not title:
        title_tag_match = re.search(r"<title>(.*?)(?:\s*\|\s*Bambu Lab Wiki)?</title>", html, re.IGNORECASE)
        title = title_tag_match.group(1).strip() if title_tag_match else "Sem Título"

    # Fallback para descrição
    description = attrs.get("description", "")
    if not description:
        desc_match = re.search(r'<meta name="description" content="([^"]*)"', html, re.IGNORECASE)
        description = desc_match.group(1).strip() if desc_match else ""

    path = attrs.get("path", "")
    if not path:
        # Tenta extrair de canonical ou og:url
        url_match = re.search(r'<meta property="og:url" content="https?://wiki\.bambulab\.com/[^/]+/([^"]+)"', html)
        path = url_match.group(1).strip() if url_match else ""

    # Extrai seções do caminho (ex: "x1/manual/intro-x1" -> section="x1", subsection="manual", slug="intro-x1")
    path_parts = [p for p in path.split("/") if p]
    section = path_parts[0] if path_parts else "geral"
    subsection = path_parts[1] if len(path_parts) > 2 else None
    slug = path_parts[-1] if path_parts else "home"

    # 2. Extrair e decodificar Sumário (TOC)
    toc_data = []
    if "toc" in attrs and attrs["toc"]:
        try:
            toc_json = base64.b64decode(attrs["toc"]).decode("utf-8")
            toc_data = json.loads(toc_json)
        except Exception:
            toc_data = []

    # 3. Extrair e decodificar Sidebar de navegação
    sidebar_data = []
    if "sidebar" in attrs and attrs["sidebar"]:
        try:
            sidebar_json = base64.b64decode(attrs["sidebar"]).decode("utf-8")
            sidebar_data = json.loads(sidebar_json)
        except Exception:
            sidebar_data = []

    # 4. Extrair o conteúdo do artigo (<template slot="contents">)
    content_match = re.search(r'<template slot="contents"><div>(.*?)</div></template>', html, re.DOTALL)
    if content_match:
        raw_body = content_match.group(1)
    else:
        # Fallback para <div class="contents"> ou <body>
        soup = BeautifulSoup(html, "html.parser")
        main_el = soup.find("div", class_="contents") or soup.find("main") or soup.find("body")
        raw_body = str(main_el) if main_el else ""

    cleaned_html, plain_text = clean_and_rewrite_content(raw_body)

    return {
        "path": path,
        "slug": slug,
        "section": section,
        "subsection": subsection,
        "title": title,
        "description": description,
        "toc": toc_data,
        "sidebar": sidebar_data,
        "html_content": cleaned_html,
        "plain_text": plain_text,
        "created_at": attrs.get("created-at"),
        "updated_at": attrs.get("updated-at"),
        "author": attrs.get("author-name", "Bambu Lab"),
    }


def clean_and_rewrite_content(raw_html: str) -> Tuple[str, str]:
    """
    Limpa o HTML do artigo:
    - Transforma URLs relativas de imagens em URLs absolutas oficiais da Bambu Lab
    - Reescreve links internos (/pt-br/... ou /en/...) para /wiki/...
    - Extrai texto puro para busca FTS5
    """
    if not raw_html:
        return "", ""

    soup = BeautifulSoup(raw_html, "html.parser")

    # Reescreve imagens
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src.startswith("/"):
            img["src"] = f"{BAMBU_BASE_URL}{src}"
        # Adiciona estilos/classes para imagens responsivas e bonitas
        classes = img.get("class", [])
        if "img-fluid" not in classes:
            classes.append("img-fluid")
        img["class"] = classes
        img["loading"] = "lazy"

    # Reescreve links internos
    for a in soup.find_all("a"):
        href = a.get("href", "")
        if href.startswith("/pt-br/") or href.startswith("/en/"):
            parts = href.split("/", 2)
            if len(parts) >= 3:
                a["href"] = f"/wiki/{parts[2]}"
        elif href.startswith("https://wiki.bambulab.com/pt-br/") or href.startswith("https://wiki.bambulab.com/en/"):
            subpath = re.sub(r"^https://wiki\.bambulab\.com/(?:pt-br|en)/", "", href)
            a["href"] = f"/wiki/{subpath}"

    cleaned_html = str(soup)
    plain_text = soup.get_text(separator=" ", strip=True)

    return cleaned_html, plain_text
