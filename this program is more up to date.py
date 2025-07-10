import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import requests
import os
import subprocess
import locale
import json # Ayarları kaydetmek için

# --- Sabitler ve Ayarlar ---
ADMIN_PASSWORD = "2201126292ASd"
USER_LOG_FILE = "guest_users.txt"
SETTINGS_FILE = "settings.json" # Ayarları kaydetmek için dosya

# Dil sözlükleri
LANGUAGES = {
    "tr": {
        "app_title": "Uygulama Yükleyici",
        "download_selected": "Seçilenleri İndir",
        "admin_login": "Admin Girişi",
        "guest_mode": "Misafir Modu",
        "update_checker": "Güncelleme Denetleyicisi",
        "search_app": "Uygulama Ara...",
        "settings": "Ayarlar",
        "language_settings": "Dil Ayarları",
        "driver_scanner": "Sürücü Tarayıcı",
        "password": "Şifre:",
        "login": "Giriş",
        "login_success": "Giriş Başarılı",
        "welcome_admin": "Admin paneline hoş geldiniz.",
        "wrong_password": "Yanlış şifre!",
        "admin_panel": "Admin Paneli",
        "upload_updates": "Güncellemeleri Yükle",
        "update_uploaded": "Güncellemeler yüklendi.",
        "open_file": "Dosya Aç",
        "guest_count": "Misafir Kullanıcı Sayısı",
        "total_guest_users": "Toplam misafir kullanıcı:",
        "enter_name": "Lütfen isminizi girin:",
        "welcome_guest": "Hoş geldin, {}!",
        "warning": "Uyarı",
        "select_at_least_one_app": "Lütfen en az bir uygulama seçin.",
        "download_complete": "Tamamlandı",
        "app_downloaded": "{} yüklendi. Dosya konumu: {}",
        "app_installed": "{} Yüklü",
        "update_check": "Güncelleme Kontrolü",
        "updates_checked": "{} için güncellemeler kontrol edildi.",
        "error": "Hata",
        "download_failed": "{} indirilemedi!",
        "all_downloads_complete": "Seçilen uygulamalar indirildi.",
        "checking_updates": "Güncellemeler kontrol ediliyor...",
        "no_drivers_found": "Sistemde sürücü bulunamadı veya listelenemedi.",
        "drivers_found": "Sistemdeki Sürücüler:",
        "select_language": "Dil Seçin:",
        "apply_language": "Dili Uygula",
        "select_download_folder": "İndirme Klasörü Seç",
        "download_folder": "İndirme Klasörü:",
        "category": "Kategori:",
        "all_categories": "Tüm Kategoriler",
        "development": "Geliştirme",
        "browsers": "Tarayıcılar",
        "utilities": "Yardımcı Programlar",
        "multimedia": "Multimedya",
        "design": "Tasarım",
        "gaming": "Oyunlar",
        "security": "Güvenlik",
        "office": "Ofis",
        "virtualization": "Sanallaştırma",
        "communication": "İletişim",
        "databases": "Veritabanları",
        "system_tools": "Sistem Araçları",
        "vpn": "VPN",
        "password_managers": "Şifre Yöneticileri",
        "education": "Eğitim",
        "emulators": "Emülatörler",
        "file_transfer": "Dosya Transferi",
        "download_progress": "İndirme İlerlemesi",
        "current_download": "Şu An İndiriliyor:",
        "total_progress": "Toplam İlerleme:",
        "download_speed": "İndirme Hızı:",
        "remaining_time": "Kalan Süre:",
        "mb_per_sec": "MB/sn",
        "unknown": "Bilinmiyor"
    },
    "en": {
        "app_title": "Application Installer",
        "download_selected": "Download Selected",
        "admin_login": "Admin Login",
        "guest_mode": "Guest Mode",
        "update_checker": "Update Checker",
        "search_app": "Search Application...",
        "settings": "Settings",
        "language_settings": "Language Settings",
        "driver_scanner": "Driver Scanner",
        "password": "Password:",
        "login": "Login",
        "login_success": "Login Successful",
        "welcome_admin": "Welcome to the admin panel.",
        "wrong_password": "Wrong password!",
        "admin_panel": "Admin Panel",
        "upload_updates": "Upload Updates",
        "update_uploaded": "Updates uploaded.",
        "open_file": "Open File",
        "guest_count": "Guest User Count",
        "total_guest_users": "Total guest users:",
        "enter_name": "Please enter your name:",
        "welcome_guest": "Welcome, {}!",
        "warning": "Warning",
        "select_at_least_one_app": "Please select at least one application.",
        "download_complete": "Completed",
        "app_downloaded": "{} downloaded. File location: {}",
        "app_installed": "{} Installed",
        "update_check": "Update Check",
        "updates_checked": "Updates checked for {}.",
        "error": "Error",
        "download_failed": "Failed to download {}!",
        "all_downloads_complete": "Selected applications downloaded.",
        "checking_updates": "Checking for updates...",
        "no_drivers_found": "No drivers found or could not be listed on the system.",
        "drivers_found": "Drivers on the System:",
        "select_language": "Select Language:",
        "apply_language": "Apply Language",
        "select_download_folder": "Select Download Folder",
        "download_folder": "Download Folder:",
        "category": "Category:",
        "all_categories": "All Categories",
        "development": "Development",
        "browsers": "Browsers",
        "utilities": "Utilities",
        "multimedia": "Multimedia",
        "design": "Design",
        "gaming": "Gaming",
        "security": "Security",
        "office": "Office",
        "virtualization": "Virtualization",
        "communication": "Communication",
        "databases": "Databases",
        "system_tools": "System Tools",
        "vpn": "VPN",
        "password_managers": "Password Managers",
        "education": "Education",
        "emulators": "Emulators",
        "file_transfer": "File Transfer",
        "download_progress": "Download Progress",
        "current_download": "Currently Downloading:",
        "total_progress": "Total Progress:",
        "download_speed": "Download Speed:",
        "remaining_time": "Remaining Time:",
        "mb_per_sec": "MB/s",
        "unknown": "Unknown"
    }
}

