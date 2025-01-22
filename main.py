import os
import time
import json
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from colorama import Fore, Style, init
import threading

# Inisialisasi colorama
init(autoreset=True)

def log_with_time(message, color=Fore.RESET):
    """Menampilkan pesan dengan waktu saat ini."""
    current_time = datetime.now().strftime("%H:%M:%S")
    print(color + f"[{current_time}] {message}" + Style.RESET_ALL)

def load_config():
    """Memuat konfigurasi dari file config.json."""
    config_file = "config.json"
    if not os.path.isfile(config_file):
        raise FileNotFoundError(f"File konfigurasi tidak ditemukan: {config_file}")
    with open(config_file, "r") as file:
        return json.load(file)

def validate_extension_path(path):
    """Memeriksa apakah path ekstensi valid dan berisi file manifest.json."""
    manifest_file = os.path.join(path, "manifest.json")
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Folder ekstensi tidak ditemukan: {path}")
    if not os.path.isfile(manifest_file):
        raise FileNotFoundError(f"File manifest.json tidak ditemukan di: {path}")
    return True

def start_browser(depined_extension_path, profile_path, mode):
    """Menginisialisasi browser dengan mode tertentu."""
    options = uc.ChromeOptions()
    options.add_argument(f"--load-extension={depined_extension_path}")
    options.add_argument(f"--user-data-dir={profile_path}")

    if mode == "headless":
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

    driver = uc.Chrome(options=options)
    return driver

def menu():
    print(Fore.CYAN + "=" * 50)
    print(Fore.YELLOW + " SELENIUM BROWSER AUTOMATION ".center(50))
    print(Fore.CYAN + "=" * 50)
    print("\nPilih opsi:")
    print("1. Login Manual")
    print("2. Mode GUI")
    print("3. Mode Headless")
    print("4. Stop dan Keluar")

def elapsed_time_thread(start_time, stop_flag):
    """Thread untuk menampilkan waktu berjalan."""
    while not stop_flag.is_set():
        elapsed = datetime.now() - start_time
        hours, remainder = divmod(elapsed.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        elapsed_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        print(Fore.CYAN + f"\rWaktu berjalan: {elapsed_str}", end="")
        time.sleep(1)

def main():
    try:
        config = load_config()
        depined_extension_path = config.get("extension_path", "./depined_extension")
        profile_path = config.get("profile_path", "./chrome_profile")

        validate_extension_path(depined_extension_path)
    except FileNotFoundError as e:
        log_with_time(f"Kesalahan: {e}", Fore.RED)
        return

    driver = None
    keep_running = True
    stop_flag = threading.Event()

    def stop_script():
        nonlocal keep_running
        log_with_time("Menutup browser dan menghentikan skrip...", Fore.MAGENTA)
        keep_running = False
        stop_flag.set()
        if driver:
            driver.quit()

    while keep_running:
        menu()
        choice = input("Masukkan pilihan: ").strip()

        if choice == "1":
            log_with_time("Memulai login manual...", Fore.GREEN)
            driver = start_browser(depined_extension_path, profile_path, "manual")
            driver.get("https://accounts.google.com")

        elif choice == "2":
            log_with_time("Memulai browser dengan GUI...", Fore.GREEN)
            driver = start_browser(depined_extension_path, profile_path, "gui")
            driver.get("https://chromewebstore.google.com")

        elif choice == "3":
            log_with_time("Memulai browser dalam mode headless...", Fore.GREEN)
            driver = start_browser(depined_extension_path, profile_path, "headless")
            driver.get("https://chromewebstore.google.com")

            log_with_time("Halaman berhasil dimuat.", Fore.BLUE)

            start_time = datetime.now()
            stop_flag.clear()
            threading.Thread(target=elapsed_time_thread, args=(start_time, stop_flag), daemon=True).start()

        elif choice == "4":
            stop_script()

        else:
            log_with_time("Pilihan tidak valid. Silakan coba lagi.", Fore.RED)

if __name__ == "__main__":
    main()
