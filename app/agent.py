"""
Agente de Inteligência Artificial para a Wiki Bambu Lab Brasil.
Suporta:
- RAG (Retrieval-Augmented Generation) sobre 2.486 artigos no SQLite FTS5
- Streaming em tempo real (Server-Sent Events)
- Diagnóstico por Foto (Gemini Vision Multimodal)
- Histórico de Conversação Multi-Turn
- Fallback automático entre modelos Gemini Flash
"""

import json
import logging
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Generator, List, Optional, Tuple

from app.config import AUTO_FALLBACK_ORDER, GEMINI_API_KEY, SUPPORTED_MODELS
from crawler.build_db import DB_FILE, get_article, get_connection, search_articles

logger = logging.getLogger("bambu_agent")

SYSTEM_PROMPT = """Você é o Assistente Especialista Oficial da Wiki Bambu Lab Brasil (PT-BR).
Sua missão é responder com máxima precisão, didática e clareza técnica a perguntas sobre todo o ecossistema Bambu Lab documentado em nossa base técnica oficial, que inclui:
- Séries de impressoras: Linhas X1 (X1-Carbon, X1E), X2D, P1 (P1P, P1S), P2S, A1, A1 Mini, A2L (grande formato com módulo de corte/caneta), Séries H2 (H2, H2S, H2C, H2D, H2D-Pro).
- Sistemas de alimentação e filamento: AMS, AMS Lite, AMS 2 Pro, AMS HT.
- Softwares e firmware: Bambu Studio, aplicativo móvel Bambu Handy, MakerWorld.
- Manutenção periódica, calibração, diagnósticos de defeitos de impressão e decodificação de erros HMS.

Diretrizes obrigatórias:
1. Baseie suas respostas prioritariamente no CONTEXTO TÉCNICO fornecido abaixo, extraído diretamente da Wiki Bambu Lab.
2. IMPORTANTE: Modelos como A2L, X2D, H2/H2S e P2S são produtos oficiais com manuais e documentação técnica presentes nesta Wiki. Nunca afirme que um produto ou termo documentado "não existe". Se o usuário perguntar sobre a A2L ou colar um link de uma impressora, explique suas características, especificações e guias conforme o contexto.
3. Caso o usuário envie uma imagem, examine cuidadosamente a foto para identificar o defeito (ex: espaguete/cabeleira, descolamento/warping, entupimento de bico/hotend, subextrusão, desalinhamento de camadas) e forneça o diagnóstico e os passos para resolução.
4. Forneça procedimentos práticos em passos claros e numerados.
5. Cite sempre os artigos técnicos relevantes usando links em markdown: [Nome do Guia](/wiki/caminho-do-artigo).
6. Responda sempre em Português do Brasil com tom cordial, profissional e focado na solução prática.
"""

PT_STOPWORDS = {
    "a", "o", "as", "os", "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas",
    "por", "para", "com", "sem", "um", "uma", "uns", "umas", "meu", "minha", "meus", "minhas",
    "seu", "sua", "seus", "suas", "este", "esta", "estes", "estas", "esse", "essa", "esses", "essas",
    "que", "quem", "qual", "quais", "onde", "como", "quando", "quanto", "porque", "se", "mas", "e", "ou",
    "já", "ainda", "está", "estou", "estão", "é", "são", "foi", "foram", "era", "ser", "estar", "ter",
    "tem", "têm", "fazer", "faz", "criando", "acontecendo", "deu", "dar"
}

SYNONYMS = {
    "cabeleira": ["espaguete", "descolamento", "primeira camada", "adesão"],
    "espaguete": ["cabeleira", "spaghetti", "descolamento", "primeira camada"],
    "spaghetti": ["espaguete", "cabeleira", "descolamento"],
    "entupimento": ["hotend", "bico", "clog", "extrusora"],
    "entupido": ["hotend", "bico", "clog", "extrusora"],
    "descolando": ["primeira camada", "adesão", "mesa", "PEI", "warping"],
    "descolamento": ["primeira camada", "adesão", "mesa", "PEI"],
    "warping": ["empenamento", "primeira camada", "borda", "brim"],
    "empenando": ["warping", "primeira camada", "mesa", "brim"],
}


def clean_query_keywords(query: str) -> List[str]:
    """Remove stopwords e retorna palavras-chave limpas preservando códigos como A1, X1, A2L."""
    raw_tokens = re.findall(r'[a-zA-Z0-9_\-]+', query)
    return [
        t.lower().strip("-") for t in raw_tokens
        if len(t.strip("-")) >= 2
        and t.lower().strip("-") not in PT_STOPWORDS
        and t.lower().strip("-") not in ["http", "https", "com", "wiki", "bambulab", "link", "www"]
    ]


