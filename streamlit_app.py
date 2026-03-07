import streamlit as st
import subprocess

# Tampilan Dashboard STV - CEO: Ronny Paslan, S.Sos
st.set_page_config(page_title="STV Cloud Control", page_icon="🔴")
st.markdown("<h1 style='text-align: center; color: #e60000;'>📺 SamuderaKepri TV (STV)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Mode: Ultra-Stabil 480p (Manual Key)</p>", unsafe_allow_html=True)

# --- KONFIGURASI DROPBOX (File 5GB Bapak) ---
DROPBOX_URL = "https://www.dropbox.com/scl/fi/rp89eo0gl7fwv4zb2flnr/video_berita.mp4?rlkey=tspflo2za6uh0qcr94z08u8xr&st=xwuetiu3&dl=1"

# --- KONFIGURASI YOUTUBE (Kunci Baru 480p) ---
STREAM_KEY = "kcbq-72xx-4e9c-kubv-efb4" 
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

st.divider()

if st.button("🚀 MULAI SIARAN LIVE (480p RINGAN)", use_container_width=True):
    st.info("Menyinkronkan Kunci Baru ke YouTube Studio... Mohon tunggu 15-30 detik.")
    
    # FFmpeg dioptimalkan untuk Bitrate 700k agar file 5GB tidak buffering
    cmd = [
        'ffmpeg', '-re', '-stream_loop', '-1', 
        '-i', DROPBOX_URL,
        '-c:v', 'libx264', 
        '-preset', 'ultrafast', 
        '-tune', 'zerolatency',
        '-b:v', '700k',         # Menyesuaikan setelan manual 480p YouTube Bapak
        '-maxrate', '800k', 
        '-bufsize', '1600k', 
        '-s', '854x480',        # Memaksa resolusi 480p agar server sangat enteng
        '-pix_fmt', 'yuv420p', 
        '-g', '40',             # Keyframe dipercepat agar siaran segera muncul
        '-c:a', 'aac', 
        '-b:a', '64k',          # Audio hemat bandwidth
        '-ar', '44100', 
        '-f', 'flv', 
        RTMP_URL
    ]
    
    try:
        # Membersihkan proses lama agar kunci baru tidak bentrok
        subprocess.run(['pkill', '-f', 'ffmpeg'], check=False)
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        st.success("✅ STV MENGUDARA DENGAN KUNCI BARU!")
        
        # Monitor Log Aktivitas
        with st.expander("Lihat Monitor Server (frame=...)"):
            log_area = st.empty()
            for line in process.stdout:
                log_area.text(line)
                
    except Exception as e:
        st.error(f"Koneksi Gagal: {e}")

if st.button("⏹️ MATIKAN TOTAL"):
    subprocess.run(['pkill', '-f', 'ffmpeg'], check=False)
    st.warning("Siaran dihentikan.")

st.sidebar.write("---")
st.sidebar.write("CEO: Ronny Paslan, S.Sos")
st.sidebar.write("Media: SamuderaKepri.co.id")
