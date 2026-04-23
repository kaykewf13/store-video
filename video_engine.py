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
    audio = AudioFileClip(audio_path)
    duracao_total = audio.duration
    
    # Filtra imagens válidas
    fotos_validas = [f for f in dados['fotos'] if f.startswith('http')]
    duracao_foto = duracao_total / (len(fotos_validas) + 1) # +1 para o QR code
    
    clips = []
    for i, img_url in enumerate(fotos_validas):
        # Salva imagem temporariamente
        temp_name = f"temp_{i}.jpg"
        img_data = requests.get(img_url).content
        with open(temp_name, 'wb') as f:
            f.write(img_data)
            
        clip = ImageClip(temp_name).set_duration(duracao_foto)
        clip = clip.resize(height=1920).set_position('center')
        clips.append(clip)
        
    # Adiciona o QR Code no final
    qr_clip = ImageClip(qr_path).set_duration(duracao_foto).resize(width=600).set_position('center')
    clips.append(qr_clip)
    
    video = concatenate_videoclips(clips, method="compose").set_audio(audio)
    output = "video_final.mp4"
    video.write_videofile(output, fps=24, codec="libx264", audio_codec="aac")
    
    return output
