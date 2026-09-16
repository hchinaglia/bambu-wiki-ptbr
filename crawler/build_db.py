"""
Módulo de gerenciamento do banco de dados SQLite para a Wiki Bambu Lab.
Inclui criação de tabelas, índices e tabela de busca textual completa FTS5 em português.
"""

import json
import os
import re
import sqlite3
import threading
from typing import Any, Dict, List, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resolve_db_path(db_path: Optional[str] = None) -> str:
    """Procura pelo arquivo do banco em múltiplos diretórios candidatos."""
    if db_path and os.path.exists(db_path) and os.path.getsize(db_path) > 1024 * 1024:
        return os.path.abspath(db_path)

    candidates = [
        os.path.join(BASE_DIR, "wiki_bambu.db"),
        os.path.join(os.getcwd(), "wiki_bambu.db"),
        os.path.abspath("wiki_bambu.db"),
        "/var/task/wiki_bambu.db",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "wiki_bambu.db"),
    ]
    for c in candidates:
        if os.path.exists(c) and os.path.getsize(c) > 1024 * 1024:
            return os.path.abspath(c)
    return os.path.join(BASE_DIR, "wiki_bambu.db")


DB_FILE = resolve_db_path()
DB_LOCK = threading.Lock()


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Retorna uma conexão com SQLite tolerante a ambientes locais e serverless (Vercel)."""
    actual_path = resolve_db_path(db_path)

    # Detecta se estamos em ambiente serverless/read-only como Vercel ou AWS Lambda
    is_serverless = (
        os.environ.get("VERCEL") == "1"
        or os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None
        or "/var/task" in actual_path
        or not os.access(actual_path, os.W_OK)
        or not os.access(os.path.dirname(actual_path) or ".", os.W_OK)
    )

    if is_serverless:
        conn = sqlite3.connect(f"file:{actual_path}?mode=ro", uri=True, timeout=60.0)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA query_only = ON;")
        except Exception:
            pass
        return conn

    try:
        conn = sqlite3.connect(actual_path, timeout=60.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA busy_timeout=60000;")
        try:
            conn.execute("PRAGMA journal_mode=WAL;")
        except Exception:
            pass
        conn.execute("SELECT 1;").fetchone()
        return conn
    except Exception:
        # Fallback definitivo para modo estritamente leitura (read-only)
        conn = sqlite3.connect(f"file:{actual_path}?mode=ro", uri=True, timeout=60.0)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA query_only = ON;")
        except Exception:
            pass
        return conn


def init_db(db_path: str = DB_FILE):
    """Inicializa as tabelas do banco de dados e a busca FTS5 se ainda não existirem."""
    if os.path.exists(db_path) and os.path.getsize(db_path) > 1024 * 1024:
        # Se o banco já existe com dados (ex: em produção/Vercel), não tenta recriar tabelas
        return

    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()

            # Tabela principal de artigos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE NOT NULL,
                    slug TEXT NOT NULL,
                    section TEXT NOT NULL,
                    subsection TEXT,
                    title TEXT NOT NULL,
                    description TEXT,
                    html_content TEXT NOT NULL,
                    plain_text TEXT,
                    toc_json TEXT,
                    sidebar_json TEXT,
                    original_url TEXT NOT NULL,
                    lang TEXT NOT NULL DEFAULT 'pt-br',
                    author TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)

            # Índices para consultas rápidas
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_path ON articles(path)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_section ON articles(section)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_articles_subsection ON articles(subsection)")

            # Tabela virtual FTS5 para busca textual completa
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS articles_search USING fts5(
                    title,
                    description,
                    plain_text,
                    content='articles',
                    content_rowid='id'
                )
            """)

            # Triggers para manter o FTS5 sincronizado automaticamente
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS articles_ai AFTER INSERT ON articles BEGIN
                    INSERT INTO articles_search(rowid, title, description, plain_text)
                    VALUES (new.id, new.title, new.description, new.plain_text);
                END;
            """)
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS articles_ad AFTER DELETE ON articles BEGIN
                    INSERT INTO articles_search(articles_search, rowid, title, description, plain_text)
                    VALUES('delete', old.id, old.title, old.description, old.plain_text);
                END;
            """)
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS articles_au AFTER UPDATE ON articles BEGIN
                    INSERT INTO articles_search(articles_search, rowid, title, description, plain_text)
                    VALUES('delete', old.id, old.title, old.description, old.plain_text);
                    INSERT INTO articles_search(rowid, title, description, plain_text)
                    VALUES (new.id, new.title, new.description, new.plain_text);
                END;
            """)

            conn.commit()
    except Exception as e:
        print(f"Aviso na inicialização do banco ({e}). Continuando...", flush=True)


def save_article(article: Dict[str, Any], db_path: str = DB_FILE) -> int:
    """Insere ou atualiza um artigo no banco de dados com lock para suportar múltiplos workers."""
    with DB_LOCK:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO articles (
                    path, slug, section, subsection, title, description,
                    html_content, plain_text, toc_json, sidebar_json,
                    original_url, lang, author, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(path) DO UPDATE SET
                    title = excluded.title,
                    description = excluded.description,
                    html_content = excluded.html_content,
                    plain_text = excluded.plain_text,
                    toc_json = excluded.toc_json,
                    sidebar_json = excluded.sidebar_json,
                    updated_at = excluded.updated_at
            """, (
                article["path"],
                article["slug"],
                article["section"],
                article.get("subsection"),
                article["title"],
                article.get("description", ""),
                article["html_content"],
                article.get("plain_text", ""),
                json.dumps(article.get("toc", []), ensure_ascii=False),
                json.dumps(article.get("sidebar", []), ensure_ascii=False),
                article.get("original_url", f"https://wiki.bambulab.com/pt-br/{article['path']}"),
                article.get("lang", "pt-br"),
                article.get("author", "Bambu Lab"),
                article.get("created_at"),
                article.get("updated_at")
            ))
            conn.commit()
            return cursor.lastrowid


