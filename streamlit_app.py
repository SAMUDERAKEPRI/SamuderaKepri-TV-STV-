import streamlit as st
import subprocess

# Konfigurasi Tampilan Dashboard STV
st.set_page_config(page_title="STV Cloud Control", page_icon="🔴")

st.markdown("<h1 style='text-align: center; color: #e60000;'>📺 SamuderaKepri TV (STV)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Pionir Penyiaran Berita Berbasis AI di Kepulauan Riau</p>", unsafe_allow_html=True)

# --- DATA STREAMING ---
STREAM_KEY = "p8fx-xjxz-gta7-1gaq-9jct" 
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

st.sidebar.header("Status Koneksi")
st.sidebar.success("YouTube Server: Connected")
st.sidebar.info(f"Stream Key: {STREAM_KEY[:4]}****")

st.divider()

# Tombol Kontrol Siaran
col1, col2 = st.columns(2)
with col1:
    start_btn = st.button("🚀 MULAI SIARAN LIVE", use_container_width=True)
with col2:
    stop_btn = st.button("⏹️ HENTIKAN SIARAN", use_container_width=True)

if start_btn:
    st.warning("Menghubungkan ke YouTube Studio... Mohon jangan tutup halaman ini.")
    
    # Perintah FFmpeg: Memutar file 'video_berita.mp4' secara berulang (-stream_loop -1)
    # Pastikan file video sudah di-upload ke GitHub dengan nama yang sama.
    cmd = [
        'ffmpeg', '-re', '-stream_loop', '-1', '-i', 'video_berita.mp4',
        '-c:v', 'libx264', '-preset', 'veryfast', '-b:v', '2500k',
        '-maxrate', '2500k', '-bufsize', '5000k', '-pix_fmt', 'yuv420p',
        '-g', '60', '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
        '-f', 'flv', RTMP_URL
    ]
    
    try:
        # Menjalankan proses streaming di latar belakang server
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        st.success("✅ SIARAN STV SEDANG BERJALAN LIVE!")
        
        # Menampilkan Log Aktivitas (Opsional, untuk memantau jika ada error)
        with st.expander("Lihat Log Teknis Streaming"):
            log_area = st.empty()
            for line in process.stdout:
                log_area.text(line)
                
    except Exception as e:
        st.error(f"Gagal memulai siaran: {e}")

if stop_btn:
    st.info("Untuk menghentikan siaran sepenuhnya, silakan klik 'Stop' pada dashboard Streamlit Cloud Bapak.")
