/**
 * 3MF Inspector para Bambu Studio
 * Descompacta e inspeciona arquivos .3mf e .gcode.3mf 100% no navegador (Client-Side)
 * usando JSZip, sem enviar o arquivo para servidores externos.
 */

class Bambu3MFInspector {
    constructor() {
        this.jszipLoaded = false;
    }

    /**
     * Garante que a biblioteca JSZip esteja carregada na página.
     */
    async loadJSZip() {
        if (window.JSZip) {
            this.jszipLoaded = true;
            return window.JSZip;
        }

        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js';
            script.onload = () => {
                this.jszipLoaded = true;
                resolve(window.JSZip);
            };
            script.onerror = () => reject(new Error('Falha ao carregar a biblioteca JSZip'));
            document.head.appendChild(script);
        });
    }

    /**
     * Inspeciona um arquivo .3mf ou .gcode.3mf
     * @param {File|Blob} file 
     * @returns {Promise<Object>} Dados estruturados da mesa e filamentos
     */
    async inspect(file) {
        const JSZip = await this.loadJSZip();
        const zip = await JSZip.loadAsync(file);

        let thumbnailUrl = null;
        let printTimeSeconds = 0;
        let totalWeightGrams = 0;
        let filaments = [];

        // 1. Busca imagem renderizada da mesa (Thumbnail 3D)
        const thumbnailCandidates = [
            'Metadata/plate_1.png',
            'Metadata/plate_1_small.png',
            'Metadata/top_view.png',
            'Metadata/pick_1.png'
        ];

        for (const candidate of thumbnailCandidates) {
            const imgFile = zip.file(candidate);
            if (imgFile) {
                const base64Data = await imgFile.async('base64');
                thumbnailUrl = `data:image/png;base64,${base64Data}`;
                break;
            }
        }

        // 2. Busca e faz parse de Metadata/slice_info.xml
        const sliceInfoFile = zip.file('Metadata/slice_info.xml');
        if (sliceInfoFile) {
            const xmlText = await sliceInfoFile.async('string');
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(xmlText, 'text/xml');

            // Lê dados da primeira mesa
            const plateNode = xmlDoc.querySelector('plate');
            if (plateNode) {
                const predictionAttr = plateNode.getAttribute('prediction');
                if (predictionAttr) {
                    printTimeSeconds = parseInt(predictionAttr, 10) || 0;
                }
                const weightAttr = plateNode.getAttribute('weight');
                if (weightAttr) {
                    totalWeightGrams = parseFloat(weightAttr) || 0;
                }
            }

            // Lê cada filamento configurado
            const filamentNodes = xmlDoc.querySelectorAll('filament');
            filamentNodes.forEach((fil, index) => {
                const id = fil.getAttribute('id') || (index + 1);
                const type = fil.getAttribute('type') || 'PLA';
                const color = fil.getAttribute('color') || '#00AE42';
                const usedGrams = parseFloat(fil.getAttribute('used_g') || 0);
                const usedMeters = parseFloat(fil.getAttribute('used_m') || 0);

                filaments.push({
                    slot: index + 1,
                    id: id,
                    type: type,
                    color: color.startsWith('#') ? color : `#${color}`,
                    usedGrams: Math.round(usedGrams * 10) / 10,
                    usedMeters: Math.round(usedMeters * 10) / 10
                });
            });
        }

        // 3. Fallback: Se não encontrou slice_info.xml, busca model_settings.config
        if (filaments.length === 0) {
            const configFiles = ['Metadata/model_settings.config', 'Metadata/project_settings.config'];
            for (const cPath of configFiles) {
                const cFile = zip.file(cPath);
                if (cFile) {
                    const content = await cFile.async('string');
                    // Procura padrões de cores hexadecimais no config
                    const hexMatches = content.match(/#[0-9A-Fa-f]{6}/g);
                    if (hexMatches) {
                        const uniqueHex = [...new Set(hexMatches)];
                        uniqueHex.slice(0, 4).forEach((hex, idx) => {
                            filaments.push({
                                slot: idx + 1,
                                id: idx + 1,
                                type: 'PLA',
                                color: hex,
                                usedGrams: 0,
                                usedMeters: 0
                            });
                        });
                    }
                    break;
                }
            }
        }

        // Se totalWeightGrams for 0 mas houver filamentos individuais com peso
        if (totalWeightGrams === 0 && filaments.length > 0) {
            totalWeightGrams = filaments.reduce((acc, f) => acc + (f.usedGrams || 0), 0);
        }

        // Formata tempo de impressão em string legível
        const hours = Math.floor(printTimeSeconds / 3600);
        const minutes = Math.floor((printTimeSeconds % 3600) / 60);
        const formattedTime = hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`;

        return {
            success: true,
            fileName: file.name,
            fileSizeFormatted: (file.size / (1024 * 1024)).toFixed(2) + ' MB',
            thumbnailUrl: thumbnailUrl,
            printTimeSeconds: printTimeSeconds,
            printTimeHours: hours,
            printTimeMinutes: minutes,
            printTimeFormatted: printTimeSeconds > 0 ? formattedTime : 'Calculado no fatiador',
            totalWeightGrams: Math.round(totalWeightGrams * 10) / 10,
            filaments: filaments,
            isMultiColor: filaments.length > 1
        };
    }
}

// Instância global para uso nas páginas
window.bambu3MFInspector = new Bambu3MFInspector();
