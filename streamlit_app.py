import streamlit as st
import subprocess
import os

st.set_page_config(page_title="STV Cloud Control", page_icon="🔴")
st.title("📺 SamuderaKepri TV (STV)")

# --- KONFIGURASI ---
# Link Google Drive Bapak
DRIVE_URL = "https://drive.google.com/file/d/1tTWI43qX0C5RUvcI3Tt_QZKc5YHlww-k/view?usp=sharing"
STREAM_KEY = "p8fx-xjxz-gta7-1gaq-9jct" 
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

def get_direct_link(url):
    try:
        # Menggunakan yt-dlp untuk mendapatkan direct link yang valid
        result = subprocess.run(['yt-dlp', '-g', url], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        st.error(f"Gagal mengambil link: {e}")
        return None

if st.button("🚀 MULAI SIARAN LIVE"):
    st.info("Sedang memproses video besar dari Google Drive... Mohon tunggu sebentar.")
    
    direct_video_url = get_direct_link(DRIVE_URL)
    
    if direct_video_url:
        # Perintah FFmpeg dengan optimasi untuk input URL besar
        cmd = [
            'ffmpeg', '-re', '-stream_loop', '-1', 
            '-i', direct_video_url,
            '-c:v', 'libx264', '-preset', 'ultrafast', '-b:v', '2000k',
            '-maxrate', '2000k', '-bufsize', '4000k', '-pix_fmt', 'yuv420p',
            '-g', '60', '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
            '-f', 'flv', RTMP_URL
        ]
        
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            st.success("✅ STV SEDANG LIVE!")
            
            log_area = st.empty()
            for line in process.stdout:
                log_area.text(line)
        except Exception as e:
            st.error(f"Gagal menjalankan FFmpeg: {e}")
    else:
        st.error("Gagal mendapatkan link video. Pastikan file di Google Drive sudah disetel 'Public'.")
