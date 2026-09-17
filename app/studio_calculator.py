"""
Motor de Cálculo e Otimização de Configurações para o Bambu Studio.
Regras e parâmetros calibrados de acordo com a documentação oficial da Bambu Lab,
perfis predefinidos de fábrica e guias técnicos de engenharia.
"""

from typing import Any, Dict, List, Optional


# Definição das Impressoras
PRINTERS_CONFIG = {
    "x1-carbon": {
        "name": "Bambu Lab X1-Carbon / X1E",
        "type": "CoreXY Fechada",
        "has_enclosure": True,
        "has_aux_fan": True,
        "has_chamber_temp": True,
        "default_nozzle_material": "Aço Endurecido (Hardened Steel)",
        "max_hotend_temp": 300,
        "max_bed_temp": 120,
    },
    "p1s": {
        "name": "Bambu Lab P1S",
        "type": "CoreXY Fechada",
        "has_enclosure": True,
        "has_aux_fan": True,
        "has_chamber_temp": False,
        "default_nozzle_material": "Aço Inoxidável (Recomenda-se upgrade para Hardened)",
        "max_hotend_temp": 300,
        "max_bed_temp": 100,
    },
    "p1p": {
        "name": "Bambu Lab P1P",
        "type": "CoreXY Aberta",
        "has_enclosure": False,
        "has_aux_fan": False,
        "has_chamber_temp": False,
        "default_nozzle_material": "Aço Inoxidável",
        "max_hotend_temp": 300,
        "max_bed_temp": 100,
    },
    "a1": {
        "name": "Bambu Lab A1 (Full Size)",
        "type": "Bed Slinger Aberta",
        "has_enclosure": False,
        "has_aux_fan": False,
        "has_chamber_temp": False,
        "default_nozzle_material": "Aço Inoxidável (Quick Swap)",
        "max_hotend_temp": 300,
        "max_bed_temp": 100,
    },
    "a1-mini": {
        "name": "Bambu Lab A1 Mini",
        "type": "Bed Slinger Mini Aberta",
        "has_enclosure": False,
        "has_aux_fan": False,
        "has_chamber_temp": False,
        "default_nozzle_material": "Aço Inoxidável (Quick Swap)",
        "max_hotend_temp": 300,
        "max_bed_temp": 80,
    },
    "a2l": {
        "name": "Bambu Lab A2L (Grande Formato)",
        "type": "Bed Slinger Aberta (330×320×325 mm)",
        "has_enclosure": False,
        "has_aux_fan": False,
        "has_chamber_temp": False,
        "default_nozzle_material": "Aço Inoxidável (Quick Swap)",
        "max_hotend_temp": 300,
        "max_bed_temp": 80,
    },
}

