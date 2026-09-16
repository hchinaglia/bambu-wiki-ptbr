#!/usr/bin/env python3
"""
Script para extrair todos os links de um idioma específico da Wiki Bambu Lab (https://wiki.bambulab.com/).
Fonte dos dados: https://wiki.bambulab.com/sitemap.xml
"""

import argparse
import csv
import json
import os
import re
import sys
import urllib.request
from collections import Counter
from typing import Dict, List, Optional, Tuple

SITEMAP_URL = "https://wiki.bambulab.com/sitemap.xml"
LOCAL_FALLBACK = "sitemap.xml"


def fetch_sitemap(url: str = SITEMAP_URL, local_file: Optional[str] = None) -> str:
    """Obtém o conteúdo XML do sitemap (via URL ou arquivo local)."""
    if local_file:
        with open(local_file, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode("utf-8", errors="ignore")
    except Exception as err:
        if os.path.exists(LOCAL_FALLBACK):
            print(f"Aviso: Não foi possível acessar a rede ({err}). Usando arquivo local '{LOCAL_FALLBACK}'.", file=sys.stderr)
            with open(LOCAL_FALLBACK, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        raise err


def parse_sitemap_urls(xml_content: str) -> List[Tuple[str, Optional[str]]]:
    """
    Extrai pares (loc, lastmod) via regex rápida.
    """
    pattern = re.compile(
        r"<url>\s*<loc>(https?://wiki\.bambulab\.com/[^<]+)</loc>(?:\s*<lastmod>([^<]+)</lastmod>)?",
        re.MULTILINE
    )
    return pattern.findall(xml_content)


def extract_language_code(url: str) -> Optional[str]:
    """Extrai o código de idioma da URL (ex: 'pt-br', 'en', 'es')."""
    match = re.match(r"https?://wiki\.bambulab\.com/([a-zA-Z0-9_-]+)/", url)
    if match:
        return match.group(1).lower()
    return None


def get_language_counts(urls_data: List[Tuple[str, Optional[str]]]) -> Counter:
    """Conta a quantidade de URLs por idioma."""
    counts = Counter()
    for url, _ in urls_data:
        lang = extract_language_code(url)
        if lang:
            counts[lang] += 1
    return counts


def filter_by_language(
    urls_data: List[Tuple[str, Optional[str]]],
    target_lang: str
) -> List[Tuple[str, Optional[str]]]:
    """Filtra as URLs pelo idioma desejado (case-insensitive)."""
    target = target_lang.lower().strip()
    return [
        (url, lastmod)
        for url, lastmod in urls_data
        if extract_language_code(url) == target
    ]


def save_output(
    data: List[Tuple[str, Optional[str]]],
    output_path: str
):
    """Salva os links no formato desejado (.txt, .json, .csv)."""
    if output_path.endswith(".json"):
        records = [{"url": url, "lastmod": lastmod} for url, lastmod in data]
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
    elif output_path.endswith(".csv"):
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["url", "lastmod"])
            for url, lastmod in data:
                writer.writerow([url, lastmod or ""])
    else:  # Padrão: arquivo texto puro com um link por linha
        with open(output_path, "w", encoding="utf-8") as f:
            for url, _ in data:
                f.write(f"{url}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Extrai todos os links de um idioma específico da Wiki Bambu Lab."
    )
    parser.add_argument(
        "--lang", "-l",
        help="Código do idioma a extrair (ex: pt-br, en, es, fr, de, it, zh)."
    )
    parser.add_argument(
        "--output", "-o",
        help="Caminho do arquivo de saída (.txt, .json, .csv). Se omitido, imprime no terminal."
    )
    parser.add_argument(
        "--list-languages", "--list",
        action="store_true",
        help="Lista todos os idiomas disponíveis no sitemap e suas respectivas contagens de páginas."
    )
    parser.add_argument(
        "--file", "-f",
        help="Caminho para um arquivo sitemap.xml local (caso já tenha baixado)."
    )

    args = parser.parse_args()

    if not args.list_languages and not args.lang:
        parser.print_help()
        print("\nExemplos de uso:")
        print("  python3 extract_wiki_links.py --list")
        print("  python3 extract_wiki_links.py --lang pt-br -o links_pt-br.txt")
        print("  python3 extract_wiki_links.py --lang en -o links_en.json")
        sys.exit(1)

    print("Carregando sitemap...", file=sys.stderr)
    try:
        xml_content = fetch_sitemap(local_file=args.file)
    except Exception as e:
        print(f"Erro ao obter sitemap: {e}", file=sys.stderr)
        sys.exit(1)

    urls_data = parse_sitemap_urls(xml_content)
    print(f"Total de URLs encontradas no sitemap: {len(urls_data)}", file=sys.stderr)

    if args.list_languages:
        counts = get_language_counts(urls_data)
        print("\nIdiomas disponíveis na Wiki Bambu Lab:")
        print(f"{'Código':<12} | {'Quantidade de Links':<20}")
        print("-" * 35)
        for lang, count in counts.most_common():
            print(f"{lang:<12} | {count:<20}")
        return

    filtered = filter_by_language(urls_data, args.lang)
    print(f"Links encontrados para '{args.lang}': {len(filtered)}", file=sys.stderr)

    if not filtered:
        counts = get_language_counts(urls_data)
        available = ", ".join(counts.keys())
        print(f"Aviso: Nenhuma página encontrada para o idioma '{args.lang}'.", file=sys.stderr)
        print(f"Idiomas disponíveis: {available}", file=sys.stderr)
        return

    if args.output:
        save_output(filtered, args.output)
        print(f"Sucesso! Links salvos em: {args.output}", file=sys.stderr)
    else:
        for url, _ in filtered:
            print(url)


if __name__ == "__main__":
    main()
