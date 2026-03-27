import streamlit as st
import subprocess
import os

# Konfigurasi Dashboard STV - CEO: Ronny Paslan, S.Sos
st.set_page_config(page_title="STV Live Control", page_icon="🔴")

st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #e60000; margin-bottom: 0;'>📺 SamuderaKepri TV (STV)</h1>
        <p style='font-size: 1.1em; color: #555;'>Mode: Siaran Stabil Berkelanjutan</p>
        <hr style='border: 1px solid #e60000;'>
    </div>
    """, unsafe_allow_html=True)

# --- KONFIGURASI BARU BAPAK ---
# Link Dropbox diubah ke dl=1 agar bisa dibaca FFmpeg sebagai file video mentah
VIDEO_URL = "https://www.dropbox.com/scl/fi/imzefzg2yetf2v8q56fpj/gelar-fakta-rsud-rat-ok.mp4?rlkey=9mpdeol4lntikwsjemhut9szy&st=bd08ytzc&dl=1"

# Kunci Live Baru Bapak
STREAM_KEY = "4yv5-4vrk-1j01-yfrd-ezfa"
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

# --- FUNGSI STOP ---
def matikan_siaran():
    try:
        subprocess.run(['pkill', '-f', 'ffmpeg'], check=False)
        return True
    except:
        return False

# --- TOMBOL KONTROL ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 MULAI SIARAN SEKARANG", use_container_width=True):
        st.info("Sedang menghubungkan ke YouTube Studio...")
        
        # Bersihkan proses lama agar tidak bentrok
        matikan_siaran()
        
        # Perintah FFmpeg dioptimasi (MODE COPY): 
        # Sangat ringan di server Streamlit sehingga tidak mudah di-kill (bisa tahan lama)
        cmd = [
            'ffmpeg', '-re', '-stream_loop', '-1', 
            '-i', VIDEO_URL,
            '-c:v', 'copy',            # Menggunakan video asli tanpa proses ulang (ringan CPU)
            '-c:a', 'aac',             # Encode audio agar kompatibel dengan YouTube
            '-b:a', '128k', 
            '-ar', '44100', 
            '-af', 'aresample=async=1', # Menjaga sinkronisasi audio saat loop
            '-f', 'flv', 
            RTMP_URL
        ]
        
        try:
            # Jalankan di background murni (detached) agar tidak terputus saat session timeout
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            st.success("✅ STV BERHASIL MENGUDARA!")
            st.toast("Siaran aktif di YouTube Studio Bapak.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

with col2:
    if st.button("⏹️ HENTIKAN TOTAL", use_container_width=True):
        if matikan_siaran():
            st.warning("Siaran telah dihentikan secara manual.")

# --- FOOTER ---
st.write("---")
st.caption(f"Broadcaster: SamuderaKepri.co.id | Admin: Ronny Paslan")
st.info("💡 **Pesan Penting:** Jika setelah 1 jam siaran berhenti, cukup tekan tombol Stop lalu tekan Start lagi. Mode 'Copy' ini adalah yang paling hemat tenaga bagi server.")