# Definição dos Materiais e suas características térmicas e físicas
FILAMENTS_CONFIG = {
    "pla-basic": {
        "name": "Bambu PLA Basic / Matte / Silk",
        "category": "Padrão",
        "abrasive": False,
        "ams_ok": True,
        "temp_nozzle_initial": 220,
        "temp_nozzle_other": 215,
        "bed_temps": {
            "textured_pei": 55,
            "smooth_pei": 55,
            "high_temp": 55,
            "cool_plate": 35,
            "engineering": 55,
        },
        "cooling": {"part_fan_min": 100, "part_fan_max": 100, "aux_fan": 70, "chamber_fan": 70},
        "max_volumetric_speed": 21.0,
        "enclosure_rule": "open",
        "drying": "55 °C por 8h (se apresentar estalos ou fios)",
        "glue": "Desnecessária em PEI Texturizado / Opcional em Placa Fria",
    },
    "petg": {
        "name": "Bambu PETG Basic / HF",
        "category": "Técnico Resistente",
        "abrasive": False,
        "ams_ok": True,
        "temp_nozzle_initial": 250,
        "temp_nozzle_other": 245,
        "bed_temps": {
            "textured_pei": 70,
            "smooth_pei": 70,
            "high_temp": 70,
            "cool_plate": 65,
            "engineering": 70,
        },
        "cooling": {"part_fan_min": 40, "part_fan_max": 70, "aux_fan": 0, "chamber_fan": 0},
        "max_volumetric_speed": 16.0,
        "enclosure_rule": "neutral",
        "drying": "65 °C por 8h (altamente recomendado antes de imprimir)",
        "glue": "Não no PEI texturizado. OBRIGATÓRIA cola líquida em PEI liso (atua como desmoldante para não rasgar o PEI)",
    },
    "abs": {
        "name": "Bambu ABS",
        "category": "Engenharia",
        "abrasive": False,
        "ams_ok": True,
        "temp_nozzle_initial": 260,
        "temp_nozzle_other": 255,
        "bed_temps": {
            "textured_pei": 95,
            "smooth_pei": 95,
            "high_temp": 95,
            "cool_plate": 90,
            "engineering": 95,
        },
        "cooling": {"part_fan_min": 0, "part_fan_max": 20, "aux_fan": 0, "chamber_fan": 0},
        "max_volumetric_speed": 18.0,
        "enclosure_rule": "closed",
        "drying": "80 °C por 8h",
        "glue": "Recomendada cola líquida Bambu para evitar warping nos cantos",
    },
    "asa": {
        "name": "Bambu ASA (Resistente UV / Externo)",
        "category": "Engenharia / Automotivo",
        "abrasive": False,
        "ams_ok": True,
        "temp_nozzle_initial": 260,
        "temp_nozzle_other": 255,
        "bed_temps": {
            "textured_pei": 95,
            "smooth_pei": 95,
            "high_temp": 95,
            "cool_plate": 90,
            "engineering": 95,
        },
        "cooling": {"part_fan_min": 0, "part_fan_max": 25, "aux_fan": 0, "chamber_fan": 0},
        "max_volumetric_speed": 18.0,
        "enclosure_rule": "closed",
        "drying": "80 °C por 8h",
        "glue": "Recomendada cola líquida Bambu para fixação em cantos críticos",
    },
    "tpu-95a": {
        "name": "Bambu TPU 95A / HF (Flexível)",
        "category": "Flexível",
        "abrasive": False,
        "ams_ok": False,
        "temp_nozzle_initial": 230,
        "temp_nozzle_other": 225,
        "bed_temps": {
            "textured_pei": 40,
            "smooth_pei": 40,
            "high_temp": 40,
            "cool_plate": 35,
            "engineering": 40,
        },
        "cooling": {"part_fan_min": 80, "part_fan_max": 100, "aux_fan": 0, "chamber_fan": 0},
        "max_volumetric_speed": 3.6,
        "enclosure_rule": "open",
        "drying": "70 °C por 8h (obrigatório, TPU absorve umidade em poucas horas)",
        "glue": "Recomendada cola líquida como desmoldante (TPU adere excessivamente ao PEI)",
    },
    "pa-cf": {
        "name": "Bambu PA-CF / PAHT-CF (Nylon Fibra de Carbono)",
        "category": "Compósitos Industriais",
        "abrasive": True,
        "ams_ok": True,
        "temp_nozzle_initial": 290,
        "temp_nozzle_other": 285,
        "bed_temps": {
            "textured_pei": 100,
            "smooth_pei": 100,
            "high_temp": 100,
            "cool_plate": 90,
            "engineering": 100,
        },
        "cooling": {"part_fan_min": 0, "part_fan_max": 30, "aux_fan": 0, "chamber_fan": 0},
        "max_volumetric_speed": 14.0,
        "enclosure_rule": "closed",
        "drying": "80 °C por 8h a 12h (Nylon é extremamente hidroscópico)",
        "glue": "Recomendada cola líquida em Placa de Engenharia ou PEI Texturizado",
    },
    "petg-cf": {
        "name": "Bambu PETG-CF (Fibra de Carbono)",
        "category": "Compósitos",
        "abrasive": True,
        "ams_ok": True,
        "temp_nozzle_initial": 255,
        "temp_nozzle_other": 250,
        "bed_temps": {
            "textured_pei": 75,
            "smooth_pei": 75,
            "high_temp": 75,
            "cool_plate": 70,
            "engineering": 75,
        },
        "cooling": {"part_fan_min": 30, "part_fan_max": 60, "aux_fan": 0, "chamber_fan": 0},
        "max_volumetric_speed": 14.0,
        "enclosure_rule": "neutral",
        "drying": "65 °C por 8h",
        "glue": "Opcional em PEI texturizado",
    },
    "pla-cf": {
        "name": "Bambu PLA-CF",
        "category": "Compósitos",
        "abrasive": True,
        "ams_ok": True,
        "temp_nozzle_initial": 220,
        "temp_nozzle_other": 215,
        "bed_temps": {
            "textured_pei": 55,
            "smooth_pei": 55,
            "high_temp": 55,
            "cool_plate": 35,
            "engineering": 55,
        },
        "cooling": {"part_fan_min": 100, "part_fan_max": 100, "aux_fan": 70, "chamber_fan": 70},
        "max_volumetric_speed": 18.0,
        "enclosure_rule": "open",
        "drying": "55 °C por 8h",
        "glue": "Não necessária em PEI",
    },
    "pc": {
        "name": "Bambu PC (Policarbonato)",
        "category": "Engenharia Avançada",
        "abrasive": False,
        "ams_ok": True,
        "temp_nozzle_initial": 275,
        "temp_nozzle_other": 270,
        "bed_temps": {
            "textured_pei": 105,
            "smooth_pei": 105,
            "high_temp": 105,
            "cool_plate": 100,
            "engineering": 110,
        },
        "cooling": {"part_fan_min": 0, "part_fan_max": 20, "aux_fan": 0, "chamber_fan": 0},
        "max_volumetric_speed": 15.0,
        "enclosure_rule": "closed",
        "drying": "80 °C por 8h a 12h",
        "glue": "OBRIGATÓRIO cola líquida Bambu em Placa de Engenharia",
    },
}

