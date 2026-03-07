import streamlit as st
import subprocess
import os
import requests

st.set_page_config(page_title="STV Cloud Control", page_icon="🔴")
st.markdown("<h1 style='text-align: center; color: #e60000;'>📺 SamuderaKepri TV (STV)</h1>", unsafe_allow_html=True)

# --- KONFIGURASI ---
FILE_ID = "1tTWI43qX0C5RUvcI3Tt_QZKc5YHlww-k"
STREAM_KEY = "p8fx-xjxz-gta7-1gaq-9jct" 
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
LOCAL_FILENAME = "video_siaran.mp4"

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': id}, stream=True)
    
    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

if st.button("🚀 MULAI SIARAN LIVE", use_container_width=True):
    if not os.path.exists(LOCAL_FILENAME):
        with st.spinner("Sedang menembus proteksi Google Drive... Mohon tunggu (proses ini hanya sekali)."):
            download_file_from_google_drive(FILE_ID, LOCAL_FILENAME)
            st.success("Video berhasil disiapkan di server!")

    st.warning("Menghubungkan ke YouTube Studio...")
    
    # FFmpeg sekarang membaca file LOKAL di server, bukan link URL lagi
    cmd = [
        'ffmpeg', '-re', '-stream_loop', '-1', 
        '-i', LOCAL_FILENAME,
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
    if os.path.exists(LOCAL_FILENAME):
        os.remove(LOCAL_FILENAME)
        st.rerun()
