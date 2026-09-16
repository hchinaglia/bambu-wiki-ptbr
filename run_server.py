#!/usr/bin/env python3
"""
Script inicializador da Wiki Bambu Lab em Português.
Inicia o servidor web na porta 8000 (ou porta customizada).
"""

import argparse
import sys
import uvicorn

from crawler.build_db import DB_FILE, init_db


def main():
    parser = argparse.ArgumentParser(description="Inicia o servidor da Wiki Bambu Lab Brasil.")
    parser.add_argument("--host", default="0.0.0.0", help="Endereço de host (padrão: 0.0.0.0).")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Porta HTTP (padrão: 8000).")
    parser.add_argument("--reload", action="store_true", help="Ativa hot reload em desenvolvimento.")

    args = parser.parse_args()

    init_db(DB_FILE)

    print("=" * 60)
    print("🚀 Wiki Bambu Lab Brasil (PT-BR) Iniciada com Sucesso!")
    print(f"👉 Acesse no navegador: http://localhost:{args.port}")
    print("=" * 60)

    uvicorn.run("app.main:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