# Objetivos / Intenções de Impressão
OBJECTIVES_CONFIG = {
    "balanced": {
        "name": "🎯 Equilibrado / Padrão Oficial",
        "description": "Balanço perfeito de fábrica entre tempo, resistência mecânica e acabamento superficial suave.",
    },
    "visual": {
        "name": "✨ Visual / Estético & Miniaturas",
        "description": "Foco máximo em resolução, minimização de linhas de camada e costura imperceptível.",
    },
    "strength": {
        "name": "🛡️ Resistência Mecânica / Estrutural",
        "description": "Paredes sólidas reforçadas, infill denso e fusão máxima entre camadas para suportar carga e impacto.",
    },
    "fast": {
        "name": "⚡ Rápido / Prototipagem Ágil",
        "description": "Camadas maiores e preenchimento veloz para economizar até 45% do tempo de impressão.",
    },
    "precision": {
        "name": "📐 Precisão Dimensional / Encaixes",
        "description": "Controle estrito de tolerâncias para roscas, engrenagens, mancais e peças de encaixe sob pressão.",
    },
    "watertight": {
        "name": "💧 Estanque / À Prova d'Água (Vaso/Recipiente)",
        "description": "Fusão completa de perímetros, sobreposição de preenchimento e fluxo aumentado para retenção de líquidos.",
    },
}


