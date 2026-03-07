import streamlit as st
import subprocess

# Tampilan Dashboard STV
st.set_page_config(page_title="STV Cloud Control", page_icon="🔴")
st.markdown("<h1 style='text-align: center; color: #e60000;'>📺 SamuderaKepri TV (STV)</h1>", unsafe_allow_html=True)

# --- KONFIGURASI DROPBOX ---
DROPBOX_URL = "https://www.dropbox.com/scl/fi/rp89eo0gl7fwv4zb2flnr/video_berita.mp4?rlkey=tspflo2za6uh0qcr94z08u8xr&st=xwuetiu3&dl=1"

# --- KONFIGURASI YOUTUBE ---
STREAM_KEY = "p8fx-xjxz-gta7-1gaq-9jct" 
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

if st.button("🚀 MULAI SIARAN LIVE (MODE STABIL 720p)", use_container_width=True):
    st.info("Mengaktifkan Mode Stabil... Mohon tunggu 30 detik.")
    
    # Optimasi FFmpeg: Menurunkan bitrate ke 1800k agar transmisi lancar tanpa buffering
    cmd = [
        'ffmpeg', '-re', '-stream_loop', '-1', 
        '-i', DROPBOX_URL,
        '-c:v', 'libx264', 
        '-preset', 'ultrafast', 
        '-tune', 'zerolatency',
        '-b:v', '1800k',        # Bitrate aman untuk koneksi cloud ke YouTube
        '-maxrate', '1800k', 
        '-bufsize', '3600k',    # Buffer diperbesar agar YouTube punya cadangan data
        '-pix_fmt', 'yuv420p', 
        '-g', '60',             # Keyframe tetap standar YouTube
        '-c:a', 'aac', 
        '-b:a', '128k', 
        '-ar', '44100', 
        '-f', 'flv', 
        RTMP_URL
    ]
    
    try:
        # Membersihkan proses FFmpeg lama jika ada
        subprocess.run(['pkill', '-f', 'ffmpeg'], check=False)
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        st.success("✅ SAMUDERAKEPRI TV MENGUDARA!")
        
        log_area = st.empty()
        for line in process.stdout:
            log_area.text(line)
                
    except Exception as e:
        st.error(f"Kesalahan: {e}")

if st.button("⏹️ HENTIKAN SIARAN"):
    subprocess.run(['pkill', '-f', 'ffmpeg'], check=False)
    st.warning("Siaran dihentikan.")
