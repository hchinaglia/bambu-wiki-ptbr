"""
Base de Conhecimento e Diagnóstico Visual de Falhas de Impressão FDM para Bambu Lab.
Contém os 14 principais problemas de fatiamento e hardware com passo a passo oficial.
"""

from typing import Any, Dict, List, Optional

DEFECTS_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "stringing",
        "name": "Stringing / Teias e Fios de Cabelo",
        "category": "extrusao",
        "category_name": "Extrusão & Bico",
        "severity": "Fácil",
        "badge_color": "warning",
        "icon": "bi-bezier2",
        "summary": "Fios finos parecidos com teias de aranha deixados pelo bico durante movimentos de viagem (travel) entre partes da peça.",
        "causes": [
            "Umidade no filamento (a água ferve dentro do bico e expande empurrando plástico).",
            "Temperatura do bico excessivamente alta para o filamento.",
            "Distância de retração insuficiente ou velocidade de retração lenta.",
            "Função 'Z-Hop' configurada com altura excessiva."
        ],
        "bambu_studio_fixes": [
            "Aba Filament -> Temperature: Reduza a temperatura do bico em 5 °C a 10 °C.",
            "Aba Setting -> Retraction: Verifique a distância de retração (0.8mm para bico Direct Drive da Bambu).",
            "Aba Others -> Travel: Ative 'Reduce infill retraction' ou 'Wipe while retracting'.",
            "Secagem do Filamento: Seque o carretel por 6h a 8h na temperatura indicada (55°C para PLA, 65°C para PETG)."
        ],
        "wiki_link": "/filamentos",
        "quick_prompt": "Minha impressão está com muito stringing (teias de aranha finas). Como calibro a retração e temperatura no Bambu Studio?"
    },
    {
        "id": "warping",
        "name": "Warping / Empenamento das Bordas",
        "category": "adesao",
        "category_name": "Adesão à Mesa",
        "severity": "Médio",
        "badge_color": "danger",
        "icon": "bi-arrow-up-right-square",
        "summary": "As extremidades inferiores da peça descolam da mesa de impressão e dobram para cima conforme as camadas superiores resfriam.",
        "causes": [
            "Contração térmica do plástico durante o resfriamento rápido (muito comum em ABS, ASA, PC e PETG).",
            "Gordura de dedos ou poeira na chapa de impressão PEI.",
            "Temperatura da mesa muito baixa.",
            "Correntes de ar ambiente ou porta/tampa superior aberta em materiais técnicos."
        ],
        "bambu_studio_fixes": [
            "Aba Others -> Bed Adhesion: Mude 'Brim type' para 'Outer brim only' com largura de 5mm a 10mm.",
            "Aba Filament -> Bed Temperature: Aumente a temperatura da mesa em +5 °C (ex: 60°C para PLA, 75°C para PETG).",
            "Limpeza da Chapa: Lave a chapa PEI com água morna e detergente neutro (evite álcool em placas texturizadas sujas).",
            "Câmara Fechada: Para ABS/ASA na P1S/X1C, mantenha porta e tampa 100% fechadas e pré-aqueça a câmara por 15 min."
        ],
        "wiki_link": "/calculadora",
        "quick_prompt": "Os cantos da minha peça estão descolando da mesa (warping). Quais parâmetros de mesa, brim e câmara devo ajustar?"
    },
    {
        "id": "under_extrusion",
        "name": "Subextrusão / Falhas e Furos nas Camadas",
        "category": "extrusao",
        "category_name": "Extrusão & Bico",
        "severity": "Médio",
        "badge_color": "danger",
        "icon": "bi-dash-circle-dotted",
        "summary": "A impressora deposita menos filamento do que o necessário, resultando em paredes fracas, buracos nas camadas e peças quebradiças.",
        "causes": [
            "Entupimento parcial do bico (clog) ou resíduos carbonizados.",
            "Vazão volumétrica máxima do filamento configurada acima do que o hotend consegue fundir.",
            "Engrenagens do extrusor sujas ou com dentes desgastados.",
            "Temperatura do bico muito baixa para a velocidade atual."
        ],
        "bambu_studio_fixes": [
            "Faça uma 'Puxada a Frio' (Cold Pull) no bico para limpar impurezas internas.",
            "Aba Filament -> Max Volumetric Speed: Reduza de 21 mm³/s para 15-16 mm³/s para garantir fusão homogênea.",
            "Aba Quality -> Wall generator: Mude para 'Arachne' para ajustar a largura de linha dinamicamente.",
            "Aumente a temperatura de extrusão em +5 °C a +10 °C."
        ],
        "wiki_link": "/wiki/x1/maintenance",
        "quick_prompt": "Minha peça está saindo com falhas e furos nas paredes (subextrusão). Como resolver entupimento parcial e fluxo no Bambu Studio?"
    },
    {
        "id": "over_extrusion",
        "name": "Superextrusão / Camadas Ásperas e Rebarbas",
        "category": "extrusao",
        "category_name": "Extrusão & Bico",
        "severity": "Fácil",
        "badge_color": "warning",
        "icon": "bi-plus-circle",
        "summary": "Excesso de plástico sendo empurrado pelo bico, causando superfícies rugosas, rebarbas nas bordas e perda de precisão dimensional.",
        "causes": [
            "Multiplicador de vazão (Flow Ratio) muito alto.",
            "Diâmetro do filamento inconsistente ou maior que 1.75 mm.",
            "Compensação dinâmica de fluxo (Flow Dynamics / Pressure Advance) descalibrada."
        ],
        "bambu_studio_fixes": [
            "Execute a Calibração de Dinâmica de Fluxo (Flow Dynamics Calibration) no menu Calibrate do Bambu Studio.",
            "Aba Filament -> Flow Ratio: Reduza de 1.00 para 0.96 ou 0.98.",
            "Aba Quality -> Line width: Certifique-se de que a largura de linha não ultrapasse 120% do diâmetro do bico."
        ],
        "wiki_link": "/calculadora",
        "quick_prompt": "Minhas superfícies estão rugosas e com excesso de plástico nas bordas. Como calibro o Flow Ratio no Bambu Studio?"
    },
    {
        "id": "layer_shift",
        "name": "Deslocamento de Camada / Layer Shift",
        "category": "mecanica",
        "category_name": "Mecânica & Movimento",
        "severity": "Crítico",
        "badge_color": "danger",
        "icon": "bi-distribute-vertical",
        "summary": "Em uma determinada altura, toda a parte superior da peça se desloca para o lado em degrau, perdendo o alinhamento com a base.",
        "causes": [
            "Colisão mecânica do bico em infill do tipo 'Grid' (que cruza linhas na mesma altura).",
            "Correias dos eixos X/Y frouxas ou polias com dentes pulando.",
            "Acelerações extremas em peças altas e pesadas.",
            "Objeto ou ferramenta colidindo com a cabeça de impressão durante o curso."
        ],
        "bambu_studio_fixes": [
            "Aba Strength -> Infill: NUNCA use infill 'Grid'! Mude imediatamente para 'Gyroid' ou 'Cross Hatch' (não cruzam linhas na mesma camada).",
            "Aba Speed -> Acceleration: Reduza acelerações de 10.000 mm/s² para 5.000 mm/s² em peças muito altas.",
            "Tensão de Correias: Solte os parafusos tensores traseiros, mova a cabeça e reaperte conforme o manual oficial da Bambu."
        ],
        "wiki_link": "/hms",
        "quick_prompt": "Minha impressão deu deslocamento de camada (layer shift). Como re-tensiono as correias e evito colisão de infill no Bambu Studio?"
    },
    {
        "id": "ghosting",
        "name": "Ghosting & Ringing / Ondulações ao Lado de Quinas",
        "category": "mecanica",
        "category_name": "Mecânica & Movimento",
        "severity": "Fácil",
        "badge_color": "warning",
        "icon": "bi-soundwave",
        "summary": "Linhas verticais repetitivas parecendo ecos ou 'fantasmas' logo após quinas pontiagudas, textos ou relevos da peça.",
        "causes": [
            "Vibrações mecânicas da impressora não compensadas durante mudanças bruscas de direção.",
            "Mesa ou bancada onde a impressora está instalada bamba ou instável.",
            "Falta de calibração de ressonância (Input Shaping).",
            "Velocidade da parede externa muito alta."
        ],
        "bambu_studio_fixes": [
            "Execute a 'Vibration Compensation' (Compensação de Ressonância) na tela da impressora ou no Bambu Studio.",
            "Aba Speed -> Outer wall: Reduza a velocidade da parede externa para 60 - 80 mm/s.",
            "Certifique-se de que a impressora está em uma mesa sólida e rígida (evite mesas com rodinhas ou pés moles)."
        ],
        "wiki_link": "/calculadora",
        "quick_prompt": "Estou com marcas de vibração e ondulações (ghosting/ringing) nas quinas da peça. Como calibrar a ressonância no Bambu Studio?"
    },
    {
        "id": "elephant_foot",
        "name": "Pé de Elefante / Base Alargada e Saliente",
        "category": "adesao",
        "category_name": "Adesão à Mesa",
        "severity": "Fácil",
        "badge_color": "info",
        "icon": "bi-align-bottom",
        "summary": "As primeiras camadas da base ficam mais largas e achatadas que o resto da peça, criando uma rebarba espessa que atrapalha encaixes.",
        "causes": [
            "Primeira camada sendo prensada com excesso de força contra a chapa de impressão.",
            "Mesa aquecida com temperatura muito alta mantendo a base mole enquanto o peso da peça a esmaga."
        ],
        "bambu_studio_fixes": [
            "Aba Quality -> Precision: Ative 'Elephant foot compensation' com valor entre 0.15mm e 0.20mm.",
            "Aba Filament -> Bed Temperature: Reduza a temperatura da mesa em 5 °C após a primeira camada.",
            "Aba Quality -> Initial layer line width: Mantenha a largura de linha inicial em 0.42mm a 0.45mm."
        ],
        "wiki_link": "/calculadora",
        "quick_prompt": "A base da minha peça está ficando mais larga que o modelo 3D (pé de elefante). Onde configuro o Elephant Foot Compensation?"
    },
    {
        "id": "z_banding",
        "name": "Z-Banding / Linhas Horizontais Repetitivas",
        "category": "mecanica",
        "category_name": "Mecânica & Movimento",
        "severity": "Médio",
        "badge_color": "warning",
        "icon": "bi-reception-3",
        "summary": "Linhas horizontais periódicas e visíveis em toda a altura da peça, dando uma textura listrada às paredes verticais.",
        "causes": [
            "Fuso roscado do eixo Z com sujeira, poeira ou graxa ressecada.",
            "Variação de temperatura na mesa aquecida (ciclos PID descalibrados).",
            "Variação no diâmetro do filamento ao longo do carretel."
        ],
        "bambu_studio_fixes": [
            "Limpeza do Fuso Z: Limpe as 3 hastes roscadas do eixo Z com pano de microfibra e aplique nova graxa sintética (Magnalube/PTFE).",
            "Aba Quality -> Layer height: Use alturas de camada proporcionais ao passo do motor (0.12mm, 0.16mm, 0.20mm).",
            "Verifique se o bico está bem parafusado no bloco aquecedor sem folgas."
        ],
        "wiki_link": "/wiki/x1/maintenance",
        "quick_prompt": "Minhas paredes estão com listras horizontais periódicas (Z-Banding). Como limpar os fusos Z e lubrificar a impressora?"
    },
    {
        "id": "blobs_zits",
        "name": "Blobs & Zits / Espinhas e Bolhas na Superfície",
        "category": "superficie",
        "category_name": "Qualidade Superficial",
        "severity": "Fácil",
        "badge_color": "warning",
        "icon": "bi-circle-half",
        "summary": "Pequenas bolinhas salientes de plástico espalhadas pelas paredes externas, parecidas com espinhas.",
        "causes": [
            "Troca de camada e ponto de início/fim de perímetro (Costura / Seam).",
            "Filamento úmido: bolhas de vapor estouram no bico e deixam marcas.",
            "Desaceleração da cabeça ao ler código G-Code com muitos nós minúsculos."
        ],
        "bambu_studio_fixes": [
            "Aba Quality -> Seam position: Mude de 'Random' para 'Aligned' ou 'Back' (oculta a costura em uma quina viva).",
            "Aba Quality -> Seam gap: Ajuste para 10% a 15% para suavizar a transição da costura.",
            "Seque o carretel de filamento em uma estufa ou no leito aquecido da impressora."
        ],
        "wiki_link": "/calculadora",
        "quick_prompt": "Aparecem pequenas bolinhas na superfície da impressão (blobs/zits). Como alinhar e esconder a costura (seam) no Bambu Studio?"
    },
    {
        "id": "poor_bridging",
        "name": "Pontes Caídas / Poor Bridging",
        "category": "temperatura",
        "category_name": "Temperatura & Resfriamento",
        "severity": "Fácil",
        "badge_color": "warning",
        "icon": "bi-cone-striped",
        "summary": "Filamentos que precisam ser estendidos horizontalmente no ar entre dois pontos caem e desmancham em fios soltos.",
        "causes": [
            "Ventoinha de resfriamento da peça (Part Fan) com velocidade insuficiente para solidificar o filamento no ar.",
            "Velocidade de ponte (Bridge Speed) muito rápida ou muito lenta.",
            "Temperatura de extrusão excessiva."
        ],
        "bambu_studio_fixes": [
            "Aba Filament -> Cooling: Certifique-se de que a ventoinha da peça atinge 100% em pontes.",
            "Aba Speed -> Bridge: Ajuste a velocidade para 30 - 50 mm/s.",
            "Aba Quality -> Line width -> Bridge: Use fluxo de ponte com densidade 0.95 para esticar o fio sem sobrecarregar."
        ],
        "wiki_link": "/calculadora",
        "quick_prompt": "As pontes horizontais da minha peça estão caindo e ficando desfiadas. Quais ajustes de ventoinha e velocidade de ponte usar?"
    },
    {
        "id": "first_layer",
        "name": "Primeira Camada Falhada ou Ondulada",
        "category": "adesao",
        "category_name": "Adesão à Mesa",
        "severity": "Médio",
        "badge_color": "danger",
        "icon": "bi-grid-1x2",
        "summary": "A primeira camada fica com linhas separadas que não se unem, ou com relevos enrugados parecendo plástico rasgado.",
        "causes": [
            "Nivelamento automático da mesa (Auto-Bed Leveling) desativado antes da impressão.",
            "Restos de filamento duro na ponta do bico interferindo no sensor piezoelétrico durante o probe.",
            "Tipo de chapa incorreto selecionado no Bambu Studio (ex: Cool Plate selecionada com chapa Textured PEI)."
        ],
        "bambu_studio_fixes": [
            "Sempre marque a opção 'Auto Bed Leveling' na janela de envio de impressão da impressora.",
            "Verifique se o bico foi limpo na calha traseira antes de iniciar o probe da mesa.",
            "No topo do Bambu Studio, certifique-se de selecionar a chapa correta: 'Textured PEI Plate'."
        ],
        "wiki_link": "/calculadora",
        "quick_prompt": "Minha primeira camada está saindo falhada ou muito colada. Como garantir o nivelamento perfeito da mesa na Bambu Lab?"
    },
    {
        "id": "delamination",
        "name": "Delaminação / Rachaduras entre Camadas",
        "category": "temperatura",
        "category_name": "Temperatura & Resfriamento",
        "severity": "Crítico",
        "badge_color": "danger",
        "icon": "bi-layers-half",
        "summary": "As camadas se separam facilmente com a mão ou abrem rachaduras horizontais durante a impressão em ABS, ASA ou PETG.",
        "causes": [
            "Falta de fusão térmica entre as camadas devido a resfriamento excessivo.",
            "Ventoinha de peça ligada com força em materiais de alta contração (ABS/ASA).",
            "Câmara fria ou correntes de ar na impressora."
        ],
        "bambu_studio_fixes": [
            "Aba Filament -> Cooling: Desligue a ventoinha auxiliar (Aux Fan = 0%) e limite a ventoinha de peça a no máximo 10-20% em ABS/ASA.",
            "Aba Filament -> Temperature: Aumente a temperatura do bico em +10 °C para promover fusão molecular.",
            "Mantenha a câmara fechada com temperatura interna acima de 40 °C."
        ],
        "wiki_link": "/filamentos",
        "quick_prompt": "Minhas peças em ABS/PETG estão rachando entre as camadas (delaminação). Quais configurações de ventoinha e câmara usar?"
    },
    {
        "id": "heat_creep",
        "name": "Heat Creep / Entupimento por Retorno de Calor",
        "category": "temperatura",
        "category_name": "Temperatura & Resfriamento",
        "severity": "Crítico",
        "badge_color": "danger",
        "icon": "bi-thermometer-high",
        "summary": "O filamento amolece antes de entrar no bico (dentro da garganta do hotend ou extrusor), gerando entupimento total.",
        "causes": [
            "Imprimir PLA com a porta de vidro e tampa 100% fechadas na X1-Carbon ou P1S (o ar interno passa de 38°C e amolece o PLA prematuramente).",
            "Ventoinha do hotend (não a de peça) com poeira ou rotação lenta."
        ],
        "bambu_studio_fixes": [
            "REGRA DE OURO DA BAMBU LAB: Ao imprimir PLA ou TPU em impressoras fechadas (X1C / P1S), deixe a porta frontal entreaberta ou retire a tampa de vidro superior!",
            "Verifique se a ventoinha do dissipador de calor está girando normalmente.",
            "Se entupir, use a agulha de desobstrução aquecendo o bico a 250 °C."
        ],
        "wiki_link": "/hms",
        "quick_prompt": "Meu filamento PLA está emperrando no extrusor por retorno de calor (heat creep). Por que devo deixar a porta aberta na P1S/X1C?"
    },
    {
        "id": "spaghetti",
        "name": "Efeito Espaguete / Emaranhado de Plástico no Ar",
        "category": "adesao",
        "category_name": "Adesão à Mesa",
        "severity": "Crítico",
        "badge_color": "danger",
        "icon": "bi-water",
        "summary": "A peça se descola da mesa no meio do trabalho e a cabeça continua expelindo plástico no ar, criando um grande ninho de filamento solto.",
        "causes": [
            "Perda total de adesão da primeira camada com a mesa.",
            "Suportes finos ou instáveis que quebraram no caminho.",
            "Colisão da cabeça de impressão que derrubou a peça."
        ],
        "bambu_studio_fixes": [
            "Na X1-Carbon, mantenha a função 'Spaghetti Detection' com IA ativada no menu da impressora para pausar automaticamente.",
            "Use suportes tipo 'Tree (auto)' com base de fixação alargada (Brim de suporte).",
            "Lave a chapa com água morna e detergente neutro antes de reimprimir."
        ],
        "wiki_link": "/calculadora",
        "quick_prompt": "Minha peça descolou e virou um emaranhado de espaguete. Como evitar perda de adesão e configurar suportes mais firmes?"
    }
]


def get_all_defects() -> List[Dict[str, Any]]:
    """Retorna a lista completa de defeitos catalogados."""
    return DEFECTS_CATALOG


def get_defect_by_id(defect_id: str) -> Optional[Dict[str, Any]]:
    """Busca um defeito específico pelo ID."""
    for d in DEFECTS_CATALOG:
        if d["id"] == defect_id:
            return d
    return None