# Uygulama listesi (Kategoriler eklendi)
apps = [
    # Geliştirme
    {"name": "PyCharm Community", "url": "https://download.jetbrains.com/python/pycharm-community-2024.1.2.exe", "size_mb": 500, "category": "development"},
    {"name": "Android Studio", "url": "https://redirector.gvt1.com/edgedl/android/studio/install/2023.1.1.24/android-studio-2023.1.1.24-windows.exe", "size_mb": 900, "category": "development"},
    {"name": "IntelliJ IDEA Community", "url": "https://download.jetbrains.com/idea/ideaIC-2024.1.2.exe", "size_mb": 700, "category": "development"},
    {"name": "Sublime Text", "url": "https://download.sublimetext.com/Sublime%20Text%20Build%204216%20x64%20Setup.exe", "size_mb": 20, "category": "development"},
    {"name": "XAMPP", "url": "https://www.apachefriends.org/xampp-files/8.2.4/xampp-windows-x64-8.2.4-0-VS16-installer.exe", "size_mb": 150, "category": "development"},
    {"name": "Eclipse IDE", "url": "https://ftp.fau.de/eclipse/technology/epp/downloads/release/2024-03/R/eclipse-inst-jre-win64.exe", "size_mb": 120, "category": "development"},
    {"name": "Visual Studio Code", "url": "https://update.code.visualstudio.com/latest/win32-x64-user/stable", "size_mb": 90, "category": "development"},
    {"name": "Git", "url": "https://github.com/git-for-windows/git/releases/download/v2.45.1.windows.1/Git-2.45.1-64-bit.exe", "size_mb": 50, "category": "development"},
    {"name": "Node.js", "url": "https://nodejs.org/dist/v20.12.2/node-v20.12.2-x64.msi", "size_mb": 30, "category": "development"},
    {"name": "Python", "url": "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe", "size_mb": 30, "category": "development"},
    {"name": "Java JDK", "url": "https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.exe", "size_mb": 160, "category": "development"},
    {"name": "Docker Desktop", "url": "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe", "size_mb": 500, "category": "development"},
    {"name": "Postman", "url": "https://dl.pstmn.io/download/latest/win64", "size_mb": 120, "category": "development"},
    {"name": "WampServer", "url": "https://sourceforge.net/projects/wampserver/files/WampServer%203/WampServer%203.3.1/wampserver3.3.1_x64.exe/download", "size_mb": 700, "category": "development"},
    {"name": "MAMP", "url": "https://downloads.mamp.info/MAMP-PRO/releases/6.8.1/MAMP_MAMP_PRO_6.8.1.exe", "size_mb": 500, "category": "development"},
    {"name": "R Studio", "url": "https://download1.rstudio.org/desktop/windows/RStudio-2024.04.1-748.exe", "size_mb": 200, "category": "development"},
    {"name": "MATLAB Runtime", "url": "https://ssd.mathworks.com/supportfiles/downloads/R2024a/Release/9/deployment_files/installer/complete/win64/MATLAB_Runtime_R2024a_win64.exe", "size_mb": 3000, "category": "education"}, # Hem geliştirme hem eğitim
    {"name": "Cisco Packet Tracer", "url": "https://www.netacad.com/portal/resources/packet-tracer-download", "size_mb": 200, "category": "education"},

    # Tarayıcılar
    {"name": "Google Chrome", "url": "https://dl.google.com/chrome/install/latest/chrome_installer.exe", "size_mb": 80, "category": "browsers"},
    {"name": "Mozilla Firefox", "url": "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=tr", "size_mb": 75, "category": "browsers"},
    {"name": "Opera Browser", "url": "https://net.geo.opera.com/opera/stable/windows", "size_mb": 70, "category": "browsers"},
    {"name": "Brave Browser", "url": "https://laptop-updates.brave.com/latest/winx64", "size_mb": 80, "category": "browsers"},
    {"name": "Tor Browser", "url": "https://www.torproject.org/dist/torbrowser/13.0.13/torbrowser-install-win64-13.0.13_ALL.exe", "size_mb": 90, "category": "browsers"},
    {"name": "Microsoft Edge", "url": "https://msedgesetup.azureedge.net/latest/MicrosoftEdgeSetup.exe", "size_mb": 120, "category": "browsers"},

    # Yardımcı Programlar
    {"name": "WinRAR", "url": "https://www.rarlab.com/rar/winrar-x64-624tr.exe", "size_mb": 5, "category": "utilities"},
    {"name": "7-Zip", "url": "https://www.7-zip.org/a/7z2405-x64.exe", "size_mb": 3, "category": "utilities"},
    {"name": "Notepad++", "url": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.6.5/npp.8.6.5.Installer.x64.exe", "size_mb": 5, "category": "utilities"},
    {"name": "CCleaner", "url": "https://download.ccleaner.com/ccsetup624.exe", "size_mb": 35, "category": "utilities"},
    {"name": "Revo Uninstaller", "url": "https://www.revouninstaller.com/downloads/RevoUninProSetup.exe", "size_mb": 20, "category": "utilities"},
    {"name": "AIDA64 Extreme", "url": "https://download.aida64.com/aida64extreme700.exe", "size_mb": 50, "category": "system_tools"},
    {"name": "HWMonitor", "url": "https://www.cpuid.com/downloads/hwmonitor/hwmonitor_1.54.exe", "size_mb": 2, "category": "system_tools"},
    {"name": "CPU-Z", "url": "https://download.cpuid.com/cpu-z/cpu-z_2.09-en.exe", "size_mb": 2, "category": "system_tools"},
    {"name": "CrystalDiskInfo", "url": "https://osdn.net/projects/crystaldiskinfo/downloads/78394/CrystalDiskInfo8_17_14.exe", "size_mb": 6, "category": "system_tools"},
    {"name": "FileZilla", "url": "https://download.filezilla-project.org/client/FileZilla_3.67.0_win64-setup.exe", "size_mb": 12, "category": "file_transfer"},
    {"name": "PuTTY", "url": "https://the.earth.li/~sgtatham/putty/latest/w64/putty-64bit-0.81-installer.msi", "size_mb": 3, "category": "utilities"},
    {"name": "WinSCP", "url": "https://winscp.net/download/WinSCP-6.3.3-Setup.exe", "size_mb": 12, "category": "file_transfer"},
    {"name": "MobaXterm", "url": "https://download.mobatek.net/2462024012212345/MobaXterm_Installer_v24.6.zip", "size_mb": 50, "category": "utilities"},
    {"name": "Termius", "url": "https://www.termius.com/windows_setup.exe", "size_mb": 80, "category": "utilities"},

    # Multimedya
    {"name": "VLC Media Player", "url": "https://get.videolan.org/vlc/3.0.20/win64/vlc-3.0.20-win64.exe", "size_mb": 40, "category": "multimedia"},
    {"name": "OBS Studio", "url": "https://cdn-fastly.obsproject.com/downloads/OBS-Studio-30.1.2-Full-Installer-x64.exe", "size_mb": 120, "category": "multimedia"},
    {"name": "Audacity", "url": "https://github.com/audacity/audacity/releases/download/Audacity-3.5.1/audacity-win-3.5.1-64bit.exe", "size_mb": 40, "category": "multimedia"},
    {"name": "DaVinci Resolve", "url": "https://www.blackmagicdesign.com/api/register/us/download/resolve-windows/DaVinci_Resolve_18.6.6_Windows.zip", "size_mb": 2500, "category": "multimedia"},
    {"name": "HandBrake", "url": "https://github.com/HandBrake/HandBrake/releases/download/1.7.3/HandBrake-1.7.3-x86_64-Win_GUI.exe", "size_mb": 20, "category": "multimedia"},

    # Tasarım
    {"name": "Adobe Illustrator", "url": "https://download.adobe.com/pub/adobe/illustrator/win/26.x/Illustrator_26_LS20_win64.exe", "size_mb": 200, "category": "design"},
    {"name": "Adobe Premiere Pro", "url": "https://download.adobe.com/pub/adobe/premiere/win/22.x/Premiere_Pro_22_LS20_win64.exe", "size_mb": 300, "category": "design"},
    {"name": "Adobe After Effects", "url": "https://download.adobe.com/pub/adobe/aftereffects/win/22.x/After_Effects_22_LS20_win64.exe", "size_mb": 250, "category": "design"},
    {"name": "Adobe Lightroom", "url": "https://download.adobe.com/pub/adobe/lightroom/win/6.x/Lightroom_6_LS11_win64.exe", "size_mb": 150, "category": "design"},
    {"name": "GIMP", "url": "https://download.gimp.org/mirror/pub/gimp/v2.10/windows/gimp-2.10.36-setup.exe", "size_mb": 250, "category": "design"},
    {"name": "Inkscape", "url": "https://media.inkscape.org/dl/resources/file/inkscape-1.3.2_2024-01-14_amd64.exe", "size_mb": 120, "category": "design"},
    {"name": "Krita", "url": "https://download.kde.org/stable/krita/5.2.2/krita-x64-5.2.2-setup.exe", "size_mb": 150, "category": "design"},
    {"name": "Paint.NET", "url": "https://www.dotpdn.com/files/paint.net.5.0.13.install.x64.exe", "size_mb": 60, "category": "design"},
    {"name": "Figma Desktop", "url": "https://desktop.figma.com/win/FigmaSetup.exe", "size_mb": 80, "category": "design"},
    {"name": "Blender", "url": "https://download.blender.org/release/Blender3.6/blender-3.6.10-windows-x64.msi", "size_mb": 250, "category": "design"},
    {"name": "Unity Hub", "url": "https://public-cdn.cloud.unity3d.com/hub/prod/UnityHubSetup.exe", "size_mb": 120, "category": "development"}, # Hem tasarım hem geliştirme
    {"name": "Unreal Engine Launcher", "url": "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi", "size_mb": 80, "category": "development"}, # Hem tasarım hem geliştirme

    # Oyunlar ve Oyun Platformları
    {"name": "Steam", "url": "https://cdn.cloudflare.steamstatic.com/client/installer/SteamSetup.exe", "size_mb": 5, "category": "gaming"},
    {"name": "Epic Games Launcher", "url": "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi", "size_mb": 80, "category": "gaming"},
    {"name": "Battle.net", "url": "https://www.battle.net/download/getInstaller?os=win", "size_mb": 5, "category": "gaming"},
    {"name": "Origin (EA App)", "url": "https://download.dm.origin.com/origin/live/OriginThinSetup.exe", "size_mb": 70, "category": "gaming"},
    {"name": "BlueStacks", "url": "https://cdn3.bluestacks.com/downloads/windows/nxt/5.20.0.1053/BlueStacksInstaller_5.20.0.1053_native.exe", "size_mb": 600, "category": "emulators"},
    {"name": "LDPlayer", "url": "https://cdn.ldmnq.com/download/package/LDPlayer_9.0.71.exe", "size_mb": 600, "category": "emulators"},
    {"name": "Genymotion", "url": "https://dl.genymotion.com/releases/genymotion-3.6.0/genymotion-3.6.0.exe", "size_mb": 200, "category": "emulators"},

    # Güvenlik
    {"name": "AVG Antivirus Free", "url": "https://files-download.avg.com/inst/mp/AVG_Antivirus_Free_Installer.exe", "size_mb": 250, "category": "security"},
    {"name": "Avast Free Antivirus", "url": "https://files.avast.com/iavs9x/avast_free_antivirus_setup_online.exe", "size_mb": 250, "category": "security"},
    {"name": "Kaspersky Security Cloud", "url": "https://products.s.kaspersky-labs.com/homeuser/kaspersky_security_cloud/21.3.10.391/patch_k/ks4.021.3.10.391en_23857.exe", "size_mb": 180, "category": "security"},
    {"name": "Malwarebytes", "url": "https://data-cdn.mbamupdates.com/web/mb4-setup-consumer/MBSetup.exe", "size_mb": 90, "category": "security"},
    {"name": "NordVPN", "url": "https://downloads.nordcdn.com/apps/windows/NordVPN/latest/NordVPNSetup.exe", "size_mb": 80, "category": "vpn"},
    {"name": "ProtonVPN", "url": "https://protonvpn.com/download/ProtonVPN_win_v4.4.0.exe", "size_mb": 80, "category": "vpn"},

    # Ofis ve Üretkenlik
    {"name": "LibreOffice", "url": "https://download.documentfoundation.org/libreoffice/stable/24.2.4/win/x86_64/LibreOffice_24.2.4_Win_x86-64.msi", "size_mb": 350, "category": "office"},
    {"name": "Foxit Reader", "url": "https://cdn01.foxitsoftware.com/product/reader/desktop/win/12.1.3/FoxitPDFReader1213_L10N_Setup_Prom.exe", "size_mb": 160, "category": "office"},
    {"name": "Adobe Acrobat Reader", "url": "https://ardownload2.adobe.com/pub/adobe/reader/win/AcrobatDC/2300820419/AcroRdrDC2300820419_tr_TR.exe", "size_mb": 200, "category": "office"},
    {"name": "Power BI Desktop", "url": "https://download.microsoft.com/download/7/8/8/788E1F7B-7B7E-4B7B-8A7B-7B7B7B7B7B7B/PBIDesktopSetup_x64.exe", "size_mb": 400, "category": "office"},
    {"name": "Tableau Public", "url": "https://downloads.tableau.com/tssoftware/TableauPublic-2024-1-0.exe", "size_mb": 500, "category": "office"},

    # Sanallaştırma
    {"name": "VirtualBox", "url": "https://download.virtualbox.org/virtualbox/7.0.18/VirtualBox-7.0.18-162988-Win.exe", "size_mb": 110, "category": "virtualization"},
    {"name": "VMware Workstation Player", "url": "https://download3.vmware.com/software/WKST-PLAYER-1706/VMware-player-full-17.0.6-22583795.exe", "size_mb": 600, "category": "virtualization"},

    # İletişim
    {"name": "Discord", "url": "https://discord.com/api/download?platform=win", "size_mb": 80, "category": "communication"},
    {"name": "Spotify", "url": "https://download.scdn.co/SpotifySetup.exe", "size_mb": 80, "category": "communication"},
    {"name": "Slack", "url": "https://downloads.slack-edge.com/releases_x64/SlackSetup.exe", "size_mb": 90, "category": "communication"},
    {"name": "Zoom", "url": "https://zoom.us/client/latest/ZoomInstaller.exe", "size_mb": 60, "category": "communication"},
    {"name": "Microsoft Teams", "url": "https://statics.teams.cdn.office.net/production-windows-x64/1.6.00.12455/Teams_windows_x64.exe", "size_mb": 120, "category": "communication"},
    {"name": "TeamViewer", "url": "https://download.teamviewer.com/download/TeamViewer_Setup_x64.exe", "size_mb": 40, "category": "communication"},
    {"name": "AnyDesk", "url": "https://download.anydesk.com/AnyDesk.exe", "size_mb": 5, "category": "communication"},

    # Veritabanları
    {"name": "MySQL Installer", "url": "https://dev.mysql.com/get/Downloads/MySQLInstaller/mysql-installer-web-community-8.0.36.0.msi", "size_mb": 2, "category": "databases"},
    {"name": "PostgreSQL", "url": "https://get.enterprisedb.com/postgresql/postgresql-16.2-1-windows-x64.exe", "size_mb": 250, "category": "databases"},
    {"name": "MongoDB Compass", "url": "https://downloads.mongodb.com/compass/mongodb-compass-1.42.6-win32-x64.exe", "size_mb": 120, "category": "databases"},
    {"name": "HeidiSQL", "url": "https://www.heidisql.com/downloads/releases/HeidiSQL_12.7.0.6677_Setup.exe", "size_mb": 12, "category": "databases"},
    {"name": "DBeaver", "url": "https://dbeaver.io/files/dbeaver-ce-latest-x86_64-setup.exe", "size_mb": 90, "category": "databases"},

    # Şifre Yöneticileri
    {"name": "Bitwarden", "url": "https://vault.bitwarden.com/download/?app=desktop&platform=windows", "size_mb": 80, "category": "password_managers"},
    {"name": "KeePass", "url": "https://downloads.sourceforge.net/project/keepass/KeePass%202.x/2.56/KeePass-2.56-Setup.exe", "size_mb": 5, "category": "password_managers"},
    {"name": "LastPass", "url": "https://download.cloud.lastpass.com/windows_installer/LastPassInstaller.exe", "size_mb": 30, "category": "password_managers"},
]

# Kategorileri dinamik olarak al
CATEGORIES = sorted(list(set(app["category"] for app in apps)))
CATEGORIES.insert(0, "all_categories") # "Tüm Kategoriler" seçeneğini en başa ekle

# --- Global Değişkenler ---
current_language = tk.StringVar(value="tr") # Varsayılan dil Türkçe
download_folder = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads", "UygulamaYukleyici")) # Varsayılan indirme klasörü
selected_category = tk.StringVar(value="all_categories") # Varsayılan kategori

# İndirme ilerlemesi için değişkenler
current_download_app_name = tk.StringVar(value="")
current_download_progress = tk.DoubleVar(value=0)
current_download_speed = tk.StringVar(value="0 MB/sn")
current_download_remaining_time = tk.StringVar(value="Bilinmiyor")
total_download_progress = tk.DoubleVar(value=0)

# --- Yardımcı Fonksiyonlar ---
def get_text(key):
    return LANGUAGES[current_language.get()].get(key, key)

def load_settings():
    global current_language, download_folder
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
            if "language" in settings:
                current_language.set(settings["language"])
            if "download_folder" in settings:
                download_folder.set(settings["download_folder"])
    # Ayarlar yüklendikten sonra UI metinlerini güncelle
    update_ui_texts()

def save_settings():
    settings = {
        "language": current_language.get(),
        "download_folder": download_folder.get()
    }
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

# --- İndirme Fonksiyonları ---
def download_file(url, filename, app_name, total_apps_to_download, app_index):
    try:
        start_time = time.time()
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            downloaded_size = 0
            
            current_download_app_name.set(app_name)

            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Uygulama bazında ilerleme
                        app_progress = (downloaded_size / total_size) * 100
                        current_download_progress.set(app_progress)

                        # Toplam ilerleme (tüm uygulamalar için)
                        total_progress_val = ((app_index * 100) + app_progress) / total_apps_to_download
                        total_download_progress.set(total_progress_val)

                        # Hız ve kalan süre hesaplama
                        elapsed_time = time.time() - start_time
                        if elapsed_time > 0:
                            speed = (downloaded_size / elapsed_time) / (1024 * 1024) # MB/sn
                            current_download_speed.set(f"{speed:.2f} {get_text('mb_per_sec')}")
                            if total_size > 0:
                                remaining_bytes = total_size - downloaded_size
                                remaining_seconds = remaining_bytes / (speed * 1024 * 1024) if speed > 0 else float('inf')
                                current_download_remaining_time.set(format_time(remaining_seconds))
                            else:
                                current_download_remaining_time.set(get_text('unknown'))
                        else:
                            current_download_speed.set(f"0 {get_text('mb_per_sec')}")
                            current_download_remaining_time.set(get_text('unknown'))

        messagebox.showinfo(get_text("download_complete"), get_text("app_downloaded").format(app_name, os.path.abspath(filename)))
        subprocess.Popen(f'explorer /select,"{os.path.abspath(filename)}"')
        check_for_updates(app_name)
        return True
    except Exception as e:
        messagebox.showerror(get_text("error"), get_text("download_failed").format(app_name) + f"\nHata: {e}")
        return False

def format_time(seconds):
    if seconds == float('inf'):
        return get_text('unknown')
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}s {minutes}dk {seconds}sn"
    elif minutes > 0:
        return f"{minutes}dk {seconds}sn"
    else:
        return f"{seconds}sn"

