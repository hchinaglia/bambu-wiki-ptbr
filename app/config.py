"""
Configurações da aplicação e chaves de API.
"""

import os

# Chave da API do Google Gemini (configurável via variável de ambiente ou direto na UI do chat)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Lista de modelos suportados conforme solicitado
SUPPORTED_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
]

# Ordem de fallback para seleção automática (os mais rápidos e estáveis primeiro)
AUTO_FALLBACK_ORDER = [
    "gemini-3.6-flash",
    "gemini-2.5-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.1-flash-lite",
]
