# Wiki Bambu Lab Brasil (PT-BR) 🇧🇷 + Agente Especialista Gemini 🤖

Sistema completo de documentação técnica baseado no acervo oficial da [Wiki Bambu Lab](https://wiki.bambulab.com/), com interface moderna 1:1 ao site oficial, **2.486+ artigos indexados em português (PT-BR)**, busca de texto completo SQLite FTS5, decodificador de erros HMS, tabela interativa de filamentos e um **Agente Inteligente de IA com RAG e Visão Multimodal**, equipado com a linha de modelos Google Gemini Flash.

---

## 🌟 Recursos do Sistema

### 1. 🤖 Agente de Suporte com IA (Gemini Flash + RAG)
- **Modelos Suportados Selecionáveis:**
  - `gemini-3.8-flash`
  - `gemini-3.7-flash`
  - `gemini-3.6-flash`
  - `gemini-3.5-flash`
  - `gemini-3.5-flash-lite`
  - `gemini-3.1-flash-lite`
  - Modo **Automático** (seleciona com fallback automático priorizando os modelos mais rápidos e estáveis).
- **Streaming em Tempo Real (SSE):** Respostas token a token com digitação fluida.
- **Visão Multimodal para Diagnóstico de Impressão:** Envie fotos da peça defeituosa (efeito espaguete, warping, deslocamento de camadas, subextrusão, entupimento de bico) e receba o diagnóstico e links diretos para a solução na wiki.
- **Gaveta Lateral (Offcanvas Drawer):** Acesse o chat com a IA de qualquer página da wiki sem perder o artigo que está lendo.

### 2. 🛠️ Ferramentas Técnicas Exclusivas
- **Decodificador de Erros HMS (`/hms`):** Pesquise qualquer código de erro Bambu Lab (ex: `HMS_0300_0100_0001_0001`, `0300-0100`, falha de aquecimento do bico, atolamento AMS) com causas detalhadas e guia passo a passo de reparo.
- **Tabela Interativa de Filamentos (`/filamentos`):** Matriz completa com temperaturas de bico/mesa, tipos de chapas de impressão compatíveis, requisitos de cola, parâmetros de secagem e compatibilidade com AMS/AMS Lite (PLA, PETG, ABS, ASA, TPU, PC, PA-CF, etc.).
- **Favoritos Locais (Bookmarks):** Salve artigos essenciais no navegador com um clique na estrela e acesse rapidamente pelo menu superior.

### 3. 📖 Documentação & Interface Oficial
- **2.486 Artigos Catalogados:** Séries X1, P1, A1, A1 Mini, H2, AMS, Bambu Studio, Bambu Handy e guias de manutenção.
- **Busca Instantânea FTS5:** Pesquisa instantânea com expansão semântica e sinônimos de impressão 3D (ex: *cabeleira* ➔ *espaguete/descolamento/adesão*).
- **TOC Dinâmico (ScrollSpy):** Sumário com acompanhamento da leitura e modo escuro/claro integrado.

### 4. 📴 100% Offline e Download de Imagens
- **Downloader de Imagens (`crawler/download_images.py`):** Baixe e armazene localmente as imagens da CDN da Bambu Lab para permitir que a wiki e os manuais funcionem em redes isoladas ou oficinas sem internet.

---

## 🚀 Como Executar o Sistema

### Opção 1: Execução Direta com Python

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Iniciar o servidor
python3 run_server.py
```
Acesse no seu navegador: **[http://localhost:8000](http://localhost:8000)**

*(Para especificar porta customizada: `python3 run_server.py --port 8080`)*

---

### Opção 2: Execução com Docker e Docker Compose

```bash
# Subir com Docker Compose
docker compose up -d

# Visualizar logs
docker compose logs -f
```

Ou usando o Docker diretamente:
```bash
docker build -t bambu-wiki-ptbr .
docker run -d -p 8000:8000 --name bambu_wiki bambu-wiki-ptbr
```

---

### Opção 3: Deploy no Vercel (Nuvem / Serverless) ☁️

O projeto já possui os arquivos [`vercel.json`](file:///home/hchinaglia/antigravity/lively-shannon/vercel.json) e [`api/index.py`](file:///home/hchinaglia/antigravity/lively-shannon/api/index.py) prontos para deploy no Vercel com empacotamento do banco SQLite em modo leitura.

#### Método A: Pelo GitHub (Recomendado)
1. Suba este repositório para o seu GitHub:
   ```bash
   git add .
   git commit -m "Bambu Wiki PT-BR com IA"
   git push origin main
   ```
2. Acesse [vercel.com](https://vercel.com/) e clique em **"Add New Project"**.
3. Importe o repositório do GitHub.
4. Em **Environment Variables**, adicione:
   - `GEMINI_API_KEY`: sua chave da API do Google Gemini.
5. Clique em **Deploy**. Em cerca de 1 a 2 minutos sua wiki estará no ar com link público HTTPS!

#### Método B: Pela CLI do Vercel
```bash
# Instalar a CLI do Vercel (caso não tenha)
npm install -g vercel

# Fazer login e deploy
vercel --prod
```

> **Nota sobre o Vercel:** O sistema roda 100% no Vercel para visualização, busca FTS5 e chat com IA. Como funções serverless operam com sistema de arquivos somente leitura, o *crawler* de download de novas páginas deve ser executado localmente antes do push.

---

## 🔑 Configuração da API do Gemini

A chave de API pode ser configurada via variável de ambiente:
```bash
export GEMINI_API_KEY="SUA_CHAVE_AQUI"
python3 run_server.py
```
*(Se não for informada, o sistema utiliza a chave configurada por padrão em `app/config.py`).*

---

## 📥 Gerenciamento de Conteúdo e Imagens Offline

### Baixar Imagens para Funcionamento 100% Offline
```bash
# Baixar as primeiras 100 imagens para teste
python3 crawler/download_images.py --limit 100

# Baixar imagens apenas da série A1
python3 crawler/download_images.py --series a1 --workers 8

# Baixar imagens e atualizar as tags <img> do banco SQLite com URLs locais (/static/images/wiki/...)
python3 crawler/download_images.py --series x1 --rewrite --workers 10
```

### Atualizar Artigos da Wiki (Crawler)
```bash
# Baixar e indexar artigos da web (priorizando PT-BR e fallback para EN)
python3 -m crawler.downloader --section x1 --workers 5
```

---

## 📂 Estrutura do Projeto

```text
├── app/
│   ├── main.py                  # Rotas FastAPI e endpoints da API
│   ├── agent.py                 # RAG, streaming SSE, visão multimodal e integração Gemini
│   ├── config.py                # Configurações, modelos Gemini e chaves
│   ├── hms_data.py              # Banco de dados estruturado de erros HMS
│   ├── filament_data.py         # Matriz técnica oficial de filamentos
│   ├── templates/               # Templates HTML Jinja2
│   │   ├── layout.html          # Base com Navbar, gaveta offcanvas de IA e favoritos
│   │   ├── home.html            # Página inicial no estilo oficial Bambu
│   │   ├── article.html         # Visualizador do artigo com botão de favoritar e TOC
│   │   ├── chat.html            # Chat IA completo com upload de imagem e streaming
│   │   ├── hms.html             # Diagnóstico interativo de erros HMS
│   │   ├── filaments.html       # Tabela e calculadora de filamentos
│   │   ├── search.html          # Resultados de busca com filtros de série
│   │   └── section.html         # Listagem de artigos por categoria
│   └── static/
│       ├── css/style.css        # Design system Bambu + Dark Mode
│       ├── js/app.js            # Lógica dos favoritos, drawer IA, streaming e busca
│       └── images/wiki/         # Cache local de imagens para uso offline
├── crawler/
│   ├── download_images.py       # Download concorrente e reescrita de imagens locais
│   ├── downloader.py            # Coletor assíncrono de páginas com cache
│   ├── parser.py                # Parser do HTML e extrator de TOC/metadados
│   ├── build_db.py              # Banco SQLite + FTS5 com modo WAL
│   └── seed_data.py             # Carga inicial de artigos essenciais
├── Dockerfile                   # Imagem Docker otimizada (Python 3.11-slim)
├── docker-compose.yml           # Orquestração com volumes persistentes
├── requirements.txt             # Dependências Python
├── extract_wiki_links.py        # Extrator de links por idioma via sitemap
├── links_en.txt                 # Lista de 2.744 URLs da wiki oficial
├── links_pt-br.txt              # Lista de 2.523 URLs em português
├── wiki_bambu.db                # Banco de dados com 2.486 artigos indexados
└── run_server.py                # Script de inicialização da aplicação
```

---

## 📝 Licença e Créditos
- Conteúdo técnico e documentação original pertencem à [Bambu Lab](https://bambulab.com/).
- Desenvolvido para a comunidade brasileira de impressão 3D.
