from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
import qrcode
import requests
from io import BytesIO

def baixar_imagem(url):
    response = requests.get(url)
    return BytesIO(response.content)

def gerar_qr(link):
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="gold", back_color="black")
    img.save("qr.png")
    return "qr.png"

def montar_video(dados, audio_path, qr_path):
    audio = AudioFileClip(audio_path)
    duracao_foto = audio.duration / len(dados['fotos'])
    
    clips = []
    for img_url in dados['fotos']:
        # Baixa e processa cada imagem
        img_data = baixar_imagem(img_url)
        clip = ImageClip(img_url).set_duration(duracao_foto)
        clip = clip.resize(height=1920).set_position('center') # Formato Reels
        clips.append(clip)
        
    video = concatenate_videoclips(clips, method="compose").set_audio(audio)
    video.write_videofile("video_final.mp4", fps=24, codec="libx264")
    return "video_final.mp4"