def calculate_slicing_profile(
    printer_id: str = "p1s",
    nozzle_size: float = 0.4,
    nozzle_material: str = "hardened",
    filament_id: str = "pla-basic",
    objective_id: str = "balanced",
    plate_id: str = "textured_pei",
    enable_support: bool = False,
    support_type: str = "tree",
) -> Dict[str, Any]:
    """Calcula todas as configurações ideais para o Bambu Studio de acordo com as especificações selecionadas."""
    
    printer = PRINTERS_CONFIG.get(printer_id, PRINTERS_CONFIG["p1s"])
    filament = FILAMENTS_CONFIG.get(filament_id, FILAMENTS_CONFIG["pla-basic"])
    objective = OBJECTIVES_CONFIG.get(objective_id, OBJECTIVES_CONFIG["balanced"])
    
    is_tpu = "tpu" in filament_id
    is_composite = filament["abrasive"]
    
    # 1. Altura de Camada (Quality)
    if nozzle_size == 0.2:
        if objective_id == "visual":
            layer_height = 0.06
            initial_layer_height = 0.08
        else:
            layer_height = 0.10
            initial_layer_height = 0.10
    elif nozzle_size == 0.6:
        if objective_id == "visual":
            layer_height = 0.24
            initial_layer_height = 0.24
        elif objective_id == "fast":
            layer_height = 0.36
            initial_layer_height = 0.28
        else:
            layer_height = 0.30
            initial_layer_height = 0.24
    elif nozzle_size == 0.8:
        if objective_id == "fast":
            layer_height = 0.48
            initial_layer_height = 0.32
        else:
            layer_height = 0.40
            initial_layer_height = 0.30
    else:  # 0.4mm padrão
        if objective_id == "visual":
            layer_height = 0.08 if not is_tpu else 0.16
            initial_layer_height = 0.16
        elif objective_id == "fast":
            layer_height = 0.28
            initial_layer_height = 0.20
        elif objective_id == "strength":
            layer_height = 0.20
            initial_layer_height = 0.20
        elif objective_id == "precision":
            layer_height = 0.16
            initial_layer_height = 0.20
        else:  # balanced
            layer_height = 0.20
            initial_layer_height = 0.20

    # 2. Larguras de Linha (Line Width)
    line_width_default = round(nozzle_size * 1.05, 2)
    line_width_outer = round(nozzle_size * 1.05, 2)
    line_width_inner = round(nozzle_size * 1.12, 2)
    line_width_infill = round(nozzle_size * 1.12, 2)
    line_width_top = round(nozzle_size * 1.00, 2)

    # 3. Paredes e Cascas (Strength)
    if objective_id == "strength":
        wall_loops = 5 if nozzle_size <= 0.4 else 4
        top_shell_layers = 6
        bottom_shell_layers = 5
        infill_density = 35
        infill_pattern = "Giroide (Gyroid)"
        infill_reason = "Resistência uniforme em todos os eixos (isotrópico) sem colisão de bico."
    elif objective_id == "visual":
        wall_loops = 3
        top_shell_layers = 5
        bottom_shell_layers = 4
        infill_density = 15
        infill_pattern = "Giroide (Gyroid)"
        infill_reason = "Evita marcas de preenchimento visíveis na parede externa (ghosting de infill)."
    elif objective_id == "fast":
        wall_loops = 2
        top_shell_layers = 3
        bottom_shell_layers = 3
        infill_density = 12
        infill_pattern = "Cruzado (Cross Hatch) ou Grade"
        infill_reason = "Altíssima velocidade de deposição e sem cruzamentos no mesmo plano."
    elif objective_id == "precision":
        wall_loops = 3
        top_shell_layers = 4
        bottom_shell_layers = 4
        infill_density = 20
        infill_pattern = "Giroide (Gyroid)"
        infill_reason = "Evita tensões residuais internas que distorcem o diâmetro de furos."
    elif objective_id == "watertight":
        wall_loops = 5
        top_shell_layers = 6
        bottom_shell_layers = 5
        infill_density = 30
        infill_pattern = "Giroide (Gyroid)"
        infill_reason = "Elimina microvazios entre paredes e preenchimento."
    else:  # balanced
        wall_loops = 2 if nozzle_size >= 0.6 else 3
        top_shell_layers = 5
        bottom_shell_layers = 3
        infill_density = 15
        infill_pattern = "Giroide (Gyroid) ou Cruzado (Cross Hatch)"
        infill_reason = "Padrão oficial recomendado pela Bambu Lab para uso geral."

    # Gerador de Paredes (Wall Generator)
    wall_generator = "Arachne" if objective_id in ("visual", "precision", "balanced") else "Clássico"

    # Costura (Seam)
    if objective_id == "visual":
        seam_position = "Traseira (Back) ou Pintura de Costura Oculta"
    elif objective_id == "precision":
        seam_position = "Alinhada (Aligned)"
    else:
        seam_position = "Alinhada (Aligned) / Canto mais próximo"

    # 4. Velocidades (Speed mm/s)
    if is_tpu:
        outer_wall_speed = 35
        inner_wall_speed = 45
        sparse_infill_speed = 50
        initial_layer_speed = 25
        top_surface_speed = 30
        max_vol_speed = 3.6
    elif objective_id == "visual":
        outer_wall_speed = 80
        inner_wall_speed = 180
        sparse_infill_speed = 220
        initial_layer_speed = 40
        top_surface_speed = 100
        max_vol_speed = min(filament["max_volumetric_speed"], 16.0)
    elif objective_id == "strength":
        outer_wall_speed = 120
        inner_wall_speed = 200
        sparse_infill_speed = 220
        initial_layer_speed = 45
        top_surface_speed = 120
        max_vol_speed = filament["max_volumetric_speed"]
    elif objective_id == "fast":
        outer_wall_speed = 220
        inner_wall_speed = 320
        sparse_infill_speed = 350
        initial_layer_speed = 50
        top_surface_speed = 180
        max_vol_speed = filament["max_volumetric_speed"]
    elif objective_id == "precision":
        outer_wall_speed = 100
        inner_wall_speed = 150
        sparse_infill_speed = 200
        initial_layer_speed = 40
        top_surface_speed = 100
        max_vol_speed = min(filament["max_volumetric_speed"], 15.0)
    else:  # balanced
        outer_wall_speed = 150
        inner_wall_speed = 250
        sparse_infill_speed = 270
        initial_layer_speed = 50
        top_surface_speed = 150
        max_vol_speed = filament["max_volumetric_speed"]

    # 5. Temperaturas (°C)
    temp_nozzle_initial = filament["temp_nozzle_initial"]
    temp_nozzle_other = filament["temp_nozzle_other"]
    
    # Ajuste para fusão máxima de camadas no modo resistência
    if objective_id in ("strength", "watertight"):
        temp_nozzle_initial += 5
        temp_nozzle_other += 5

    # Temperatura da mesa com base na chapa
    recommended_bed = filament["bed_temps"].get(plate_id, 55)
    max_bed = printer.get("max_bed_temp", 120)
    bed_temp = min(recommended_bed, max_bed)

    # 6. Resfriamento (Cooling)
    cooling = dict(filament["cooling"])
    if not printer["has_aux_fan"]:
        cooling["aux_fan"] = 0
    if not printer["has_enclosure"]:
        cooling["chamber_fan"] = 0

    # 7. Regras de Gabinete / Portas
    enclosure_status = ""
    if printer["has_enclosure"]:
        if filament["enclosure_rule"] == "open":
            enclosure_status = "⚠️ DEIXE A PORTA DE VIDRO ENTREABERTA ou remova a tampa superior para evitar entupimento por calor (heat creep) no hotend durante impressões longas."
        elif filament["enclosure_rule"] == "closed":
            enclosure_status = "🔒 MANTENHA A CÂMARA 100% FECHADA. O calor interno retido é essencial para evitar empenamento (warping) e delaminação das camadas."
        else:
            enclosure_status = "Porta e tampa podem ficar fechadas ou abertas indiferente."
    else:
        if filament["enclosure_rule"] == "closed":
            enclosure_status = "❌ ATENÇÃO: Esta impressora possui estrutura aberta. Materiais técnicos como ABS, ASA e PC sofrem sério empenamento sem câmara fechada aquecida."
        else:
            enclosure_status = "Estrutura aberta compatível com este filamento."

    # 8. Suportes
    support_recommendations = {}
    if enable_support:
        if support_type == "tree":
            support_recommendations = {
                "type": "Suporte em Árvore (Tree Support)",
                "style": "Tree Slim (para miniaturas/estátuas) ou Tree Hybrid (para mecânicas)",
                "overhang_angle": 50 if objective_id == "visual" else 45,
                "top_z_distance": 0.20 if not is_tpu else 0.24,
                "top_interface_layers": 3,
                "tree_branch_angle": 45,
                "tip": "Suportes em árvore gastam menos filamento e destacam com mínima marca na peça."
            }
        else:
            support_recommendations = {
                "type": "Suporte Normal (Snug)",
                "style": "Snug (Ajustado aos contornos)",
                "overhang_angle": 45,
                "top_z_distance": 0.20,
                "top_interface_layers": 3,
                "tip": "Ideal para pontes retas, tetos e geometrias planas horizontais."
            }
    else:
        support_recommendations = {
            "type": "Desativado",
            "tip": "Bambu Lab possui excelente capacidade de pontes (bridges) e saliências até 45°-50° sem suporte."
        }

    # 9. Adesão à Mesa (Brim)
    if objective_id in ("strength", "watertight") or filament_id in ("abs", "asa", "pc"):
        brim_type = "Aba Externa (Outer Brim Only)"
        brim_width = "5 a 8 mm"
        brim_tip = "Essencial para evitar descolamento dos cantos afiados da peça."
    elif is_tpu:
        brim_type = "Sem Aba (Sem Brim)"
        brim_width = "0 mm"
        brim_tip = "TPU já adere muito fortemente. Usar cola líquida como desmoldante."
    else:
        brim_type = "Automático (Auto Brim)"
        brim_width = "5 mm (se área de contato for pequena)"
        brim_tip = "O Bambu Studio detecta automaticamente se a base da peça for instável."

    # 10. Checklist do Especialista e Alertas Críticos
    expert_alerts: List[Dict[str, str]] = []

    # Alerta de bico endurecido
    if is_composite and nozzle_material != "hardened":
        expert_alerts.append({
            "level": "danger",
            "title": "ALERTA CRÍTICO DE BICO: Fibra de Carbono Abrasiva",
            "message": "Este filamento contém fibras de carbono que desgastam e inutilizam bicos de aço inoxidável em poucas horas de impressão! Utilize OBRIGATORIAMENTE bico de Aço Endurecido (Hardened Steel) e engrenagens de extrusora endurecidas."
        })

    # Alerta de TPU no AMS
    if not filament["ams_ok"]:
        expert_alerts.append({
            "level": "danger",
            "title": "NÃO UTILIZE NO AMS / AMS LITE",
            "message": "Filamentos flexíveis como TPU enrolam nas engrenagens e canais do alimentador do AMS, provocando travamento mecânico. Alimente o TPU SEMPRE pelo suporte externo traseiro de carretel."
        })

    # Alerta de desmoldante no PEI Liso
    if plate_id == "smooth_pei" and filament_id in ("petg", "tpu-95a"):
        expert_alerts.append({
            "level": "warning",
            "title": "ALERTA DE DESMOLDANTE (PEI Liso)",
            "message": "PETG e TPU têm fusão molecular excessiva com chapas PEI lisas. Se imprimir sem cola líquida Bambu, a peça pode arrancar o filme de PEI ao ser removida!"
        })

    # Alerta de secagem
    expert_alerts.append({
        "level": "info",
        "title": "Secagem Prévia Recomendada",
        "message": f"Parâmetro oficial: {filament['drying']}."
    })

    # Dica de compensação dimensional para encaixes
    if objective_id == "precision":
        expert_alerts.append({
            "level": "success",
            "title": "Dica de Furo & Encaixe (Bambu Studio)",
            "message": "Se parafusos ou rolamentos ficarem muito justos, ative no Bambu Studio: Aba 'Quality' -> 'Precision' -> 'X-Y Hole Compensation' = +0.05mm a +0.10mm."
        })

    # Alerta de limite térmico de mesa
    if recommended_bed > max_bed:
        expert_alerts.append({
            "level": "warning",
            "title": f"Limite Térmico de Mesa ({printer['name']})",
            "message": f"O filamento sugere {recommended_bed} °C na mesa, porém a mesa da {printer['name']} opera até no máximo {max_bed} °C. O perfil foi ajustado para {bed_temp} °C."
        })

    # Alerta específico para A2L com TPU
    if printer_id == "a2l" and is_tpu:
        expert_alerts.append({
            "level": "info",
            "title": "A2L: Suporte a TPU & AMS HT",
            "message": "A Bambu Lab A2L possui compatibilidade oficial com TPU 90A / 95A através do novo módulo AMS HT com alimentação de baixa fricção ou suporte externo. Mantenha o filamento seco (< 20% umidade)."
        })

    return {
        "inputs": {
            "printer": printer,
            "nozzle_size": nozzle_size,
            "nozzle_material": nozzle_material,
            "filament": filament,
            "objective": objective,
            "plate_id": plate_id,
            "enable_support": enable_support,
            "support_type": support_type,
        },
        "quality": {
            "layer_height": layer_height,
            "initial_layer_height": initial_layer_height,
            "wall_generator": wall_generator,
            "seam_position": seam_position,
            "line_width": {
                "default": line_width_default,
                "outer_wall": line_width_outer,
                "inner_wall": line_width_inner,
                "sparse_infill": line_width_infill,
                "top_surface": line_width_top,
            }
        },
        "strength": {
            "wall_loops": wall_loops,
            "top_shell_layers": top_shell_layers,
            "bottom_shell_layers": bottom_shell_layers,
            "infill_density": infill_density,
            "infill_pattern": infill_pattern,
            "infill_reason": infill_reason,
        },
        "speed": {
            "outer_wall": outer_wall_speed,
            "inner_wall": inner_wall_speed,
            "sparse_infill": sparse_infill_speed,
            "initial_layer": initial_layer_speed,
            "top_surface": top_surface_speed,
            "max_volumetric_speed": max_vol_speed,
        },
        "temperature": {
            "nozzle_initial": temp_nozzle_initial,
            "nozzle_other": temp_nozzle_other,
            "bed": bed_temp,
        },
        "cooling": cooling,
        "enclosure_status": enclosure_status,
        "support": support_recommendations,
        "adhesion": {
            "brim_type": brim_type,
            "brim_width": brim_width,
            "brim_tip": brim_tip,
            "glue_recommendation": filament["glue"],
        },
        "alerts": expert_alerts,
    }


