FROM python:3.11-slim

LABEL maintainer="Bambu Lab Wiki PT-BR"
LABEL description="Offline Bambu Lab Wiki em Português com Agente de IA RAG Gemini"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

WORKDIR /app

# Instalar dependências do sistema necessárias para SQLite3 e compilações leves
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do projeto
COPY app/ /app/app/
COPY crawler/ /app/crawler/
COPY run_server.py /app/
COPY extract_wiki_links.py /app/

# Copiar banco de dados (se existir durante o build)
COPY wiki_bambu.db /app/

# Diretório para cache de imagens estáticas e páginas
RUN mkdir -p /app/app/static/images/wiki /app/cache/pages

# Porta exposta
EXPOSE 8000

# Healthcheck simples
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/api/stats || exit 1

# Comando de inicialização
CMD ["python", "run_server.py", "--host", "0.0.0.0", "--port", "8000"]
