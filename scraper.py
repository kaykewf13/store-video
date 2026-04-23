from playwright.async_api import async_playwright

async def get_shein_data(url):
    async with async_playwright() as p:
        # Lança o navegador de forma assíncrona
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            # Aumentamos o timeout para 60 segundos
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(3000) # Espera carregar as imagens
            
            titulo = await page.title()
            titulo = titulo.split('|')[0].strip()
            
            # Tenta pegar o preço com um seletor mais comum da SHEIN
            try:
                preco = await page.inner_text('.product-intro__head-price')
            except:
                preco = "Ver no App"

            # Busca as imagens
            img_elements = await page.query_selector_all('.main-image__item img')
            fotos = []
            for img in img_elements[:4]:
                src = await img.get_attribute('src')
                if src:
                    full_url = f"https:{src}" if src.startswith('//') else src
                    fotos.append(full_url)
            
            await browser.close()
            return {"nome": titulo, "preco": preco, "fotos": fotos}
        
        except Exception as e:
            await browser.close()
            print(f"Erro no Scraper: {e}")
            return {"nome": "Produto SHEIN", "preco": "Oferta", "fotos": []}
