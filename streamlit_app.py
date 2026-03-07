import streamlit as st
import subprocess

# Tampilan Dashboard STV
st.set_page_config(page_title="STV Cloud Control", page_icon="🔴")
st.markdown("<h1 style='text-align: center; color: #e60000;'>📺 SamuderaKepri TV (STV)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Status: Cloud Broadcaster Ready</p>", unsafe_allow_html=True)

# --- KONFIGURASI DROPBOX (DIRECT LINK) ---
DROPBOX_URL = "https://www.dropbox.com/scl/fi/rp89eo0gl7fwv4zb2flnr/video_berita.mp4?rlkey=tspflo2za6uh0qcr94z08u8xr&st=xwuetiu3&dl=1"

# --- KONFIGURASI YOUTUBE ---
STREAM_KEY = "p8fx-xjxz-gta7-1gaq-9jct" 
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

st.divider()

if st.button("🚀 MULAI SIARAN LIVE (MODE STABIL)", use_container_width=True):
    st.info("Menghubungkan ke Dropbox & YouTube... Siaran akan segera muncul.")
    
# Perintah FFmpeg yang dioptimalkan untuk mengatasi buffering
    cmd = [
        'ffmpeg', '-re', '-stream_loop', '-1', 
        '-i', DROPBOX_URL,
        '-c:v', 'libx264', 
        '-preset', 'ultrafast', 
        '-tune', 'zerolatency',
        '-b:v', '1500k',        # Menurunkan bitrate ke 1.5Mbps agar lebih ringan
        '-maxrate', '1500k', 
        '-bufsize', '3000k',    # Ukuran buffer yang lebih seimbang
        '-pix_fmt', 'yuv420p', 
        '-g', '60',             # Keyframe tetap di 2 detik untuk standar YouTube
        '-c:a', 'aac', 
        '-b:a', '96k',          # Mengecilkan sedikit bitrate audio agar transmisi lancar
        '-ar', '44100', 
        '-f', 'flv', 
        RTMP_URL
    ]
    
    try:
        # Menjalankan proses streaming di background server
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        st.success("✅ SAMUDERAKEPRI TV SEDANG LIVE!")
        
        # Monitor Log Aktivitas
        with st.expander("Lihat Monitor Aktivitas Server"):
            log_area = st.empty()
            for line in process.stdout:
                log_area.text(line)
                
    except Exception as e:
        st.error(f"Terjadi kesalahan koneksi: {e}")

st.sidebar.markdown("---")
st.sidebar.write("CEO: Ronny Paslan, S.Sos")
st.sidebar.write("Media: SamuderaKepri.co.id")
