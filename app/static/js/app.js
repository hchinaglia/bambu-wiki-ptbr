/**
 * Wiki Bambu Lab PT-BR - Client Interactions
 */

document.addEventListener("DOMContentLoaded", () => {
    initTheme();
    initGlobalSearch();
    initScrollSpy();
    initCopyUrl();
    initBookmarks();
    initDrawerChat();
});

/* -------------------------------------------------------------------------- */
/* Theme Toggle (Dark / Light)                                                */
/* -------------------------------------------------------------------------- */
function initTheme() {
    const themeToggleBtn = document.getElementById("themeToggle");
    const themeIcon = document.getElementById("themeIcon");
    const htmlElement = document.documentElement;

    const savedTheme = localStorage.getItem("wiki_theme") || "light";
    setTheme(savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", () => {
            const currentTheme = htmlElement.getAttribute("data-theme");
            const newTheme = currentTheme === "dark" ? "light" : "dark";
            setTheme(newTheme);
        });
    }

    function setTheme(theme) {
        htmlElement.setAttribute("data-theme", theme);
        localStorage.setItem("wiki_theme", theme);
        if (themeIcon) {
            if (theme === "dark") {
                themeIcon.className = "bi bi-sun";
            } else {
                themeIcon.className = "bi bi-moon-stars";
            }
        }
    }
}

/* -------------------------------------------------------------------------- */
/* Live Search Autocomplete & Shortcuts                                       */
/* -------------------------------------------------------------------------- */
function initGlobalSearch() {
    const searchInput = document.getElementById("globalSearchInput");
    const searchDropdown = document.getElementById("searchDropdown");
    let debounceTimer = null;

    if (!searchInput || !searchDropdown) return;

    // Tecla de atalho (Ctrl+K ou /)
    window.addEventListener("keydown", (e) => {
        if ((e.key === "/" || ((e.ctrlKey || e.metaKey) && e.key === "k")) && document.activeElement !== searchInput) {
            e.preventDefault();
            searchInput.focus();
            searchInput.select();
        } else if (e.key === "Escape") {
            searchDropdown.classList.add("d-none");
            searchInput.blur();
        }
    });

    searchInput.addEventListener("input", (e) => {
        const query = e.target.value.trim();
        clearTimeout(debounceTimer);

        if (query.length < 2) {
            searchDropdown.classList.add("d-none");
            searchDropdown.innerHTML = "";
            return;
        }

        debounceTimer = setTimeout(async () => {
            try {
                const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                const data = await response.json();

                if (data.results && data.results.length > 0) {
                    searchDropdown.innerHTML = data.results.map(r => `
                        <a href="${r.path}" class="search-dropdown-item">
                            <div class="d-flex justify-content-between align-items-center mb-1">
                                <strong class="small text-body">${escapeHtml(r.title)}</strong>
                                <span class="badge bg-light text-muted border small" style="font-size: 0.65rem;">${escapeHtml(r.section)}</span>
                            </div>
                            <div class="text-muted small text-truncate" style="font-size: 0.8rem;">
                                ${r.snippet ? r.snippet : ''}
                            </div>
                        </a>
                    `).join("") + `
                        <div class="p-2 text-center bg-light border-top">
                            <a href="/search?q=${encodeURIComponent(query)}" class="small text-success text-decoration-none fw-semibold">
                                Ver todos os resultados para "${escapeHtml(query)}" &rarr;
                            </a>
                        </div>
                    `;
                    searchDropdown.classList.remove("d-none");
                } else {
                    searchDropdown.innerHTML = `
                        <div class="p-3 text-center text-muted small">
                            Nenhum resultado rápido para "<strong>${escapeHtml(query)}</strong>"
                        </div>
                    `;
                    searchDropdown.classList.remove("d-none");
                }
            } catch (err) {
                console.error("Erro na busca:", err);
            }
        }, 250);
    });

    // Fecha o dropdown ao clicar fora
    document.addEventListener("click", (e) => {
        if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
            searchDropdown.classList.add("d-none");
        }
    });
}

