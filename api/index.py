import os
import sys

# Adiciona o diretório raiz do projeto ao sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.main import app as fastapi_app


async def app(scope, receive, send):
    """
    Middleware ASGI para o Vercel CLI 59+.
    O Vercel reescreve todas as rotas internamente para /api/index.py e envia o
    caminho real requisitado pelo usuário no cabeçalho 'x-matched-path'.
    Este middleware restaura o caminho original no ASGI scope para o FastAPI rotear perfeitamente.
    """
    if scope["type"] == "http":
        headers = dict(scope.get("headers", []))
        
        # Recupera o caminho original enviado pelo Vercel
        raw_orig = (
            headers.get(b"x-matched-path")
            or headers.get(b"x-forwarded-uri")
            or headers.get(b"x-original-uri")
            or headers.get(b"x-invoke-path")
        )

        if raw_orig:
            if b"?" in raw_orig:
                path_part, qs_part = raw_orig.split(b"?", 1)
                clean_path = path_part.decode("utf-8")
                if not scope.get("query_string"):
                    scope["query_string"] = qs_part
            else:
                clean_path = raw_orig.decode("utf-8")

            # Normaliza caminhos que apontam para o script
            if clean_path in ("/api/index.py", "/api/index", "/api"):
                scope["path"] = "/"
            else:
                scope["path"] = clean_path
        elif scope.get("path") in ("/api/index.py", "/api/index", "/api"):
            scope["path"] = "/"

        scope["raw_path"] = scope["path"].encode("utf-8")

    await fastapi_app(scope, receive, send)
