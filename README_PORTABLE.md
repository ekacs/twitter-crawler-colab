# 🐦 Twitter (X) Data Crawler - Versi Portable (Windows)

Aplikasi Twitter Crawler siap pakai tanpa memerlukan instalasi Python, Node.js, atau pengaturan sistem apa pun di komputer pengguna.

*Reach me* 😉ekacs (github.com/ekacs | ekacsisfreeman@gmail.com ) 

---

## 🚀 Cara Menjalankan untuk Pengguna Akhir (User)

1. Pastikan folder aplikasi ini sudah memiliki folder `runtime`.
2. Klik ganda (**double click**) file:

   ```text
   JALANKAN_APLIKASI.bat
   ```
3. Aplikasi akan langsung membuka browser secara otomatis di alamat:

   ```text
   http://localhost:8501
   ```
4. Masukkan **Twitter Auth Token** akun Anda, tentukan kata kunci pencarian, dan klik **Mulai Crawling**.
5. File hasil unduhan akan tersimpan di dalam folder `tweets-data/` dan dapat langsung diunduh melalui tombol di browser.

---

## 🍏 Cara Menjalankan di Mac (macOS)

Di Mac, sistem keamanan macOS (Gatekeeper dan arsitektur CPU Intel vs Apple Silicon M1/M2/M3/M4) tidak mengizinkan binary Windows (`.exe`/`.bat`). 

Namun, pengguna Mac bisa menjalankan aplikasi ini dengan **1 langkah mudah**:

1. Pastikan Mac sudah terpasang **Python** dan **Node.js** (atau bisa dipasang otomatis jika ada Homebrew).
2. Klik ganda (**double click**) file:

   ```text
   JALANKAN_APLIKASI_MAC.command
   ```

   *(Jika macOS memunculkan izin terminal pada saat pertama kali, cukup berikan izin eksekusi sekali lewat Terminal: `chmod +x JALANKAN_APLIKASI_MAC.command`).*
3. Script otomatis membuat environment terisolasi (`runtime_mac/`), memasang semua library, dan membuka browser di `http://localhost:8501`.

Jika Anda baru mendownload repository ini dan ingin merakit folder `runtime` portabel:

1. Pastikan komputer pembuat memiliki koneksi internet.
2. Klik ganda file:

   ```text
   build_portable.bat
   ```

   *(atau jalankan `python build_portable.py` di terminal).*
3. Script otomatis akan mengunduh:
   - Python Embeddable
   - Pip dan semua library (`streamlit`, `pandas`, `playwright`)
   - Node.js Portable (`node.exe` & `npx.cmd`)
   - Browser Chromium headless
4. Setelah selesai, folder proyek ini siap di-ZIP dan dibagikan ke pengguna lain!
