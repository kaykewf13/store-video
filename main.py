from fastapi import FastAPI
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

# Configurações fixas
AFFILIATE_ID = "SR8YR"
BRAND_NAME = "@kaykestore"

@app.get("/")
def home():
    return {"status": "Sistema Kayke Store Online"}

@app.post("/gerar-video/")
async def gerar_video(url_shein: str):
    # 1. Módulo de Scraping (Simulado)
    print(f"Extraindo dados de: {url_shein}")
    
    # 2. Módulo de Narração (ElevenLabs)
    # voice = generate(text="Confira esse achado...", api_key=os.getenv("ELEVEN_API"))
    
    # 3. Módulo de Edição (MoviePy)
    # Aqui entra a lógica de montagem das fotos + QR Code
    
    link_final = f"{url_shein}?affiliate_id={AFFILIATE_ID}"
    
    return {
        "mensagem": "Vídeo em processamento",
        "link_afiliado": link_final,
        "loja": BRAND_NAME
    }
