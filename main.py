from fastapi import FastAPI, BackgroundTasks
import scraper
import audio_engine
import video_engine
import os

app = FastAPI()

AFFILIATE_ID = "SR8YR"
BRAND = "@kaykestore"

@app.get("/")
def check():
    return {"status": f"Sistema {BRAND} Ativo"}

@app.post("/criar-video/")
async def criar_video(url_shein: str):
    # 1. Pega dados da SHEIN
    dados = scraper.get_shein_data(url_shein)
    
    # 2. Cria o roteiro e narração
    texto = f"Olha esse achadinho na SHEIN! Esse {dados['nome']} por apenas {dados['preco']}. Qualidade absurda! Link com desconto SR8YR na bio da {BRAND}!"
    audio_path = audio_engine.gerar_narracao(texto)
    
    # 3. Cria QR Code
    link_afiliado = f"{url_shein}&affiliate_id={AFFILIATE_ID}"
    qr_path = video_engine.gerar_qr(link_afiliado)
    
    # 4. Monta o vídeo
    video_path = video_engine.montar_video(dados, audio_path, qr_path)
    
    return {
        "mensagem": "Vídeo Criado com Sucesso!",
        "video": video_path,
        "detalhes": dados
    }
