"""
Módulo de tradução automática para artigos que existem apenas em inglês na Wiki Bambu Lab.
"""

import json
import urllib.parse
import urllib.request
from typing import Optional


def translate_text(text: str, source_lang: str = "en", target_lang: str = "pt") -> str:
    """
    Traduz pequenos blocos de texto (títulos, descrições) de inglês para português.
    Utiliza endpoint de tradução com fallback seguro.
    """
    if not text or not text.strip():
        return text

    try:
        url = (
            "https://translate.googleapis.com/translate_a/single?client=gtx&sl="
            + source_lang
            + "&tl="
            + target_lang
            + "&dt=t&q="
            + urllib.parse.quote(text)
        )
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            translated_pieces = [piece[0] for piece in result[0] if piece and piece[0]]
            return "".join(translated_pieces)
    except Exception:
        # Fallback se não houver conexão de rede
        return text
