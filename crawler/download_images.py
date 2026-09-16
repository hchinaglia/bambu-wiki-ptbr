"""
Script para download e cache local de imagens da Wiki Bambu Lab.
Permite transformar a base de conhecimento em 100% autônoma e offline.

Uso:
  python3 crawler/download_images.py --limit 100
  python3 crawler/download_images.py --series a1 --workers 8
  python3 crawler/download_images.py --rewrite --limit 500
  python3 crawler/download_images.py --all --workers 12
"""

import argparse
import os
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Set, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_IMG_DIR = os.path.join(BASE_DIR, "app", "static", "images", "wiki")
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


def sanitize_rel_path(url: str) -> Optional[str]:
    """
    Converte uma URL da wiki Bambu em um caminho de arquivo relativo seguro.
    Exemplo:
      https://wiki.bambulab.com/x1/manual/intro.png -> x1/manual/intro.png
      /stock-images/new/a1.png -> stock-images/new/a1.png
    """
    if url.startswith("//"):
        url = "https:" + url
    elif url.startswith("/"):
        url = "https://wiki.bambulab.com" + url

    parsed = urllib.parse.urlparse(url)
    if "bambulab.com" not in parsed.netloc and not parsed.netloc.endswith("bambulab.com"):
        return None

    path = urllib.parse.unquote(parsed.path).lstrip("/")
    if not path:
        return None

    # Normalizar separadores e evitar directory traversal
    parts = [p for p in path.split("/") if p and p != "." and p != ".."]
    if not parts:
        return None

    return os.path.join(*parts)


def get_all_images(db_path: str, series: Optional[str] = None) -> List[Tuple[str, str]]:
    """
    Varre os artigos do SQLite e retorna uma lista de (url_original, rel_path_local).
    """
    if not os.path.exists(db_path):
        print(f"Banco de dados '{db_path}' não encontrado!", file=sys.stderr)
        return []

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT path, html_content FROM articles WHERE html_content LIKE '%<img%'"
    params = []
    if series:
        query += " AND (path LIKE ? OR path = ?)"
        params.extend([f"{series}/%", series])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    url_to_relpath: Dict[str, str] = {}

    img_regex = re.compile(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', re.IGNORECASE)

    for art_path, html in rows:
        if not html:
            continue
        matches = img_regex.findall(html)
        for match in matches:
            clean_url = match.strip()
            if not clean_url or clean_url.startswith("data:"):
                continue

            rel_path = sanitize_rel_path(clean_url)
            if rel_path:
                url_to_relpath[clean_url] = rel_path

    return list(url_to_relpath.items())


def download_single_image(url: str, rel_path: str, timeout: int = 15) -> Tuple[bool, int, str]:
    """
    Baixa uma imagem individual e salva no disco.
    Retorna: (sucesso: bool, bytes_baixados: int, mensagem: str)
    """
    full_url = url
    if full_url.startswith("//"):
        full_url = "https:" + full_url
    elif full_url.startswith("/"):
        full_url = "https://wiki.bambulab.com" + full_url

    dest_path = os.path.join(STATIC_IMG_DIR, rel_path)

    # Verificar se já existe
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
        return True, 0, "cached"

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Encode URL para caracteres especiais/chineses
    parsed = urllib.parse.urlsplit(full_url)
    encoded_path = urllib.parse.quote(urllib.parse.unquote(parsed.path))
    safe_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, encoded_path, parsed.query, parsed.fragment))

    req = urllib.request.Request(safe_url, headers={"User-Agent": DEFAULT_USER_AGENT})

    temp_path = dest_path + ".tmp"
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status != 200:
                return False, 0, f"HTTP {response.status}"
            content = response.read()

        with open(temp_path, "wb") as f:
            f.write(content)

        os.replace(temp_path, dest_path)
        return True, len(content), "ok"

    except Exception as e:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass
        return False, 0, str(e)


