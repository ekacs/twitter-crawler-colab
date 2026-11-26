import os
import sys
import shutil
import urllib.request
import zipfile
import subprocess

PYTHON_VER = "3.11.9"
PYTHON_ZIP_URL = f"https://www.python.org/ftp/python/{PYTHON_VER}/python-{PYTHON_VER}-embed-amd64.zip"
GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"
NODE_VER = "v20.18.1"
NODE_ZIP_URL = f"https://nodejs.org/dist/{NODE_VER}/node-{NODE_VER}-win-x64.zip"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RUNTIME_DIR = os.path.join(ROOT_DIR, "runtime")
PYTHON_DIR = os.path.join(RUNTIME_DIR, "python")
NODE_DIR = os.path.join(RUNTIME_DIR, "node")
BROWSERS_DIR = os.path.join(RUNTIME_DIR, "playwright-browsers")
TEMP_DIR = os.path.join(ROOT_DIR, "temp_downloads")


def download_file(url, target_path):
    print(f"--> Mengunduh: {url}")
    urllib.request.urlretrieve(url, target_path)


def setup_portable():
    print("=" * 60)
    print("   MEMULAI PROSES BUILD TWITTER CRAWLER PORTABLE")
    print("=" * 60)

    os.makedirs(RUNTIME_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    # 1. Download & Setup Python Embeddable
    python_exe = os.path.join(PYTHON_DIR, "python.exe")
    if not os.path.exists(python_exe):
        print("\n[1/4] Menyiapkan Python Embeddable...")
        py_zip = os.path.join(TEMP_DIR, f"python-{PYTHON_VER}.zip")
        download_file(PYTHON_ZIP_URL, py_zip)

        os.makedirs(PYTHON_DIR, exist_ok=True)
        print("--> Mengekstrak Python...")
        with zipfile.ZipFile(py_zip, "r") as z:
            z.extractall(PYTHON_DIR)

        # Aktifkan site-packages pada Python embeddable (._pth file)
        pth_file = None
        for f in os.listdir(PYTHON_DIR):
            if f.endswith("._pth"):
                pth_file = os.path.join(PYTHON_DIR, f)
                break

        if pth_file and os.path.exists(pth_file):
            print("--> Mengaktifkan import site pada file ._pth...")
            with open(pth_file, "r", encoding="utf-8") as f:
                content = f.read()
            # Un-comment 'import site'
            lines = []
            for line in content.splitlines():
                if line.strip() == "#import site":
                    lines.append("import site")
                else:
                    lines.append(line)
            if "import site" not in lines:
                lines.append("import site")
            with open(pth_file, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")

        # Install pip
        print("--> Menyiapkan pip untuk Python portabel...")
        get_pip_py = os.path.join(TEMP_DIR, "get-pip.py")
        download_file(GET_PIP_URL, get_pip_py)
        subprocess.run([python_exe, get_pip_py, "--no-warn-script-location"], check=True)
    else:
        print("\n[1/4] Python Embeddable sudah tersedia, lewati.")

    # 2. Install Python Dependencies
    print("\n[2/4] Menginstal library Python (Streamlit, Pandas, Playwright)...")
    req_file = os.path.join(ROOT_DIR, "requirements.txt")
    subprocess.run([
        python_exe, "-m", "pip", "install", "-r", req_file,
        "--no-warn-script-location"
    ], check=True)

    # 3. Setup Node.js Portable
    node_exe = os.path.join(NODE_DIR, "node.exe")
    if not os.path.exists(node_exe):
        print("\n[3/4] Menyiapkan Node.js Portable...")
        node_zip = os.path.join(TEMP_DIR, f"node-{NODE_VER}.zip")
        download_file(NODE_ZIP_URL, node_zip)

        print("--> Mengekstrak Node.js...")
        extract_tmp = os.path.join(TEMP_DIR, "node_extracted")
        with zipfile.ZipFile(node_zip, "r") as z:
            z.extractall(extract_tmp)

        extracted_subdirs = [os.path.join(extract_tmp, d) for d in os.listdir(extract_tmp) if os.path.isdir(os.path.join(extract_tmp, d))]
        if extracted_subdirs:
            if os.path.exists(NODE_DIR):
                shutil.rmtree(NODE_DIR)
            shutil.move(extracted_subdirs[0], NODE_DIR)
    else:
        print("\n[3/4] Node.js Portable sudah tersedia, lewati.")

    # 4. Download Playwright Chromium ke runtime portabel
    print("\n[4/4] Mengunduh Chromium ke dalam folder runtime portabel...")
    os.makedirs(BROWSERS_DIR, exist_ok=True)
    env = os.environ.copy()
    env["PATH"] = NODE_DIR + os.pathsep + env.get("PATH", "")
    env["PLAYWRIGHT_BROWSERS_PATH"] = BROWSERS_DIR

    npx_cmd = os.path.join(NODE_DIR, "npx.cmd")
    if os.path.exists(npx_cmd):
        cmd = [npx_cmd, "-y", "playwright", "install", "chromium"]
    else:
        cmd = ["npx", "-y", "playwright", "install", "chromium"]

    try:
        subprocess.run(cmd, env=env, check=True, shell=True)
    except Exception as e:
        print(f"Peringatan saat install Chromium: {e}")

    # Bersihkan temp_downloads
    if os.path.exists(TEMP_DIR):
        try:
            shutil.rmtree(TEMP_DIR)
        except Exception:
            pass

    print("\n" + "=" * 60)
    print("   BERHASIL! BUNDLE PORTABLE SUDAH SELESAI DIBUAT!")
    print("=" * 60)
    print("Semua file sudah lengkap di folder 'runtime'.")
    print("Pengguna cukup menjalankan file 'JALANKAN_APLIKASI.bat'!")


if __name__ == "__main__":
    setup_portable()
