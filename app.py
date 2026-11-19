import os
import shutil
import subprocess
from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Twitter (X) Data Crawler",
    page_icon="🐦",
    layout="wide"
)

@st.cache_resource(show_spinner="Menyiapkan browser Chromium untuk pertama kali...")
def ensure_playwright_chromium():
    if shutil.which("npx"):
        try:
            subprocess.run(
                ["npx", "-y", "playwright", "install", "chromium"],
                capture_output=True,
                text=True,
                shell=(os.name == "nt")
            )
        except Exception:
            pass

ensure_playwright_chromium()

st.title("🐦 Twitter (X) Data Crawler Sederhana")
st.markdown(
    "Aplikasi sederhana untuk mengambil data tweet berdasarkan **kata kunci** dan **periode waktu**, "
    "menampilkannya dalam **DataFrame**, dan mengunduhnya sebagai file **CSV**. by EKaCS"
)

# Sidebar untuk panduan singkat
with st.sidebar:
    st.header("🔑 Cara Mendapatkan Auth Token")
    st.markdown(
        """
        1. Buka [x.com](https://x.com) di browser dan login.
        2. Tekan **`F12`** (Inspect Element).
        3. Buka tab **Application** (Chrome/Edge) atau **Storage** (Firefox).
        4. Pilih **Cookies** $\\rightarrow$ `https://x.com`.
        5. Cari cookie bernama **`auth_token`**, lalu salin nilainya (*Value*).
        """
    )
    st.info("💡 Disarankan menggunakan akun kedua/dummy untuk proses crawling.")

# Form Input Parameter
with st.form("crawler_form"):
    st.subheader("⚙️ Parameter Pencarian")

    twitter_auth_token = st.text_input(
        "Twitter Auth Token (Wajib)",
        type="password",
        placeholder="Masukkan auth_token dari cookie x.com..."
    )

    kata_kunci = st.text_input(
        "Kata Kunci Pencarian",
        value="timnas indonesia",
        placeholder="Contoh: timnas indonesia"
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        tanggal_mulai = st.date_input("Tanggal Mulai", value=date(2026, 1, 1))
    with col2:
        tanggal_akhir = st.date_input("Tanggal Akhir", value=date.today())
    with col3:
        bahasa = st.selectbox(
            "Bahasa Tweet",
            options=["id", "en", "Semua Bahasa"],
            index=0
        )
    with col4:
        jumlah_tweet = st.number_input(
            "Jumlah Maksimal Tweet",
            min_value=10,
            max_value=5000,
            value=100,
            step=10
        )

    nama_file_csv = st.text_input(
        "Nama File Output CSV",
        value="hasil_crawling_twitter.csv"
    )

    submit_btn = st.form_submit_button("🚀 Mulai Crawling", use_container_width=True)

# Proses Crawling saat tombol ditekan
if submit_btn:
    if not twitter_auth_token.strip():
        st.error("❌ Mohon isi **Twitter Auth Token** terlebih dahulu!")
    elif not kata_kunci.strip():
        st.error("❌ Mohon isi **Kata Kunci Pencarian** terlebih dahulu!")
    elif tanggal_mulai > tanggal_akhir:
        st.error("❌ **Tanggal Mulai** tidak boleh lebih besar dari **Tanggal Akhir**!")
    else:
        # Pastikan nama file berakhiran .csv
        clean_filename = nama_file_csv.strip()
        if not clean_filename.endswith(".csv"):
            clean_filename += ".csv"

        # Susun query pencarian
        search_query = f"{kata_kunci.strip()} since:{tanggal_mulai} until:{tanggal_akhir}"
        if bahasa != "Semua Bahasa":
            search_query += f" lang:{bahasa}"

        st.info(f"🔍 **Query Pencarian:** `{search_query}`")

        # Hapus file lama jika ada agar tidak tercampur
        output_path = os.path.join("tweets-data", clean_filename)
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except OSError:
                pass

        cmd = [
            "npx", "-y", "tweet-harvest@2.7.1",
            "-o", clean_filename,
            "-s", search_query,
            "--tab", "LATEST",
            "-l", str(jumlah_tweet),
            "--token", twitter_auth_token.strip()
        ]

        with st.spinner(f"⏳ Sedang melakukan crawling hingga {jumlah_tweet} tweet... Mohon tunggu."):
            try:
                process = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    shell=(os.name == "nt")
                )

                with st.expander("📋 Lihat Log Proses Crawling"):
                    st.code((process.stdout or "") + "\n" + (process.stderr or ""))

                if os.path.exists(output_path):
                    df = pd.read_csv(output_path)
                    st.session_state["crawled_df"] = df
                    st.session_state["csv_filename"] = clean_filename
                    # Simpan juga di root folder aplikasi
                    df.to_csv(clean_filename, index=False, encoding="utf-8-sig")
                    st.success(f"✅ Berhasil mengambil **{len(df)}** data tweet!")
                else:
                    st.error(
                        "❌ File hasil crawling tidak ditemukan. Pastikan **Auth Token** valid, "
                        "Node.js & Playwright Chromium sudah terinstal (`npx playwright install chromium`), "
                        "dan kata kunci memiliki hasil pada periode waktu tersebut."
                    )
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat menjalankan crawler: {e}")

# Tampilkan DataFrame & Tombol Unduh CSV jika data sudah ada di session_state
if "crawled_df" in st.session_state and st.session_state["crawled_df"] is not None:
    df_result = st.session_state["crawled_df"]
    filename_result = st.session_state.get("csv_filename", "hasil_crawling_twitter.csv")

    st.divider()
    st.subheader(f"📊 Hasil DataFrame ({len(df_result)} Tweet)")
    st.dataframe(df_result, use_container_width=True)

    csv_bytes = df_result.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label=f"💾 Unduh CSV ({filename_result})",
        data=csv_bytes,
        file_name=filename_result,
        mime="text/csv",
        use_container_width=True
    )