def retrieve_wiki_context(
    query: str,
    current_path: Optional[str] = None,
    limit: int = 4
) -> Tuple[str, List[Dict[str, str]]]:
    """
    Busca os artigos mais relevantes no banco SQLite com:
    1. Extração e resolução de links/URLs completos ou parciais (ex: https://wiki.bambulab.com/en/a2l, /wiki/a2l).
    2. Correspondência direta por caminho exato ou seção raiz (ex: 'a2l', 'x1', 'ams').
    3. Contexto da página atualmente navegada pelo usuário (current_path).
    4. Busca textual FTS5 com expansão de sinônimos e termos alfanuméricos curtos (ex: A1, P1, X1, A2L).
    """
    extracted_paths: List[str] = []

    # 1. Detecta URLs ou caminhos da wiki na pergunta
    url_pattern = re.compile(r'https?://[^\s<>\"\'()]+|/wiki/[^\s<>\"\'()]+', re.IGNORECASE)
    urls = url_pattern.findall(query)
    for u in urls:
        parsed = urllib.parse.urlparse(u)
        path = parsed.path.strip("/")
        for prefix in ["en/", "pt-br/", "zh-cn/", "wiki/"]:
            if path.startswith(prefix):
                path = path[len(prefix):]
        if path:
            extracted_paths.append(path)

    # Adiciona a página atual em que o usuário está, se informada
    if current_path:
        clean_cp = current_path.strip("/").replace("wiki/", "")
        if clean_cp and clean_cp not in extracted_paths and not clean_cp.startswith(("chat", "hms", "filamentos", "search")):
            extracted_paths.append(clean_cp)

    # 2. Limpar query para FTS5 removendo URLs para não gerar erro de sintaxe
    clean_text = query
    for u in urls:
        clean_text = clean_text.replace(u, " ")

    raw_tokens = re.findall(r'[a-zA-Z0-9_\-]+', clean_text)
    keywords = [
        t.lower().strip("-") for t in raw_tokens
        if len(t.strip("-")) >= 2
        and t.lower().strip("-") not in PT_STOPWORDS
        and t.lower().strip("-") not in ["http", "https", "com", "wiki", "bambulab", "link", "www"]
    ]

    # Também adiciona partes dos caminhos extraídos (ex: 'a2l', 'intro')
    for ep in extracted_paths:
        for part in ep.split("/"):
            part_clean = part.lower().strip("-")
            if len(part_clean) >= 2 and part_clean not in keywords and part_clean not in PT_STOPWORDS:
                keywords.append(part_clean)

    found_articles: List[Dict[str, Any]] = []
    seen_paths = set()

    # 3. Busca direta por caminhos extraídos e seções raiz
    for p in extracted_paths:
        art = get_article(p, db_path=DB_FILE)
        if art and art["path"] not in seen_paths:
            found_articles.append(art)
            seen_paths.add(art["path"])

        with get_connection(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, path, section, subsection, title, description, plain_text FROM articles WHERE path LIKE ? OR section = ? LIMIT ?",
                (f"{p}/%", p, limit)
            )
            for sub_row in cursor.fetchall():
                sub_dict = dict(sub_row)
                if sub_dict["path"] not in seen_paths:
                    found_articles.append(sub_dict)
                    seen_paths.add(sub_dict["path"])
                if len(found_articles) >= limit:
                    break

    # 4. Busca textual FTS5
    if len(found_articles) < limit and keywords:
        clean_query = " ".join(keywords)
        search_results = search_articles(clean_query, limit=limit * 2, db_path=DB_FILE)

        if len(search_results) < 2:
            expanded_terms = []
            for w in keywords:
                if w in SYNONYMS:
                    expanded_terms.extend(SYNONYMS[w])
            if expanded_terms:
                extra = search_articles(" ".join(expanded_terms[:3]), limit=limit, db_path=DB_FILE)
                search_results.extend(extra)

        for sr in search_results:
            if sr["path"] not in seen_paths:
                art = get_article(sr["path"], db_path=DB_FILE)
                if art:
                    found_articles.append(art)
                    seen_paths.add(sr["path"])
            if len(found_articles) >= limit:
                break

    # 5. Fallback palavra por palavra
    if not found_articles and keywords:
        for w in keywords:
            res = search_articles(w, limit=limit, db_path=DB_FILE)
            for sr in res:
                if sr["path"] not in seen_paths:
                    art = get_article(sr["path"], db_path=DB_FILE)
                    if art:
                        found_articles.append(art)
                        seen_paths.add(sr["path"])
                if len(found_articles) >= limit:
                    break
            if found_articles:
                break

    context_parts = []
    sources = []

    for art in found_articles[:limit]:
        title = art.get("title", "Guia")
        path = art.get("path", "")
        desc = art.get("description", "")
        plain = (art.get("plain_text") or "")[:1800]

        source_info = {
            "title": title,
            "path": f"/wiki/{path}",
            "section": art.get("section", "")
        }
        sources.append(source_info)

        context_parts.append(
            f"--- ARTIGO: {title} (Link: /wiki/{path}) ---\n"
            f"Seção: {art.get('section', '')}\n"
            f"Descrição: {desc}\n"
            f"Conteúdo:\n{plain}\n"
        )

    context_str = "\n".join(context_parts) if context_parts else "Nenhum artigo específico encontrado para esta busca."
    return context_str, sources


