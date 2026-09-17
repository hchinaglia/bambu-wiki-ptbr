"""
Base de Conhecimento e Checklist Oficial de Manutenção Preventiva para Impressoras Bambu Lab.
Baseado estritamente nos manuais de manutenção periódica da Bambu Lab.
"""

from typing import Any, Dict, List

MAINTENANCE_PRINTERS = [
    {"id": "all", "name": "Todas as Impressoras"},
    {"id": "x1-carbon", "name": "Bambu Lab X1-Carbon / X1E"},
    {"id": "p1s", "name": "Bambu Lab P1S"},
    {"id": "p1p", "name": "Bambu Lab P1P"},
    {"id": "a1", "name": "Bambu Lab A1"},
    {"id": "a1-mini", "name": "Bambu Lab A1 Mini"},
    {"id": "a2l", "name": "Bambu Lab A2L (Grande Formato)"},
    {"id": "ams", "name": "Sistema AMS / AMS Lite"},
]

MAINTENANCE_TASKS: List[Dict[str, Any]] = [
    {
        "id": "carbon_rods_clean",
        "title": "Limpeza das Hastes de Carbono (Eixo X)",
        "printers": ["x1-carbon", "p1s", "p1p"],
        "category": "Eixo X",
        "frequency_days": 30,
        "frequency_label": "A cada 30 dias ou 150h de impressão",
        "difficulty": "Fácil (10 min)",
        "tools_needed": "Álcool Isopropílico 99% (IPA) e pano de microfibra sem fiapos",
        "critical_alert": "⚠️ ALERTA CRÍTICO: NUNCA aplique graxa, óleo ou lubrificante nas hastes de carbono! As buchas da cabeça são de grafite autolubrificante e graxa causará acúmulo de poeira e danos irreversíveis.",
        "steps": [
            "Desligue a impressora da tomada antes de iniciar.",
            "Dobre o pano de microfibra e umedeça generosamente com álcool isopropílico (IPA 99%).",
            "Limpe suavemente as duas hastes de carbono do eixo X de uma extremidade à outra.",
            "Mova a cabeça de impressão manualmente para o centro e limpe as extremidades onde ela estava repousada.",
            "Repita a limpeza até o pano sair limpo (sem resíduos escuros de poeira de carbono)."
        ],
        "wiki_guide_url": "/wiki/x1/maintenance/clean-carbon-rods"
    },
    {
        "id": "z_lead_screws_lube",
        "title": "Limpeza e Lubrificação dos Fusos Roscados (Eixo Z)",
        "printers": ["x1-carbon", "p1s", "p1p", "a1", "a1-mini", "a2l"],
        "category": "Eixo Z",
        "frequency_days": 90,
        "frequency_label": "A cada 90 dias ou 300h de impressão",
        "difficulty": "Médio (15 min)",
        "tools_needed": "Graxa sintética com PTFE (Magnalube-G ou graxa oficial Bambu Lab), pincel pequeno e pano de microfibra",
        "critical_alert": "Nunca deixe a graxa velha acumular poeira; limpe primeiro com o pano antes de aplicar nova graxa.",
        "steps": [
            "Abaixe a mesa de impressão para o fundo da impressora através da tela de controle.",
            "Use um pano de microfibra limpo para remover toda a graxa preta e resíduos dos fusos roscados de aço do eixo Z.",
            "Com um pincel ou ponta de espátula, aplique uma fina camada de graxa sintética nova ao longo dos fusos.",
            "Pelo painel da impressora, suba e desça a mesa completamente 2 ou 3 vezes para distribuir a graxa uniformemente.",
            "Remova qualquer excesso de graxa que se acumular nas extremidades dos fusos."
        ],
        "wiki_guide_url": "/wiki/x1/maintenance/lead-screw-lubrication"
    },
    {
        "id": "y_axis_lube",
        "title": "Limpeza e Lubrificação das Guias Metálicas (Eixo Y)",
        "printers": ["x1-carbon", "p1s", "p1p", "a1", "a2l"],
        "category": "Eixo Y",
        "frequency_days": 90,
        "frequency_label": "A cada 90 dias ou 300h de impressão",
        "difficulty": "Fácil (10 min)",
        "tools_needed": "Óleo lubrificante mineral fino (ISO VG 32/68 ou óleo de máquina de costura Singer)",
        "critical_alert": "Use poucas gotas; excesso de óleo pode espirrar na chapa de impressão.",
        "steps": [
            "Limpe as duas hastes metálicas cilíndricas do eixo Y com um pano limpo para remover poeira.",
            "Aplique de 2 a 3 gotas de óleo lubrificante mineral fino em cada haste metálica.",
            "Mova o conjunto do eixo X para frente e para trás manualmente para lubrificar os rolamentos lineares.",
            "Passe um pano seco para retirar qualquer gota em excesso."
        ],
        "wiki_guide_url": "/wiki/p1/maintenance/linear-rails"
    },
    {
        "id": "belt_tension",
        "title": "Re-tensionamento de Correias dos Eixos X e Y",
        "printers": ["x1-carbon", "p1s", "p1p"],
        "category": "Correias",
        "frequency_days": 90,
        "frequency_label": "A cada 90 dias ou após aviso de ressonância HMS",
        "difficulty": "Fácil (5 min)",
        "tools_needed": "Chave Allen H2.0 (inclusa na caixa da impressora)",
        "critical_alert": "Não aperte demais; o sistema de molas internas da Bambu Lab ajusta a tensão sozinho.",
        "steps": [
            "Desligue a impressora.",
            "Localize os dois parafusos tensores de correia na parte traseira da impressora.",
            "Solte os parafusos apenas 1 a 2 voltas (NÃO remova os parafusos!).",
            "Mova a cabeça de impressão suavemente em padrão cruzado (frente, trás, esquerda, direita) 3 vezes para as molas igualarem a tensão.",
            "Com a cabeça parada no canto traseiro, aperte firmemente os dois parafusos tensores.",
            "Ligue a impressora e execute a calibração de compensação de vibração."
        ],
        "wiki_guide_url": "/wiki/x1/maintenance/belt-tension"
    },
    {
        "id": "filament_cutter",
        "title": "Inspeção da Lâmina do Cortador de Filamento",
        "printers": ["x1-carbon", "p1s", "p1p", "a1", "a1-mini", "a2l"],
        "category": "Cabeça de Impressão",
        "frequency_days": 90,
        "frequency_label": "A cada 90 dias ou 3.000 trocas de filamento",
        "difficulty": "Médio (10 min)",
        "tools_needed": "Chave Allen H1.5/H2.0 e lâmina reserva (inclusa no kit sobressalente)",
        "critical_alert": "Cuidado ao manipular a lâmina; ela é extremamente afiada.",
        "steps": [
            "Retire a capa frontal magnética da cabeça de impressão.",
            "Pressione a alavanca lateral do cortador e verifique se a lâmina desliza suavemente e retorna pela mola.",
            "Se a ponta estiver cega ou entortada, solte o parafuso de fixação e substitua pela lâmina reserva.",
            "Recoloque a capa magnética e faça um teste manual de corte de filamento."
        ],
        "wiki_guide_url": "/wiki/x1/maintenance/replace-cutter"
    },
    {
        "id": "ams_desiccant",
        "title": "Inspeção e Troca da Sílica Gel do AMS",
        "printers": ["ams"],
        "category": "AMS",
        "frequency_days": 45,
        "frequency_label": "A cada 30 a 60 dias (ou se o indicador do AMS passar de nível 3)",
        "difficulty": "Fácil (5 min)",
        "tools_needed": "2 sachês novos de sílica gel ou esferas dessecantes recarregáveis",
        "critical_alert": "Filamento úmido causa estalos, teias e emperramento do AMS.",
        "steps": [
            "Remova os 4 carretéis de filamento de dentro do AMS.",
            "Abra os dois compartimentos traseiros de sílica gel levantando a tampa plástica.",
            "Verifique se o dessecante virou gel líquido ou mudou de cor (sílica saturada).",
            "Substitua por novos sachês secos de 50g ou sílica laranja/azul regenerada em forno.",
            "Feche as tampas e recoloque os carretéis."
        ],
        "wiki_guide_url": "/wiki/ams/maintenance/replace-desiccant"
    },
    {
        "id": "extruder_cleaning",
        "title": "Inspeção e Limpeza das Engrenagens do Extrusor",
        "printers": ["x1-carbon", "p1s", "p1p", "a1", "a1-mini", "a2l"],
        "category": "Extrusor",
        "frequency_days": 180,
        "frequency_label": "A cada 180 dias ou após quebra de filamento abrasivo",
        "difficulty": "Avançado (20 min)",
        "tools_needed": "Pincel de cerdas duras, pinça fina e chave Allen H2.0",
        "critical_alert": "Cuidado com os cabos flat e sensores do bico durante a abertura.",
        "steps": [
            "Desconecte os cabos do hotend e retire o conjunto do extrusor conforme o manual.",
            "Abra a tampa do extrusor e verifique se há pó plástico acumulado nos dentes das engrenagens.",
            "Use o pincel e a pinça para limpar completamente os dentes de tração de aço temperado.",
            "Verifique se as engrenagens giram suavemente sem folga excessiva.",
            "Feche o extrusor e reconecte os conectores na placa da cabeça."
        ],
        "wiki_guide_url": "/wiki/x1/maintenance/extruder-maintenance"
    },
    {
        "id": "full_calibration",
        "title": "Calibração Completa de Vibração e Nivelamento",
        "printers": ["x1-carbon", "p1s", "p1p", "a1", "a1-mini", "a2l"],
        "category": "Calibração",
        "frequency_days": 90,
        "frequency_label": "A cada 90 dias ou sempre que trocar de mesa/bancada",
        "difficulty": "Automático (15 min)",
        "tools_needed": "Nenhuma ferramenta necessária",
        "critical_alert": "Não encoste na impressora ou na mesa durante a calibração de vibração.",
        "steps": [
            "Limpe a chapa de impressão e certifique-se de que está bem assentada nos batentes.",
            "Na tela da impressora, acesse Configurações -> Calibração -> Iniciar Calibração Geral.",
            "Aguarde o ciclo automático de nivelamento de mesa e compensação de ressonância (cerca de 12 a 15 minutos).",
            "A impressora emitirá um sinal sonoro confirmando a conclusão com sucesso."
        ],
        "wiki_guide_url": "/wiki/x1/manual/calibration"
    }
]


def get_all_maintenance_tasks() -> List[Dict[str, Any]]:
    """Retorna todas as tarefas de manutenção."""
    return MAINTENANCE_TASKS


def get_tasks_for_printer(printer_id: str) -> List[Dict[str, Any]]:
    """Retorna tarefas aplicáveis a uma impressora específica."""
    if not printer_id or printer_id == "all":
        return MAINTENANCE_TASKS
    return [t for t in MAINTENANCE_TASKS if printer_id in t["printers"] or "all" in t["printers"]]
