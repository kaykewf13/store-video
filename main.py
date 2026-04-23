from fastapi import FastAPI, BackgroundTasks, Query
from fastapi.responses import FileResponse
import scraper
import audio_engine
import video_engine
import os

app = FastAPI()

AFFILIATE_ID = "SR8YR"
BRAND = "@kaykestore"

@app.get("/")
def check():
    return {"status": "Motor Kayke Store Online", "loja": BRAND}

@app.get("/gerar-video/") # Mudamos para GET para facilitar o teste no navegador
async def criar_video(url: str = Query(..., alias="url")):
    # 1. Pega dados da SHEIN
    dados = scraper.get_shein_data(url)
    
    # 2. Cria o roteiro e narração
    texto = f"Olha esse achadinho na SHEIN! Esse {dados['nome']} por apenas {dados['preco']}. Qualidade absurda! Link com desconto SR8YR na bio da {BRAND}!"
    audio_path = audio_engine.gerar_narracao(texto)
    
    # 3. Cria QR Code
    link_afiliado = f"{url}&affiliate_id={AFFILIATE_ID}"
    qr_path = video_engine.gerar_qr(link_afiliado)
    
    # 4. Monta o vídeo
    video_path = video_engine.montar_video(dados, audio_path, qr_path)
    
    # 5. Entrega o arquivo pronto para download
    return FileResponse(
        video_path, 
        media_type='video/mp4', 
        filename=f"video_shein_{AFFILIATE_ID}.mp4"
    )
