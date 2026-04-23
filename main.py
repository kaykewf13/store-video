from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import scraper
import audio_engine
import video_engine
import os

app = FastAPI()

@app.get("/gerar-video/")
async def criar_video(url: str = Query(..., alias="url")):
    # O SEGREDO ESTÁ AQUI: Adicionamos o 'await'
    dados = await scraper.get_shein_data(url)
    
    # Resto do processo segue igual
    texto = f"Confira esse achadinho na SHEIN! Esse {dados['nome']} por apenas {dados['preco']}. Link na bio da @kaykestore!"
    audio_path = audio_engine.gerar_narracao(texto)
    
    link_afiliado = f"{url}&affiliate_id=SR8YR"
    qr_path = video_engine.gerar_qr(link_afiliado)
    
    video_path = video_engine.montar_video(dados, audio_path, qr_path)
    
    return FileResponse(video_path, media_type='video/mp4', filename="video_kaykestore.mp4")