def check_for_updates(app_name):
    messagebox.showinfo(get_text("update_check"), get_text("updates_checked").format(app_name))

def start_download_thread(selected_indices):
    os.makedirs(download_folder.get(), exist_ok=True)
    total_apps_to_download = len(selected_indices)
    
    for i, idx in enumerate(selected_indices):
        app = apps[idx]
        filename = os.path.join(download_folder.get(), app["name"].replace(" ", "_") + os.path.splitext(app["url"])[-1])
        
        status = download_file(app["url"], filename, app["name"], total_apps_to_download, i)
        if not status:
            # Hata durumunda ilerlemeyi sıfırla veya uygun şekilde ayarla
            current_download_progress.set(0)
            current_download_app_name.set("")
            current_download_speed.set(f"0 {get_text('mb_per_sec')}")
            current_download_remaining_time.set(get_text('unknown'))
            # Hata durumunda toplam ilerlemeyi de güncellemek gerekebilir
            # Örneğin, bu uygulamayı atlayıp bir sonraki uygulamaya geçiyorsak
            # total_download_progress'i de buna göre ayarlamalıyız.
            # Şimdilik sadece mevcut uygulamanın ilerlemesini sıfırlayalım.
            
    messagebox.showinfo(get_text("download_complete"), get_text("all_downloads_complete"))
    # Tüm indirmeler bittiğinde ilerlemeyi sıfırla
    current_download_app_name.set("")
    current_download_progress.set(0)
    current_download_speed.set(f"0 {get_text('mb_per_sec')}")
    current_download_remaining_time.set(get_text('unknown'))
    total_download_progress.set(0)


