import streamlit as st
import subprocess

# Tampilan Sederhana agar enteng di PC Bapak
st.set_page_config(page_title="STV Ultra-Light", page_icon="🔴")
st.title("📺 STV Cloud Control (Mode Hemat)")

# --- KONFIGURASI DROPBOX ---
DROPBOX_URL = "https://www.dropbox.com/scl/fi/rp89eo0gl7fwv4zb2flnr/video_berita.mp4?rlkey=tspflo2za6uh0qcr94z08u8xr&st=xwuetiu3&dl=1"

# --- KONFIGURASI YOUTUBE ---
STREAM_KEY = "p8fx-xjxz-gta7-1gaq-9jct" 
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

if st.button("🚀 MULAI LIVE (ULTRA RINGAN 600K)", use_container_width=True):
    st.info("Mengaktifkan Mode Hemat Data... Mohon tunggu.")
    
    # FFmpeg khusus untuk koneksi terbatas & spek rendah
    cmd = [
        'ffmpeg', '-re', '-stream_loop', '-1', 
        '-i', DROPBOX_URL,
        '-c:v', 'libx264', 
        '-preset', 'ultrafast', 
        '-tune', 'zerolatency',
        '-b:v', '600k',         # Bitrate di bawah 700 agar anti-buffering
        '-maxrate', '700k', 
        '-bufsize', '1400k', 
        '-s', '854x480',        # Paksa resolusi ke 480p agar enteng
        '-pix_fmt', 'yuv420p', 
        '-g', '40',             # Keyframe lebih rapat agar cepat muncul
        '-c:a', 'aac', 
        '-b:a', '64k',          # Audio hemat data
        '-ar', '44100', 
        '-f', 'flv', 
        RTMP_URL
    ]
    
    try:
        # Hapus proses lama agar tidak tabrakan
        subprocess.run(['pkill', '-f', 'ffmpeg'], check=False)
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        st.success("✅ STV MENGUDARA (MODE HEMAT)!")
        
        # Monitor Log
        log_area = st.empty()
        for line in process.stdout:
            log_area.text(line)
                
    except Exception as e:
        st.error(f"Gagal: {e}")

if st.button("⏹️ MATIKAN SIARAN"):
    subprocess.run(['pkill', '-f', 'ffmpeg'], check=False)
    st.warning("Siaran Berhenti.")