def build_contents_payload(
    question: str,
    context_text: str,
    history: Optional[List[Dict[str, str]]] = None,
    image_b64: Optional[str] = None,
    mime_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Monta a lista de contents com histórico, contexto e imagem opcional."""
    contents = []

    # Se houver histórico anterior, insere as rodadas passadas
    if history:
        for turn in history[-6:]:  # Mantém as últimas 3 interações
            role = turn.get("role", "user")
            text = turn.get("text", "")
            if text:
                contents.append({
                    "role": "model" if role in ("model", "bot", "assistant") else "user",
                    "parts": [{"text": text}]
                })

    # Mensagem atual do usuário com contexto injetado
    user_parts = []
    if image_b64 and mime_type:
        user_parts.append({
            "inlineData": {
                "mimeType": mime_type,
                "data": image_b64
            }
        })

    prompt_text = (
        f"CONTEXTO EXTRAÍDO DA WIKI BAMBU LAB:\n"
        f"{context_text}\n\n"
        f"PERGUNTA DO USUÁRIO:\n"
        f"{question.strip()}\n\n"
        f"Responda detalhadamente em português com base no contexto e na imagem (se fornecida), citando os manuais da Wiki com links [Título](/wiki/caminho)."
    )
    user_parts.append({"text": prompt_text})

    contents.append({
        "role": "user",
        "parts": user_parts
    })

    return contents


def ask_agent(
    question: str,
    selected_model: str = "auto",
    history: Optional[List[Dict[str, str]]] = None,
    image_b64: Optional[str] = None,
    mime_type: Optional[str] = None,
    current_path: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Resposta síncrona/completa do agente."""
    if not question or not question.strip():
        return {
            "answer": "Por favor, digite uma pergunta para que eu possa pesquisar na Wiki Bambu Lab.",
            "model_used": "none",
            "sources": [],
            "status": "error"
        }

    active_key = (api_key or "").strip() or GEMINI_API_KEY
    if not active_key:
        return {
            "answer": "⚠️ **Nenhuma chave da API Gemini informada.**\n\nPor favor, insira sua chave gratuita do Google Gemini no menu de configurações do chat (ícone ⚙️) para conversar com a IA. Você pode gerar uma chave gratuita em [aistudio.google.com](https://aistudio.google.com/).",
            "model_used": "none",
            "sources": [],
            "status": "error"
        }

    context_text, sources = retrieve_wiki_context(question, current_path=current_path, limit=4)
    contents = build_contents_payload(question, context_text, history, image_b64, mime_type)

    if selected_model == "auto" or selected_model not in SUPPORTED_MODELS:
        models_to_try = AUTO_FALLBACK_ORDER
        is_auto = True
    else:
        models_to_try = [selected_model] + [m for m in AUTO_FALLBACK_ORDER if m != selected_model]
        is_auto = False

    last_error = None
    for model_name in models_to_try:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={active_key}"
            payload = {
                "contents": contents,
                "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2048}
            }
            timeout = 25 if ("3.8" in model_name or "3.7" in model_name or image_b64) else 15
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "answer": text,
                    "model_used": model_name,
                    "is_auto": is_auto,
                    "sources": sources,
                    "status": "success"
                }
        except urllib.error.HTTPError as e:
            try:
                err_json = json.loads(e.read().decode("utf-8"))
                last_error = err_json.get("error", {}).get("message", str(e))
            except Exception:
                last_error = str(e)
            print(f"Aviso: Modelo {model_name} falhou com HTTP {e.code}: {last_error}", flush=True)
            if "leaked" in last_error.lower() or "not valid" in last_error.lower():
                break
            continue
        except Exception as e:
            last_error = str(e)
            print(f"Aviso: Modelo {model_name} falhou ({e}). Tentando próximo...", flush=True)
            continue

    if last_error and "leaked" in last_error.lower():
        msg = "⚠️ **Chave do Gemini Bloqueada pelo Google:**\n\nSua chave de API foi reportada pelo Google como vazada publicamente no GitHub e revogada por segurança. Por favor, gere uma nova chave em [aistudio.google.com](https://aistudio.google.com/) e salve-a no ícone ⚙️ acima."
    elif last_error and "not valid" in last_error.lower():
        msg = "⚠️ **Chave da API Gemini Inválida:**\n\nVerifique se a chave digitada está correta no menu de configurações (ícone ⚙️)."
    else:
        msg = f"Desculpe, ocorreu uma instabilidade ao conectar ao Gemini: {last_error}. Tente novamente em instantes."

    return {
        "answer": msg,
        "model_used": "failed",
        "sources": sources,
        "status": "error"
    }


