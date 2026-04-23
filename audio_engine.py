import requests
import os

def gerar_narracao(texto):
    api_key = os.getenv("ELEVEN_API_KEY")
    voice_id = "Bella" # Ou o ID da voz que você escolheu
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open("audio.mp3", "wb") as f:
            f.write(response.content)
        return "audio.mp3"
    return None
