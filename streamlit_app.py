import streamlit as st
import subprocess
import os

st.set_page_config(page_title="STV Cloud Control", page_icon="🔴")
st.title("📺 SamuderaKepri TV (STV)")

# --- KONFIGURASI ---
DRIVE_URL = "https://drive.google.com/file/d/1tTWI43qX0C5RUvcI3Tt_QZKc5YHlww-k/view?usp=sharing"
STREAM_KEY = "p8fx-xjxz-gta7-1gaq-9jct" 
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
FILENAME = "video_siaran_stv.mp4"

# Fungsi untuk membersihkan proses FFmpeg yang nyangkut
def kill_old_processes():
    try:
        subprocess.run(['pkill', '-f', 'ffmpeg'], check=False)
    except:
        pass

if st.button("🚀 MULAI SIARAN LIVE", use_container_width=True):
    # 1. Bersihkan dulu siaran lama agar tidak bentrok
    kill_old_processes()
    
    # 2. Cek file video
    if not os.path.exists(FILENAME):
        with st.spinner("Mengunduh video..."):
            subprocess.run(['yt-dlp', '-o', FILENAME, DRIVE_URL], check=True)

    st.success("Memulai transmisi bersih ke YouTube...")

    # 3. Jalankan FFmpeg dengan parameter yang disukai YouTube
    cmd = [
        'ffmpeg', '-re', '-stream_loop', '-1', 
        '-i', FILENAME,
        '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency',
        '-b:v', '2500k', '-maxrate', '2500k', '-bufsize', '5000k', 
        '-pix_fmt', 'yuv420p', '-g', '60', 
        '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
        '-f', 'flv', RTMP_URL
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    st.info("Status: Mengudara (Pastikan tab YouTube Studio dalam kondisi Segar/Refresh)")
    
    log_area = st.empty()
    for line in process.stdout:
        log_area.text(line)

if st.button("⏹️ HENTIKAN TOTAL"):
    kill_old_processes()
    st.warning("Semua siaran dihentikan.")