# Alias de compatibilidade
ask_gemini_agent = ask_agent


def stream_agent_response(
    question: str,
    selected_model: str = "auto",
    history: Optional[List[Dict[str, str]]] = None,
    image_b64: Optional[str] = None,
    mime_type: Optional[str] = None,
    current_path: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Generator[str, None, None]:
    """
    Gerador para Server-Sent Events (SSE) transmitindo a resposta token a token em tempo real.
    """
    active_key = (api_key or "").strip() or GEMINI_API_KEY
    if not active_key:
        yield f"data: {json.dumps({'type': 'error', 'message': 'Nenhuma chave da API Gemini configurada. Insira sua chave no ícone ⚙️ para conversar com a IA.'})}\n\n"
        return

    context_text, sources = retrieve_wiki_context(question, current_path=current_path, limit=4)
    contents = build_contents_payload(question, context_text, history, image_b64, mime_type)

    if selected_model == "auto" or selected_model not in SUPPORTED_MODELS:
        models_to_try = AUTO_FALLBACK_ORDER
    else:
        models_to_try = [selected_model] + [m for m in AUTO_FALLBACK_ORDER if m != selected_model]

    last_error = None
    for model_name in models_to_try:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:streamGenerateContent?alt=sse&key={active_key}"
            payload = {
                "contents": contents,
                "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2048}
            }
            timeout = 30 if ("3.8" in model_name or "3.7" in model_name or image_b64) else 20
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )

            with urllib.request.urlopen(req, timeout=timeout) as response:
                first_chunk = True
                for line in response:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("data: "):
                        data_chunk = json.loads(line_str[6:].strip())
                        parts = data_chunk.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                        if parts and "text" in parts[0]:
                            chunk_text = parts[0]["text"]
                            if first_chunk:
                                yield f"data: {json.dumps({'type': 'init', 'model': model_name, 'sources': sources})}\n\n"
                                first_chunk = False
                            yield f"data: {json.dumps({'type': 'token', 'token': chunk_text})}\n\n"

                if not first_chunk:
                    yield f"data: {json.dumps({'type': 'done'})}\n\n"
                    return
        except urllib.error.HTTPError as e:
            try:
                err_json = json.loads(e.read().decode("utf-8"))
                last_error = err_json.get("error", {}).get("message", str(e))
            except Exception:
                last_error = str(e)
            print(f"Streaming falhou com {model_name} HTTP {e.code}: {last_error}", flush=True)
            if "leaked" in last_error.lower() or "not valid" in last_error.lower():
                break
            continue
        except Exception as e:
            last_error = str(e)
            print(f"Streaming falhou com {model_name} ({e}). Tentando próximo modelo...", flush=True)
            continue

    # Fallback final com generateContent síncrono dividido em tokens caso alt=sse falhe
    try:
        res = ask_agent(question, selected_model=selected_model, history=history, image_b64=image_b64, mime_type=mime_type, current_path=current_path, api_key=active_key)
        if res.get("status") == "success":
            yield f"data: {json.dumps({'type': 'init', 'model': res.get('model_used', 'gemini'), 'sources': res.get('sources', [])})}\n\n"
            answer = res.get("answer", "")
            words = answer.split(" ")
            for i in range(0, len(words), 3):
                chunk = " ".join(words[i:i+3]) + (" " if i+3 < len(words) else "")
                yield f"data: {json.dumps({'type': 'token', 'token': chunk})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return
        elif res.get("answer"):
            last_error = res.get("answer")
    except Exception as e:
        print(f"Fallback síncrono também falhou: {e}", flush=True)
        last_error = str(e)

    if last_error and "leaked" in str(last_error).lower():
        err_msg = "Sua chave da API Gemini foi bloqueada pelo Google (detectada como pública no GitHub). Por favor, gere uma nova chave em aistudio.google.com e configure-a no ícone ⚙️."
    elif last_error and "not valid" in str(last_error).lower():
        err_msg = "Chave da API Gemini inválida. Por favor, verifique a chave inserida no ícone ⚙️."
    else:
        err_msg = f"Instabilidade na API do Gemini: {last_error or 'Tente novamente em instantes'}."

    yield f"data: {json.dumps({'type': 'error', 'message': err_msg})}\n\n"