def generate_bambu_studio_json_config(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gera arquivo JSON no formato nativo de predefinição (preset) do Bambu Studio.
    Pode ser importado diretamente no software através de:
    Menu Arquivo > Importar > Importar Configurações...
    """
    inputs = profile.get("inputs", {})
    quality = profile.get("quality", {})
    strength = profile.get("strength", {})
    speed = profile.get("speed", {})
    temp = profile.get("temperature", {})
    cooling = profile.get("cooling", {})
    adhesion = profile.get("adhesion", {})
    support = profile.get("support", {})

    printer_name = inputs.get("printer", {}).get("name", "Bambu Lab")
    filament_name = inputs.get("filament", {}).get("name", "Filamento")
    objective_name = inputs.get("objective", {}).get("name", "Equilibrado")
    nozzle = inputs.get("nozzle_size", 0.4)

    preset_name = f"BambuWiki_{filament_name.split('/')[0].strip().replace(' ', '_')}_{objective_name.replace(' ', '_')}"

    # Mapeamento do padrão de infill para código interno do Bambu Studio
    infill_map = {
        "gyroid": "gyroid",
        "grid": "grid",
        "cross_hatch": "crosshatch",
        "rectilinear": "rectilinear",
        "honeycomb": "honeycomb",
        "adaptive_cubic": "adaptivecubic"
    }
    bambu_infill = infill_map.get(strength.get("infill_pattern", "gyroid"), "gyroid")

    # Mapeamento de suporte
    bambu_support_type = "tree_auto" if "Árvore" in str(support.get("type", "")) else "normal_auto"
    enable_support_val = "1" if inputs.get("enable_support") else "0"

    density = str(strength.get("infill_density", 15))
    if not density.endswith("%"):
        density = f"{density}%"

    return {
        "type": "process",
        "name": preset_name,
        "from": "User",
        "inherits": f"{quality.get('layer_height', 0.20):.2f}mm Standard @BBL {printer_name.split(' ')[-1]}",
        "version": "1.9.0.0",
        "instantiation": "true",
        "layer_height": str(quality.get("layer_height", 0.20)),
        "initial_layer_print_height": str(quality.get("initial_layer_height", 0.20)),
        "wall_loops": str(strength.get("wall_loops", 2)),
        "top_shell_layers": str(strength.get("top_shell_layers", 4)),
        "bottom_shell_layers": str(strength.get("bottom_shell_layers", 3)),
        "sparse_infill_density": density,
        "sparse_infill_pattern": bambu_infill,
        "outer_wall_speed": str(speed.get("outer_wall", 120)),
        "inner_wall_speed": str(speed.get("inner_wall", 200)),
        "sparse_infill_speed": str(speed.get("sparse_infill", 250)),
        "internal_solid_infill_speed": str(speed.get("sparse_infill", 200)),
        "top_surface_speed": str(speed.get("top_surface", 100)),
        "initial_layer_speed": str(speed.get("initial_layer", 50)),
        "gap_infill_speed": str(speed.get("inner_wall", 180)),
        "travel_speed": "500",
        "enable_support": enable_support_val,
        "support_type": bambu_support_type,
        "support_threshold_angle": "30",
        "brim_type": "auto_brim" if adhesion.get("brim_type") != "no_brim" else "no_brim",
        "brim_width": str(adhesion.get("brim_width", 5)),
        "seam_position": quality.get("seam_position", "aligned"),
        "wall_generator": quality.get("wall_generator", "classic"),
        "default_filament_profile": [
            f"Bambu {filament_name} @base"
        ],
        "filament_max_volumetric_speed": [
            str(speed.get("max_volumetric_speed", 20))
        ],
        "nozzle_temperature": [
            str(temp.get("nozzle_other", 220))
        ],
        "nozzle_temperature_initial_layer": [
            str(temp.get("nozzle_initial", 220))
        ],
        "hot_plate_temp": [
            str(temp.get("bed", 55))
        ],
        "hot_plate_temp_initial_layer": [
            str(temp.get("bed", 55))
        ],
        "fan_cooling_layer_time": ["60"],
        "fan_max_speed": [str(cooling.get("part_fan_max", 100))],
        "fan_min_speed": [str(cooling.get("part_fan_min", 100))]
    }
