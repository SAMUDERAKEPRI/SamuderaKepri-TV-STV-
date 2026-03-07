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

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def get_direct_link(id):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    
    return response.url

if st.button("🚀 MULAI SIARAN LIVE", use_container_width=True):
    st.info("Sedang menembus enkripsi Google Drive... Mohon tunggu.")
    
    # Mendapatkan link yang sudah melewati konfirmasi virus scan
    direct_link = get_direct_link(FILE_ID)
    
    if direct_link:
        st.success("Koneksi berhasil! Menghubungkan ke YouTube Studio...")
        
        # FFmpeg diperintahkan membaca langsung dari stream Google
        cmd = [
            'ffmpeg', '-re', '-stream_loop', '-1', 
            '-i', direct_link,
            '-c:v', 'libx264', '-preset', 'ultrafast', '-b:v', '2500k',
            '-maxrate', '2500k', '-bufsize', '5000k', '-pix_fmt', 'yuv420p',
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
            st.error(f"Gagal transmisi: {e}")
    else:
        st.error("Gagal mendapatkan akses file. Pastikan file di Google Drive sudah 'Anyone with the link'.")
