from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
import scraper, audio_engine, video_engine
import os

app = FastAPI()

@app.get("/gerar-video")
async def criar_video(url: str = Query(...)):
    # PASSO 1: SCRAPER
    try:
        dados = await scraper.get_shein_data(url)
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": "Falha no Scraper", "detalhes": str(e)})

    # PASSO 2: ÁUDIO
    try:
        texto = f"Olha esse achadinho na SHEIN! Esse {dados['nome']} por apenas {dados['preco']}. Link SR8YR na bio da @kaykestore!"
        audio_path = audio_engine.gerar_narracao(texto)
        if not audio_path:
            return JSONResponse(status_code=500, content={"erro": "ElevenLabs negou o acesso. Verifique sua API KEY."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": "Falha no Motor de Voz", "detalhes": str(e)})

    # PASSO 3: VÍDEO
    try:
        qr_path = video_engine.gerar_qr(f"{url}&affiliate_id=SR8YR")
        video_path = video_engine.montar_video(dados, audio_path, qr_path)
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": "Falha na Montagem do Vídeo", "detalhes": str(e)})

    return FileResponse(video_path, media_type='video/mp4', filename="video_kaykestore.mp4")
