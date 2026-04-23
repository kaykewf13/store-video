from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
import qrcode
import requests
import os

def gerar_qr(link):
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#D4AF37", back_color="black")
    img.save("qr.png")
    return "qr.png"

def montar_video(dados, audio_path, qr_path):
    if not audio_path or not os.path.exists(audio_path):
        raise Exception("Falha no áudio: O arquivo de narração não foi gerado.")

    audio = AudioFileClip(audio_path)
    
    # Se não houver fotos, usamos uma imagem padrão para não dar erro 500
    fotos_validas = [f for f in dados.get('fotos', []) if f.startswith('http')]
    
    if not fotos_validas:
        # Imagem de segurança caso o scraper falhe nas fotos
        fotos_validas = ["https://via.placeholder.com/1080x1920.png?text=Confira+na+Kayke+Store"]

    duracao_foto = audio.duration / (len(fotos_validas) + 1)
    
    clips = []
    for i, img_url in enumerate(fotos_validas):
        temp_name = f"temp_{i}.jpg"
        try:
            img_data = requests.get(img_url, timeout=10).content
            with open(temp_name, 'wb') as f:
                f.write(img_data)
            clip = ImageClip(temp_name).set_duration(duracao_foto).resize(height=1920).set_position('center')
            clips.append(clip)
        except:
            continue
        
    qr_clip = ImageClip(qr_path).set_duration(duracao_foto).resize(width=600).set_position('center')
    clips.append(qr_clip)
    
    video = concatenate_videoclips(clips, method="compose").set_audio(audio)
    output = "video_final.mp4"
    video.write_videofile(output, fps=24, codec="libx264", audio_codec="aac")
    return output
