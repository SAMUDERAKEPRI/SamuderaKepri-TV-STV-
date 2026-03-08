import streamlit as st
import subprocess
import os

# Tampilan Dashboard STV - CEO: Ronny Paslan, S.Sos
st.set_page_config(page_title="STV Playlist Control", page_icon="🔴")

st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #e60000; margin-bottom: 0;'>📺 SamuderaKepri TV (STV)</h1>
        <p style='font-size: 1.1em; color: #555;'>Mode: Siaran Berita Baru (Ultra-Stabil 480p)</p>
        <hr style='border: 1px solid #e60000;'>
    </div>
    """, unsafe_allow_html=True)

# --- KONFIGURASI VIDEO BARU BAPAK ---
# Judul: Demokrasi di Titik Nadir
VIDEO_URL = "https://www.dropbox.com/scl/fi/7le01a9c5abgx2dyzve4m/Demokrasi-di-Titik-Nadir-Antara-Makan-Gratis-Penjara-dan-Amputasi-Digital.mp4?rlkey=xa4fybiifu38zmp2zlpl48ttw&st=6tpp0a3b&dl=1"

# --- KONFIGURASI YOUTUBE BARU BAPAK ---
STREAM_KEY = "193h-u5vb-jxaq-jqz7-c65b"
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

# --- TOMBOL KONTROL ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 MULAI SIARAN LIVE", use_container_width=True):
        st.info("Menghubungkan video baru ke YouTube Studio...")
        
        # Perintah FFmpeg: Stabil, Ringan, 480p, Audio 128k
        cmd = [
            'ffmpeg', '-re', '-stream_loop', '-1', 
            '-i', VIDEO_URL,
            '-c:v', 'libx264', 
            '-preset', 'ultrafast', 
            '-tune', 'zerolatency',
            '-b:v', '650k', 
            '-maxrate', '750k', 
            '-bufsize', '1500k', 
            '-s', '854x480', 
            '-pix_fmt', 'yuv420p', 
            '-g', '40', 
            '-c:a', 'aac', 
            '-b:a', '128k', 
            '-ar', '44100', 
            '-ac', '2', 
            '-f', 'flv', 
            RTMP_URL
        ]
        
        try:
            # Bersihkan proses lama agar tidak bentrok dengan kunci baru
            subprocess.run(['pkill', '-f', 'ffmpeg'], check=False)
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            st.success("✅ STV MENGUDARA DENGAN BERITA BARU!")
            
            # Monitor Aktivitas Server
            with st.expander("Monitor Status Server (Real-time)"):
                log_area = st.empty()
                for line in process.stdout:
                    log_area.text(line)
                    
        except Exception as e:
            st.error(f"Koneksi Gagal: {e}")

with col2:
    if st.button("⏹️ MATIKAN TOTAL", use_container_width=True):
        subprocess.run(['pkill', '-f', 'ffmpeg'], check=False)
        st.warning("Siaran dihentikan.")

# --- FOOTER IDENTITAS ---
st.sidebar.write("---")
st.sidebar.write("**CEO:** Ronny Paslan, S.Sos")
st.sidebar.write("**Media:** SamuderaKepri.co.id")
st.sidebar.info("Tips: Setelah klik Save di GitHub, lakukan 'Reboot App' di Streamlit Cloud agar Kunci YouTube baru Bapak aktif.")