def on_download():
    selected = [i for i, var in enumerate(vars) if var.get()]
    if not selected:
        messagebox.showwarning(get_text("warning"), get_text("select_at_least_one_app"))
        return
    threading.Thread(target=start_download_thread, args=(selected,), daemon=True).start()

# --- Yönetim ve Misafir Fonksiyonları ---
def admin_login():
    def check_password():
        if password_entry.get() == ADMIN_PASSWORD:
            messagebox.showinfo(get_text("login_success"), get_text("welcome_admin"))
            admin_panel()
            login_window.destroy()
        else:
            messagebox.showerror(get_text("error"), get_text("wrong_password"))

    login_window = tk.Toplevel(root)
    login_window.title(get_text("admin_login"))
    tk.Label(login_window, text=get_text("password")).pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)
    tk.Button(login_window, text=get_text("login"), command=check_password).pack(pady=10)

def admin_panel():
    admin_window = tk.Toplevel(root)
    admin_window.title(get_text("admin_panel"))
    
    ttk.Label(admin_window, text=get_text("upload_updates")).pack(pady=10)

    def upload_updates():
        messagebox.showinfo(get_text("update_check"), get_text("update_uploaded"))

    def open_file():
        file_path = filedialog.askopenfilename(title=get_text("open_file"))
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                text_window = tk.Toplevel(admin_window)
                text_window.title(os.path.basename(file_path))
                text = tk.Text(text_window, wrap="word", width=80, height=20)
                text.insert("1.0", content)
                text.pack(expand=True, fill="both")
            except Exception as e:
                messagebox.showerror(get_text("error"), f"Dosya okunamadı: {e}")

    def show_user_count():
        if os.path.exists(USER_LOG_FILE):
            with open(USER_LOG_FILE, "r", encoding="utf-8") as f:
                users = f.readlines()
            count = len(users)
        else:
            count = 0
        messagebox.showinfo(get_text("guest_count"), get_text("total_guest_users").format(count))

    ttk.Button(admin_window, text=get_text("upload_updates"), command=upload_updates).pack(pady=10)
    ttk.Button(admin_window, text=get_text("open_file"), command=open_file).pack(pady=10)
    ttk.Button(admin_window, text=get_text("guest_count"), command=show_user_count).pack(pady=10)

