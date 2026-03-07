import streamlit as st
import subprocess
import os

# Tampilan Dashboard STV - CEO: Ronny Paslan, S.Sos
st.set_page_config(page_title="STV Playlist Control", page_icon="🔴")

st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #e60000; margin-bottom: 0;'>📺 SamuderaKepri TV (STV)</h1>
        <p style='font-size: 1.1em; color: #555;'>Mode: Playlist 4 Berita (Ultra-Stabil 480p)</p>
        <hr style='border: 1px solid #e60000;'>
    </div>
    """, unsafe_allow_html=True)

# --- KONFIGURASI VIDEO (4 LINK DROPBOX BAPAK) ---
# Link otomatis disesuaikan ke dl=1 agar server bisa membaca data video langsung
v1 = "https://www.dropbox.com/scl/fi/ps5vaxqax73rg7u9q2v51/berita1.mp4?rlkey=7149zc0uq2cbid7pj1p2kln5w&st=wfgkep5k&dl=1"
v2 = "https://www.dropbox.com/scl/fi/5wtfgxldqikf2ys9radq7/berita2.mp4?rlkey=9rf4uaubek09nv2lqtqx9ho8k&st=zxe3669i&dl=1"
v3 = "https://www.dropbox.com/scl/fi/am7hw3jalu6dd1fhmyp4j/berita3.mp4?rlkey=rar6rvus2aseni6ea48sfpv9a&st=2w166nnl&dl=1"
v4 = "https://www.dropbox.com/scl/fi/rn2wy1zv1pewt4kgjemx6/berita4.mp4?rlkey=h8ey50y6sn4xlq4u70gl8y5ek&st=w8lnyq3d&dl=1"

# --- KONFIGURASI YOUTUBE (Kunci Baru 480p Bapak) ---
STREAM_KEY = "kcbq-72xx-4e9c-kubv-efb4" 
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

# Fungsi untuk membuat file daftar putar (Playlist) untuk FFmpeg
def create_playlist():
    with open("list.txt", "w") as f:
        f.write(f"file '{v1}'\n")
        f.write(f"file '{v2}'\n")
        f.write(f"file '{v3}'\n")
        f.write(f"file '{v4}'\n")

# --- TOMBOL KONTROL ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 MULAI SIARAN PLAYLIST", use_container_width=True):
        st.info("Menyusun playlist & menyambung ke YouTube Studio...")
        create_playlist()
        
        # Perintah FFmpeg Concatenate: Memutar v1 -> v2 -> v3 -> v4 secara berurutan
        # -stream_loop -1 memastikan playlist mengulang terus menerus
        cmd = [
            'ffmpeg', '-re', '-f', 'concat', '-safe', '0', 
            '-protocol_whitelist', 'file,http,https,tcp,tls,crypto',
            '-stream_loop', '-1',             
            '-i', 'list.txt',
            '-c:v', 'libx264', 
            '-preset', 'ultrafast', 
            '-tune', 'zerolatency',
            '-b:v', '650k',                   # Bitrate rendah agar stabil
            '-maxrate', '750k', 
            '-bufsize', '1500k', 
            '-s', '854x480',                  # Resolusi 480p sesuai kunci manual Bapak
            '-pix_fmt', 'yuv420p', 
            '-g', '40',                       
            '-c:a', 'aac', 
            '-b:a', '64k',                    
            '-ar', '44100', 
            '-f', 'flv', 
            RTMP_URL
        ]
        
        try:
            # Bersihkan proses lama agar tidak bentrok
            subprocess.run(['pkill', '-f', 'ffmpeg'], check=False)
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            st.success("✅ STV MENGUDARA DENGAN 4 BERITA!")
            
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
st.sidebar.info("Tips: Setelah klik Save di GitHub, lakukan 'Reboot App' di Streamlit Cloud agar perubahan aktif.")