def rewrite_database_image_urls(db_path: str, url_map: Dict[str, str]) -> int:
    """
    Reescreve as tags <img> do banco SQLite apontando para o caminho local /static/images/wiki/...
    Apenas substitui URLs cujos arquivos existam localmente.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT path, html_content FROM articles WHERE html_content LIKE '%<img%'")
    articles = cursor.fetchall()

    updated_count = 0

    for path, html in articles:
        if not html:
            continue

        changed = False
        new_html = html

        for orig_url, rel_path in url_map.items():
            local_fs_path = os.path.join(STATIC_IMG_DIR, rel_path)
            if not os.path.exists(local_fs_path) or os.path.getsize(local_fs_path) == 0:
                continue

            local_web_path = f"/static/images/wiki/{rel_path.replace(os.sep, '/')}"
            if orig_url in new_html:
                new_html = new_html.replace(f'src="{orig_url}"', f'src="{local_web_path}"')
                new_html = new_html.replace(f"src='{orig_url}'", f"src='{local_web_path}'")
                changed = True

        if changed and new_html != html:
            cursor.execute("UPDATE articles SET html_content = ? WHERE path = ?", (new_html, path))
            updated_count += 1

    conn.commit()
    conn.close()
    return updated_count


def main():
    parser = argparse.ArgumentParser(description="Baixar e armazenar imagens da Wiki Bambu Lab localmente.")
    parser.add_argument("--db", default=os.path.join(BASE_DIR, "wiki_bambu.db"), help="Caminho do banco wiki_bambu.db")
    parser.add_argument("--series", "-s", help="Filtrar por série (ex: x1, p1, a1, ams, software)")
    parser.add_argument("--limit", "-n", type=int, help="Limite de imagens a baixar")
    parser.add_argument("--workers", "-w", type=int, default=8, help="Número de threads concorrentes (padrão: 8)")
    parser.add_argument("--rewrite", action="store_true", help="Atualizar banco SQLite com URLs locais para imagens baixadas")
    parser.add_argument("--timeout", type=int, default=15, help="Timeout por requisição em segundos")

    args = parser.parse_args()

    print(f"=== Bambu Wiki Image Downloader ===")
    print(f"Diretório destino: {STATIC_IMG_DIR}")
    os.makedirs(STATIC_IMG_DIR, exist_ok=True)

    items = get_all_images(args.db, series=args.series)
    total_found = len(items)
    print(f"Total de imagens únicas encontradas no banco: {total_found}")

    if args.limit and args.limit < total_found:
        items = items[:args.limit]
        print(f"Limitado para as primeiras {len(items)} imagens.")

    if not items:
        print("Nenhuma imagem para processar.")
        return

    print(f"Iniciando download com {args.workers} workers...")
    start_time = time.time()
    success_count = 0
    cached_count = 0
    error_count = 0
    total_bytes = 0

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(download_single_image, url, rel_path, args.timeout): (url, rel_path)
            for url, rel_path in items
        }

        for idx, future in enumerate(as_completed(futures), 1):
            url, rel_path = futures[future]
            try:
                ok, nbytes, status = future.result()
                if ok:
                    if status == "cached":
                        cached_count += 1
                    else:
                        success_count += 1
                        total_bytes += nbytes
                else:
                    error_count += 1
            except Exception as e:
                error_count += 1

            if idx % 50 == 0 or idx == len(items):
                elapsed = time.time() - start_time
                mb = total_bytes / (1024 * 1024)
                print(
                    f"Progresso: {idx}/{len(items)} ({idx/len(items)*100:.1f}%) "
                    f"| Novos: {success_count} ({mb:.1f} MB) | Cache: {cached_count} | Falhas: {error_count} "
                    f"| Tempo: {elapsed:.1f}s"
                )

    elapsed = time.time() - start_time
    mb_total = total_bytes / (1024 * 1024)
    print("\n--- Resumo do Download ---")
    print(f"Total processado: {len(items)}")
    print(f"Baixados com sucesso: {success_count} ({mb_total:.2f} MB)")
    print(f"Já existiam em cache: {cached_count}")
    print(f"Erros de download: {error_count}")
    print(f"Tempo decorrido: {elapsed:.1f} segundos")

    if args.rewrite:
        print("\nReescrevendo URLs no banco de dados SQLite para as imagens baixadas...")
        url_map = dict(items)
        rewritten = rewrite_database_image_urls(args.db, url_map)
        print(f"Artigos atualizados com URLs locais: {rewritten}")


if __name__ == "__main__":
    main()