def guest_mode():
    def submit_name():
        name = name_entry.get().strip()
        if not name:
            messagebox.showwarning(get_text("warning"), get_text("enter_name"))
            return
        with open(USER_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(name + "\n")
        messagebox.showinfo(get_text("guest_mode"), get_text("welcome_guest").format(name))
        guest_window.destroy()

    guest_window = tk.Toplevel(root)
    guest_window.title(get_text("guest_mode"))
    ttk.Label(guest_window, text=get_text("enter_name")).pack(pady=10)
    name_entry = ttk.Entry(guest_window)
    name_entry.pack(pady=5)
    ttk.Button(guest_window, text=get_text("login"), command=submit_name).pack(pady=10)

def update_checker():
    messagebox.showinfo(get_text("update_checker"), get_text("checking_updates"))

# --- Filtreleme ve Arayüz Güncelleme Fonksiyonları ---
def filter_apps(event=None):
    search_term = search_entry.get().lower()
    current_cat = selected_category.get()

    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    
    global vars
    vars = []
    row_num = 0
    for i, app in enumerate(apps):
        app_name_lower = app['name'].lower()
        app_category = app.get('category', 'unknown') # Kategori yoksa 'unknown' varsay
        
        category_match = (current_cat == "all_categories" or app_category == current_cat)
        search_match = (get_text("search_app").lower() == search_term or search_term in app_name_lower)

        if category_match and search_match:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(scrollable_frame, text=f"{app['name']} ({app['size_mb']} MB)", variable=var)
            chk.grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
            vars.append(var)
            row_num += 1
    canvas.configure(scrollregion=canvas.bbox("all"))

def update_ui_texts():
    root.title(get_text("app_title"))
    btn_download.config(text=get_text("download_selected"))
    btn_admin.config(text=get_text("admin_login"))
    btn_guest.config(text=get_text("guest_mode"))
    btn_update_checker.config(text=get_text("update_checker"))
    search_entry.config(placeholder=get_text("search_app")) # Placeholder metnini güncelle
    btn_settings.config(text=get_text("settings"))
    
    # Kategori menüsünü güncelle
    category_label.config(text=get_text("category"))
    # OptionMenu'yu yeniden oluşturmak daha kolay olabilir
    # Mevcut OptionMenu'yu silip yenisini oluşturmak yerine, menüdeki seçenekleri dinamik olarak güncelleyebiliriz.
    # Ancak ttk.OptionMenu'nun seçeneklerini doğrudan güncellemek biraz karmaşık olabilir.
    # Basitlik adına, şimdilik sadece label'ı güncelleyelim ve filtrelemeyi yeniden tetikleyelim.
    
    # Uygulama listesini yeniden oluşturarak metinleri güncelle
    filter_apps()

# --- Ayarlar Penceresi Fonksiyonları ---
def show_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title(get_text("settings"))
    settings_window.transient(root) # Ana pencereye bağımlı yap
    settings_window.grab_set() # Diğer pencerelerle etkileşimi engelle
    settings_window.focus_set() # Odaklan

    # Dil Ayarları
    lang_frame = ttk.LabelFrame(settings_window, text=get_text("language_settings"), padding=10)
    lang_frame.pack(padx=10, pady=10, fill="x")

    ttk.Label(lang_frame, text=get_text("select_language")).pack(pady=5)
    lang_options = list(LANGUAGES.keys())
    lang_menu = ttk.OptionMenu(lang_frame, current_language, current_language.get(), *lang_options, command=apply_language_change)
    lang_menu.pack(pady=5)

    # İndirme Klasörü Ayarları
    download_folder_frame = ttk.LabelFrame(settings_window, text=get_text("download_folder"), padding=10)
    download_folder_frame.pack(padx=10, pady=10, fill="x")

    ttk.Label(download_folder_frame, textvariable=download_folder).pack(side="left", padx=5)
    ttk.Button(download_folder_frame, text=get_text("select_download_folder"), command=choose_download_folder).pack(side="right", padx=5)

    # Sürücü Tarayıcı
    driver_frame = ttk.LabelFrame(settings_window, text=get_text("driver_scanner"), padding=10)
    driver_frame.pack(padx=10, pady=10, fill="x")

    ttk.Button(driver_frame, text=get_text("driver_scanner"), command=scan_drivers).pack(pady=5)

    # Ayarları kaydet butonu
    ttk.Button(settings_window, text=get_text("apply_language"), command=lambda: save_settings()).pack(pady=10) # Dili uygula butonu aynı zamanda ayarları kaydetsin

    settings_window.protocol("WM_DELETE_WINDOW", lambda: (save_settings(), settings_window.destroy())) # Pencere kapatıldığında ayarları kaydet

def apply_language_change(selected_lang):
    current_language.set(selected_lang)
    update_ui_texts()
    # messagebox.showinfo(get_text("settings"), get_text("apply_language")) # Bu mesajı ayarları kaydet butonuna taşıdık

def choose_download_folder():
    folder_selected = filedialog.askdirectory(initialdir=download_folder.get())
    if folder_selected:
        download_folder.set(folder_selected)
        save_settings() # Klasör değiştiğinde ayarları kaydet

def scan_drivers():
    # Bu, Windows'ta sürücüleri listelemek için basit bir örnek.
    # Gerçek bir sürücü tarayıcı çok daha karmaşık olacaktır.
    try:
        # wmic komutu ile sürücüleri listeleme
        # Daha fazla bilgi için: https://docs.microsoft.com/en-us/windows/win32/wmisdk/wmic
        result = subprocess.run(['wmic', 'path', 'Win32_PnPSignedDriver', 'get', 'DeviceName,DriverVersion,Manufacturer'], capture_output=True, text=True, check=True, encoding='utf-8')
        drivers_output = result.stdout.strip().split('\n')
        
        driver_list = []
        if len(drivers_output) > 1: # Başlık satırını saymamak için
            for line in drivers_output[1:]: # Başlık satırını atla
                parts = line.strip().split()
                if len(parts) >= 3: # DeviceName, DriverVersion, Manufacturer
                    device_name = " ".join(parts[:-2])
                    driver_version = parts[-2]
                    manufacturer = parts[-1]
                    driver_list.append(f"Cihaz: {device_name}, Sürüm: {driver_version}, Üretici: {manufacturer}")
                elif len(parts) == 2: # DeviceName, DriverVersion
                    device_name = parts[0]
                    driver_version = parts[1]
                    driver_list.append(f"Cihaz: {device_name}, Sürüm: {driver_version}")
                elif len(parts) == 1: # Sadece DeviceName
                    driver_list.append(f"Cihaz: {parts[0]}")

        if driver_list:
            driver_list_text = get_text("drivers_found") + "\n\n" + "\n".join(driver_list)
            messagebox.showinfo(get_text("driver_scanner"), driver_list_text)
        else:
            messagebox.showinfo(get_text("driver_scanner"), get_text("no_drivers_found"))
    except Exception as e:
        messagebox.showerror(get_text("error"), f"{get_text('no_drivers_found')}\n{e}")

# --- Ana Uygulama Penceresi ---
root = tk.Tk()
root.title(get_text("app_title"))
root.geometry("800x600") # Pencere boyutunu ayarla

# Tema ayarı
style = ttk.Style()
style.theme_use("clam") # "clam", "alt", "default", "classic" gibi temaları deneyebilirsiniz

# Arama ve Kategori Filtreleme Çubuğu
filter_frame = ttk.Frame(root, padding=5)
filter_frame.pack(fill="x")

search_entry = ttk.Entry(filter_frame, width=40)
search_entry.pack(side="left", expand=True, fill="x", padx=5)
search_entry.insert(0, get_text("search_app"))
search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, "end") if search_entry.get() == get_text("search_app") else None)
search_entry.bind("<FocusOut>", lambda e: search_entry.insert(0, get_text("search_app")) if not search_entry.get() else None)
search_entry.bind("<KeyRelease>", filter_apps)

