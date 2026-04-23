from playwright.sync_api import sync_playwright

def get_shein_data(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Simula um navegador comum para evitar bloqueio
        page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
        
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(3000) # Espera renderizar imagens
            
            titulo = page.title().split('|')[0].strip()
            # Tenta encontrar o preço
            try:
                preco = page.inner_text('.product-intro__head-price')
            except:
                preco = "Oferta Especial"

            # Pega as 4 primeiras imagens grandes
            img_elements = page.query_selector_all('.main-image__item img')
            fotos = []
            for img in img_elements[:4]:
                src = img.get_attribute('src')
                if src:
                    full_url = f"https:{src}" if src.startswith('//') else src
                    fotos.append(full_url)
            
            browser.close()
            return {"nome": titulo, "preco": preco, "fotos": fotos}
        except Exception as e:
            browser.close()
            return {"nome": "Produto SHEIN", "preco": "Confira", "fotos": []}