def get_article(path: str, db_path: str = DB_FILE) -> Optional[Dict[str, Any]]:
    """Recupera um artigo pelo seu caminho relativo (ex: 'x1/manual/intro-x1')."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE path = ?", (path.strip("/"),))
        row = cursor.fetchone()
        if not row:
            return None
        res = dict(row)
        res["toc"] = json.loads(res["toc_json"]) if res.get("toc_json") else []
        res["sidebar"] = json.loads(res["sidebar_json"]) if res.get("sidebar_json") else []
        return res


def search_articles(query: str, limit: int = 20, db_path: str = DB_FILE) -> List[Dict[str, Any]]:
    """Realiza busca textual utilizando FTS5 com ranqueamento bm25."""
    if not query or not query.strip():
        return []

    # Extrai tokens alfanuméricos preservando hífens e modelos (ex: a1, a2l, a1-mini, x1-carbon)
    raw_tokens = re.findall(r'[a-zA-Z0-9_\-]+', query)
    tokens = [t.strip("-") for t in raw_tokens if len(t.strip("-")) >= 2]

    if not tokens:
        return []

    safe_query = " ".join([f'"{token}"*' for token in tokens])

    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    a.id, a.path, a.section, a.subsection, a.title, a.description,
                    snippet(articles_search, 2, '<mark>', '</mark>', '...', 25) as snippet,
                    bm25(articles_search) as rank
                FROM articles_search s
                JOIN articles a ON a.id = s.rowid
                WHERE articles_search MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (safe_query, limit))
            return [dict(r) for r in cursor.fetchall()]
        except Exception:
            like_term = f"%{tokens[0]}%"
            cursor.execute("""
                SELECT id, path, section, subsection, title, description,
                       description as snippet, 0 as rank
                FROM articles
                WHERE title LIKE ? OR path LIKE ? OR description LIKE ?
                LIMIT ?
            """, (like_term, like_term, like_term, limit))
            return [dict(r) for r in cursor.fetchall()]


def get_sections_summary(db_path: str = DB_FILE) -> List[Dict[str, Any]]:
    """Retorna a contagem de artigos por seção e subseção."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT section, COUNT(*) as count 
            FROM articles 
            GROUP BY section 
            ORDER BY count DESC
        """)
        return [dict(r) for r in cursor.fetchall()]


def get_articles_by_section(section: str, db_path: str = DB_FILE) -> List[Dict[str, Any]]:
    """Retorna todos os artigos de uma seção."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, path, slug, section, subsection, title, description, updated_at
            FROM articles
            WHERE section = ?
            ORDER BY subsection, title
        """, (section,))
        return [dict(r) for r in cursor.fetchall()]


if __name__ == "__main__":
    init_db()
    print("Banco de dados inicializado com sucesso!")