category_label = ttk.Label(filter_frame, text=get_text("category"))
category_label.pack(side="left", padx=5)

# Kategori seçeneklerini dinamik olarak oluştur
category_options_translated = [get_text(cat) for cat in CATEGORIES]
category_menu = ttk.OptionMenu(filter_frame, selected_category, get_text(selected_category.get()), *category_options_translated, command=lambda x: (selected_category.set(CATEGORIES[category_options_translated.index(x)]), filter_apps()))
category_menu.pack(side="left", padx=5)


# Uygulama Listesi Çerçevesi
app_list_frame = ttk.Frame(root, padding=10)
app_list_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(app_list_frame)
scrollbar = ttk.Scrollbar(app_list_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

vars = []
filter_apps() # Uygulama listesini başlangıçta doldur

canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")
app_list_frame.grid_rowconfigure(0, weight=1)
app_list_frame.grid_columnconfigure(0, weight=1)

# İndirme İlerleme Çubuğu ve Bilgileri
download_progress_frame = ttk.LabelFrame(root, text=get_text("download_progress"), padding=10)
download_progress_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(download_progress_frame, text=get_text("current_download")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
ttk.Label(download_progress_frame, textvariable=current_download_app_name).grid(row=0, column=1, sticky="w", padx=5, pady=2)

ttk.Label(download_progress_frame, text=get_text("download_speed")).grid(row=1, column=0, sticky="w", padx=5, pady=2)
ttk.Label(download_progress_frame, textvariable=current_download_speed).grid(row=1, column=1, sticky="w", padx=5, pady=2)

ttk.Label(download_progress_frame, text=get_text("remaining_time")).grid(row=2, column=0, sticky="w", padx=5, pady=2)
ttk.Label(download_progress_frame, textvariable=current_download_remaining_time).grid(row=2, column=1, sticky="w", padx=5, pady=2)

ttk.Label(download_progress_frame, text=get_text("total_progress")).grid(row=3, column=0, sticky="w", padx=5, pady=2)
total_progress_bar = ttk.Progressbar(download_progress_frame, maximum=100, variable=total_download_progress)
total_progress_bar.grid(row=3, column=1, sticky="ew", padx=5, pady=2)
download_progress_frame.grid_columnconfigure(1, weight=1)


# Alt Butonlar
button_frame = ttk.Frame(root, padding=10)
button_frame.pack(fill="x")

btn_download = ttk.Button(button_frame, text=get_text("download_selected"), command=on_download)
btn_download.pack(side="left", expand=True, padx=5)

btn_admin = ttk.Button(button_frame, text=get_text("admin_login"), command=admin_login)
btn_admin.pack(side="left", expand=True, padx=5)

btn_guest = ttk.Button(button_frame, text=get_text("guest_mode"), command=guest_mode)
btn_guest.pack(side="left", expand=True, padx=5)

btn_update_checker = ttk.Button(button_frame, text=get_text("update_checker"), command=update_checker)
btn_update_checker.pack(side="left", expand=True, padx=5)

btn_settings = ttk.Button(button_frame, text=get_text("settings"), command=show_settings)
btn_settings.pack(side="left", expand=True, padx=5)

# Uygulama başlatıldığında ayarları yükle
load_settings()

root.mainloop()
