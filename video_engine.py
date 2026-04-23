from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip
import qrcode
from PIL import Image

def criar_video_final(imagens_paths, audio_path, qr_path, output_name="video_final.mp4"):
    # 1. Carrega o áudio para saber a duração total
    audio = AudioFileClip(audio_path)
    duracao_total = audio.duration
    
    # 2. Processa as imagens (slideshow)
    n_fotos = len(imagens_paths)
    duracao_por_foto = (duracao_total - 3) / n_fotos  # Reserva 3s para o QR Code final
    
    clips = []
    for img_path in imagens_paths:
        clip = ImageClip(img_path).set_duration(duracao_por_foto)
        # Redimensiona para o padrão Reels/TikTok (1080x1920)
        clip = clip.resize(height=1920).set_position('center')
        clips.append(clip)
    
    # 3. Adiciona o Frame Final com o QR Code
    qr_frame = ImageClip(qr_path).set_duration(3).resize(width=600).set_position('center')
    clips.append(qr_frame)
    
    # 4. Monta o vídeo
    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(audio)
    
    # 5. Exporta (Otimizado para mobile)
    video.write_videofile(output_name, fps=24, codec="libx264", audio_codec="aac")
    
    return output_name
