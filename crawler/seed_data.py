"""
Script para popular o banco de dados inicial com artigos estruturados em Português (PT-BR)
cobrindo as principais categorias da Wiki Bambu Lab:
- Série X (X1/X1-Carbon)
- Série P (P1P/P1S)
- Série A (A1/A1 Mini)
- Sistema AMS (Multi-material)
- Software (Bambu Studio / Bambu Handy)
- Manutenção Periódica
- Solução de Problemas (Troubleshooting e Códigos HMS)
"""

from crawler.build_db import init_db, save_article

SEED_ARTICLES = [
    {
        "path": "x1/manual/intro-x1",
        "slug": "intro-x1",
        "section": "x1",
        "subsection": "manual",
        "title": "Introdução ao X1 e X1-Carbon",
        "description": "Visão geral dos componentes principais da impressora Bambu Lab Série X1, especificações e arquitetura CoreXY.",
        "toc": [
            {"title": "Visão Geral do X1", "anchor": "#visao-geral", "children": []},
            {"title": "Sistema de Movimento CoreXY", "anchor": "#sistema-corexy", "children": []},
            {"title": "Câmara Fechada e Extrusora Todo-Metal", "anchor": "#camara-extrusora", "children": []},
            {"title": "Sistema Micro Lidar e Câmera com IA", "anchor": "#lidar-ia", "children": []},
            {"title": "Especificações Técnicas", "anchor": "#especificacoes", "children": []}
        ],
        "sidebar": [
            {"label": "Início", "url": "/"},
            {"label": "Série X", "url": "/wiki/x1"},
            {"label": "Série P", "url": "/wiki/p1"},
            {"label": "Série A", "url": "/wiki/a1"},
            {"label": "AMS", "url": "/wiki/ams"},
            {"label": "Software", "url": "/wiki/software"}
        ],
        "html_content": """
        <div class="wiki-content">
            <p class="lead">A <strong>Bambu Lab X1-Carbon</strong> é uma impressora 3D de alta performance projetada com foco em velocidade, precisão e compatibilidade com materiais de engenharia avançados (incluindo filamentos reforçados com fibra de carbono).</p>
            
            <h2 id="visao-geral">Visão Geral do X1</h2>
            <p>O ecossistema X1 integra sensores avançados, calibração automatizada de nivelamento de mesa e compensação ativa de vibração, permitindo alcançar velocidades de até 500 mm/s com aceleração de 20.000 mm/s².</p>
            
            <div class="alert alert-info">
                <strong>Dica:</strong> A versão X1-Carbon inclui bico de aço temperado de alta durabilidade e engrenagens de extrusão reforçadas, ideais para filamentos abrasivos como PA-CF, PETG-CF e PLA-CF.
            </div>

            <h2 id="sistema-corexy">Sistema de Movimento CoreXY</h2>
            <p>Diferente de impressoras estilo "bedslinger" (onde a mesa se move no eixo Y), a série X1 utiliza uma arquitetura CoreXY ultra-rígida com barras de fibra de carbono leves no eixo X. Isso reduz drasticamente o peso móvel da cabeça de impressão, minimizando artefatos como <em>ghosting</em> e <em>ringing</em>.</p>

            <h2 id="camara-extrusora">Câmara Fechada e Extrusora Todo-Metal</h2>
            <p>A câmara totalmente fechada permite manter temperaturas internas estáveis de até 60°C, essencial para evitar empenamento (<em>warping</em>) em materiais como ABS, ASA e Policarbonato (PC). O conjunto inclui:</p>
            <ul>
                <li>Hotend todo-metal resistente até 300°C.</li>
                <li>Ventilador auxiliar de resfriamento de peças com controle PWM.</li>
                <li>Filtro de carvão ativado para retenção de odores e compostos voláteis (VOCs).</li>
            </ul>

            <h2 id="lidar-ia">Sistema Micro Lidar e Câmera com IA</h2>
            <p>O sensor Micro Lidar mede com precisão micrométrica a calibração de fluxo de extrusão e inspeciona automaticamente a primeira camada. A câmera integrada de alta definição monitora a impressão em tempo real e identifica falhas (como acúmulo de filamento ou descolamento de peças).</p>

            <h2 id="especificacoes">Especificações Técnicas</h2>
            <table class="table table-bordered">
                <thead>
                    <tr><th>Parâmetro</th><th>Valor</th></tr>
                </thead>
                <tbody>
                    <tr><td>Volume de Impressão</td><td>256 × 256 × 256 mm³</td></tr>
                    <tr><td>Velocidade Máxima</td><td>500 mm/s</td></tr>
                    <tr><td>Aceleração Máxima</td><td>20.000 mm/s²</td></tr>
                    <tr><td>Temperatura Máxima do Bico</td><td>300 °C</td></tr>
                    <tr><td>Temperatura Máxima da Mesa</td><td>110 °C (120 °C a 220V)</td></tr>
                </tbody>
            </table>
        </div>
        """
    },
    {
        "path": "x1/maintenance/belt-tension",
        "slug": "belt-tension",
        "section": "x1",
        "subsection": "maintenance",
        "title": "Ajuste e Tensão das Correias da Série X1",
        "description": "Procedimento passo a passo para tensionar corretamente as correias XY da Bambu Lab X1 e X1-Carbon.",
        "toc": [
            {"title": "Quando realizar o tensionamento?", "anchor": "#quando-realizar", "children": []},
            {"title": "Ferramentas Necessárias", "anchor": "#ferramentas", "children": []},
            {"title": "Passo a Passo", "anchor": "#passo-a-passo", "children": []},
            {"title": "Calibração pós-ajuste", "anchor": "#pos-ajuste", "children": []}
        ],
        "html_content": """
        <div class="wiki-content">
            <p>As correias do sistema CoreXY precisam manter uma tensão equilibrada entre os lados esquerdo e direito para garantir círculos perfeitos, cantos nítidos e evitar perda de passos em altas acelerações.</p>

            <h2 id="quando-realizar">Quando realizar o tensionamento?</h2>
            <ul>
                <li>Após as primeiras 200 a 300 horas de impressão (assentamento inicial das correias).</li>
                <li>Caso o autoteste reporte ressonância fora do padrão ou código HMS de tensão de correia.</li>
                <li>A cada 3 a 6 meses como rotina de manutenção preventiva.</li>
            </ul>

            <h2 id="ferramentas">Ferramentas Necessárias</h2>
            <ul>
                <li>Chave sextavada Allen H1.5 e H2.0 (fornecidas no kit de ferramentas da impressora).</li>
            </ul>

            <h2 id="passo-a-passo">Passo a Passo</h2>
            <ol>
                <li><strong>Desligue a impressora</strong> e desconecte o cabo de energia.</li>
                <li>Na parte traseira da impressora, localize os 4 parafusos de retenção dos tensionadores de mola (dois do lado esquerdo e dois do lado direito).</li>
                <li>Solte os 4 parafusos dando apenas <strong>1 a 2 voltas completas</strong> no sentido anti-horário. <span class="text-danger">Não remova os parafusos!</span></li>
                <li>Mova a cabeça de impressão manualmente para frente e para trás, de canto a canto, cerca de 3 a 5 vezes de maneira suave. Isso permite que as molas internas equilibrem automaticamente a tensão em toda a extensão da correia.</li>
                <li>Com a cabeça de impressão posicionada no centro da câmara, aperte firmemente os 4 parafusos traseiros.</li>
            </ol>

            <h2 id="pos-ajuste">Calibração pós-ajuste</h2>
            <p>Ligue a impressora e vá no painel de controle em: <code>Configurações &rarr; Calibração &rarr; Calibração de Ressonância da Máquina</code>. Deixe o teste completar para recalibrar a compensação de vibração.</p>
        </div>
        """
    },
    {
        "path": "p1/manual/intro-p1s",
        "slug": "intro-p1s",
        "section": "p1",
        "subsection": "manual",
        "title": "Introdução à Bambu Lab P1S e P1P",
        "description": "Guia de início rápido, componentes da série P1, diferenças entre P1P e P1S e configuração inicial.",
        "toc": [
            {"title": "Diferença entre P1P e P1S", "anchor": "#diferenca-p1p-p1s", "children": []},
            {"title": "Conectividade e Controle", "anchor": "#conectividade", "children": []},
            {"title": "Primeira Impressão", "anchor": "#primeira-impressao", "children": []}
        ],
        "html_content": """
        <div class="wiki-content">
            <p class="lead">A série <strong>Bambu Lab P1</strong> herda o confiável sistema de movimento CoreXY e a alta velocidade da série X1 em um pacote focado em excelente custo-benefício.</p>

            <h2 id="diferenca-p1p-p1s">Diferença entre P1P e P1S</h2>
            <table class="table table-bordered">
                <thead><tr><th>Recurso</th><th>Bambu Lab P1P</th><th>Bambu Lab P1S</th></tr></thead>
                <tbody>
                    <tr><td>Gabinete</td><td>Aberto (personalizável com painéis)</td><td>Totalmente fechado com portas de vidro e painéis laterais</td></tr>
                    <tr><td>Ventilador Auxiliar</td><td>Opcional</td><td>Incluso de fábrica</td></tr>
                    <tr><td>Filtro de Carvão</td><td>Opcional</td><td>Incluso com duto de exaustão ativo</td></tr>
                    <tr><td>Materiais Ideais</td><td>PLA, PETG, TPU</td><td>PLA, PETG, TPU, ABS, ASA, PVA, PA</td></tr>
                </tbody>
            </table>

            <h2 id="conectividade">Conectividade e Controle</h2>
            <p>A série P1 possui conexão Wi-Fi nativa e Bluetooth para emparelhamento direto com o aplicativo <strong>Bambu Handy</strong> no smartphone ou com o fatiador <strong>Bambu Studio</strong> no computador. Também suporta modo LAN puro (sem necessidade de nuvem externa) e impressão direta por cartão MicroSD.</p>

            <h2 id="primeira-impressao">Primeira Impressão</h2>
            <p>Remova os parafusos de fixação da mesa de transporte indicados na etiqueta vermelha antes de ligar a máquina. O sistema executará automaticamente o nivelamento automático da mesa (ABL) e o teste de vibração.</p>
        </div>
        """
    },
    {
        "path": "a1/manual/intro-a1",
        "slug": "intro-a1",
        "section": "a1",
        "subsection": "manual",
        "title": "Introdução à Bambu Lab A1 e A1 Mini",
        "description": "Conheça as impressoras compactas da Série A: troca rápida de bico, cancelamento de ruído e sistema AMS Lite.",
        "toc": [
            {"title": "Recursos Inovadores da Série A", "anchor": "#recursos", "children": []},
            {"title": "Troca Rápida de Hotend sem Ferramentas", "anchor": "#troca-rapida", "children": []},
            {"title": "Cancelamento Ativo de Ruído do Motor", "anchor": "#cancelamento-ruido", "children": []},
            {"title": "Compatibilidade com AMS Lite", "anchor": "#ams-lite", "children": []}
        ],
        "html_content": """
        <div class="wiki-content">
            <p class="lead">A série A da Bambu Lab (A1 e A1 Mini) redefiniu a experiência das impressoras estilo "bedslinger", trazendo calibração de fluxo de alta frequência por sensor de corrente parasita e operação extremamente silenciosa.</p>

            <h2 id="recursos">Recursos Inovadores da Série A</h2>
            <ul>
                <li><strong>Calibração Dinâmica de Fluxo:</strong> Não há necessidade de padrões manuais de teste de calibração; um sensor mede a pressão interna do bico em tempo real.</li>
                <li><strong>Mesa PEI Texturizada Dupla-Face:</strong> Excelente adesão em alta temperatura e descolamento espontâneo após o resfriamento.</li>
                <li><strong>Tela Sensível ao Toque Colorida:</strong> Interface rápida e intuitiva com pré-visualização de modelos 3D.</li>
            </ul>

            <h2 id="troca-rapida">Troca Rápida de Hotend sem Ferramentas</h2>
            <p>A cabeça de impressão da Série A possui um mecanismo de clipe rápido: basta soltar a trava magnética e puxar o bico. Não é necessário desconectar fios nem lidar com chaves sextavadas para trocar entre bicos de 0.2 mm, 0.4 mm, 0.6 mm ou 0.8 mm.</p>

            <h2 id="cancelamento-ruido">Cancelamento Ativo de Ruído do Motor</h2>
            <p>Durante a calibração inicial, a impressora emite sinais sonoros para medir as harmônicas dos motores de passo e aplicar frequências de cancelamento ativas, resultando em níveis de ruído abaixo de 48 dB.</p>

            <h2 id="ams-lite">Compatibilidade com AMS Lite</h2>
            <p>Conecte o AMS Lite para impressão multicolorida em até 4 filamentos simultâneos, com carregamento rápido e detecção de nó ou fim de carretel.</p>
        </div>
        """
    },
    {
        "path": "ams/manual/intro-ams",
        "slug": "intro-ams",
        "section": "ams",
        "subsection": "manual",
        "title": "Sistema de Filamentos Múltiplos AMS: Como Funciona",
        "description": "Entenda o funcionamento do Automatic Material System (AMS), gestão de umidade, RFID e combinação de filamentos.",
        "toc": [
            {"title": "O que é o AMS?", "anchor": "#o-que-e-ams", "children": []},
            {"title": "Sensores RFID e Identificação Inteligente", "anchor": "#rfid", "children": []},
            {"title": "Gestão de Umidade e Dessecantes", "anchor": "#umidade", "children": []},
            {"title": "Troca de Filamento Automática (Backup)", "anchor": "#backup-filamento", "children": []}
        ],
        "html_content": """
        <div class="wiki-content">
            <p class="lead">O <strong>Bambu Lab AMS</strong> (Automatic Material System) é um módulo estanque para 4 carretéis que permite impressão multicolorida, uso de materiais solúveis de suporte e troca contínua de filamento sem intervenção manual.</p>

            <h2 id="o-que-e-ams">O que é o AMS?</h2>
            <p>O sistema é composto por 4 alimentadores independentes acionados por motores de tração, sensores de fim de curso e um seletor central (Hub do AMS). A cada troca de cor, o filamento atual é cortado na cabeça de impressão, retraído até o AMS e o próximo filamento é alimentado com precisão milimétrica.</p>

            <h2 id="rfid">Sensores RFID e Identificação Inteligente</h2>
            <p>Ao inserir um carretel oficial da Bambu Lab, leitores RFID embutidos identificam imediatamente:</p>
            <ul>
                <li>Tipo de material (PLA Basic, Matte, PETG-CF, etc.)</li>
                <li>Cor exata em código hexadecimal</li>
                <li>Temperatura recomendada do bico e da mesa</li>
            </ul>
            <p>Essas informações sincronizam instantaneamente com o Bambu Studio e Bambu Handy.</p>

            <h2 id="umidade">Gestão de Umidade e Dessecantes</h2>
            <p>O corpo do AMS possui vedação de borracha em todo o perímetro e dois compartimentos inferiores para sachês de sílica gel / dessecante. O visor e os sensores integrados indicam os níveis de umidade interna de 1 a 5.</p>

            <h2 id="backup-filamento">Troca de Filamento Automática (Backup)</h2>
            <p>Caso dois carretéis tenham o mesmo tipo e cor de filamento, o AMS alterna automaticamente para o carretel reserva assim que o primeiro acabar, garantindo que impressões longas nunca falhem por falta de material.</p>
        </div>
        """
    },
    {
        "path": "software/bambu-studio/quick-start",
        "slug": "quick-start",
        "section": "software",
        "subsection": "bambu-studio",
        "title": "Bambu Studio: Guia Rápido de Fatiamento e Configuração",
        "description": "Aprenda a fatiar seus primeiros modelos 3D, configurar suportes de árvore, pintura multicolorida e envio via nuvem ou LAN.",
        "toc": [
            {"title": "Instalação e Conexão", "anchor": "#instalacao", "children": []},
            {"title": "Pintura de Modelos Multicoloridos", "anchor": "#pintura", "children": []},
            {"title": "Suportes Tipo Árvore (Tree Supports)", "anchor": "#suportes", "children": []},
            {"title": "Envio e Monitoramento", "anchor": "#envio", "children": []}
        ],
        "html_content": """
        <div class="wiki-content">
            <p class="lead">O <strong>Bambu Studio</strong> é o fatiador oficial da Bambu Lab, baseado em código aberto com perfis pré-ajustados de fábrica para máxima qualidade e velocidade de impressão.</p>

            <h2 id="instalacao">Instalação e Conexão</h2>
            <ol>
                <li>Baixe o instalador no site oficial da Bambu Lab para Windows, macOS ou Linux.</li>
                <li>Faça login com a sua conta Bambu Lab vinculada à impressora.</li>
                <li>No menu de dispositivos, a sua impressora aparecerá automaticamente pronta para receber comandos e enviar vídeos ao vivo.</li>
            </ol>

            <h2 id="pintura">Pintura de Modelos Multicoloridos</h2>
            <p>A ferramenta de pintura de cores (ícone de balde de tinta ou tecla <code>N</code>) permite colorir qualquer modelo 3D com facilidade:</p>
            <ul>
                <li><strong>Preenchimento por Área:</strong> Detecta superfícies conectadas por ângulo para preenchimento de cor instantâneo.</li>
                <li><strong>Pincel Esférico / Círculo:</strong> Para desenhar detalhes livres e contornos.</li>
                <li><strong>Preenchimento por Camada:</strong> Altera a cor a partir de uma altura Z determinada.</li>
            </ul>

            <h2 id="suportes">Suportes Tipo Árvore (Tree Supports)</h2>
            <p>Para modelos complexos com partes suspensas (overhangs), ative os <strong>Suportes Tipo Árvore Orgânicos</strong>. Eles utilizam menos filamento, reduzem o tempo de impressão e se soltam da peça com facilidade sem deixar marcas visíveis.</p>

            <h2 id="envio">Envio e Monitoramento</h2>
            <p>Após fatiar (<code>Ctrl + R</code>), clique em <strong>Imprimir</strong> para transferir o arquivo via nuvem criptografada ou selecione <strong>Modo LAN</strong> para transferência direta na sua rede local sem internet.</p>
        </div>
        """
    },
    {
        "path": "general/troubleshooting/first-layer",
        "slug": "first-layer",
        "section": "general",
        "subsection": "troubleshooting",
        "title": "Solução de Problemas: Adesão e Qualidade da Primeira Camada",
        "description": "Como resolver descolamento de peças, empenamento (warping) e calibrar a primeira camada com precisão.",
        "toc": [
            {"title": "Causas Comuns de Descolamento", "anchor": "#causas", "children": []},
            {"title": "Limpeza Adequada da Placa de Construção", "anchor": "#limpeza", "children": []},
            {"title": "Diferenças entre Placas PEI e Cola Líquida", "anchor": "#placas", "children": []},
            {"title": "Configuração de Borda (Brim) e Temperatura", "anchor": "#configuracao", "children": []}
        ],
        "html_content": """
        <div class="wiki-content">
            <p class="lead">A primeira camada é a base de qualquer impressão 3D bem-sucedida. Falhas nesta etapa geralmente causam soltura da peça durante o processo ou desalinhamentos dimensionais.</p>

            <h2 id="causas">Causas Comuns de Descolamento</h2>
            <ul>
                <li>Gordura ou óleo natural dos dedos na superfície da placa de impressão.</li>
                <li>Seleção incorreta do tipo de placa no fatiador (ex: placa fria selecionada enquanto usa PEI texturizado).</li>
                <li>Temperatura insuficiente da mesa de impressão para o filamento utilizado.</li>
                <li>Correntes de ar frio incidindo sobre a câmara durante a impressão.</li>
            </ul>

            <h2 id="limpeza">Limpeza Adequada da Placa de Construção</h2>
            <div class="alert alert-warning">
                <strong>Importante:</strong> Evite limpar com solventes fortes ou acetona pura em placas com revestimento de PEI texturizado, pois isso danifica a película adesiva!
            </div>
            <p>O método de limpeza mais eficiente recomendado pela engenharia da Bambu Lab é:</p>
            <ol>
                <li>Lave a placa com água morna e <strong>detergente neutro de louça</strong> (sem hidratantes ou óleos adicionais).</li>
                <li>Esfregue suavemente com uma esponja macia (lado amarelo) para remover resíduos de plástico e óleos.</li>
                <li>Enxágue abundantemente e seque com toalha de papel limpa sem tocar na superfície com as mãos desprotegidas.</li>
            </ol>

            <h2 id="placas">Diferenças entre Placas PEI e Cola Líquida</h2>
            <ul>
                <li><strong>Placa PEI Texturizada:</strong> Não requer cola para PLA e PETG; excelente fixação térmica por micro-rugosidade.</li>
                <li><strong>Placa Fria / Alta Temperatura Suave:</strong> Utilize uma camada fina de cola líquida Bambu Lab ou bastão de cola para atuar tanto como adesivo quanto como camada desmoldante.</li>
            </ul>

            <h2 id="configuracao">Configuração de Borda (Brim) e Temperatura</h2>
            <p>Para peças com base pequena ou materiais propensos a contração térmica (como ABS e PC), ative a opção <strong>Brim (Borda Externa)</strong> com largura de 5 mm a 8 mm no Bambu Studio.</p>
        </div>
        """
    },
    {
        "path": "general/filament-guide/materials",
        "slug": "materials",
        "section": "general",
        "subsection": "filament-guide",
        "title": "Guia de Filamentos Bambu Lab: PLA, PETG, ABS, TPU e Fibras de Carbono",
        "description": "Tabela comparativa de filamentos, temperaturas de extrusão, compatibilidade com AMS e requisitos de secagem.",
        "toc": [
            {"title": "Tabela Comparativa de Materiais", "anchor": "#tabela-materiais", "children": []},
            {"title": "Filamentos Compatíveis com o AMS", "anchor": "#ams-compatibilidade", "children": []},
            {"title": "Importância da Secagem prévia", "anchor": "#secagem", "children": []}
        ],
        "html_content": """
        <div class="wiki-content">
            <p class="lead">Cada tipo de filamento possui características mecânicas, térmicas e de processamento específicas. Escolher o material adequado garante a resistência necessária para o projeto.</p>

            <h2 id="tabela-materiais">Tabela Comparativa de Materiais</h2>
            <table class="table table-bordered">
                <thead>
                    <tr><th>Material</th><th>Temp. Bico</th><th>Temp. Mesa</th><th>Câmara Fechada?</th><th>AMS Compatível?</th></tr>
                </thead>
                <tbody>
                    <tr><td><strong>PLA Basic / Matte</strong></td><td>210 - 230 °C</td><td>35 - 55 °C</td><td>Não recomendada (abrir porta)</td><td>Sim</td></tr>
                    <tr><td><strong>PETG Basic / HF</strong></td><td>230 - 260 °C</td><td>65 - 75 °C</td><td>Opcional</td><td>Sim</td></tr>
                    <tr><td><strong>ABS / ASA</strong></td><td>240 - 270 °C</td><td>90 - 100 °C</td><td>Obrigatória (&gt; 45 °C)</td><td>Sim</td></tr>
                    <tr><td><strong>TPU 95A</strong></td><td>220 - 240 °C</td><td>35 - 45 °C</td><td>Não</td><td><span class="text-danger">Não (alimentação externa)</span></td></tr>
                    <tr><td><strong>PA-CF / PETG-CF</strong></td><td>260 - 300 °C</td><td>80 - 100 °C</td><td>Recomendada</td><td>Sim (com roletes reforçados)</td></tr>
                </tbody>
            </table>

            <h2 id="ams-compatibilidade">Filamentos Compatíveis com o AMS</h2>
            <p>Materiais muito flexíveis (como TPU de dureza menor que 95A) ou excessivamente frágeis não devem passar pelo AMS original, pois podem dobrar no canal do alimentador ou quebrar na retração. Nesses casos, utilize o suporte traseiro de carretel único.</p>

            <h2 id="secagem">Importância da Secagem prévia</h2>
            <p>Materiais hidroscópicos como PETG, TPU e principalmente Nylon (PA) absorvem umidade do ar ambiente em poucas horas. A água acumulada ferve dentro do bico quente a 250°C, causando estalos, fios (<em>stringing</em>) e perda severa de resistência entre camadas. Seque o filamento a 65°C por 6 a 8 horas antes de imprimir.</p>
        </div>
        """
    }
]


def seed_database(db_path: str = "wiki_bambu.db"):
    init_db(db_path)
    print(f"Populando banco {db_path} com artigos fundamentais em Português...")
    for art in SEED_ARTICLES:
        save_article(art, db_path=db_path)
        print(f" ✓ [{art['section']}] {art['title']}")
    print(f"\nBanco de dados populado com sucesso! Total de {len(SEED_ARTICLES)} artigos cadastrados.")


if __name__ == "__main__":
    seed_database()
