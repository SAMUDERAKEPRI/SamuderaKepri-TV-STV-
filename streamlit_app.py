import streamlit as st
import subprocess
import os

st.set_page_config(page_title="STV Cloud Control", page_icon="🔴")
st.markdown("<h1 style='text-align: center; color: #e60000;'>📺 SamuderaKepri TV (STV)</h1>", unsafe_allow_html=True)

# --- KONFIGURASI ---
# Link preview yang Bapak berikan
DRIVE_URL = "https://drive.google.com/file/d/1tTWI43qX0C5RUvcI3Tt_QZKc5YHlww-k/view?usp=sharing"
STREAM_KEY = "p8fx-xjxz-gta7-1gaq-9jct" 
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
FILENAME = "video_siaran_stv.mp4"

if st.button("🚀 MULAI SIARAN LIVE", use_container_width=True):
    # Proses Download jika file belum ada di server
    if not os.path.exists(FILENAME):
        with st.spinner("Sedang menembus proteksi Google Drive... Proses ini memakan waktu beberapa menit."):
            try:
                # yt-dlp adalah tool paling ampuh untuk menembus proteksi Google
                subprocess.run(['yt-dlp', '-o', FILENAME, DRIVE_URL], check=True)
                st.success("Video berhasil diunduh ke server!")
            except Exception as e:
                st.error(f"Gagal menembus proteksi Google: {e}")
                st.stop()

    st.warning("Menghubungkan ke YouTube Studio... Siaran segera muncul.")

# Perintah FFmpeg yang disempurnakan untuk stabilitas YouTube
    cmd = [
        'ffmpeg', '-re', '-stream_loop', '-1', 
        '-i', FILENAME,
        '-c:v', 'libx264', 
        '-preset', 'ultrafast', 
        '-tune', 'zerolatency', # Mengurangi jeda agar cepat muncul
        '-b:v', '2500k', 
        '-maxrate', '2500k', 
        '-bufsize', '5000k', 
        '-pix_fmt', 'yuv420p', # Format warna standar YouTube
        '-g', '60', # Keyframe interval (sangat penting untuk YouTube)
        '-c:a', 'aac', 
        '-b:a', '128k', 
        '-ar', '44100', 
        '-f', 'flv', 
        RTMP_URL
    ]
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        st.success("✅ SAMUDERAKEPRI TV SEDANG LIVE!")
        
        log_area = st.empty()
        for line in process.stdout:
            log_area.text(line)
    except Exception as e:
        st.error(f"Gagal transmisi: {e}")

if st.button("🗑️ Reset Sistem (Hapus Cache)"):
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
        st.rerun()
