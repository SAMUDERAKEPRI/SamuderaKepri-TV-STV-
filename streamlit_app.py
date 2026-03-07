import streamlit as st
import subprocess
import gdown
import os

st.set_page_config(page_title="STV Cloud Control", page_icon="🔴")
st.title("📺 SamuderaKepri TV (STV)")

# --- KONFIGURASI ---
FILE_ID = "1tTWI43qX0C5RUvcI3Tt_QZKc5YHlww-k"
STREAM_KEY = "p8fx-xjxz-gta7-1gaq-9jct" 
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
OUTPUT_FILENAME = "video_siaran.mp4"

if st.button("🚀 MULAI SIARAN LIVE (STABIL MODE)"):
    # Langkah 1: Download file dari Drive ke Server Streamlit
    if not os.path.exists(OUTPUT_FILENAME):
        with st.spinner("Mengunduh video dari Cloud ke Server... (Hanya sekali)"):
            url = f'https://drive.google.com/uc?id={FILE_ID}'
            gdown.download(url, OUTPUT_FILENAME, quiet=False)
    
    st.success("Video siap! Memulai transmisi ke YouTube...")

    # Langkah 2: Jalankan FFmpeg menggunakan file lokal server
    cmd = [
        'ffmpeg', '-re', '-stream_loop', '-1', 
        '-i', OUTPUT_FILENAME,
        '-c:v', 'libx264', '-preset', 'ultrafast', '-b:v', '2500k',
        '-maxrate', '2500k', '-bufsize', '5000k', '-pix_fmt', 'yuv420p',
        '-g', '60', '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
        '-f', 'flv', RTMP_URL
    ]
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        st.success("✅ SAMUDERAKEPRI TV SEDANG LIVE!")
        
        log_area = st.empty()
        for line in process.stdout:
            log_area.text(line)
    except Exception as e:
        st.error(f"Gagal: {e}")

if st.button("🗑️ Hapus Cache Video"):
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)
        st.info("File video dihapus dari server. Klik 'Mulai' lagi untuk download ulang.")
