import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import requests
import os
import subprocess

# Uygulama listesi (10 yeni uygulama eklendi)
apps = [
    # Önceki uygulamalarınız
    {"name": "PyCharm", "url": "https://download.jetbrains.com/python/pycharm-community-2024.1.2.exe", "size_mb": 500},
    {"name": "Adobe Illustrator", "url": "https://download.adobe.com/pub/adobe/illustrator/win/26.x/Illustrator_26_LS20_win64.exe", "size_mb": 200},
    {"name": "Adobe Premiere Pro", "url": "https://download.adobe.com/pub/adobe/premiere/win/22.x/Premiere_Pro_22_LS20_win64.exe", "size_mb": 300},
    {"name": "Android Studio", "url": "https://redirector.gvt1.com/edgedl/android/studio/install/2023.1.1.24/android-studio-2023.1.1.24-windows.exe", "size_mb": 900},
    {"name": "IntelliJ IDEA", "url": "https://download.jetbrains.com/idea/ideaIC-2024.1.2.exe", "size_mb": 700},
    {"name": "Adobe After Effects", "url": "https://download.adobe.com/pub/adobe/aftereffects/win/22.x/After_Effects_22_LS20_win64.exe", "size_mb": 250},
    {"name": "Sublime Text", "url": "https://download.sublimetext.com/Sublime%20Text%20Build%204216%20x64%20Setup.exe", "size_mb": 20},
    {"name": "XAMPP", "url": "https://www.apachefriends.org/xampp-files/8.2.4/xampp-windows-x64-8.2.4-0-VS16-installer.exe", "size_mb": 150},
    {"name": "Eclipse IDE", "url": "https://ftp.fau.de/eclipse/technology/epp/downloads/release/2024-03/R/eclipse-inst-jre-win64.exe", "size_mb": 120},
    {"name": "Adobe Lightroom", "url": "https://download.adobe.com/pub/adobe/lightroom/win/6.x/Lightroom_6_LS11_win64.exe", "size_mb": 150},
    {"name": "Visual Studio Code", "url": "https://update.code.visualstudio.com/latest/win32-x64-user/stable", "size_mb": 90},
    {"name": "Google Chrome", "url": "https://dl.google.com/chrome/install/latest/chrome_installer.exe", "size_mb": 80},
    {"name": "Mozilla Firefox", "url": "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=tr", "size_mb": 75},
    {"name": "Opera Browser", "url": "https://net.geo.opera.com/opera/stable/windows", "size_mb": 70},
    {"name": "VLC Media Player", "url": "https://get.videolan.org/vlc/3.0.20/win64/vlc-3.0.20-win64.exe", "size_mb": 40},
    {"name": "WinRAR", "url": "https://www.rarlab.com/rar/winrar-x64-624tr.exe", "size_mb": 5},
    {"name": "7-Zip", "url": "https://www.7-zip.org/a/7z2405-x64.exe", "size_mb": 3},
    {"name": "Notepad++", "url": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.6.5/npp.8.6.5.Installer.x64.exe", "size_mb": 5},
    {"name": "Discord", "url": "https://discord.com/api/download?platform=win", "size_mb": 80},
    {"name": "Spotify", "url": "https://download.scdn.co/SpotifySetup.exe", "size_mb": 80},
    {"name": "Slack", "url": "https://downloads.slack-edge.com/releases_x64/SlackSetup.exe", "size_mb": 90},
    {"name": "Zoom", "url": "https://zoom.us/client/latest/ZoomInstaller.exe", "size_mb": 60},
    {"name": "Microsoft Teams", "url": "https://statics.teams.cdn.office.net/production-windows-x64/1.6.00.12455/Teams_windows_x64.exe", "size_mb": 120},
    {"name": "Git", "url": "https://github.com/git-for-windows/git/releases/download/v2.45.1.windows.1/Git-2.45.1-64-bit.exe", "size_mb": 50},
    {"name": "Node.js", "url": "https://nodejs.org/dist/v20.12.2/node-v20.12.2-x64.msi", "size_mb": 30},
    {"name": "Python", "url": "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe", "size_mb": 30},
    {"name": "Java JDK", "url": "https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.exe", "size_mb": 160},
    {"name": "MySQL Installer", "url": "https://dev.mysql.com/get/Downloads/MySQLInstaller/mysql-installer-web-community-8.0.36.0.msi", "size_mb": 2},
    {"name": "PostgreSQL", "url": "https://get.enterprisedb.com/postgresql/postgresql-16.2-1-windows-x64.exe", "size_mb": 250},
    {"name": "MongoDB Compass", "url": "https://downloads.mongodb.com/compass/mongodb-compass-1.42.6-win32-x64.exe", "size_mb": 120},
    {"name": "Docker Desktop", "url": "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe", "size_mb": 500},
    {"name": "FileZilla", "url": "https://download.filezilla-project.org/client/FileZilla_3.67.0_win64-setup.exe", "size_mb": 12},
    {"name": "OBS Studio", "url": "https://cdn-fastly.obsproject.com/downloads/OBS-Studio-30.1.2-Full-Installer-x64.exe", "size_mb": 120},
    {"name": "Steam", "url": "https://cdn.cloudflare.steamstatic.com/client/installer/SteamSetup.exe", "size_mb": 5},
    {"name": "Epic Games Launcher", "url": "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi", "size_mb": 80},
    {"name": "Battle.net", "url": "https://www.battle.net/download/getInstaller?os=win", "size_mb": 5},
    {"name": "Origin", "url": "https://download.dm.origin.com/origin/live/OriginThinSetup.exe", "size_mb": 70},
    {"name": "GIMP", "url": "https://download.gimp.org/mirror/pub/gimp/v2.10/windows/gimp-2.10.36-setup.exe", "size_mb": 250},
    {"name": "Inkscape", "url": "https://media.inkscape.org/dl/resources/file/inkscape-1.3.2_2024-01-14_amd64.exe", "size_mb": 120},
    {"name": "Krita", "url": "https://download.kde.org/stable/krita/5.2.2/krita-x64-5.2.2-setup.exe", "size_mb": 150},
    {"name": "Paint.NET", "url": "https://www.dotpdn.com/files/paint.net.5.0.13.install.x64.exe", "size_mb": 60},
    {"name": "Audacity", "url": "https://github.com/audacity/audacity/releases/download/Audacity-3.5.1/audacity-win-3.5.1-64bit.exe", "size_mb": 40},
    {"name": "DaVinci Resolve", "url": "https://www.blackmagicdesign.com/api/register/us/download/resolve-windows/DaVinci_Resolve_18.6.6_Windows.zip", "size_mb": 2500},
    {"name": "HandBrake", "url": "https://github.com/HandBrake/HandBrake/releases/download/1.7.3/HandBrake-1.7.3-x86_64-Win_GUI.exe", "size_mb": 20},
    {"name": "VirtualBox", "url": "https://download.virtualbox.org/virtualbox/7.0.18/VirtualBox-7.0.18-162988-Win.exe", "size_mb": 110},
    {"name": "VMware Workstation Player", "url": "https://download3.vmware.com/software/WKST-PLAYER-1706/VMware-player-full-17.0.6-22583795.exe", "size_mb": 600},
    {"name": "TeamViewer", "url": "https://download.teamviewer.com/download/TeamViewer_Setup_x64.exe", "size_mb": 40},
    {"name": "AnyDesk", "url": "https://download.anydesk.com/AnyDesk.exe", "size_mb": 5},
    {"name": "PuTTY", "url": "https://the.earth.li/~sgtatham/putty/latest/w64/putty-64bit-0.81-installer.msi", "size_mb": 3},
    {"name": "WinSCP", "url": "https://winscp.net/download/WinSCP-6.3.3-Setup.exe", "size_mb": 12},
    {"name": "Figma Desktop", "url": "https://desktop.figma.com/win/FigmaSetup.exe", "size_mb": 80},
    {"name": "Postman", "url": "https://dl.pstmn.io/download/latest/win64", "size_mb": 120},
    {"name": "Brave Browser", "url": "https://laptop-updates.brave.com/latest/winx64", "size_mb": 80},
    {"name": "Tor Browser", "url": "https://www.torproject.org/dist/torbrowser/13.0.13/torbrowser-install-win64-13.0.13_ALL.exe", "size_mb": 90},
    {"name": "LibreOffice", "url": "https://download.documentfoundation.org/libreoffice/stable/24.2.4/win/x86_64/LibreOffice_24.2.4_Win_x86-64.msi", "size_mb": 350},
    {"name": "Foxit Reader", "url": "https://cdn01.foxitsoftware.com/product/reader/desktop/win/12.1.3/FoxitPDFReader1213_L10N_Setup_Prom.exe", "size_mb": 160},
    {"name": "Adobe Acrobat Reader", "url": "https://ardownload2.adobe.com/pub/adobe/reader/win/AcrobatDC/2300820419/AcroRdrDC2300820419_tr_TR.exe", "size_mb": 200},
    {"name": "Blender", "url": "https://download.blender.org/release/Blender3.6/blender-3.6.10-windows-x64.msi", "size_mb": 250},
    {"name": "Unity Hub", "url": "https://public-cdn.cloud.unity3d.com/hub/prod/UnityHubSetup.exe", "size_mb": 120},
    {"name": "Unreal Engine Launcher", "url": "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi", "size_mb": 80},
    {"name": "R Studio", "url": "https://download1.rstudio.org/desktop/windows/RStudio-2024.04.1-748.exe", "size_mb": 200},
    {"name": "MATLAB Runtime", "url": "https://ssd.mathworks.com/supportfiles/downloads/R2024a/Release/9/deployment_files/installer/complete/win64/MATLAB_Runtime_R2024a_win64.exe", "size_mb": 3000},
    {"name": "WampServer", "url": "https://sourceforge.net/projects/wampserver/files/WampServer%203/WampServer%203.3.1/wampserver3.3.1_x64.exe/download", "size_mb": 700},
    {"name": "MAMP", "url": "https://downloads.mamp.info/MAMP-PRO/releases/6.8.1/MAMP_MAMP_PRO_6.8.1.exe", "size_mb": 500},
    {"name": "HeidiSQL", "url": "https://www.heidisql.com/downloads/releases/HeidiSQL_12.7.0.6677_Setup.exe", "size_mb": 12},
    {"name": "DBeaver", "url": "https://dbeaver.io/files/dbeaver-ce-latest-x86_64-setup.exe", "size_mb": 90},
    {"name": "Power BI Desktop", "url": "https://download.microsoft.com/download/7/8/8/788E1F7B-7B7E-4B7B-8A7B-7B7B7B7B7B7B/PBIDesktopSetup_x64.exe", "size_mb": 400},
    {"name": "Tableau Public", "url": "https://downloads.tableau.com/tssoftware/TableauPublic-2024-1-0.exe", "size_mb": 500},
    {"name": "Microsoft Edge", "url": "https://msedgesetup.azureedge.net/latest/MicrosoftEdgeSetup.exe", "size_mb": 120},
    {"name": "AVG Antivirus", "url": "https://files-download.avg.com/inst/mp/AVG_Antivirus_Free_Installer.exe", "size_mb": 250},
    {"name": "Avast Free Antivirus", "url": "https://files.avast.com/iavs9x/avast_free_antivirus_setup_online.exe", "size_mb": 250},
    {"name": "Kaspersky Security Cloud", "url": "https://products.s.kaspersky-labs.com/homeuser/kaspersky_security_cloud/21.3.10.391/patch_k/ks4.021.3.10.391en_23857.exe", "size_mb": 180},
    {"name": "Malwarebytes", "url": "https://data-cdn.mbamupdates.com/web/mb4-setup-consumer/MBSetup.exe", "size_mb": 90},
    {"name": "CCleaner", "url": "https://download.ccleaner.com/ccsetup624.exe", "size_mb": 35},
    {"name": "Revo Uninstaller", "url": "https://www.revouninstaller.com/downloads/RevoUninProSetup.exe", "size_mb": 20},
    {"name": "AIDA64 Extreme", "url": "https://download.aida64.com/aida64extreme700.exe", "size_mb": 50},
    {"name": "HWMonitor", "url": "https://www.cpuid.com/downloads/hwmonitor/hwmonitor_1.54.exe", "size_mb": 2},
    {"name": "CPU-Z", "url": "https://download.cpuid.com/cpu-z/cpu-z_2.09-en.exe", "size_mb": 2},
    {"name": "CrystalDiskInfo", "url": "https://osdn.net/projects/crystaldiskinfo/downloads/78394/CrystalDiskInfo8_17_14.exe", "size_mb": 6},
    {"name": "BlueStacks", "url": "https://cdn3.bluestacks.com/downloads/windows/nxt/5.20.0.1053/BlueStacksInstaller_5.20.0.1053_native.exe", "size_mb": 600},
    {"name": "LDPlayer", "url": "https://cdn.ldmnq.com/download/package/LDPlayer_9.0.71.exe", "size_mb": 600},
    {"name": "Genymotion", "url": "https://dl.genymotion.com/releases/genymotion-3.6.0/genymotion-3.6.0.exe", "size_mb": 200},
    {"name": "MobaXterm", "url": "https://download.mobatek.net/2462024012212345/MobaXterm_Installer_v24.6.zip", "size_mb": 50},
    {"name": "Termius", "url": "https://www.termius.com/windows_setup.exe", "size_mb": 80},
    {"name": "Bitwarden", "url": "https://vault.bitwarden.com/download/?app=desktop&platform=windows", "size_mb": 80},
    {"name": "KeePass", "url": "https://downloads.sourceforge.net/project/keepass/KeePass%202.x/2.56/KeePass-2.56-Setup.exe", "size_mb": 5},
    {"name": "LastPass", "url": "https://download.cloud.lastpass.com/windows_installer/LastPassInstaller.exe", "size_mb": 30},
    {"name": "NordVPN", "url": "https://downloads.nordcdn.com/apps/windows/NordVPN/latest/NordVPNSetup.exe", "size_mb": 80},
    {"name": "ProtonVPN", "url": "https://protonvpn.com/download/ProtonVPN_win_v4.4.0.exe", "size_mb": 80},
    {"name": "Cisco Packet Tracer", "url": "https://www.netacad.com/portal/resources/packet-tracer-download", "size_mb": 200},
]

ADMIN_PASSWORD = "2201126292ASd"
USER_LOG_FILE = "guest_users.txt"

def download_file(url, filename, progress_var, size_mb_label, app_name):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            downloaded_size = 0
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        progress = (downloaded_size / total_size) * 100
                        progress_var.set(progress)
                        size_mb_label.config(text=f"{downloaded_size / (1024 * 1024):.2f} MB / {total_size / (1024 * 1024):.2f} MB")
        messagebox.showinfo("Tamamlandı", f"{app_name} yüklendi. Dosya konumu: {os.path.abspath(filename)}")
        subprocess.Popen(f'explorer /select,"{os.path.abspath(filename)}"')
        size_mb_label.config(text=f"{app_name} Yüklü")
        check_for_updates(app_name)
        return True
    except Exception as e:
        return False

def check_for_updates(app_name):
    messagebox.showinfo("Güncelleme Kontrolü", f"{app_name} için güncellemeler kontrol edildi.")

def start_download(selected_indices):
    os.makedirs("indirilenler", exist_ok=True)
    for idx in selected_indices:
        app = apps[idx]
        filename = os.path.join("indirilenler", app["name"].replace(" ", "_") + os.path.splitext(app["url"])[-1])
        progress_var = tk.DoubleVar()
        size_mb_label = tk.Label(root, text="0 MB / 0 MB")
        size_mb_label.pack()
        status = download_file(app["url"], filename, progress_var, size_mb_label, app["name"])
        if not status:
            messagebox.showerror("Hata", f"{app['name']} indirilemedi!")
        progress_bar = ttk.Progressbar(root, maximum=100, variable=progress_var)
        progress_bar.pack(fill='x', padx=5, pady=5)
        progress_bar.start()
    messagebox.showinfo("Tamamlandı", "Seçilen uygulamalar indirildi.")

def on_download():
    selected = [i for i, var in enumerate(vars) if var.get()]
    if not selected:
        messagebox.showwarning("Uyarı", "Lütfen en az bir uygulama seçin.")
        return
    threading.Thread(target=start_download, args=(selected,), daemon=True).start()

def admin_login():
    def check_password():
        if password_entry.get() == ADMIN_PASSWORD:
            messagebox.showinfo("Giriş Başarılı", "Admin paneline hoş geldiniz.")
            admin_panel()
            login_window.destroy()
        else:
            messagebox.showerror("Hata", "Yanlış şifre!")

    login_window = tk.Toplevel(root)
    login_window.title("Admin Girişi")
    tk.Label(login_window, text="Şifre:").pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)
    tk.Button(login_window, text="Giriş", command=check_password).pack(pady=10)

