#!/usr/bin/env bash

# Pindah ke direktori tempat script ini berada
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "==================================================="
echo "    Twitter (X) Data Crawler - macOS Edition"
echo "==================================================="
echo ""

# 1. Cek ketersediaan Node.js / npx
if ! command -v npx &> /dev/null; then
    echo "[!] Node.js / npx belum terpasang di Mac Anda."
    echo "[*] Mencoba memasang Node.js menggunakan Homebrew..."
    if command -v brew &> /dev/null; then
        brew install node
    else
        echo "[ERROR] Homebrew belum terinstal."
        echo "Silakan pasang Node.js terlebih dahulu melalui https://nodejs.org"
        exit 1
    fi
fi

# 2. Cek ketersediaan Python 3
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "[ERROR] Python 3 tidak ditemukan di Mac Anda."
    echo "Silakan pasang Python dari https://www.python.org atau jalankan: brew install python"
    exit 1
fi

# 3. Setup Virtual Environment otomatis (isolasi agar tidak mengotori sistem)
VENV_DIR="$DIR/runtime_mac"
if [ ! -d "$VENV_DIR" ]; then
    echo "[*] Menyiapkan lingkungan virtual environment untuk pertama kali..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install --upgrade pip
    echo "[*] Menginstal library (Streamlit, Pandas, Playwright)..."
    "$VENV_DIR/bin/pip" install -r requirements.txt
    echo "[*] Menginstal browser Chromium untuk Playwright..."
    npx -y playwright install chromium
fi

echo ""
echo "[*] Membuka Twitter Crawler di browser..."
echo "[*] Tekan CTRL + C di Terminal ini untuk menghentikan aplikasi."
echo ""

"$VENV_DIR/bin/streamlit" run app.py --server.port=8501
