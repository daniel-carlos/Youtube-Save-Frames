import os
import subprocess
from datetime import timedelta
import json
from yt_dlp import YoutubeDL
import cv2 as cv

video_url = "url de um vídeo do youtube"
interval = 5 # diferença de tempo (em segundos) entre as capturas
start_time = 20 # posição (em segundos) da primeira captura
end_time = 67 # limite de parada (em segundos). 0 ou valores negativos, limite passa a ser a duração do próprio vídeo

def save_image(frame, filename):
    if frame is None:
        print("Imagem inválida!")
        return False

    rate = [int(cv.IMWRITE_JPEG_QUALITY), 95]

    # Salva a imagem
    success = cv.imwrite(filename, frame, rate)

    # Show success/fake message
    if success:
        print(f"Saved: {filename}")
    else:
        print(f"Failed: {filename}")

    return success


def save_frame(cap, filename):
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return False
    save_image(frame, filename)
    return True


def skip_frame(cap):
    cap.grab()


def capture_frames(video_url, interval=5, start_time=0, end_time=-1):
    json_data = json.loads(subprocess.check_output(
        f'yt-dlp -f 22 "{video_url}" -j --skip-download ', shell=True).decode('utf-8').strip())

    stream_url = json_data['url']
    duration_s = json_data['duration']
    fps = json_data['fps']
    live_status = json_data['live_status']
    title = json_data['title']
    video_id = json_data['id']

    start_frame = int(start_time * fps)
    end_frame = int(min(end_time, duration_s) * fps) if end_time > 0 else (duration_s * fps)

    cap = cv.VideoCapture(stream_url)

    # place capture on start position
    cap.set(cv.CAP_PROP_POS_FRAMES, start_frame)

    capture_folder = f"captures/{video_id}"
    os.makedirs(capture_folder, exist_ok=True)

    frame = start_frame

    target_frame = frame + interval * fps

    while frame < end_frame:
        if (frame >= target_frame) or frame == start_frame:
            target_frame = frame + interval * fps
            capture_file = f"{video_id}__{int(frame/fps)}.jpg"
            capture_path = os.path.join(capture_folder, capture_file)
            if not save_frame(cap, capture_path):
                break
        else:
            # running cap.grab() many times is more performant then using cap.set(cv.CAP_PROP_POS_FRAMES, target_frame)
            skip_frame(cap)
        frame += 1

capture_frames(video_url, interval, start_time, end_time)