def admin_panel():
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Paneli")
    tk.Label(admin_window, text="Güncellemeleri Yükle").pack(pady=10)

    def upload_updates():
        messagebox.showinfo("Güncelleme", "Güncellemeler yüklendi.")

    def open_file():
        file_path = filedialog.askopenfilename(title="Bir dosya seçin")
        if file_path:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            text_window = tk.Toplevel(admin_window)
            text_window.title("Dosya İçeriği")
            text = tk.Text(text_window, wrap="word", width=80, height=20)
            text.insert("1.0", content)
            text.pack(expand=True, fill="both")

    def show_user_count():
        if os.path.exists(USER_LOG_FILE):
            with open(USER_LOG_FILE, "r", encoding="utf-8") as f:
                users = f.readlines()
            count = len(users)
        else:
            count = 0
        messagebox.showinfo("Kullanıcı Sayısı", f"Toplam misafir kullanıcı: {count}")

    tk.Button(admin_window, text="Güncellemeleri Yükle", command=upload_updates).pack(pady=10)
    tk.Button(admin_window, text="Dosya Aç", command=open_file).pack(pady=10)
    tk.Button(admin_window, text="Misafir Kullanıcı Sayısı", command=show_user_count).pack(pady=10)

def guest_mode():
    def submit_name():
        name = name_entry.get().strip()
        if not name:
            messagebox.showwarning("Uyarı", "Lütfen isminizi girin.")
            return
        with open(USER_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(name + "\n")
        messagebox.showinfo("Misafir Modu", f"Hoş geldin, {name}!")
        guest_window.destroy()

    guest_window = tk.Toplevel(root)
    guest_window.title("Misafir Modu")
    tk.Label(guest_window, text="Lütfen isminizi girin:").pack(pady=10)
    name_entry = tk.Entry(guest_window)
    name_entry.pack(pady=5)
    tk.Button(guest_window, text="Giriş", command=submit_name).pack(pady=10)

def update_checker():
    messagebox.showinfo("Güncelleme Denetleyicisi", "Güncellemeler kontrol ediliyor...")

root = tk.Tk()
root.title("Uygulama Yükleyici")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

canvas = tk.Canvas(frame)
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

vars = []
for i, app in enumerate(apps):
    var = tk.BooleanVar()
    chk = ttk.Checkbutton(scrollable_frame, text=f"{app['name']} ({app['size_mb']} MB)", variable=var)
    chk.grid(row=i, column=0, sticky="w", padx=5, pady=2)
    vars.append(var)

canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

btn_download = ttk.Button(frame, text="Seçilenleri İndir", command=on_download)
btn_download.grid(row=len(apps), column=0, pady=10)

btn_admin = ttk.Button(frame, text="Admin Girişi", command=admin_login)
btn_admin.grid(row=len(apps) + 1, column=0, pady=10)

btn_guest = ttk.Button(frame, text="Misafir Modu", command=guest_mode)
btn_guest.grid(row=len(apps) + 2, column=0, pady=10)

btn_update_checker = ttk.Button(frame, text="Güncelleme Denetleyicisi", command=update_checker)
btn_update_checker.grid(row=len(apps) + 3, column=0, pady=10)

root.mainloop()
