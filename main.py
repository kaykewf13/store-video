import requests
import os

def gerar_narracao_viral(texto, voice_id="EXAV8jWnz4Wbc086B86c"): # ID da Bella (exemplo)
    api_key = os.getenv("ELEVEN_API_KEY")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    data = {
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        file_path = "narração_temp.mp3"
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path
    else:
        print(f"Erro ElevenLabs: {response.text}")
        return None
