"""
Downloader assíncrono / concorrente para coletar páginas da Wiki Bambu Lab.
Baixa preferencialmente a versão oficial em português ('pt-br') e faz fallback para 'en'.
"""

import argparse
import os
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Tuple

from crawler.build_db import init_db, save_article
from crawler.parser import parse_wiki_page

CACHE_DIR = "cache/pages"
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def fetch_url(url: str, timeout: int = 20) -> Tuple[int, Optional[str]]:
    """Baixa o conteúdo HTML de uma URL com cabeçalhos padrão."""
    req = urllib.request.Request(url, headers={"User-Agent": DEFAULT_USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status, response.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return 0, None


def get_cache_path(path: str) -> str:
    """Retorna o caminho do arquivo de cache para um path relativo."""
    safe_name = path.replace("/", "_").replace("\\", "_") + ".html"
    return os.path.join(CACHE_DIR, safe_name)


def download_and_process_page(en_url: str, db_path: str = "wiki_bambu.db") -> bool:
    """
    Processa uma URL:
    1. Tenta a versão correspondente em pt-br.
    2. Se não existir, tenta a versão em en.
    3. Faz o parsing e salva no banco de dados SQLite.
    """
    path_suffix = en_url.replace("https://wiki.bambulab.com/en/", "").strip("/")
    if not path_suffix:
        return False

    cache_file = get_cache_path(path_suffix)
    html_content = None

    # Verifica cache local primeiro
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8", errors="ignore") as f:
            html_content = f.read()

    # Se não está em cache, baixa da web
    if not html_content:
        pt_url = f"https://wiki.bambulab.com/pt-br/{path_suffix}"
        status, content = fetch_url(pt_url)

        if status == 200 and content:
            html_content = content
        else:
            # Fallback para versão em inglês
            status_en, content_en = fetch_url(en_url)
            if status_en == 200 and content_en:
                html_content = content_en

        # Salva no cache se baixou com sucesso
        if html_content:
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(cache_file, "w", encoding="utf-8") as f:
                f.write(html_content)

    if not html_content:
        return False

    article_data = parse_wiki_page(html_content)
    if article_data and article_data.get("title"):
        save_article(article_data, db_path=db_path)
        return True

    return False


def run_crawler(links_file: str = "links_en.txt", section: Optional[str] = None, limit: Optional[int] = None, workers: int = 5, db_path: str = "wiki_bambu.db"):
    init_db(db_path)
    os.makedirs(CACHE_DIR, exist_ok=True)

    if not os.path.exists(links_file):
        print(f"Arquivo de links '{links_file}' não encontrado!", file=sys.stderr)
        return

    with open(links_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    if section:
        urls = [u for u in urls if f"/en/{section}/" in u or u.endswith(f"/en/{section}")]

    if limit:
        urls = urls[:limit]

    total = len(urls)
    print(f"Iniciando download e processamento de {total} artigos com {workers} workers...", file=sys.stderr)

    success_count = 0
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(download_and_process_page, url, db_path): url for url in urls}
        for idx, future in enumerate(as_completed(futures), 1):
            url = futures[future]
            try:
                if future.result():
                    success_count += 1
            except Exception as e:
                print(f"Erro em {url}: {e}", file=sys.stderr)

            if idx % 20 == 0 or idx == total:
                elapsed = time.time() - start_time
                print(f"Progresso: {idx}/{total} ({idx/total*100:.1f}%) - {success_count} salvos - {elapsed:.1f}s", file=sys.stderr)

    print(f"\nFinalizado! Total de artigos processados: {success_count}/{total}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Coletor e indexador de artigos da Wiki Bambu Lab.")
    parser.add_argument("--links", default="links_en.txt", help="Arquivo com a lista de URLs em inglês.")
    parser.add_argument("--section", "-s", help="Filtrar por seção específica (ex: x1, p1, a1, ams, software).")
    parser.add_argument("--limit", "-n", type=int, help="Número máximo de páginas a processar.")
    parser.add_argument("--workers", "-w", type=int, default=5, help="Número de threads simultâneas.")
    parser.add_argument("--db", default="wiki_bambu.db", help="Caminho do banco SQLite.")

    args = parser.parse_args()
    run_crawler(links_file=args.links, section=args.section, limit=args.limit, workers=args.workers, db_path=args.db)


if __name__ == "__main__":
    main()
