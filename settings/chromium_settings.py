async def chromium_custom(instance):
    """
    Iniciaiza uma instância do Chromium com contexto persistente e ambiente controlado.
    A função cria um perfil temporário no Desktop, remove qualquer execução anterior
    e inicializa o navegador Chromium com configurações voltadas para automação estável
    (remoção de popups, extensões e sinais de automação)
    
    Args:
        instance: Instância utilizada para inicializar o navegador.
        
    Returns:
        tuple:
            - browser (BrowserContext): Contexto persistente do Chromium.
            - page (Page): Primeira aba aberta no navegador.
    """

    import shutil
    from pathlib import Path

    temp_profile = Path.home() / 'Desktop' / 'playwright-profile'

    # --- Limpeza da temp_profile antes de cada run ---
    if temp_profile.exists():
        shutil.rmtree(temp_profile)
    else:
        temp_profile.mkdir(exist_ok=True, parents=True)

    # -- Configuração de Chromium
    browser = await instance.chromium.launch_persistent_context(
        user_data_dir=str(temp_profile),
        headless=False, # Extração vai ocorrer sem renderização gráfica
        args=[
            "--disable-popup-blocking",
            "--disable-notifications",
            "--disable-infobars",
            "--disable-blink-features=AutomationControlled",
            "--no-default-browser-check",
            "--no-first-run",
            "--start-maximized",
            "--disable-extensions",
            "--disable-dev-shm-usage",
            "--disable-gpu"
        ],
        chromium_sandbox=False,
    )

    page = browser.pages[0]
    return browser, page

async def start_browser():
    """
    Inicializa e configura a intância do navegador.
    A função inicia o playwright em modo sìncrono, lança uma instância
    personalizada do Chromium e retorna os objetos necessários para
    controle da automação.
    
    Lógica utilizadas:
        - Inicia o Playwright.
        - Abre o navegador Chromium via configuração customizada.
        - Retorna os objetos de controle de sessão.

    Return:
        tuple:
            (playwright, browser, page)
            Instâncias necessárias para controle de navegador.
        """
    
    from playwright.async_api import async_playwright

    playwright = await async_playwright().start()
    browser, page = await chromium_custom(playwright)
    return playwright, browser, page