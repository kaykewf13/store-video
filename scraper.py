from playwright.sync_api import sync_playwright

def get_shein_data(url):
    with sync_playwright() as p:
        # Abre um navegador "escondido"
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Simula um usuário real para evitar bloqueios
        page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        
        page.goto(url)
        page.wait_for_timeout(2000) # Espera carregar

        # Extrai o título e o preço
        try:
            titulo = page.title()
            # Tenta pegar o preço (seletor genérico da SHEIN)
            preco = page.inner_text('.product-intro__head-price') or "Preço na Loja"
        except:
            titulo = "Look Incrível SHEIN"
            preco = "Confira o link"

        # Pega as primeiras 3 imagens grandes do produto
        images = page.query_selector_all('.main-image__item img')
        fotos = [img.get_attribute('src') for img in images[:3]]
        
        # Se as fotos vierem sem o "https:", a gente conserta
        fotos = [f if f.startswith('http') else f"https:{f}" for f in fotos]

        browser.close()
        return {
            "nome": titulo,
            "preco": preco,
            "fotos": fotos
        }
