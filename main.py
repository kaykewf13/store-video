from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
import scraper
import audio_engine
import video_engine
import os

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "Kayke Store Online", "msg": "Use /gerar-video?url=LINK_DA_SHEIN"}

# Aceita tanto /gerar-video quanto /criar-video para não dar erro
@app.get("/gerar-video")
@app.get("/criar-video")
async def processar(url: str = Query(...)):
    try:
        # 1. Scraper
        dados = await scraper.get_shein_data(url)
        
        # 2. Audio
        texto = f"Olha esse achadinho na SHEIN! Esse {dados['nome']} por apenas {dados['preco']}. Qualidade nota dez! Link SR8YR na bio da @kaykestore!"
        audio_path = audio_engine.gerar_narracao(texto)
        
        # 3. Video
        link_afiliado = f"{url}&affiliate_id=SR8YR"
        qr_path = video_engine.gerar_qr(link_afiliado)
        video_path = video_engine.montar_video(dados, audio_path, qr_path)
        
        return FileResponse(video_path, media_type='video/mp4')
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})