/* -------------------------------------------------------------------------- */
/* ScrollSpy para Sumário da Página (TOC)                                     */
/* -------------------------------------------------------------------------- */
function initScrollSpy() {
    const tocLinks = document.querySelectorAll(".toc-link");
    if (tocLinks.length === 0) return;

    const headingIds = Array.from(tocLinks).map(link => {
        const href = link.getAttribute("href");
        return href.startsWith("#") ? href.substring(1) : null;
    }).filter(Boolean);

    const headings = headingIds.map(id => document.getElementById(id)).filter(Boolean);
    if (headings.length === 0) return;

    function onScroll() {
        const scrollPosition = window.scrollY + 140;
        let currentActiveId = null;

        for (let i = 0; i < headings.length; i++) {
            const heading = headings[i];
            if (heading.offsetTop <= scrollPosition) {
                currentActiveId = heading.id;
            }
        }

        tocLinks.forEach(link => {
            const href = link.getAttribute("href");
            if (href === `#${currentActiveId}`) {
                link.classList.add("active");
            } else {
                link.classList.remove("active");
            }
        });
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
}

/* -------------------------------------------------------------------------- */
/* Botão Compartilhar / Copiar Link                                           */
/* -------------------------------------------------------------------------- */
function initCopyUrl() {
    const btn = document.getElementById("copyUrlBtn");
    if (!btn) return;

    btn.addEventListener("click", () => {
        navigator.clipboard.writeText(window.location.href).then(() => {
            const originalHtml = btn.innerHTML;
            btn.innerHTML = '<i class="bi bi-check2 text-success me-1"></i> Copiado!';
            setTimeout(() => {
                btn.innerHTML = originalHtml;
            }, 2000);
        });
    });
}

function escapeHtml(text) {
    if (!text) return "";
    const div = document.createElement("div");
    div.innerText = text;
    return div.innerHTML;
}

/* -------------------------------------------------------------------------- */
/* Sistema de Favoritos (Bookmarks Locais)                                    */
/* -------------------------------------------------------------------------- */
function getBookmarks() {
    try {
        return JSON.parse(localStorage.getItem("wiki_bookmarks") || "[]");
    } catch {
        return [];
    }
}

function saveBookmarks(list) {
    localStorage.setItem("wiki_bookmarks", JSON.stringify(list));
    renderBookmarks();
}

function initBookmarks() {
    renderBookmarks();
    updateCurrentArticleBookmarkButton();
}

function renderBookmarks() {
    const list = getBookmarks();
    const badge = document.getElementById("bookmarksBadge");
    const container = document.getElementById("bookmarksList");

    if (badge) badge.innerText = list.length;
    if (!container) return;

    if (list.length === 0) {
        container.innerHTML = '<div class="text-center py-3 text-muted small">Nenhum manual salvo ainda.</div>';
        return;
    }

    container.innerHTML = list.map(item => `
        <div class="d-flex align-items-center justify-content-between p-1.5 border-bottom">
            <a href="/wiki/${item.path}" class="text-decoration-none text-body small text-truncate pe-2">
                <span class="badge bg-light text-muted border text-uppercase" style="font-size: 0.65rem;">${item.section}</span>
                <span class="fw-semibold ms-1">${escapeHtml(item.title)}</span>
            </a>
            <button class="btn btn-sm btn-link text-danger p-0 ms-auto" onclick="removeBookmark('${item.path}')" title="Remover dos favoritos">
                <i class="bi bi-x"></i>
            </button>
        </div>
    `).join("");
}

function removeBookmark(path) {
    let list = getBookmarks();
    list = list.filter(i => i.path !== path);
    saveBookmarks(list);
    updateCurrentArticleBookmarkButton();
}

function toggleCurrentBookmark(path, title, section) {
    let list = getBookmarks();
    const index = list.findIndex(i => i.path === path);
    if (index >= 0) {
        list.splice(index, 1);
    } else {
        list.push({ path, title, section, added_at: new Date().toISOString() });
    }
    saveBookmarks(list);
    updateCurrentArticleBookmarkButton();
}

function updateCurrentArticleBookmarkButton() {
    const btn = document.getElementById("bookmarkBtn");
    const icon = document.getElementById("bookmarkIcon");
    const text = document.getElementById("bookmarkText");
    if (!btn || !icon || !text) return;

    if (!btn.dataset.listenerAttached) {
        btn.dataset.listenerAttached = "true";
        btn.addEventListener("click", function() {
            toggleCurrentBookmark(btn.dataset.path, btn.dataset.title, btn.dataset.section);
        });
    }

    // Detecta o path da página atual
    const currentPath = btn.dataset.path || window.location.pathname.replace(/^\/wiki\//, "").replace(/\/$/, "");
    const list = getBookmarks();
    const isBookmarked = list.some(i => i.path === currentPath);

    if (isBookmarked) {
        icon.className = "bi bi-star-fill text-warning";
        text.innerText = "Salvo";
        btn.classList.remove("btn-outline-warning");
        btn.classList.add("btn-warning", "text-dark");
    } else {
        icon.className = "bi bi-star";
        text.innerText = "Favoritar";
        btn.classList.remove("btn-warning", "text-dark");
        btn.classList.add("btn-outline-warning");
    }
}

/* -------------------------------------------------------------------------- */
/* Gaveta Lateral de Chat com Streaming e Visão Multimodal                   */
/* -------------------------------------------------------------------------- */
let drawerHistory = [];
let drawerAttachedB64 = null;
let drawerAttachedMime = null;

function initDrawerChat() {
    // Inicialização da gaveta lateral de chat
}

function handleDrawerImageUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    drawerAttachedMime = file.type;
    const reader = new FileReader();
    reader.onload = (event) => {
        const fullDataUrl = event.target.result;
        drawerAttachedB64 = fullDataUrl.split(",")[1];
        document.getElementById("drawerPreviewImg").src = fullDataUrl;
        document.getElementById("drawerImageName").innerText = file.name;
        document.getElementById("drawerImagePreview").classList.remove("d-none");
        document.getElementById("drawerImagePreview").classList.add("d-flex");
    };
    reader.readAsDataURL(file);
}

function clearDrawerImage() {
    drawerAttachedB64 = null;
    drawerAttachedMime = null;
    const input = document.getElementById("drawerImageInput");
    if (input) input.value = "";
    const preview = document.getElementById("drawerImagePreview");
    if (preview) {
        preview.classList.add("d-none");
        preview.classList.remove("d-flex");
    }
}

function sendDrawerPrompt(text) {
    const input = document.getElementById("drawerChatInput");
    const form = document.getElementById("drawerChatForm");
    if (input && form) {
        input.value = text;
        form.dispatchEvent(new Event("submit"));
    }
}

// Abre a gaveta de chat e preenche com contexto do artigo para tirar dúvida
window.askArticleDoubt = function(title, path) {
    const drawerEl = document.getElementById("aiChatDrawer");
    if (drawerEl && window.bootstrap && window.bootstrap.Offcanvas) {
        const offcanvas = bootstrap.Offcanvas.getOrCreateInstance(drawerEl);
        offcanvas.show();
    }
    const input = document.getElementById("drawerChatInput");
    if (input) {
        const prompt = `Olá! Gostaria de tirar uma dúvida sobre o procedimento "${title}": `;
        input.value = prompt;
        setTimeout(() => {
            input.focus();
            input.setSelectionRange(prompt.length, prompt.length);
        }, 350);
    }
};

async function handleDrawerChatSubmit(e) {
    e.preventDefault();
    const input = document.getElementById("drawerChatInput");
    const messages = document.getElementById("drawerMessages");
    const sendBtn = document.getElementById("drawerSendBtn");
    const modelSelect = document.getElementById("drawerModelSelect");

    const query = input.value.trim();
    if (!query && !drawerAttachedB64) return;

    const userText = query || "Analise esta imagem em busca de falhas de impressão ou erros:";
    const selectedModel = modelSelect ? modelSelect.value : "auto";
    const imgToSendB64 = drawerAttachedB64;
    const mimeToSend = drawerAttachedMime;

    // Adiciona mensagem do usuário na gaveta
    const userMsgDiv = document.createElement("div");
    userMsgDiv.className = "chat-message user-message d-flex gap-2.5 mb-3 justify-content-end";
    let imgTag = imgToSendB64 ? `<img src="data:${mimeToSend};base64,${imgToSendB64}" class="d-block mb-1.5 rounded" style="max-height: 120px; max-width: 100%;">` : "";
    userMsgDiv.innerHTML = `
        <div class="message-content bg-success text-white rounded-3 p-2.5 shadow-xs" style="max-width: 85%;">
            ${imgTag}
            <p class="mb-0">${escapeHtml(userText)}</p>
        </div>
        <div class="avatar rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center flex-shrink-0" style="width: 28px; height: 28px; font-size: 0.75rem;">
            <i class="bi bi-person"></i>
        </div>
    `;
    messages.appendChild(userMsgDiv);
    messages.scrollTop = messages.scrollHeight;

    // Limpa input e imagem
    input.value = "";
    clearDrawerImage();
    input.disabled = true;
    if (sendBtn) sendBtn.disabled = true;

    // Mensagem de streaming do bot
    const botMsgId = "drawer-msg-" + Date.now();
    const botMsgDiv = document.createElement("div");
    botMsgDiv.id = botMsgId;
    botMsgDiv.className = "chat-message bot-message d-flex gap-2.5 mb-3";
    botMsgDiv.innerHTML = `
        <div class="avatar rounded-circle bg-success text-white d-flex align-items-center justify-content-center flex-shrink-0" style="width: 28px; height: 28px; font-size: 0.75rem;">
            <i class="bi bi-robot"></i>
        </div>
        <div class="message-content bg-body border rounded-3 p-2.5 shadow-xs" style="max-width: 88%;">
            <div class="d-flex justify-content-between align-items-center mb-1.5 pb-1 border-bottom">
                <span class="fw-semibold text-success" style="font-size: 0.78rem;">Bambu Lab IA</span>
                <span class="drawer-model-badge badge bg-success-subtle text-success border border-success-subtle rounded-pill" style="font-size: 0.6rem;">
                    Pesquisando...
                </span>
            </div>
            <div class="drawer-markdown-body small text-body" style="line-height: 1.55;">
                <span class="placeholder-glow"><span class="placeholder col-6"></span></span>
            </div>
            <div class="drawer-sources-container"></div>
        </div>
    `;
    messages.appendChild(botMsgDiv);
    messages.scrollTop = messages.scrollHeight;

    let fullText = "";
    let sources = [];
    const userApiKey = localStorage.getItem("bambu_gemini_api_key") || "";

    try {
        const response = await fetch("/api/chat/stream", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "x-gemini-key": userApiKey
            },
            body: JSON.stringify({
                query: userText,
                model: selectedModel,
                history: drawerHistory,
                image_b64: imgToSendB64,
                mime_type: mimeToSend,
                current_path: window.location.pathname.replace(/^\/wiki\//, "").replace(/\/$/, ""),
                api_key: userApiKey
            })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split("\n\n");
            buffer = lines.pop();

            for (const chunk of lines) {
                if (chunk.startsWith("data: ")) {
                    try {
                        const evt = JSON.parse(chunk.substring(6));
                        if (evt.type === "init") {
                            const badge = botMsgDiv.querySelector(".drawer-model-badge");
                            if (badge) badge.innerText = evt.model;
                            sources = evt.sources || [];
                        } else if (evt.type === "token") {
                            fullText += evt.token;
                            const body = botMsgDiv.querySelector(".drawer-markdown-body");
                            if (body && window.marked) {
                                body.innerHTML = marked.parse(fullText);
                                messages.scrollTop = messages.scrollHeight;
                            }
                        } else if (evt.type === "done") {
                            const body = botMsgDiv.querySelector(".drawer-markdown-body");
                            if (body && window.marked) body.innerHTML = marked.parse(fullText);

                            if (sources && sources.length > 0) {
                                const srcEl = botMsgDiv.querySelector(".drawer-sources-container");
                                if (srcEl) {
                                    srcEl.innerHTML = `
                                        <div class="mt-2 pt-1.5 border-top">
                                             <span class="text-muted text-uppercase d-block mb-1 fw-bold" style="font-size: 0.65rem;">
                                                 <i class="bi bi-bookmarks text-success me-1"></i> Fontes na Wiki:
                                             </span>
                                             <div class="d-flex flex-wrap gap-1">
                                                 ${sources.map(s => `
                                                     <a href="${s.path}" class="badge bg-light text-dark border text-decoration-none py-1 px-1.5" style="font-size: 0.68rem;">
                                                         <i class="bi bi-file-earmark-text text-success me-0.5"></i> ${escapeHtml(s.title)}
                                                     </a>
                                                 `).join("")}
                                             </div>
                                         </div>
                                     `;
                                }
                            }
                        } else if (evt.type === "error") {
                            const badge = botMsgDiv.querySelector(".drawer-model-badge");
                            if (badge) {
                                badge.className = "drawer-model-badge badge bg-danger text-white rounded-pill";
                                badge.innerText = "Atenção";
                            }
                            const body = botMsgDiv.querySelector(".drawer-markdown-body");
                            if (body) {
                                body.innerHTML = `
                                    <div class="alert alert-warning border-warning p-2.5 rounded-3 mb-2 small">
                                        <i class="bi bi-exclamation-triangle-fill text-warning me-1"></i>
                                        <strong>${escapeHtml(evt.message || "Erro de conexão com o Gemini.")}</strong>
                                    </div>
                                    <p class="small text-muted mb-2" style="font-size: 0.75rem;">Para conversar com a IA, insira sua chave gratuita da API Gemini:</p>
                                    <button class="btn btn-sm btn-success py-1 px-2.5 rounded-pill small" onclick="const c = document.getElementById('drawerApiKeyCollapse'); if(c) { c.classList.toggle('show'); document.getElementById('drawerApiKeyInput')?.focus(); }">
                                        <i class="bi bi-key-fill me-1"></i> Configurar Chave Gemini
                                    </button>
                                `;
                            }
                            break;
                        }
                    } catch (pErr) {
                        console.error("Erro SSE:", pErr);
                    }
                }
            }
        }

        if (fullText) {
            drawerHistory.push({ role: "user", text: userText });
            drawerHistory.push({ role: "model", text: fullText });
        }

    } catch (err) {
        console.error("Erro na gaveta:", err);
        const body = botMsgDiv.querySelector(".drawer-markdown-body");
        if (body) body.innerText = "Erro ao consultar o assistente. Verifique a internet e tente novamente.";
    } finally {
        input.disabled = false;
        if (sendBtn) sendBtn.disabled = false;
        input.focus();
    }
}

// Inicialização da Gestão de Chave API Gemini no Navegador
function initApiKeyManagement() {
    const savedKey = localStorage.getItem("bambu_gemini_api_key") || "";
    
    // Atualiza campo e status da gaveta
    const drawerInput = document.getElementById("drawerApiKeyInput");
    const drawerStatus = document.getElementById("drawerApiKeyStatus");
    const drawerSaveBtn = document.getElementById("saveDrawerApiKeyBtn");
    
    if (drawerInput && savedKey) drawerInput.value = savedKey;
    if (drawerStatus) {
        if (savedKey) {
            drawerStatus.innerHTML = `<span class="text-success"><i class="bi bi-check-circle-fill me-1"></i> Chave ativa: <code>${savedKey.substring(0, 8)}...${savedKey.slice(-4)}</code></span>`;
        } else {
            drawerStatus.innerHTML = `<span class="text-muted">Nenhuma chave salva.</span>`;
        }
    }

    if (drawerSaveBtn) {
        drawerSaveBtn.addEventListener("click", function() {
            const val = (drawerInput ? drawerInput.value : "").trim();
            if (val) {
                localStorage.setItem("bambu_gemini_api_key", val);
                if (drawerStatus) drawerStatus.innerHTML = `<span class="text-success"><i class="bi bi-check-circle-fill me-1"></i> Chave salva com sucesso!</span>`;
                setTimeout(() => {
                    const c = document.getElementById("drawerApiKeyCollapse");
                    if (c) c.classList.remove("show");
                }, 1200);
            } else {
                localStorage.removeItem("bambu_gemini_api_key");
                if (drawerStatus) drawerStatus.innerHTML = `<span class="text-muted">Chave removida.</span>`;
            }
        });
    }

    // Atualiza campo e status na página /chat
    const chatInput = document.getElementById("chatApiKeyInput");
    const chatStatus = document.getElementById("chatApiKeyStatus");
    const chatSaveBtn = document.getElementById("saveChatApiKeyBtn");

    if (chatInput && savedKey) chatInput.value = savedKey;
    if (chatStatus) {
        if (savedKey) {
            chatStatus.innerHTML = `<span class="text-success"><i class="bi bi-check-circle-fill me-1"></i> Chave ativa: <code>${savedKey.substring(0, 8)}...${savedKey.slice(-4)}</code></span>`;
        } else {
            chatStatus.innerHTML = `<span class="text-muted">Nenhuma chave personalizada salva.</span>`;
        }
    }

    if (chatSaveBtn) {
        chatSaveBtn.addEventListener("click", function() {
            const val = (chatInput ? chatInput.value : "").trim();
            if (val) {
                localStorage.setItem("bambu_gemini_api_key", val);
                if (chatStatus) chatStatus.innerHTML = `<span class="text-success"><i class="bi bi-check-circle-fill me-1"></i> Chave salva com sucesso!</span>`;
                setTimeout(() => {
                    const c = document.getElementById("chatApiKeyCollapse");
                    if (c) c.classList.remove("show");
                }, 1200);
            } else {
                localStorage.removeItem("bambu_gemini_api_key");
                if (chatStatus) chatStatus.innerHTML = `<span class="text-muted">Chave removida.</span>`;
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", initApiKeyManagement);
