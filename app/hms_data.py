"""
Base de dados estruturada de Códigos de Erro HMS (Health Management System) da Bambu Lab.
Mapeia códigos numéricos para diagnósticos em português, causas prováveis e guias de resolução.
"""

from typing import Any, Dict, List, Optional

HMS_DATABASE: List[Dict[str, Any]] = [
    {
        "code": "0300 0100 0001 0004",
        "raw_code": "0300_0100_0001_0004",
        "module": "Cabeça de Impressão / Aquecedor",
        "severity": "Alta",
        "title": "A temperatura do bico está anormal",
        "description": "O sensor do bico detectou uma temperatura fora da faixa segura ou falha na leitura do termistor.",
        "causes": [
            "Cabo do aquecedor cerâmico ou termistor solto ou desconectado.",
            "Termistor danificado ou queimado por curto-circuito.",
            "Placa da cabeça de impressão (TH Board) com mau contato no conector."
        ],
        "solution_steps": [
            "Desligue a impressora e espere o bico esfriar completamente.",
            "Remova a tampa frontal da cabeça de impressão.",
            "Verifique se o conector branco do termistor e do aquecedor cerâmico estão firmemente encaixados na placa TH.",
            "Inspecione se não há fios rompidos ou pasta térmica vazando sobre os contatos elétricos."
        ],
        "wiki_path": "x1/troubleshooting/hmscode/0300_0100_0001_0004"
    },
    {
        "code": "0700 8000 0002 0001",
        "raw_code": "0700_8000_0002_0001",
        "module": "Sistema AMS (Multi-Material)",
        "severity": "Média",
        "title": "O motor do alimentador do AMS está sobrecarregado ou travado",
        "description": "O filamento encontrou resistência excessiva durante a alimentação ou retração no canal do alimentador do AMS.",
        "causes": [
            "Carretel de filamento com nós ou cruzamento de fios.",
            "Carretel incompatível ou muito pesado travando nas bordas do AMS.",
            "Tubo de PTFE com curvatura muito acentuada causando atrito.",
            "Pedaço de filamento quebrado dentro do funil do alimentador."
        ],
        "solution_steps": [
            "Abra a tampa do AMS e verifique se o carretel gira livremente com a mão.",
            "Puxe suavemente o filamento para verificar se está enrolado ou preso embaixo de outra volta.",
            "Verifique o tubo de PTFE traseiro garantindo que não haja dobras em ângulo reto.",
            "Se necessário, desmonte o alimentador do slot correspondente para retirar fragmentos de filamento quebrados."
        ],
        "wiki_path": "general/troubleshooting/filament-track-switch"
    },
    {
        "code": "0300 0300 0001 0001",
        "raw_code": "0300_0300_0001_0001",
        "module": "Câmara & IA de Visão",
        "severity": "Média",
        "title": "Possível falha de espaguete (cabeleira) detectada pela IA",
        "description": "A câmera interna identificou um acúmulo desordenado de filamento solto sobre a mesa de impressão.",
        "causes": [
            "A peça descolou da placa de impressão durante a execução.",
            "Adesão insuficiente na primeira camada (mesa suja de gordura ou sem cola).",
            "Geometria com saliência extrema sem suportes adequados."
        ],
        "solution_steps": [
            "Pause a impressão imediatamente pelo painel ou aplicativo Bambu Handy.",
            "Inspecione a mesa visualmente para confirmar se a peça se moveu.",
            "Se a peça se soltou, cancele a impressão, limpe a placa PEI com água morna e detergente neutro e reinicie."
        ],
        "wiki_path": "general/troubleshooting/first-layer"
    },
    {
        "code": "0500 0200 0001 0002",
        "raw_code": "0500_0200_0001_0002",
        "module": "Eixo Z & Nivelamento",
        "severity": "Alta",
        "title": "A mesa de impressão não consegue atingir a posição inicial (Home)",
        "description": "Os sensores de força do leito aquecido não detectaram o contato no tempo esperado ou encontraram obstáculos.",
        "causes": [
            "Objeto estranho ou resto de plástico embaixo da mesa de impressão travando os fusos Z.",
            "Placa de impressão posicionada fora dos encaixes traseiros.",
            "Tensão irregular das correias do eixo Z na parte inferior."
        ],
        "solution_steps": [
            "Verifique o fundo da câmara da impressora e remova restos de filamento caídos embaixo da mesa.",
            "Certifique-se de que a placa flexível de impressão está perfeitamente alinhada com as guias magnéticas traseiras.",
            "Execute um novo teste de autodiagnóstico no menu de calibração."
        ],
        "wiki_path": "x1/maintenance/belt-tension"
    },
    {
        "code": "0300 0a00 0001 0001",
        "raw_code": "0300_0a00_0001_0001",
        "module": "Sensores de Ressonância (MC)",
        "severity": "Baixa",
        "title": "Ressonância do eixo XY fora da faixa ideal",
        "description": "O teste de compensação de vibração mediu uma frequência de ressonância fora dos parâmetros esperados.",
        "causes": [
            "Correias de movimento CoreXY frouxas ou com tensão desequilibrada entre os lados.",
            "Hastes de fibra de carbono do eixo X com acúmulo de poeira ou resíduos de plástico.",
            "A impressora está apoiada sobre uma superfície instável ou mesa bamba."
        ],
        "solution_steps": [
            "Limpe as hastes de carbono com álcool isopropílico e pano de microfibra sem fiapos (não use graxa nem óleo nas hastes de carbono!).",
            "Solte os parafusos traseiros dos tensionadores de correia, mova o cabeçote manualmente 5 vezes e reaperte.",
            "Rode a Calibração de Ressonância nas configurações da máquina."
        ],
        "wiki_path": "x1/maintenance/belt-tension"
    },
    {
        "code": "0700 4500 0002 0001",
        "raw_code": "0700_4500_0002_0001",
        "module": "AMS Hub / Sensor de Filamento",
        "severity": "Média",
        "title": "Filamento quebrado ou retração incompleta",
        "description": "O sensor de filamento na entrada do extrusor ainda detecta filamento enquanto o AMS tenta recolher o fio.",
        "causes": [
            "Filamento úmido e quebradiço partiu dentro do tubo de PTFE.",
            "Extrusora com fragmento retido na alavanca de corte.",
            "Lâmina de corte desgastada ou emperrada."
        ],
        "solution_steps": [
            "Pressione a alavanca manual do cortador de filamento no lado esquerdo da cabeça de impressão para garantir que cortou até o fim.",
            "Desconecte o acoplador de tubo PTFE superior e puxe manualmente o filamento se estiver acessível.",
            "Aqueça o hotend e empurre um filamento novo para purgar fragmentos se necessário."
        ],
        "wiki_path": "general/troubleshooting/filament-track-switch"
    }
]


def search_hms_codes(query: str) -> List[Dict[str, Any]]:
    """Busca códigos HMS por correspondência de código numérico, módulo ou descrição."""
    if not query:
        return HMS_DATABASE

    q_clean = query.replace("_", " ").replace("-", " ").strip().lower()
    results = []

    for item in HMS_DATABASE:
        code_str = item["code"].lower()
        raw_code = item["raw_code"].lower()
        title = item["title"].lower()
        desc = item["description"].lower()
        module = item["module"].lower()

        if q_clean in code_str or q_clean in raw_code or q_clean in title or q_clean in desc or q_clean in module:
            results.append(item)

    return results
