import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
import os

apps = [
    {"name": "Google Chrome", "url": "https://dl.google.com/chrome/install/latest/chrome_installer.exe", "size_mb": 90},
    {"name": "OBS Studio", "url": "https://cdn-fastly.obsproject.com/downloads/OBS-Studio-30.1.2-Full-Installer-x64.exe", "size_mb": 180},
    {"name": "Visual Studio Code", "url": "https://update.code.visualstudio.com/latest/win32-x64-user/stable", "size_mb": 90},
    {"name": "GitHub Desktop", "url": "https://central.github.com/deployments/desktop/desktop/latest/win32", "size_mb": 120},
    {"name": "VLC Media Player", "url": "https://get.videolan.org/vlc/3.0.20/win64/vlc-3.0.20-win64.exe", "size_mb": 40},
    {"name": "DriverPack", "url": "https://download.drp.su/driverpack.exe", "size_mb": 25},
    {"name": "Minecraft Launcher (Java & Bedrock)", "url": "https://launcher.mojang.com/download/MinecraftInstaller.exe", "size_mb": 33},
    {"name": "Steam", "url": "https://cdn.cloudflare.steamstatic.com/client/installer/SteamSetup.exe", "size_mb": 2},
    {"name": "Epic Games Launcher", "url": "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi", "size_mb": 150},
    {"name": "Xbox", "url": "https://aka.ms/XboxInstaller", "size_mb": 120},
    {"name": "Unity Hub", "url": "https://public-cdn.cloud.unity3d.com/hub/prod/UnityHubSetup.exe", "size_mb": 150},
    {"name": "Unreal Engine", "url": "https://launcher-public.epicgames.com/installer/download/EpicGamesLauncherInstaller.msi", "size_mb": 181},
    {"name": "Godot Engine", "url": "https://downloads.tuxfamily.org/godotengine/4.2.2/Godot_v4.2.2-stable_win64.exe.zip", "size_mb": 50},
    {"name": "Rufus", "url": "https://github.com/pbatard/rufus/releases/download/v4.4/rufus-4.4.exe", "size_mb": 1},
    {"name": "CapCut", "url": "https://lf16-capcut.faceulv.com/obj/capcutpc-packages-us/packages/CapCut_3_7_0_1120_capcutpc_0.exe", "size_mb": 2},
    {"name": "VMware Workstation Player", "url": "https://download3.vmware.com/software/WKST-PLAYER-1703/VMware-player-full-17.0.3-22164363.exe", "size_mb": 217},
]

def download_file(url, filename):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        return True
    except Exception as e:
        return False

def start_download(selected_indices):
    os.makedirs("indirilenler", exist_ok=True)
    for idx in selected_indices:
        app = apps[idx]
        filename = os.path.join("indirilenler", app["name"].replace(" ", "_") + os.path.splitext(app["url"])[-1])
        status = download_file(app["url"], filename)
        if not status:
            messagebox.showerror("Hata", f"{app['name']} indirilemedi!")
    messagebox.showinfo("Tamamlandı", "Seçilen uygulamalar indirildi.")

def on_download():
    selected = [i for i, var in enumerate(vars) if var.get()]
    if not selected:
        messagebox.showwarning("Uyarı", "Lütfen en az bir uygulama seçin.")
        return
    threading.Thread(target=start_download, args=(selected,), daemon=True).start()

root = tk.Tk()
root.title("Uygulama Yükleyici")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

vars = []
for i, app in enumerate(apps):
    var = tk.BooleanVar()
    chk = ttk.Checkbutton(frame, text=f"{app['name']} ({app['size_mb']} MB)", variable=var)
    chk.grid(row=i, column=0, sticky="w", padx=5, pady=2)
    vars.append(var)

btn = ttk.Button(frame, text="Seçilenleri İndir", command=on_download)
btn.grid(row=len(apps), column=0, pady=10)

root.mainloop()
