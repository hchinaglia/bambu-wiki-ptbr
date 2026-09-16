"""
Base de dados técnica e matriz de compatibilidade de filamentos oficiais Bambu Lab.
Inclui temperaturas de bico e mesa, requisitos de câmara, placas recomendadas,
uso de adesivos/cola, secagem e compatibilidade com o sistema AMS.
"""

from typing import Any, Dict, List, Optional

FILAMENT_DATABASE: List[Dict[str, Any]] = [
    {
        "id": "pla-basic",
        "name": "Bambu PLA Basic / Matte",
        "category": "Padrão",
        "nozzle_temp": "210 - 230 °C",
        "bed_temp": "35 - 55 °C",
        "chamber_req": "Porta/tampa aberta (evitar entupimento por calor)",
        "recommended_plate": "PEI Texturizado / Placa Suave / Placa Fria",
        "glue_needed": "Não (PEI) / Opcional (Placa Fria)",
        "ams_compatible": "Sim (100% compatível)",
        "drying_recommendation": "55 °C por 8 horas (apenas se notar fios ou estalos)",
        "description": "Filamento mais popular, fácil de imprimir, acabamento impecável e alta precisão dimensional.",
        "compatible_printers": ["X1", "X1-Carbon", "P1P", "P1S", "A1", "A1 Mini", "H2"]
    },
    {
        "id": "petg-hf",
        "name": "Bambu PETG Basic / HF (High Flow)",
        "category": "Técnico / Resistente",
        "nozzle_temp": "230 - 260 °C",
        "bed_temp": "65 - 75 °C",
        "chamber_req": "Fechada ou aberta indiferente",
        "recommended_plate": "PEI Texturizado / Alta Temperatura",
        "glue_needed": "Não no PEI / Recomendado como desmoldante em placa lisa",
        "ams_compatible": "Sim (100% compatível)",
        "drying_recommendation": "65 °C por 8 horas (altamente recomendado antes de imprimir)",
        "description": "Excelente resistência mecânica, térmica e química. Ideal para suportes, peças externas e utilitários duráveis.",
        "compatible_printers": ["X1", "X1-Carbon", "P1P", "P1S", "A1", "A1 Mini", "H2"]
    },
    {
        "id": "abs",
        "name": "Bambu ABS",
        "category": "Engenharia",
        "nozzle_temp": "240 - 270 °C",
        "bed_temp": "90 - 100 °C",
        "chamber_req": "Câmara totalmente fechada (> 45 °C)",
        "recommended_plate": "PEI Texturizado / Placa de Engenharia",
        "glue_needed": "Recomendado (cola líquida Bambu)",
        "ams_compatible": "Sim (compatível)",
        "drying_recommendation": "80 °C por 8 horas",
        "description": "Alta resistência a impacto e temperatura (até 85°C), fácil pós-processamento com lixa ou vapor de acetona.",
        "compatible_printers": ["X1", "X1-Carbon", "P1S", "X1E"]
    },
    {
        "id": "asa",
        "name": "Bambu ASA",
        "category": "Engenharia / Automotivo",
        "nozzle_temp": "240 - 270 °C",
        "bed_temp": "90 - 100 °C",
        "chamber_req": "Câmara totalmente fechada (> 45 °C)",
        "recommended_plate": "PEI Texturizado / Placa de Engenharia",
        "glue_needed": "Recomendado (cola líquida)",
        "ams_compatible": "Sim (compatível)",
        "drying_recommendation": "80 °C por 8 horas",
        "description": "Resistente a raios ultravioleta (UV) e intempéries. Não amarela e não degrada sob sol direto. Ideal para uso automotivo e externo.",
        "compatible_printers": ["X1", "X1-Carbon", "P1S", "X1E"]
    },
    {
        "id": "tpu-95a",
        "name": "Bambu TPU 95A / HF",
        "category": "Flexível",
        "nozzle_temp": "220 - 240 °C",
        "bed_temp": "35 - 45 °C",
        "chamber_req": "Aberta",
        "recommended_plate": "PEI Texturizado",
        "glue_needed": "Recomendado como desmoldante (cola líquida)",
        "ams_compatible": "NÃO (Usar suporte traseiro de carretel)",
        "drying_recommendation": "70 °C por 8 horas (obrigatório para evitar bolhas e stringing)",
        "description": "Material elastomérico flexível com memória de forma e excelente resistência à abrasão. Não deve passar pelo alimentador do AMS.",
        "compatible_printers": ["X1", "X1-Carbon", "P1P", "P1S", "A1", "A1 Mini", "H2"]
    },
    {
        "id": "pc",
        "name": "Bambu PC (Policarbonato)",
        "category": "Engenharia Avançada",
        "nozzle_temp": "260 - 280 °C",
        "bed_temp": "100 - 110 °C",
        "chamber_req": "Câmara fechada e pré-aquecida (> 55 °C)",
        "recommended_plate": "Placa de Engenharia / PEI Texturizado",
        "glue_needed": "Obrigatório (cola líquida)",
        "ams_compatible": "Sim",
        "drying_recommendation": "80 °C por 8 a 12 horas",
        "description": "Altíssima resistência mecânica, rigidez e temperatura de deflexão térmica acima de 110°C.",
        "compatible_printers": ["X1-Carbon", "X1E", "P1S"]
    },
    {
        "id": "pa-cf",
        "name": "Bambu PA-CF (Nylon Fibra de Carbono)",
        "category": "Compósitos Reforçados",
        "nozzle_temp": "280 - 300 °C",
        "bed_temp": "80 - 100 °C",
        "chamber_req": "Câmara fechada",
        "recommended_plate": "Placa de Engenharia / PEI Texturizado",
        "glue_needed": "Recomendado (cola líquida)",
        "ams_compatible": "Sim (requer bico e engrenagens de aço temperado)",
        "drying_recommendation": "80 °C por 8 a 12 horas (Nylon é extremamente hidroscópico)",
        "description": "Excelente resistência química, térmica e rigidez estrutural para peças funcionais, engrenagens e gabaritos industriais.",
        "compatible_printers": ["X1-Carbon", "X1E", "P1S (com bico temperado)"]
    },
    {
        "id": "petg-cf",
        "name": "Bambu PETG-CF",
        "category": "Compósitos Reforçados",
        "nozzle_temp": "240 - 270 °C",
        "bed_temp": "70 - 80 °C",
        "chamber_req": "Fechada ou aberta",
        "recommended_plate": "PEI Texturizado",
        "glue_needed": "Opcional",
        "ams_compatible": "Sim (com bico de aço temperado)",
        "drying_recommendation": "65 °C por 8 horas",
        "description": "Acabamento fosco texturizado que esconde quase totalmente as linhas de camada. Fácil de imprimir com alta rigidez.",
        "compatible_printers": ["X1", "X1-Carbon", "P1P", "P1S", "A1", "A1 Mini"]
    },
    {
        "id": "pla-cf",
        "name": "Bambu PLA-CF",
        "category": "Compósitos Reforçados",
        "nozzle_temp": "210 - 240 °C",
        "bed_temp": "45 - 55 °C",
        "chamber_req": "Aberta",
        "recommended_plate": "PEI Texturizado",
        "glue_needed": "Não",
        "ams_compatible": "Sim (com bico de aço temperado)",
        "drying_recommendation": "55 °C por 8 horas",
        "description": "Fácil de imprimir como PLA tradicional, com acabamento fosco de alta rigidez e aspecto de fibra de carbono.",
        "compatible_printers": ["X1", "X1-Carbon", "P1P", "P1S", "A1", "A1 Mini"]
    },
    {
        "id": "support-pla",
        "name": "Bambu Support for PLA / PETG",
        "category": "Suporte Destacável",
        "nozzle_temp": "215 - 235 °C",
        "bed_temp": "45 - 55 °C",
        "chamber_req": "Aberta",
        "recommended_plate": "Conforme material principal",
        "glue_needed": "Conforme material principal",
        "ams_compatible": "Sim (ideal para usar apenas na camada de interface)",
        "drying_recommendation": "55 °C por 8 horas",
        "description": "Material de interface de suporte que não se funde quimicamente com o PLA, permitindo destacar suportes sem deixar marcas.",
        "compatible_printers": ["X1", "X1-Carbon", "P1P", "P1S", "A1", "A1 Mini"]
    }
]


def get_filaments(printer: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Filtra filamentos por impressora e/ou categoria."""
    results = FILAMENT_DATABASE
    if printer:
        p_clean = printer.strip().lower()
        results = [
            f for f in results
            if any(p_clean in cp.lower() for cp in f["compatible_printers"])
        ]
    if category and category != "Todos":
        c_clean = category.strip().lower()
        results = [f for f in results if c_clean == f["category"].lower()]
    return results
