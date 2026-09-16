r"""
Catálogo de Cores, Mapeamento Perceptual de Filamentos e Comparador de Preços.
Suporta:
- Filamentos Oficiais Bambu Lab (PLA Basic, Matte, Silk, PETG, TPU)
- Principais Marcas Compatíveis no Brasil (Voolt3D, 3D Fila, Printalot, Sunlu, eSun, Creality)
- Algoritmo de Distância Perceptual Euclidiana ponderada (\Delta E aproximado)
- Recomendações automáticas de material (PLA, PETG, TPU, ASA) por análise visual
- Geradores de links diretos de preços para Mercado Livre, Shopee, Amazon e Google Shopping
- Base de cupons de desconto ativos para compras de filamentos 3D no Brasil
"""

import math
import re
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple

# ==============================================================================
# 1. CATÁLOGO DE CORES OFICIAIS BAMBU LAB
# ==============================================================================
BAMBU_OFFICIAL_COLORS = [
    # PLA Basic
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Jade White (Branco Jade)", "hex": "#FFFFFF", "type": "PLA", "code": "10100", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Bambu Green (Verde Bambu Oficial)", "hex": "#00AE42", "type": "PLA", "code": "10500", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Black (Preto Profundo)", "hex": "#1A1A1A", "type": "PLA", "code": "10101", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Flame Red (Vermelho Vivo)", "hex": "#D8232A", "type": "PLA", "code": "10200", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Sun Yellow (Amarelo Solar)", "hex": "#FFD100", "type": "PLA", "code": "10400", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Cobalt Blue (Azul Cobalto)", "hex": "#00629B", "type": "PLA", "code": "10600", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Mandarine Orange (Laranja Mandarina)", "hex": "#FF6A13", "type": "PLA", "code": "10300", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Cyan (Ciano Claro)", "hex": "#00A3E0", "type": "PLA", "code": "10601", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Magenta (Magenta Rosa)", "hex": "#D10074", "type": "PLA", "code": "10201", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Purple (Roxo Íris)", "hex": "#6C2D82", "type": "PLA", "code": "10700", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Silver (Prata Metálico)", "hex": "#A2AAAD", "type": "PLA", "code": "10103", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Bronze / Gold (Ouro Nobre)", "hex": "#8A6E3E", "type": "PLA", "code": "10800", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Brown (Marrom Terra)", "hex": "#5C4033", "type": "PLA", "code": "10801", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Mistletoe Green (Verde Escuro)", "hex": "#1E5E3A", "type": "PLA", "code": "10501", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Beige / Skin (Pele / Bege)", "hex": "#E8BEAC", "type": "PLA", "code": "10401", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Basic", "name": "Gray (Cinza Médio)", "hex": "#768692", "type": "PLA", "code": "10102", "ams": True},

    # PLA Matte (Acabamento Fosco / Sem brilho - Oculta linhas de camada)
    {"brand": "Bambu Lab", "line": "PLA Matte", "name": "Matte Charcoal (Preto Carvão Fosco)", "hex": "#2B2B2B", "type": "PLA", "code": "11101", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Matte", "name": "Matte Ivory White (Branco Marfim Fosco)", "hex": "#F4F1EA", "type": "PLA", "code": "11100", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Matte", "name": "Matte Marine Blue (Azul Marinho Fosco)", "hex": "#1B365D", "type": "PLA", "code": "11600", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Matte", "name": "Matte Dark Brown (Marrom Escuro Fosco)", "hex": "#4A3525", "type": "PLA", "code": "11800", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Matte", "name": "Matte Sakura Pink (Rosa Sakura Fosco)", "hex": "#FFB7C5", "type": "PLA", "code": "11201", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Matte", "name": "Matte Lemon Yellow (Amarelo Limão Fosco)", "hex": "#FFF04B", "type": "PLA", "code": "11400", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Matte", "name": "Matte Desert Tan (Cáqui / Deserto)", "hex": "#D2B48C", "type": "PLA", "code": "11801", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Matte", "name": "Matte Grass Green (Verde Grama Fosco)", "hex": "#4A773C", "type": "PLA", "code": "11500", "ams": True},

    # PLA Silk (Efeito Sedoso Metálico)
    {"brand": "Bambu Lab", "line": "PLA Silk", "name": "Silk Gold (Ouro Brilhante Sedoso)", "hex": "#D4AF37", "type": "PLA", "code": "13800", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Silk", "name": "Silk Silver (Prata Espelhado Sedoso)", "hex": "#C0C0C0", "type": "PLA", "code": "13100", "ams": True},
    {"brand": "Bambu Lab", "line": "PLA Silk", "name": "Silk Copper (Cobre Rosado Sedoso)", "hex": "#B87333", "type": "PLA", "code": "13801", "ams": True},

    # PETG Basic / HF (Resistência Mecânica e Térmica)
    {"brand": "Bambu Lab", "line": "PETG HF", "name": "PETG Black (Preto Técnico)", "hex": "#1A1A1A", "type": "PETG", "code": "30101", "ams": True},
    {"brand": "Bambu Lab", "line": "PETG HF", "name": "PETG White (Branco Puro)", "hex": "#FFFFFF", "type": "PETG", "code": "30100", "ams": True},
    {"brand": "Bambu Lab", "line": "PETG HF", "name": "PETG Translucent (Translúcido Natural)", "hex": "#E0E0E0", "type": "PETG", "code": "30000", "ams": True},
    {"brand": "Bambu Lab", "line": "PETG HF", "name": "PETG Gray (Cinza Técnico)", "hex": "#708090", "type": "PETG", "code": "30102", "ams": True},
    {"brand": "Bambu Lab", "line": "PETG HF", "name": "PETG Blue (Azul Royal)", "hex": "#0047AB", "type": "PETG", "code": "30600", "ams": True},
    {"brand": "Bambu Lab", "line": "PETG HF", "name": "PETG Red (Vermelho Resistente)", "hex": "#C41E3A", "type": "PETG", "code": "30200", "ams": True},

    # TPU 95A (Flexível)
    {"brand": "Bambu Lab", "line": "TPU 95A", "name": "TPU Black (Preto Borracha)", "hex": "#111111", "type": "TPU", "code": "40101", "ams": False},
    {"brand": "Bambu Lab", "line": "TPU 95A", "name": "TPU White (Branco Flexível)", "hex": "#FAFAFA", "type": "TPU", "code": "40100", "ams": False},
    {"brand": "Bambu Lab", "line": "TPU 95A", "name": "TPU Blue (Azul Elástico)", "hex": "#0070BA", "type": "TPU", "code": "40600", "ams": False},
]

# ==============================================================================
# 2. MARCAS NACIONAIS E COMPATÍVEIS NO BRASIL (CUSTO-BENEFÍCIO)
# ==============================================================================
NATIONAL_BRANDS_COLORS = [
    # Voolt3D (Excelente custo-benefício nacional, carretel compatível)
    {"brand": "Voolt3D", "line": "PLA Nacional", "name": "Branco Puro Neve", "hex": "#FFFFFF", "type": "PLA", "price_avg": "R$ 79 - 89"},
    {"brand": "Voolt3D", "line": "PLA Nacional", "name": "Preto Noite", "hex": "#151515", "type": "PLA", "price_avg": "R$ 79 - 89"},
    {"brand": "Voolt3D", "line": "PLA Nacional", "name": "Vermelho Ferrari", "hex": "#CC1100", "type": "PLA", "price_avg": "R$ 79 - 89"},
    {"brand": "Voolt3D", "line": "PLA Nacional", "name": "Azul Bic / Royal", "hex": "#003399", "type": "PLA", "price_avg": "R$ 79 - 89"},
    {"brand": "Voolt3D", "line": "PLA Nacional", "name": "Amarelo Canário", "hex": "#FFCC00", "type": "PLA", "price_avg": "R$ 79 - 89"},
    {"brand": "Voolt3D", "line": "PLA Nacional", "name": "Verde Bandeira", "hex": "#008833", "type": "PLA", "price_avg": "R$ 79 - 89"},
    {"brand": "Voolt3D", "line": "PLA Nacional", "name": "Laranja Cenoura", "hex": "#FF6600", "type": "PLA", "price_avg": "R$ 79 - 89"},
    {"brand": "Voolt3D", "line": "PLA Nacional", "name": "Cinza Chumbo", "hex": "#666666", "type": "PLA", "price_avg": "R$ 79 - 89"},
    {"brand": "Voolt3D", "line": "PLA Nacional", "name": "Rosa Chiclete", "hex": "#FF69B4", "type": "PLA", "price_avg": "R$ 79 - 89"},
    {"brand": "Voolt3D", "line": "PLA Nacional", "name": "Pele Clara / Nude", "hex": "#F0C8B0", "type": "PLA", "price_avg": "R$ 79 - 89"},
    {"brand": "Voolt3D", "line": "PLA Nacional", "name": "Roxo Uva", "hex": "#5A189A", "type": "PLA", "price_avg": "R$ 79 - 89"},
    {"brand": "Voolt3D", "line": "PETG Nacional", "name": "PETG Preto Resistente", "hex": "#1B1B1B", "type": "PETG", "price_avg": "R$ 85 - 95"},
    {"brand": "Voolt3D", "line": "PETG Nacional", "name": "PETG Cristal / Translúcido", "hex": "#EEEEEE", "type": "PETG", "price_avg": "R$ 85 - 95"},

    # 3D Fila (Tradição e alta precisão dimensional em Minas Gerais)
    {"brand": "3D Fila", "line": "PLA EasyFill", "name": "Branco Ártico", "hex": "#FCFCFC", "type": "PLA", "price_avg": "R$ 89 - 105"},
    {"brand": "3D Fila", "line": "PLA EasyFill", "name": "Preto Ônix", "hex": "#101010", "type": "PLA", "price_avg": "R$ 89 - 105"},
    {"brand": "3D Fila", "line": "PLA EasyFill", "name": "Vermelho Tomate", "hex": "#D62828", "type": "PLA", "price_avg": "R$ 89 - 105"},
    {"brand": "3D Fila", "line": "PLA EasyFill", "name": "Azul Safira", "hex": "#00509D", "type": "PLA", "price_avg": "R$ 89 - 105"},
    {"brand": "3D Fila", "line": "PLA EasyFill", "name": "Amarelo Ouro", "hex": "#FFBA08", "type": "PLA", "price_avg": "R$ 89 - 105"},
    {"brand": "3D Fila", "line": "PLA EasyFill", "name": "Verde Floresta", "hex": "#1B4332", "type": "PLA", "price_avg": "R$ 89 - 105"},
    {"brand": "3D Fila", "line": "PETG XT", "name": "PETG Preto", "hex": "#181818", "type": "PETG", "price_avg": "R$ 95 - 115"},

    # Printalot (Filamentos premium com alta fidelidade de cor)
    {"brand": "Printalot", "line": "PLA HD", "name": "Super White (Branco Extremo)", "hex": "#FFFFFF", "type": "PLA", "price_avg": "R$ 105 - 120"},
    {"brand": "Printalot", "line": "PLA HD", "name": "Deep Black (Preto Intenso)", "hex": "#0F0F0F", "type": "PLA", "price_avg": "R$ 105 - 120"},
    {"brand": "Printalot", "line": "PLA HD", "name": "Gris Plata (Prata Metálico)", "hex": "#A8A9AD", "type": "PLA", "price_avg": "R$ 105 - 120"},
    {"brand": "Printalot", "line": "PLA HD", "name": "Rojo Fuego (Vermelho Vivo)", "hex": "#C91818", "type": "PLA", "price_avg": "R$ 105 - 120"},
    {"brand": "Printalot", "line": "PLA HD", "name": "Azul Cobalto", "hex": "#0C2340", "type": "PLA", "price_avg": "R$ 105 - 120"},

    # Sunlu / eSun (Importadas conceituadas, muito usadas no AMS)
    {"brand": "Sunlu", "line": "PLA Meta / Plus", "name": "Branco Gelo", "hex": "#FAFAFA", "type": "PLA", "price_avg": "R$ 95 - 110"},
    {"brand": "Sunlu", "line": "PLA Meta / Plus", "name": "Preto Clássico", "hex": "#181818", "type": "PLA", "price_avg": "R$ 95 - 110"},
    {"brand": "Sunlu", "line": "PLA Meta / Plus", "name": "Cinza Claro", "hex": "#B0B0B0", "type": "PLA", "price_avg": "R$ 95 - 110"},
    {"brand": "eSun", "line": "PLA+ (High Speed)", "name": "Branco Frio", "hex": "#FFFFFF", "type": "PLA", "price_avg": "R$ 110 - 130"},
    {"brand": "eSun", "line": "PLA+ (High Speed)", "name": "Preto Sólido", "hex": "#141414", "type": "PLA", "price_avg": "R$ 110 - 130"},
    {"brand": "eSun", "line": "PLA+ (High Speed)", "name": "Vermelho Vivo", "hex": "#CC0000", "type": "PLA", "price_avg": "R$ 110 - 130"},
]

# ==============================================================================
# 3. CUPONS DE DESCONTO E DICAS PROMOCIONAIS ATIVAS
# ==============================================================================
PROMO_COUPONS = [
    {
        "store": "Mercado Livre",
        "code": "TECH10 / VALE15",
        "discount": "R$ 10 a R$ 25 OFF",
        "description": "Válido em compras acima de R$ 99 ou R$ 149 na categoria Informática e Impressão 3D.",
        "tip": "Dê preferência a vendedores com selo 'MercadoLíder Platinum' e envio Full para frete grátis."
    },
    {
        "store": "Shopee Brasil",
        "code": "FRETE GRÁTIS + CUPOM 10%",
        "discount": "Frete Grátis + até R$ 20 OFF",
        "description": "Ative o cupom mensal de frete grátis e cupons de loja oficial no app da Shopee.",
        "tip": "Muitas lojas oficiais de filamento (Voolt3D, 3D Fila) dão 5% extra na primeira compra da loja."
    },
    {
        "store": "Amazon Brasil",
        "code": "PRIME / PROMO3D",
        "discount": "Frete Grátis Prime + Desconto Progressivo",
        "description": "Desconto automático ao levar 2 ou mais carretéis de filamentos participantes.",
        "tip": "Assinantes Amazon Prime recebem no dia seguinte com frete gratuito em capitais."
    },
    {
        "store": "Lojas Nacionais (3D Fila / Voolt3D)",
        "code": "BAMBUBRASIL / PRIMEIRACOMPRA",
        "discount": "5% a 10% OFF no PIX",
        "description": "Desconto direto para pagamento à vista via PIX em sites fabricantes nacionais.",
        "tip": "Comprar combos de 3 a 5 carretéis costuma liberar frete grátis direto da fábrica."
    }
]


# ==============================================================================
# 4. FUNÇÕES MATEMÁTICAS DE COR
# ==============================================================================
def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    """Converte string hexadecimal (#RRGGBB ou RRGGBB) para tupla (R, G, B)."""
    hex_clean = hex_str.strip().lstrip("#")
    if len(hex_clean) == 3:
        hex_clean = "".join([c * 2 for c in hex_clean])
    if len(hex_clean) != 6:
        return (128, 128, 128)
    try:
        r = int(hex_clean[0:2], 16)
        g = int(hex_clean[2:4], 16)
        b = int(hex_clean[4:6], 16)
        return (r, g, b)
    except ValueError:
        return (128, 128, 128)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Converte RGB para string #RRGGBB."""
    return f"#{max(0, min(255, int(r))):02X}{max(0, min(255, int(g))):02X}{max(0, min(255, int(b))):02X}"


def color_distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> float:
    """
    Calcula distância perceptual entre duas cores RGB usando a fórmula ponderada de redmean.
    Retorna valor de 0 (cores idênticas) até ~765.
    """
    r_mean = (c1[0] + c2[0]) / 2.0
    dr = c1[0] - c2[0]
    dg = c1[1] - c2[1]
    db = c1[2] - c2[2]
    return math.sqrt(
        (2.0 + r_mean / 256.0) * (dr ** 2)
        + 4.0 * (dg ** 2)
        + (2.0 + (255.0 - r_mean) / 256.0) * (db ** 2)
    )


def match_color_to_filaments(
    target_hex: str,
    preferred_material: Optional[str] = None
) -> Dict[str, Any]:
    """
    Encontra o filamento oficial Bambu Lab mais próximo e a melhor alternativa nacional.
    """
    target_rgb = hex_to_rgb(target_hex)

    # 1. Filtra e busca o melhor Bambu Lab
    bambu_candidates = BAMBU_OFFICIAL_COLORS
    if preferred_material:
        filtered = [f for f in bambu_candidates if f["type"].upper() == preferred_material.upper()]
        if filtered:
            bambu_candidates = filtered

    best_bambu = None
    best_bambu_dist = 999999.0
    for fil in bambu_candidates:
        rgb = hex_to_rgb(fil["hex"])
        dist = color_distance(target_rgb, rgb)
        if dist < best_bambu_dist:
            best_bambu_dist = dist
            best_bambu = fil

    # 2. Busca a melhor alternativa nacional
    nat_candidates = NATIONAL_BRANDS_COLORS
    if preferred_material:
        filtered_nat = [f for f in nat_candidates if f["type"].upper() == preferred_material.upper()]
        if filtered_nat:
            nat_candidates = filtered_nat

    best_nat = None
    best_nat_dist = 999999.0
    for fil in nat_candidates:
        rgb = hex_to_rgb(fil["hex"])
        dist = color_distance(target_rgb, rgb)
        if dist < best_nat_dist:
            best_nat_dist = dist
            best_nat = fil

    # Calcula precisão em porcentagem (0 a 100%)
    max_dist = 765.0
    bambu_pct = max(0, min(100, int((1.0 - (best_bambu_dist / max_dist)) * 100)))
    nat_pct = max(0, min(100, int((1.0 - (best_nat_dist / max_dist)) * 100)))

    return {
        "target_hex": target_hex,
        "bambu_match": {
            **best_bambu,
            "accuracy_pct": bambu_pct,
            "distance": round(best_bambu_dist, 1),
            "search_links": build_marketplace_links(best_bambu["brand"], best_bambu["name"], best_bambu["type"])
        },
        "national_match": {
            **best_nat,
            "accuracy_pct": nat_pct,
            "distance": round(best_nat_dist, 1),
            "search_links": build_marketplace_links(best_nat["brand"], best_nat["name"], best_nat["type"])
        } if best_nat else None
    }


# ==============================================================================
# 5. GERADOR DE LINKS DE PREÇO NOS MARKETPLACES
# ==============================================================================
def build_marketplace_links(brand: str, color_name: str, material: str) -> Dict[str, str]:
    """Gera URLs de busca direta com filtros otimizados para compras no Brasil."""
    clean_color = re.sub(r'\(.*?\)', '', color_name).strip()
    term = f"filamento {brand} {material} {clean_color}".strip()
    encoded = urllib.parse.quote_plus(term)

    return {
        "mercadolivre": f"https://lista.mercadolivre.com.br/{encoded}",
        "shopee": f"https://shopee.com.br/search?keyword={encoded}",
        "amazon": f"https://www.amazon.com.br/s?k={encoded}",
        "google_shopping": f"https://www.google.com/search?tbm=shop&q={encoded}"
    }


# ==============================================================================
# 6. HEURÍSTICA E RECOMENDAÇÃO AUTOMÁTICA DE MATERIAL
# ==============================================================================
def infer_material_recommendation(
    context_hint: str = "",
    detected_labels: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Infere se o objeto deve ser impresso em PLA, PETG, TPU, ABS ou ASA
    com base no contexto e descrição visual.
    """
    text = (context_hint + " " + " ".join(detected_labels or [])).lower()

    # Peças Flexíveis
    if any(k in text for k in ["flex", "flexivel", "gaxeta", "capinha", "pneu", "amortecedor", "vedacao", "tpu", "borracha"]):
        return {
            "material": "TPU",
            "title": "TPU 95A / HF (Material Flexível)",
            "badge_color": "warning",
            "reason": "A geometria e aplicação indicam necessidade de flexibilidade, absorção de impacto e memória elastomérica.",
            "ams_alert": "⚠️ ATENÇÃO AMS: O filamento TPU não deve passar pelo sistema AMS para evitar emperramento. Imprima através do suporte de carretel traseiro individual.",
            "bambu_studio_preset": "0.20mm Standard @Bambu TPU 95A (Velocidade reduzida para 30-50mm/s)"
        }

    # Peças Mecânicas / Externas / Alta Temperatura
    if any(k in text for k in ["suporte", "engrenagem", "mecanica", "externo", "carro", "automotivo", "chuva", "sol", "resistencia", "petg", "asa", "copo", "vaso", "estanque"]):
        if any(k in text for k in ["carro", "automotivo", "sol", "temperatura", "asa"]):
            return {
                "material": "ASA",
                "title": "Bambu ASA / ABS (Resistência UV e Térmica)",
                "badge_color": "danger",
                "reason": "Indicado para peças que ficarão expostas ao calor (> 80°C) ou à luz solar direta sem amarelar nem deformar.",
                "ams_alert": "✅ 100% Compatível com o sistema AMS Bambu Lab.",
                "bambu_studio_preset": "Câmara 100% fechada, mesa a 90-100°C e ventoinha auxiliar desligada."
            }
        return {
            "material": "PETG",
            "title": "Bambu PETG HF / Basic (Resistência Mecânica & Funcional)",
            "badge_color": "info",
            "reason": "Excelente união intercamadas, durabilidade química e resistência ao impacto superior ao PLA convencional.",
            "ams_alert": "✅ 100% Compatível com o sistema AMS Bambu Lab.",
            "bambu_studio_preset": "Mesa texturizada PEI a 70°C, bico a 240°C e adesão sem cola."
        }

    # Padrão: Figuras, Miniaturas, Decoração, Brinquedos, Renders gerais
    return {
        "material": "PLA",
        "title": "Bambu PLA Basic / PLA Matte (Visual Impecável & Fácil Impressão)",
        "badge_color": "success",
        "reason": "Ideal para modelos multicoloridos, colecionáveis, maquetes e decorações. Possui máxima vivacidade de cor, zero empenamento (warping) e acabamento preciso.",
        "ams_alert": "✅ 100% Otimizado para troca automática no sistema AMS (até 16 cores com múltiplos AMS).",
        "bambu_studio_preset": "0.20mm Standard / 0.12mm Fino, tampa superior entreaberta e ventoinhas ativas."
    }
